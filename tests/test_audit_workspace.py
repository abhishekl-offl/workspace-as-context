from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.audit_workspace import audit_workspace, parse_wikilinks


class ParseWikilinksTests(unittest.TestCase):
    def test_parses_paths_aliases_and_headings(self) -> None:
        content = "[[domain/note|A note]] [[other#Section]] [[plain]]"
        self.assertEqual(parse_wikilinks(content), ["domain/note", "other", "plain"])

    def test_ignores_code_examples(self) -> None:
        content = "Use `[[path/note|Display]]`.\n\n```text\n[[another/example]]\n```"
        self.assertEqual(parse_wikilinks(content), [])


class AuditWorkspaceTests(unittest.TestCase):
    def make_workspace(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "index.md").write_text("# Index\n\n[[domain/note]]\n", encoding="utf-8")
        (root / "domain").mkdir()
        (root / "domain" / "note.md").write_text("# Note\n\n[[index]]\n", encoding="utf-8")
        return temporary, root

    def test_connected_workspace_passes(self) -> None:
        temporary, root = self.make_workspace()
        self.addCleanup(temporary.cleanup)
        result = audit_workspace(root)
        self.assertTrue(result.passed)
        self.assertEqual(result.markdown_files, 2)
        self.assertEqual(result.wikilinks, 2)

    def test_broken_link_fails(self) -> None:
        temporary, root = self.make_workspace()
        self.addCleanup(temporary.cleanup)
        (root / "index.md").write_text("# Index\n\n[[missing]]\n", encoding="utf-8")
        result = audit_workspace(root)
        self.assertFalse(result.passed)
        self.assertEqual(len(result.broken_links), 1)

    def test_orphan_note_fails(self) -> None:
        temporary, root = self.make_workspace()
        self.addCleanup(temporary.cleanup)
        (root / "domain" / "orphan.md").write_text("# Orphan\n", encoding="utf-8")
        result = audit_workspace(root)
        self.assertFalse(result.passed)
        self.assertEqual(result.orphan_notes, (Path("domain/orphan.md"),))


if __name__ == "__main__":
    unittest.main()
