#!/usr/bin/env python3
"""Process Agent Command Center lifecycle and exact-command events.

Conversation lifecycle data stays in the event state. User-controlled mode
preferences are persisted locally so an explicit toggle survives conversations.
Only booleans are stored; no message content or credentials are written.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shlex
import sys
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = 1
STARTUP_HINT = "send --help to learn more about available tools in agent-command-center"
QUIZME_OPTIONS = frozenset({"--mc", "--one-at-a-time", "--confirm", "--record"})
PREFERENCES_ENV = "AGENT_COMMAND_CENTER_PREFERENCES"

DEFAULT_STATE: dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "startup_hint_emitted": False,
    "clean_slate": False,
    "quizme": {
        "enabled": False,
        "multiple_choice": False,
        "one_at_a_time": False,
        "confirm": False,
        "record": False,
    },
    "internal_lang": {"internal": False, "response": False},
    "user_run_scripts": False,
}


class RuntimeProtocolError(ValueError):
    """Raised when a host supplies a malformed runtime event or state."""


def _closed_keys(value: Mapping[str, Any], allowed: set[str], label: str) -> None:
    extras = sorted(set(value) - allowed)
    if extras:
        raise RuntimeProtocolError(f"{label} contains unsupported fields: {', '.join(extras)}")


def normalize_state(value: Mapping[str, Any] | None) -> dict[str, Any]:
    """Return a validated deep copy of runtime state."""

    if value is None:
        return copy.deepcopy(DEFAULT_STATE)
    if not isinstance(value, Mapping):
        raise RuntimeProtocolError("state must be an object")
    _closed_keys(
        value,
        {"schema_version", "startup_hint_emitted", "clean_slate", "quizme", "internal_lang", "user_run_scripts"},
        "state",
    )
    if value.get("schema_version") != SCHEMA_VERSION:
        raise RuntimeProtocolError(f"state.schema_version must equal {SCHEMA_VERSION}")
    result = copy.deepcopy(DEFAULT_STATE)
    for name in ("startup_hint_emitted", "clean_slate"):
        if not isinstance(value.get(name), bool):
            raise RuntimeProtocolError(f"state.{name} must be boolean")
        result[name] = value[name]
    if "user_run_scripts" in value:
        if not isinstance(value["user_run_scripts"], bool):
            raise RuntimeProtocolError("state.user_run_scripts must be boolean")
        result["user_run_scripts"] = value["user_run_scripts"]
    for group, fields in {
        "quizme": {"enabled", "multiple_choice", "one_at_a_time", "confirm", "record"},
        "internal_lang": {"internal", "response"},
    }.items():
        nested = value.get(group)
        if not isinstance(nested, Mapping):
            raise RuntimeProtocolError(f"state.{group} must be an object")
        _closed_keys(nested, fields, f"state.{group}")
        missing = sorted(fields - set(nested))
        if missing:
            raise RuntimeProtocolError(f"state.{group} is missing fields: {', '.join(missing)}")
        for name in fields:
            if not isinstance(nested[name], bool):
                raise RuntimeProtocolError(f"state.{group}.{name} must be boolean")
            result[group][name] = nested[name]
    if result["quizme"]["record"] and not result["quizme"]["confirm"]:
        raise RuntimeProtocolError("state.quizme.record requires state.quizme.confirm")
    return result


def _preferences_path() -> Path:
    configured = os.environ.get(PREFERENCES_ENV)
    return Path(configured).expanduser() if configured else Path.home() / ".config" / "agent-command-center" / "preferences.json"


def _preference_state() -> dict[str, Any]:
    path = _preferences_path()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return copy.deepcopy(DEFAULT_STATE)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeProtocolError(f"cannot read persisted preferences: {exc}") from exc
    if not isinstance(payload, Mapping):
        raise RuntimeProtocolError("persisted preferences must be an object")
    return normalize_state({"schema_version": SCHEMA_VERSION, "startup_hint_emitted": False, **payload})


def _persist_preferences(state: Mapping[str, Any]) -> None:
    path = _preferences_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    payload = {"schema_version": SCHEMA_VERSION, "clean_slate": state["clean_slate"], "quizme": state["quizme"], "internal_lang": state["internal_lang"], "user_run_scripts": state["user_run_scripts"]}
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent), text=True)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except OSError as exc:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise RuntimeProtocolError(f"cannot persist preferences: {exc}") from exc


def _active_mode_skills(state: Mapping[str, Any]) -> list[str]:
    active: list[str] = []
    if state["clean_slate"]:
        active.append("clean-slate")
    if state["quizme"]["enabled"]:
        active.append("quizme-mode")
    if state["internal_lang"]["internal"] or state["internal_lang"]["response"]:
        active.append("internal-lang")
    if state["user_run_scripts"]:
        active.append("user-run-scripts")
    return active


def _descriptor_patch(state: Mapping[str, Any], command_skill: str | None, help_requested: bool) -> dict[str, Any]:
    explicit = _active_mode_skills(state)
    if command_skill and command_skill != "help" and command_skill not in explicit:
        explicit.append(command_skill)
    patch: dict[str, Any] = {}
    if help_requested:
        patch["action"] = {"help_requested": True}
    if explicit:
        patch["constraints"] = {"explicit_skills": explicit}
    return patch


def apply_descriptor_patch(descriptor: Mapping[str, Any], patch: Mapping[str, Any]) -> dict[str, Any]:
    """Apply a runtime patch without dropping host-normalized explicit skills."""

    if not isinstance(descriptor, Mapping) or not isinstance(patch, Mapping):
        raise RuntimeProtocolError("descriptor and patch must be objects")
    result = copy.deepcopy(dict(descriptor))
    action = result.get("action")
    constraints = result.get("constraints")
    if not isinstance(action, dict) or not isinstance(constraints, dict):
        raise RuntimeProtocolError("descriptor requires action and constraints objects")
    patch_action = patch.get("action", {})
    patch_constraints = patch.get("constraints", {})
    if not isinstance(patch_action, Mapping) or not isinstance(patch_constraints, Mapping):
        raise RuntimeProtocolError("descriptor patch action and constraints must be objects")
    action.update(copy.deepcopy(dict(patch_action)))
    additions = patch_constraints.get("explicit_skills", [])
    existing = constraints.get("explicit_skills")
    if not isinstance(existing, list) or not all(isinstance(item, str) for item in existing):
        raise RuntimeProtocolError("descriptor.constraints.explicit_skills must be an array of strings")
    if not isinstance(additions, list) or not all(isinstance(item, str) for item in additions):
        raise RuntimeProtocolError("patch.constraints.explicit_skills must be an array of strings")
    constraints["explicit_skills"] = list(dict.fromkeys([*existing, *additions]))
    return result


def _parse_message(message: str, state: dict[str, Any]) -> tuple[str | None, bool, list[str], bool]:
    """Apply an exact command and return skill, consumed, notices, help flag."""

    stripped = message.strip()
    if not stripped.startswith("--"):
        return None, False, [], False
    try:
        tokens = shlex.split(stripped)
    except ValueError as exc:
        return None, False, [f"Malformed command was not consumed: {exc}."], False
    if not tokens:
        return None, False, [], False

    command, *arguments = tokens
    notices: list[str] = []
    if command == "--help":
        if arguments:
            notices.append("Unsupported --help arguments; send exact command --help.")
            return None, False, notices, False
        return "help", True, notices, True

    if command == "--clean-slate":
        if not arguments:
            state["clean_slate"] = True
            notices.append("Clean-slate mode is on.")
        elif arguments == ["off"]:
            state["clean_slate"] = False
            notices.append("Clean-slate mode is off.")
        else:
            notices.append("Unsupported --clean-slate arguments; expected no argument or 'off'.")
            return None, False, notices, False
        return "clean-slate", True, notices, False

    if command == "--quizme":
        unsupported = sorted(set(arguments) - QUIZME_OPTIONS)
        if unsupported:
            notices.append(
                "Unsupported --quizme arguments; the command was not applied: "
                + " ".join(unsupported)
                + "."
            )
            return None, False, notices, False
        supported = set(arguments) & QUIZME_OPTIONS
        quizme = state["quizme"]
        if not supported:
            quizme["enabled"] = not quizme["enabled"]
            for name in ("multiple_choice", "one_at_a_time", "confirm", "record"):
                quizme[name] = False
        else:
            quizme["enabled"] = True
            quizme["multiple_choice"] = "--mc" in supported
            quizme["one_at_a_time"] = "--one-at-a-time" in supported
            quizme["record"] = "--record" in supported
            quizme["confirm"] = "--confirm" in supported or quizme["record"]
        notices.append(f"Quizme mode is {'on' if quizme['enabled'] else 'off'}.")
        return "quizme-mode", True, notices, False

    if command == "--internal-lang":
        internal_lang = state["internal_lang"]
        if len(arguments) == 1 and arguments[0] in {"on", "off"}:
            internal_lang["internal"] = arguments[0] == "on"
            notices.append(f"Internal compact notation is {arguments[0]}.")
        elif len(arguments) == 2 and arguments[0] == "--response" and arguments[1] in {"on", "off"}:
            internal_lang["response"] = arguments[1] == "on"
            notices.append(f"Compact response notation is {arguments[1]}.")
        else:
            notices.append(
                "Unsupported --internal-lang arguments; expected on|off or --response on|off."
            )
            return None, False, notices, False
        return "internal-lang", True, notices, False

    if command == "--ill-run-scripts":
        if arguments:
            notices.append("Unsupported --ill-run-scripts arguments; send the exact toggle command.")
            return None, False, notices, False
        state["user_run_scripts"] = not state["user_run_scripts"]
        notices.append(f"User-run-scripts mode is {'on' if state['user_run_scripts'] else 'off'}.")
        return "user-run-scripts", True, notices, False

    return None, False, [f"Unknown command {command!r} was not consumed."], False


def process_event(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Process one pack lifecycle or user-message event."""

    if not isinstance(payload, Mapping):
        raise RuntimeProtocolError("event payload must be an object")
    _closed_keys(payload, {"schema_version", "event", "message", "state"}, "event payload")
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise RuntimeProtocolError(f"event schema_version must equal {SCHEMA_VERSION}")
    event = payload.get("event")
    if event not in {"pack_loaded", "user_message"}:
        raise RuntimeProtocolError("event must be 'pack_loaded' or 'user_message'")
    if event == "pack_loaded" and "message" in payload:
        raise RuntimeProtocolError("pack_loaded events must not contain message")
    if event == "user_message" and not isinstance(payload.get("message"), str):
        raise RuntimeProtocolError("user_message events require a string message")

    persisted = _preference_state()
    state = normalize_state(payload.get("state"))
    for key in ("clean_slate", "quizme", "internal_lang", "user_run_scripts"):
        state[key] = copy.deepcopy(persisted[key])
    startup_messages: list[str] = []
    if not state["startup_hint_emitted"]:
        startup_messages.append(STARTUP_HINT)
        state["startup_hint_emitted"] = True

    command_skill: str | None = None
    consumed = False
    notices: list[str] = []
    help_requested = False
    source_sha256: str | None = None
    if event == "user_message":
        message = payload["message"]
        source_sha256 = hashlib.sha256(message.encode("utf-8")).hexdigest()
        command_skill, consumed, notices, help_requested = _parse_message(message, state)
        if consumed and command_skill in {"clean-slate", "quizme-mode", "internal-lang", "user-run-scripts"}:
            _persist_preferences(state)

    return {
        "schema_version": SCHEMA_VERSION,
        "startup_messages": startup_messages,
        "notices": notices,
        "recognized_command": command_skill,
        "consume_message": consumed,
        "source_sha256": source_sha256,
        "descriptor_patch": _descriptor_patch(state, command_skill, help_requested),
        "descriptor_patch_policy": "deep_merge_with_explicit_skill_union",
        "state": state,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "event_json",
        nargs="?",
        type=Path,
        help="Event JSON file. Read stdin when omitted.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        raw = args.event_json.read_text(encoding="utf-8") if args.event_json else sys.stdin.read()
        result = process_event(json.loads(raw))
    except (OSError, json.JSONDecodeError, RuntimeProtocolError) as exc:
        print(f"runtime adapter error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
