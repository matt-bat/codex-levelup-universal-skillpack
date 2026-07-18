#!/usr/bin/env python3
"""Record bounded, content-free routing telemetry or print an aggregate summary."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from statistics import median


TASK_CLASSES = {
    "answer", "inspect", "diagnose", "review", "score", "edit", "implement", "test",
    "operate", "release", "governance"
}
CHECKPOINTS = {"initial", "post_inspection", "post_plan", "post_diff", "pre_external_action"}
OUTCOMES = {"pass", "fail", "blocked", "unverified", "not_run"}
DEFAULT_OUT = Path(__file__).resolve().parents[2] / ".routing-observations.jsonl"
DEFAULT_CATALOG = Path(__file__).resolve().parents[2] / "skill-catalog.json"
MAX_RECORDS = 100
REQUIRED_KEYS = {
    "schema_version", "recorded_at_utc", "task_class", "checkpoint", "selected_skills",
    "route_changed", "corrections", "retries", "validation_outcome", "user_revision",
    "safety_omission",
}
OPTIONAL_KEYS = {"tool_calls", "elapsed_ms"}


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    record = sub.add_parser("record", help="Append one privacy-bounded observation.")
    record.add_argument("--out", type=Path, default=DEFAULT_OUT)
    record.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    record.add_argument("--task-class", choices=sorted(TASK_CLASSES), required=True)
    record.add_argument("--checkpoint", choices=sorted(CHECKPOINTS), required=True)
    record.add_argument("--selected-skills", default="")
    record.add_argument("--route-changed", action="store_true")
    record.add_argument("--corrections", type=int, default=0)
    record.add_argument("--retries", type=int, default=0)
    record.add_argument("--validation-outcome", choices=sorted(OUTCOMES), required=True)
    record.add_argument("--tool-calls", type=int)
    record.add_argument("--elapsed-ms", type=int)
    record.add_argument("--user-revision", action="store_true")
    record.add_argument("--safety-omission", action="store_true")
    record.add_argument("--max-records", type=int, default=MAX_RECORDS)
    summary = sub.add_parser("summary", help="Print aggregate metrics without task content.")
    summary.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return root


def nonnegative(name: str, value: int | None) -> None:
    if value is not None and value < 0:
        raise SystemExit(f"{name} must be non-negative")


def read_records(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    records: list[dict[str, object]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{number}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            raise SystemExit(f"{path}:{number}: unsupported observation record")
        keys = set(value)
        if not REQUIRED_KEYS.issubset(keys) or not keys.issubset(REQUIRED_KEYS | OPTIONAL_KEYS):
            raise SystemExit(f"{path}:{number}: invalid observation fields")
        if value.get("task_class") not in TASK_CLASSES or value.get("checkpoint") not in CHECKPOINTS:
            raise SystemExit(f"{path}:{number}: invalid observation classification")
        if value.get("validation_outcome") not in OUTCOMES:
            raise SystemExit(f"{path}:{number}: invalid observation outcome")
        timestamp = value.get("recorded_at_utc")
        try:
            parsed_timestamp = datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else None
        except ValueError as exc:
            raise SystemExit(f"{path}:{number}: invalid recorded_at_utc") from exc
        if parsed_timestamp is None or parsed_timestamp.tzinfo is None or len(timestamp) > 40:
            raise SystemExit(f"{path}:{number}: invalid recorded_at_utc")
        skills = value.get("selected_skills")
        if not isinstance(skills, list) or any(
            not isinstance(skill, str) or re.fullmatch(r"[a-z][a-z0-9-]{0,63}", skill) is None
            for skill in skills
        ):
            raise SystemExit(f"{path}:{number}: invalid selected skill names")
        if len(skills) != len(set(skills)):
            raise SystemExit(f"{path}:{number}: duplicate selected skill names")
        for key in ("corrections", "retries", "tool_calls", "elapsed_ms"):
            if key in value and (
                not isinstance(value[key], int)
                or isinstance(value[key], bool)
                or int(value[key]) < 0
            ):
                raise SystemExit(f"{path}:{number}: invalid non-negative count {key}")
        for key in ("route_changed", "user_revision", "safety_omission"):
            if not isinstance(value.get(key), bool):
                raise SystemExit(f"{path}:{number}: {key} must be boolean")
        records.append(value)
    return records


def write_records(path: Path, records: list[dict[str, object]]) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(record, sort_keys=True) + "\n" for record in records)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        handle.write(payload)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def record(args: argparse.Namespace) -> None:
    for name in ("corrections", "retries", "tool_calls", "elapsed_ms"):
        nonnegative(name, getattr(args, name))
    if args.max_records < 1 or args.max_records > MAX_RECORDS:
        raise SystemExit(f"max-records must be between 1 and {MAX_RECORDS}")
    skills = [item.strip() for item in args.selected_skills.split(",") if item.strip()]
    if len(skills) != len(set(skills)):
        raise SystemExit("selected-skills must not contain duplicates")
    if any(re.fullmatch(r"[a-z][a-z0-9-]{0,63}", skill) is None for skill in skills):
        raise SystemExit("selected-skills must contain comma-separated skill names")
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        known_skills = {
            item["name"] for item in catalog["skills"]
            if isinstance(item, dict) and isinstance(item.get("name"), str)
        }
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise SystemExit(f"cannot validate selected skills against catalog: {exc}") from exc
    unknown_skills = sorted(set(skills) - known_skills)
    if unknown_skills:
        raise SystemExit(f"selected-skills contains names outside the catalog: {unknown_skills}")
    item: dict[str, object] = {
        "schema_version": 1,
        "recorded_at_utc": datetime.now(UTC).isoformat(),
        "task_class": args.task_class,
        "checkpoint": args.checkpoint,
        "selected_skills": skills,
        "route_changed": args.route_changed,
        "corrections": args.corrections,
        "retries": args.retries,
        "validation_outcome": args.validation_outcome,
        "user_revision": args.user_revision,
        "safety_omission": args.safety_omission,
    }
    if args.tool_calls is not None:
        item["tool_calls"] = args.tool_calls
    if args.elapsed_ms is not None:
        item["elapsed_ms"] = args.elapsed_ms
    records = read_records(args.out)
    records.append(item)
    write_records(args.out, records[-args.max_records :])
    print(f"Recorded observation: {args.out.resolve()}")
    print(f"Retained records: {min(len(records), args.max_records)}")


def summarize(args: argparse.Namespace) -> None:
    records = read_records(args.out)
    task_counts = Counter(str(item.get("task_class")) for item in records)
    outcome_counts = Counter(str(item.get("validation_outcome")) for item in records)
    selected_counts = sorted(len(item.get("selected_skills", [])) for item in records)
    tool_counts = [int(item["tool_calls"]) for item in records if "tool_calls" in item]
    elapsed_values = [int(item["elapsed_ms"]) for item in records if "elapsed_ms" in item]
    selected_median = median(selected_counts) if selected_counts else 0
    payload = {
        "records": len(records),
        "task_classes": dict(sorted(task_counts.items())),
        "validation_outcomes": dict(sorted(outcome_counts.items())),
        "route_changes": sum(bool(item.get("route_changed")) for item in records),
        "corrections": sum(int(item.get("corrections", 0)) for item in records),
        "retries": sum(int(item.get("retries", 0)) for item in records),
        "user_revisions": sum(bool(item.get("user_revision")) for item in records),
        "safety_omissions": sum(bool(item.get("safety_omission")) for item in records),
        "median_selected_skills": selected_median,
        "median_tool_calls": median(tool_counts) if tool_counts else None,
        "median_elapsed_ms": median(elapsed_values) if elapsed_values else None,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


def main() -> None:
    args = parser().parse_args()
    if args.command == "record":
        record(args)
    else:
        summarize(args)


if __name__ == "__main__":
    main()
