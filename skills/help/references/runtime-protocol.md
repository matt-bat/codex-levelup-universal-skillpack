# Host Runtime Protocol

Use this protocol when a host can execute local adapters. It makes startup and
mode behavior deterministic while leaving semantic task routing to the
canonical typed router. Explicit mode preferences persist across conversations
in a local JSON file; lifecycle startup signaling remains conversation-local.

## Event

Send one JSON object to `scripts/runtime_adapter.py` on stdin:

```json
{
  "schema_version": 1,
  "event": "user_message",
  "message": "--clean-slate",
  "state": null
}
```

`event` is either `pack_loaded` or `user_message`. Omit `message` for
`pack_loaded`. Omit `state` on the first event; afterwards, pass the exact
`state` object returned by the previous event. Durable preferences are reloaded
on every event, so toggles apply in later conversations. Set
`AGENT_COMMAND_CENTER_PREFERENCES` to a writable path for tests or a host
profile; otherwise the adapter uses `~/.config/agent-command-center/preferences.json`.

## Result

The adapter returns:

1. `startup_messages`: emit each string in order before other assistant output
2. `notices`: concise state changes or command errors to surface to the user
3. `recognized_command`: the owning skill or `null`
4. `consume_message`: whether the exact command is complete and should not be
   treated as an ordinary task
5. `source_sha256`: binding to the exact user message
6. `descriptor_patch`: apply to the normalized task descriptor before routing
7. `descriptor_patch_policy`: requires a deep merge that unions, rather than
   replaces, `constraints.explicit_skills`
8. `state`: pass unchanged into the next event for that conversation

Reject malformed adapter input. Do not silently repair or partially apply it.
Unknown commands and invalid forms of known commands are not consumed and do
not mutate state, so the complete message remains available to ordinary task
handling.

Use `apply_descriptor_patch()` when integrating in Python. Equivalent hosts must
preserve host-normalized explicit skills, append adapter-selected mode skills in
order without duplicates, and apply scalar action fields from the patch.

## Supported Commands

The executable grammar is:

```text
--help
--quizme [--mc] [--one-at-a-time] [--confirm] [--record]
--internal-lang on|off
--internal-lang --response on|off
--clean-slate
--clean-slate off
--ill-run-scripts
```

`--ill-run-scripts` is a bare toggle. When on, it pauses before easily executable scripts and gives the user an exact command and working directory.

All user-facing activation commands begin with `--`. Exact-command parsing does
not infer semantic task fields from keywords. The host must still normalize the
ordinary request into `task-descriptor.schema.json`, preserve the message digest
with its trace, and route every unresolved interpretation through
`eliminate-assumptions`.

## Conformance

Run:

```sh
python3 -m unittest skills.skill-governance.tests.test_runtime_adapter -v
```

A host that cannot execute this adapter must implement the same input, output,
state-transition, exact-command, and fail-closed behavior. Do not claim runtime
conformance from documentation alone.
