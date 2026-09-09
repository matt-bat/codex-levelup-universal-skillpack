import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import tracemalloc
import unittest
from unittest import mock


SKILLS_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = SKILLS_ROOT / "advanced-svg/scripts/render_svg.py"
FIXTURE = SKILLS_ROOT / "advanced-svg/assets/render-smoke.svg"
SPEC = importlib.util.spec_from_file_location("advanced_svg_render", SCRIPT)
assert SPEC and SPEC.loader
renderer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = renderer
SPEC.loader.exec_module(renderer)


class TestAdvancedSvgRender(unittest.TestCase):
    def test_rsvg_renders_multiple_sizes_and_reports_visible_bounds(self):
        if not shutil.which("rsvg-convert"):
            self.skipTest("rsvg-convert is unavailable")
        report = renderer.verify(FIXTURE, ["rsvg"], [(32, 32), (128, 128)], 1, 0.12, None)
        self.assertEqual(report["status"], "pass")
        self.assertEqual([item["size"] for item in report["sizes"]], [[32, 32], [128, 128]])
        for item in report["sizes"]:
            output = item["outputs"]["rsvg"]
            self.assertGreater(output["visible_pixel_count"], 0)
            self.assertEqual(len(output["visible_bbox"]), 4)

    def test_blank_render_fails_even_when_svg_is_structurally_valid(self):
        if not shutil.which("rsvg-convert"):
            self.skipTest("rsvg-convert is unavailable")
        with tempfile.TemporaryDirectory() as temp_dir:
            blank = Path(temp_dir) / "blank.svg"
            blank.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" aria-hidden="true"></svg>',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(renderer.RenderError, "fully transparent"):
                renderer.verify(blank, ["rsvg"], [(16, 16)], 1, 0.12, None)

    def test_missing_required_renderer_fails_closed(self):
        with mock.patch.object(renderer, "_renderer_binary", return_value=None):
            with self.assertRaisesRegex(renderer.RenderError, "require 2"):
                renderer.verify(FIXTURE, ["rsvg", "chromium"], [(16, 16)], 2, 0.12, None)

    def test_visible_region_metric_detects_small_divergent_detail(self):
        transparent = bytearray(100 * 100 * 4)
        left = bytearray(transparent)
        right = bytearray(transparent)
        for pixel in range(10):
            offset = (50 * 100 + 45 + pixel) * 4
            left[offset : offset + 4] = bytes((255, 255, 255, 255))
            right[offset : offset + 4] = bytes((0, 0, 0, 255))
        left_image = renderer.DecodedPng(100, 100, bytes(left))
        right_image = renderer.DecodedPng(100, 100, bytes(right))
        metrics = renderer._comparison_metrics(left_image, right_image)
        self.assertLess(metrics["mean_channel_diff"], 0.01)
        self.assertGreater(metrics["visible_region_diff"], 0.7)

    def test_visible_bounds_are_computed_with_constant_auxiliary_memory(self):
        pixels = bytes((255, 255, 255, 255)) * (1024 * 1024)
        image = renderer.DecodedPng(1024, 1024, pixels)
        tracemalloc.start()
        try:
            metrics = renderer._metrics(image)
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        self.assertEqual(metrics["visible_bbox"], [0, 0, 1024, 1024])
        self.assertLess(peak, 1_000_000)

    def test_bbox_delta_normalizes_each_axis_independently(self):
        left = bytearray(100 * 10 * 4)
        right = bytearray(left)
        left[(4 * 100 + 50) * 4 + 3] = 255
        right[(5 * 100 + 50) * 4 + 3] = 255
        metrics = renderer._comparison_metrics(
            renderer.DecodedPng(100, 10, bytes(left)),
            renderer.DecodedPng(100, 10, bytes(right)),
        )
        self.assertAlmostEqual(metrics["normalized_bbox_delta"], 0.1)

    def test_chromium_no_sandbox_requires_root_or_explicit_opt_in(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            svg = work / "safe.svg"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true"/>')
            with mock.patch.object(renderer.os, "geteuid", return_value=1000), mock.patch.object(
                renderer, "_run"
            ) as run:
                renderer._render_chromium("chrome", svg, work / "safe.png", 16, 16, work)
                self.assertNotIn("--no-sandbox", run.call_args.args[0])

                renderer._render_chromium(
                    "chrome", svg, work / "trusted.png", 16, 16, work, chromium_no_sandbox=True
                )
                self.assertIn("--no-sandbox", run.call_args.args[0])

    def test_cross_renderer_matrix_when_chromium_is_available(self):
        if not shutil.which("rsvg-convert") or not renderer._renderer_binary("chromium"):
            self.skipTest("cross-renderer dependencies are unavailable")
        report = renderer.verify(FIXTURE, ["rsvg", "chromium"], [(64, 64)], 2, 0.12, None)
        comparison = report["sizes"][0]["comparisons"][0]
        self.assertEqual(comparison["status"], "pass")
        self.assertLessEqual(comparison["mean_channel_diff"], 0.12)


if __name__ == "__main__":
    unittest.main()
