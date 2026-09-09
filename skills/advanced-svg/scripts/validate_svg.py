#!/usr/bin/env python3
"""Perform deterministic structural and safety checks on an SVG file."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

SVG_NS = "http://www.w3.org/2000/svg"
UNSAFE_ELEMENTS = {"script", "foreignObject"}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
DANGEROUS_SCHEMES = {"javascript", "vbscript"}


def local_name(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path)
    parser.add_argument(
        "--allow-external",
        action="store_true",
        help="Do not report ordinary HTTP(S) or relative external references.",
    )
    return parser.parse_args()


def classify_reference(value: str) -> str | None:
    stripped = value.strip().strip("'\"")
    if stripped.startswith("#") or stripped in {"none", "currentColor", "context-fill", "context-stroke"}:
        return None
    if stripped.startswith("url("):
        inner = stripped[4:-1].strip().strip("'\"") if stripped.endswith(")") else stripped
        if inner.startswith("#"):
            return None
        stripped = inner
    parsed = urlparse(stripped)
    if parsed.scheme.lower() in DANGEROUS_SCHEMES:
        return "dangerous"
    if stripped.lower().startswith("data:text/html"):
        return "dangerous"
    if parsed.scheme or stripped.startswith("//") or (stripped and not stripped.startswith("var(")):
        return "external"
    return None


def validate(path: Path, allow_external: bool) -> list[str]:
    findings: list[str] = []
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"ERROR parse: {exc}"]
    if re.search(r"<!DOCTYPE|<\?xml-stylesheet", source, re.IGNORECASE):
        findings.append("ERROR active-document-directive: DOCTYPE and xml-stylesheet are not allowed")
    try:
        root = ET.fromstring(source)
    except ET.ParseError as exc:
        return [f"ERROR parse: {exc}"]

    if root.tag != f"{{{SVG_NS}}}svg":
        findings.append("ERROR root: expected an SVG root in the SVG namespace")
    if not root.get("viewBox"):
        findings.append("ERROR viewport: root SVG has no viewBox")

    decorative = root.get("aria-hidden", "").lower() == "true"
    direct_titles = [
        child for child in root if local_name(child.tag) == "title" and "".join(child.itertext()).strip()
    ]
    explicit_name = bool(root.get("aria-label") or root.get("aria-labelledby") or direct_titles)
    if decorative and explicit_name:
        findings.append("ERROR accessibility: decorative SVG must not also expose an accessible name")
    elif not decorative and not explicit_name:
        findings.append(
            "ERROR accessibility: declare aria-hidden='true' for decorative SVG or provide title, aria-label, or aria-labelledby"
        )

    ids: dict[str, str] = {}
    referenced: set[str] = set()
    for element in root.iter():
        tag = local_name(element.tag)
        element_id = element.get("id")
        location = f"<{tag}{' id=' + repr(element_id) if element_id else ''}>"
        if element_id:
            if element_id in ids:
                findings.append(f"ERROR id: duplicate {element_id!r} at {location}; first seen at {ids[element_id]}")
            else:
                ids[element_id] = location
        if tag in UNSAFE_ELEMENTS:
            findings.append(f"ERROR unsafe-element: {location}")
        if tag == "style":
            css = "".join(element.itertext())
            if re.search(r"@import\b", css, re.IGNORECASE):
                findings.append(f"ERROR css-import: {location}")
            for match in CSS_URL.finditer(css):
                target = match.group(2).strip()
                if target.startswith("#"):
                    referenced.add(target[1:])
                    continue
                classification = classify_reference(target)
                if classification == "dangerous":
                    findings.append(f"ERROR dangerous-css-reference: {target!r} in {location}")
                elif classification == "external" and not allow_external:
                    findings.append(f"ERROR external-css-reference: {target!r} in {location}")

        for raw_name, value in element.attrib.items():
            name = local_name(raw_name)
            if name.lower().startswith("on"):
                findings.append(f"ERROR event-handler: {name!r} on {location}")
            if name in {"href", "src"} and value.strip().startswith("#"):
                referenced.add(value.strip()[1:])
            if name in {"aria-labelledby", "aria-describedby"}:
                referenced.update(token for token in value.split() if token)
            if name in {"href", "src"}:
                classification = classify_reference(value)
                if classification == "dangerous":
                    findings.append(f"ERROR dangerous-reference: {name}={value!r} on {location}")
                elif classification == "external" and not allow_external:
                    findings.append(f"ERROR external-reference: {name}={value!r} on {location}")
            for match in CSS_URL.finditer(value):
                target = match.group(2).strip()
                if target.startswith("#"):
                    referenced.add(target[1:])
                    continue
                classification = classify_reference(target)
                if classification == "dangerous":
                    findings.append(f"ERROR dangerous-css-reference: {target!r} on {location}")
                elif classification == "external" and not allow_external:
                    findings.append(f"ERROR external-css-reference: {target!r} on {location}")

    for target in sorted(referenced - set(ids)):
        findings.append(f"ERROR unresolved-reference: #{target}")
    return findings


def main() -> int:
    args = parse_args()
    findings = validate(args.svg, args.allow_external)
    if findings:
        print("\n".join(findings), file=sys.stderr)
        return 1
    print(f"SVG validation passed: {args.svg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
