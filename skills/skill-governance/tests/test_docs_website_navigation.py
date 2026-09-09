from pathlib import Path
import re
import unittest
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[3]
DOCS_ROOT = REPO_ROOT / "skills" / "docs"
DOCS_HOME = DOCS_ROOT / "README.md"
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
GENERATED_OR_EVIDENCE_PAGES = {
    DOCS_ROOT / "chat-history-index.md",
    DOCS_ROOT / "chat-history-summary.md",
    DOCS_ROOT / "skill-decision-tree.md",
    DOCS_ROOT / "skill-index.md",
}


def local_targets(page: Path):
    for match in LINK_PATTERN.finditer(page.read_text(encoding="utf-8")):
        raw = match.group(1).strip()
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        target_text = raw.split(maxsplit=1)[0]
        if target_text.startswith(("#", "http://", "https://", "mailto:")):
            continue
        path_text = unquote(target_text.split("#", 1)[0].split("?", 1)[0])
        if not path_text:
            continue
        target = (REPO_ROOT / path_text.lstrip("/")) if path_text.startswith("/") else (page.parent / path_text)
        yield target.resolve()


class TestDocsWebsiteNavigation(unittest.TestCase):
    def test_documentation_home_indexes_every_docs_page(self):
        home = DOCS_HOME.read_text(encoding="utf-8")
        for page in sorted(DOCS_ROOT.rglob("*.md")):
            if page == DOCS_HOME:
                continue
            relative = page.relative_to(DOCS_ROOT).as_posix()
            with self.subTest(page=relative):
                self.assertIn(f"(./{relative})", home)

    def test_maintained_guide_pages_link_back_to_documentation_home(self):
        for page in sorted(DOCS_ROOT.rglob("*.md")):
            if page == DOCS_HOME or page in GENERATED_OR_EVIDENCE_PAGES:
                continue
            with self.subTest(page=page.relative_to(DOCS_ROOT).as_posix()):
                self.assertIn("[Documentation home]", page.read_text(encoding="utf-8"))

    def test_every_local_docs_link_resolves(self):
        for page in sorted(DOCS_ROOT.rglob("*.md")):
            for target in local_targets(page):
                with self.subTest(
                    page=page.relative_to(REPO_ROOT).as_posix(),
                    target=str(target),
                ):
                    self.assertTrue(target.exists(), f"broken local link from {page}: {target}")

    def test_primary_entry_pages_link_to_documentation_home(self):
        for relative in ("README.md", "START_HERE.md", "skills/README.md", "skills/USAGE.md"):
            page = REPO_ROOT / relative
            with self.subTest(page=relative):
                self.assertIn("docs/README.md", page.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
