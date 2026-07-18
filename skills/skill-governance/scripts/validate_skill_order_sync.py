#!/usr/bin/env python3
"""Compatibility check for skill ordering in the two generated catalog views."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_SKILLS_ROOT = SCRIPT_PATH.parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT))
    parser.add_argument("--skill-map-path", default="SKILL-MAP.md")
    parser.add_argument("--skill-index-path", default="docs/skill-index.md")
    return parser.parse_args()


def parse_skill_map_order(path: Path) -> list[str]:
    if not path.exists():
        raise SystemExit(f"Missing skill map file: {path}")
    lines = path.read_text(encoding="utf-8").splitlines()
    in_section = False
    order: list[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if line in {"## Skill Index", "## Decision Ownership"}:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        match = re.search(r"`([a-z0-9-]+)`", line)
        if match:
            order.append(match.group(1))
    if not order:
        raise SystemExit(f"No skills found in `## Skill Index` section: {path}")
    return order


def parse_skill_index_order(path: Path) -> list[str]:
    if not path.exists():
        raise SystemExit(f"Missing skill index file: {path}")
    lines = path.read_text(encoding="utf-8").splitlines()
    in_table = False
    order: list[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("| Skill |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            if order:
                break
            continue
        if line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 1:
            continue
        match = re.search(r"`([a-z0-9-]+)`", cells[0])
        skill_name = match.group(1) if match else ""
        if skill_name:
            order.append(skill_name)
    if not order:
        raise SystemExit(f"No skill rows found in index table: {path}")
    return order


def main() -> None:
    args = parse_args()
    skills_root = Path(args.skills_root).resolve()
    skill_map_path = Path(args.skill_map_path)
    if not skill_map_path.is_absolute():
        skill_map_path = skills_root / skill_map_path
    skill_index_path = Path(args.skill_index_path)
    if not skill_index_path.is_absolute():
        skill_index_path = skills_root / skill_index_path

    map_order = parse_skill_map_order(skill_map_path)
    index_order = parse_skill_index_order(skill_index_path)

    errors: list[str] = []
    if len(map_order) != len(index_order):
        errors.append(
            f"Skill count mismatch: SKILL-MAP has {len(map_order)} entries, skill-index has {len(index_order)} entries"
        )

    map_set = set(map_order)
    index_set = set(index_order)
    missing_in_index = sorted(map_set - index_set)
    missing_in_map = sorted(index_set - map_set)
    if missing_in_index:
        errors.append(f"Missing in docs/skill-index.md: {missing_in_index}")
    if missing_in_map:
        errors.append(f"Missing in SKILL-MAP.md: {missing_in_map}")

    max_len = min(len(map_order), len(index_order))
    for idx in range(max_len):
        left = map_order[idx]
        right = index_order[idx]
        if left != right:
            errors.append(f"Order mismatch at position {idx + 1}: SKILL-MAP=`{left}` vs skill-index=`{right}`")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        raise SystemExit(1)

    print("Skill ordering sync validation passed.")
    print(f"Checked SKILL-MAP: {skill_map_path}")
    print(f"Checked skill-index: {skill_index_path}")
    print(f"Skill count: {len(map_order)}")


if __name__ == "__main__":
    main()
