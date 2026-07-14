#!/usr/bin/env python3
"""Run lightweight integrity checks for this public repository."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    "README.md",
    "PRINCIPLES.md",
    "REFERENCE-ARCHITECTURE.md",
    "ADOPTION-GUIDE.md",
    "ACKNOWLEDGEMENTS.md",
    "LICENSE",
    "starter/AGENTS.md",
    "starter/_context.md",
    "starter/index.md",
    "starter/log.md",
    "tools/audit_workspace.py",
)
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PRIVATE_MARKERS = ("/" + "Users" + "/", "abhishekl.offl" + "@" + "gmail.com")


def repository_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)


def text_files() -> list[Path]:
    allowed = {".md", ".py", ".yml", ".yaml", ".svg", ".txt", ""}
    return [path for path in repository_files() if path.suffix.lower() in allowed]


def check_required_paths(errors: list[str]) -> None:
    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).exists():
            errors.append(f"missing required path: {relative}")


def check_public_text(errors: list[str]) -> None:
    for path in text_files():
        content = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if "\u2014" in content or "\u2013" in content:
            errors.append(f"en or em dash found: {relative}")
        for marker in PRIVATE_MARKERS:
            if marker in content:
                errors.append(f"private marker found in {relative}: {marker}")


def check_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        content = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_PATTERN.finditer(content):
            target = match.group(1).strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            candidate = (path.parent / target).resolve()
            if not candidate.exists():
                errors.append(f"broken Markdown link in {path.relative_to(ROOT)}: {target}")


def check_svg(errors: list[str]) -> None:
    for path in ROOT.rglob("*.svg"):
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            errors.append(f"invalid SVG {path.relative_to(ROOT)}: {exc}")


def main() -> int:
    errors: list[str] = []
    check_required_paths(errors)
    check_public_text(errors)
    check_markdown_links(errors)
    check_svg(errors)

    if errors:
        print("Repository validation failed")
        for error in errors:
            print(f"  {error}")
        return 1

    print("Repository validation passed")
    print(f"Checked files: {len(repository_files())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
