#!/usr/bin/env python3
"""Render an SVG through independent engines and compare deterministic pixels."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any, Sequence


SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from validate_svg import validate as validate_structure  # noqa: E402


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CHROME_CANDIDATES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")


class RenderError(RuntimeError):
    """Raised when a renderer or PNG result violates the verification contract."""


@dataclass(frozen=True)
class DecodedPng:
    width: int
    height: int
    pixels: bytes


def _paeth(left: int, above: int, upper_left: int) -> int:
    estimate = left + above - upper_left
    left_distance = abs(estimate - left)
    above_distance = abs(estimate - above)
    upper_left_distance = abs(estimate - upper_left)
    if left_distance <= above_distance and left_distance <= upper_left_distance:
        return left
    if above_distance <= upper_left_distance:
        return above
    return upper_left


def decode_png(path: Path) -> DecodedPng:
    """Decode non-interlaced, 8-bit PNG into RGBA without third-party packages."""

    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise RenderError(f"{path} is not a PNG")
    offset = len(PNG_SIGNATURE)
    width = height = bit_depth = color_type = interlace = None
    compressed = bytearray()
    palette: bytes | None = None
    transparency: bytes | None = None
    while offset < len(data):
        if offset + 12 > len(data):
            raise RenderError(f"{path} has a truncated PNG chunk")
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_data = data[offset + 8 : offset + 8 + length]
        if len(chunk_data) != length:
            raise RenderError(f"{path} has a truncated {chunk_type!r} chunk")
        offset += 12 + length
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, _compression, _filter, interlace = struct.unpack(
                ">IIBBBBB", chunk_data
            )
        elif chunk_type == b"PLTE":
            palette = chunk_data
        elif chunk_type == b"tRNS":
            transparency = chunk_data
        elif chunk_type == b"IDAT":
            compressed.extend(chunk_data)
        elif chunk_type == b"IEND":
            break
    if not all(value is not None for value in (width, height, bit_depth, color_type, interlace)):
        raise RenderError(f"{path} has no valid IHDR")
    if bit_depth != 8 or interlace != 0:
        raise RenderError(f"{path} must use 8-bit non-interlaced PNG output")
    channels_by_type = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
    if color_type not in channels_by_type:
        raise RenderError(f"{path} uses unsupported PNG color type {color_type}")
    channels = channels_by_type[color_type]
    row_bytes = width * channels
    try:
        raw = zlib.decompress(bytes(compressed))
    except zlib.error as exc:
        raise RenderError(f"{path} contains invalid compressed pixels: {exc}") from exc
    if len(raw) != height * (row_bytes + 1):
        raise RenderError(f"{path} has an unexpected decoded byte length")

    rows: list[bytearray] = []
    cursor = 0
    previous = bytearray(row_bytes)
    for _row_index in range(height):
        filter_type = raw[cursor]
        cursor += 1
        encoded = raw[cursor : cursor + row_bytes]
        cursor += row_bytes
        decoded = bytearray(row_bytes)
        for index, value in enumerate(encoded):
            left = decoded[index - channels] if index >= channels else 0
            above = previous[index]
            upper_left = previous[index - channels] if index >= channels else 0
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = above
            elif filter_type == 3:
                predictor = (left + above) // 2
            elif filter_type == 4:
                predictor = _paeth(left, above, upper_left)
            else:
                raise RenderError(f"{path} uses unsupported PNG filter {filter_type}")
            decoded[index] = (value + predictor) & 0xFF
        rows.append(decoded)
        previous = decoded

    rgba = bytearray(width * height * 4)
    target = 0
    for row in rows:
        for offset in range(0, len(row), channels):
            sample = row[offset : offset + channels]
            if color_type == 0:
                red = green = blue = sample[0]
                alpha = 255
            elif color_type == 2:
                red, green, blue = sample
                alpha = 255
            elif color_type == 3:
                palette_index = sample[0]
                palette_offset = palette_index * 3
                if palette is None or palette_offset + 3 > len(palette):
                    raise RenderError(f"{path} has an invalid PNG palette index")
                red, green, blue = palette[palette_offset : palette_offset + 3]
                alpha = transparency[palette_index] if transparency and palette_index < len(transparency) else 255
            elif color_type == 4:
                red = green = blue = sample[0]
                alpha = sample[1]
            else:
                red, green, blue, alpha = sample
            rgba[target : target + 4] = bytes((red, green, blue, alpha))
            target += 4
    return DecodedPng(width=width, height=height, pixels=bytes(rgba))


def _renderer_binary(renderer: str) -> str | None:
    if renderer == "rsvg":
        return shutil.which("rsvg-convert")
    if renderer == "chromium":
        configured = os.environ.get("CHROME_BIN")
        if configured and Path(configured).is_file():
            return configured
        return next((path for name in CHROME_CANDIDATES if (path := shutil.which(name))), None)
    raise RenderError(f"unknown renderer: {renderer}")


def _run(command: list[str], renderer: str) -> None:
    completed = subprocess.run(command, text=True, capture_output=True, check=False, timeout=60)
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RenderError(f"{renderer} failed with exit {completed.returncode}: {detail}")


def _render_rsvg(binary: str, svg: Path, output: Path, width: int, height: int) -> None:
    _run(
        [binary, "--width", str(width), "--height", str(height), "--output", str(output), str(svg)],
        "rsvg",
    )


def _render_chromium(
    binary: str,
    svg: Path,
    output: Path,
    width: int,
    height: int,
    work: Path,
    chromium_no_sandbox: bool = False,
) -> None:
    markup = svg.read_text(encoding="utf-8")
    html = work / f"browser-{width}x{height}.html"
    html.write_text(
        "<!doctype html><meta charset='utf-8'>"
        "<meta http-equiv='Content-Security-Policy' "
        "content=\"default-src 'none'; img-src data:; style-src 'unsafe-inline'\">"
        "<style>"
        f"html,body{{margin:0;width:{width}px;height:{height}px;overflow:hidden;background:transparent}}"
        f"svg{{display:block;width:{width}px!important;height:{height}px!important}}"
        "</style>" + markup,
        encoding="utf-8",
    )
    command = [binary, "--headless=new"]
    if chromium_no_sandbox or (hasattr(os, "geteuid") and os.geteuid() == 0):
        command.append("--no-sandbox")
    command.extend(
        [
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--default-background-color=00000000",
            f"--window-size={width},{height}",
            f"--screenshot={output}",
            html.resolve().as_uri(),
        ]
    )
    _run(command, "chromium")


def _metrics(image: DecodedPng) -> dict[str, Any]:
    visible_pixel_count = 0
    min_x = image.width
    min_y = image.height
    max_x = -1
    max_y = -1
    for pixel_index in range(image.width * image.height):
        if image.pixels[pixel_index * 4 + 3] != 0:
            x = pixel_index % image.width
            y = pixel_index // image.width
            visible_pixel_count += 1
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
    if visible_pixel_count == 0:
        raise RenderError("renderer produced a fully transparent image")
    return {
        "visible_pixel_count": visible_pixel_count,
        "visible_fraction": round(visible_pixel_count / (image.width * image.height), 6),
        "visible_bbox": [min_x, min_y, max_x + 1, max_y + 1],
    }


def _comparison_metrics(left: DecodedPng, right: DecodedPng) -> dict[str, float]:
    if (left.width, left.height) != (right.width, right.height):
        raise RenderError("renderer outputs have different pixel dimensions")
    total_difference = 0
    visible_difference = 0
    union_pixels = 0
    mask_mismatch = 0
    for index in range(0, len(left.pixels), 4):
        left_alpha = left.pixels[index + 3]
        right_alpha = right.pixels[index + 3]
        pixel_difference = 0
        for channel in range(3):
            pixel_difference += abs(
                left.pixels[index + channel] * left_alpha // 255
                - right.pixels[index + channel] * right_alpha // 255
            )
        pixel_difference += abs(left_alpha - right_alpha)
        total_difference += pixel_difference
        left_visible = left_alpha > 8
        right_visible = right_alpha > 8
        if left_visible or right_visible:
            union_pixels += 1
            visible_difference += pixel_difference
            if left_visible != right_visible:
                mask_mismatch += 1
    left_bbox = _metrics(left)["visible_bbox"]
    right_bbox = _metrics(right)["visible_bbox"]
    bbox_delta = max(
        abs(left_bbox[index] - right_bbox[index])
        / (left.width if index in (0, 2) else left.height)
        for index in range(4)
    )
    return {
        "mean_channel_diff": total_difference / (len(left.pixels) * 255),
        "visible_region_diff": visible_difference / (max(1, union_pixels) * 4 * 255),
        "mask_mismatch_fraction": mask_mismatch / max(1, union_pixels),
        "normalized_bbox_delta": bbox_delta,
    }


def verify(
    svg: Path,
    renderers: Sequence[str],
    sizes: Sequence[tuple[int, int]],
    require_renderers: int,
    max_mean_channel_diff: float,
    output_dir: Path | None,
    min_transparent_margin: int = 0,
    max_visible_region_diff: float = 0.18,
    max_mask_mismatch: float = 0.08,
    max_normalized_bbox_delta: float = 0.05,
    chromium_no_sandbox: bool = False,
) -> dict[str, Any]:
    findings = validate_structure(svg, False)
    if findings:
        raise RenderError("structural validation failed: " + "; ".join(findings))
    resolved: dict[str, str] = {}
    for renderer in renderers:
        binary = _renderer_binary(renderer)
        if binary:
            resolved[renderer] = binary
    if len(resolved) < require_renderers:
        missing = sorted(set(renderers) - set(resolved))
        raise RenderError(
            f"found {len(resolved)} renderer(s), require {require_renderers}; missing: {', '.join(missing) or 'none'}"
        )

    temporary = tempfile.TemporaryDirectory(prefix="advanced-svg-render-") if output_dir is None else None
    work = Path(temporary.name) if temporary else output_dir
    assert work is not None
    work.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "svg": str(svg),
        "svg_sha256": hashlib.sha256(svg.read_bytes()).hexdigest(),
        "renderers": resolved,
        "sizes": [],
        "max_mean_channel_diff": max_mean_channel_diff,
        "min_transparent_margin": min_transparent_margin,
        "max_visible_region_diff": max_visible_region_diff,
        "max_mask_mismatch": max_mask_mismatch,
        "max_normalized_bbox_delta": max_normalized_bbox_delta,
        "chromium_no_sandbox": chromium_no_sandbox,
    }
    try:
        for width, height in sizes:
            images: dict[str, DecodedPng] = {}
            size_report: dict[str, Any] = {"size": [width, height], "outputs": {}, "comparisons": []}
            for renderer, binary in resolved.items():
                output = work / f"{svg.stem}-{renderer}-{width}x{height}.png"
                if renderer == "rsvg":
                    _render_rsvg(binary, svg, output, width, height)
                else:
                    _render_chromium(
                        binary,
                        svg,
                        output,
                        width,
                        height,
                        work,
                        chromium_no_sandbox,
                    )
                image = decode_png(output)
                if (image.width, image.height) != (width, height):
                    raise RenderError(
                        f"{renderer} produced {image.width}x{image.height}; expected {width}x{height}"
                    )
                images[renderer] = image
                metrics = _metrics(image)
                left, top, right, bottom = metrics["visible_bbox"]
                actual_margin = min(left, top, width - right, height - bottom)
                if actual_margin < min_transparent_margin:
                    raise RenderError(
                        f"{renderer} visible bounds leave {actual_margin}px transparent margin; "
                        f"require {min_transparent_margin}px at {width}x{height}"
                    )
                size_report["outputs"][renderer] = {
                    "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                    **metrics,
                    "minimum_transparent_margin": actual_margin,
                }
                if output_dir is not None:
                    size_report["outputs"][renderer]["path"] = str(output)
            for left_name, right_name in combinations(images, 2):
                metrics = _comparison_metrics(images[left_name], images[right_name])
                failures = []
                if metrics["mean_channel_diff"] > max_mean_channel_diff:
                    failures.append("full-canvas difference")
                if metrics["visible_region_diff"] > max_visible_region_diff:
                    failures.append("visible-region difference")
                if metrics["mask_mismatch_fraction"] > max_mask_mismatch:
                    failures.append("visibility-mask mismatch")
                if metrics["normalized_bbox_delta"] > max_normalized_bbox_delta:
                    failures.append("visible-bounds delta")
                size_report["comparisons"].append(
                    {
                        "renderers": [left_name, right_name],
                        **{name: round(value, 6) for name, value in metrics.items()},
                        "status": "fail" if failures else "pass",
                    }
                )
                if failures:
                    raise RenderError(
                        f"{left_name}/{right_name} exceeded {', '.join(failures)} thresholds "
                        f"at {width}x{height}: {json.dumps(metrics, sort_keys=True)}"
                    )
            report["sizes"].append(size_report)
    finally:
        if temporary:
            temporary.cleanup()
    report["status"] = "pass"
    return report


def _size(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split("x", 1)
        width, height = int(width_text), int(height_text)
    except (ValueError, AttributeError) as exc:
        raise argparse.ArgumentTypeError("size must be WIDTHxHEIGHT") from exc
    if not 1 <= width <= 4096 or not 1 <= height <= 4096:
        raise argparse.ArgumentTypeError("size dimensions must be between 1 and 4096")
    return width, height


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path)
    parser.add_argument("--renderer", action="append", choices=("rsvg", "chromium"))
    parser.add_argument("--size", action="append", type=_size)
    parser.add_argument("--require-renderers", type=int, default=1, choices=(1, 2))
    parser.add_argument("--max-mean-channel-diff", type=float, default=0.12)
    parser.add_argument("--max-visible-region-diff", type=float, default=0.18)
    parser.add_argument("--max-mask-mismatch", type=float, default=0.08)
    parser.add_argument("--max-normalized-bbox-delta", type=float, default=0.05)
    parser.add_argument("--min-transparent-margin", type=int, default=0)
    parser.add_argument(
        "--chromium-no-sandbox",
        action="store_true",
        help="disable Chromium's process sandbox for an already-isolated trusted CI runner",
    )
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    renderers = args.renderer or ["rsvg", "chromium"]
    sizes = args.size or [(32, 32), (128, 128), (512, 512)]
    for name in (
        "max_mean_channel_diff",
        "max_visible_region_diff",
        "max_mask_mismatch",
        "max_normalized_bbox_delta",
    ):
        if not 0 <= getattr(args, name) <= 1:
            print(f"render verification error: --{name.replace('_', '-')} must be between 0 and 1", file=sys.stderr)
            return 2
    if args.min_transparent_margin < 0:
        print("render verification error: --min-transparent-margin must be non-negative", file=sys.stderr)
        return 2
    try:
        report = verify(
            args.svg,
            renderers,
            sizes,
            args.require_renderers,
            args.max_mean_channel_diff,
            args.output_dir,
            args.min_transparent_margin,
            args.max_visible_region_diff,
            args.max_mask_mismatch,
            args.max_normalized_bbox_delta,
            args.chromium_no_sandbox,
        )
    except (OSError, subprocess.TimeoutExpired, RenderError) as exc:
        print(f"render verification error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
