#!/usr/bin/env python3
"""Audit an Obsidian-style Markdown workspace for graph health."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


WIKILINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")
FENCED_CODE_PATTERN = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_PATTERN = re.compile(r"`[^`]*`")
DEFAULT_ORPHAN_EXEMPTIONS = {
    "AGENTS.md",
    "_context.md",
    "index.md",
    "log.md",
}


@dataclass(frozen=True)
class LinkIssue:
    source: Path
    target: str


@dataclass(frozen=True)
class AuditResult:
    markdown_files: int
    wikilinks: int
    broken_links: tuple[LinkIssue, ...]
    orphan_notes: tuple[Path, ...]

    @property
    def passed(self) -> bool:
        return not self.broken_links and not self.orphan_notes


def markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if ".git" not in path.parts and not any(part.startswith(".") for part in path.relative_to(root).parts)
    )


def parse_wikilinks(content: str) -> list[str]:
    content = FENCED_CODE_PATTERN.sub("", content)
    content = INLINE_CODE_PATTERN.sub("", content)
    targets: list[str] = []
    for match in WIKILINK_PATTERN.finditer(content):
        target = match.group(1).split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            targets.append(target)
    return targets


def candidate_paths(root: Path, source: Path, target: str) -> list[Path]:
    raw = Path(target)
    with_suffix = raw if raw.suffix else raw.with_suffix(".md")
    candidates = [root / with_suffix, source.parent / with_suffix]

    if "/" not in target and "\\" not in target:
        candidates.extend(path for path in root.rglob(with_suffix.name))

    unique: list[Path] = []
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved not in unique:
            unique.append(resolved)
    return unique


def resolve_target(root: Path, source: Path, target: str) -> Path | None:
    matches = [path for path in candidate_paths(root, source, target) if path.is_file()]
    if len(matches) == 1:
        return matches[0]
    return None


def audit_workspace(root: Path) -> AuditResult:
    root = root.resolve()
    files = markdown_files(root)
    incoming = {path.resolve(): 0 for path in files}
    broken: list[LinkIssue] = []
    link_count = 0

    for source in files:
        content = source.read_text(encoding="utf-8")
        for target in parse_wikilinks(content):
            link_count += 1
            resolved = resolve_target(root, source, target)
            if resolved is None:
                broken.append(LinkIssue(source.relative_to(root), target))
                continue
            if resolved in incoming and resolved != source.resolve():
                incoming[resolved] += 1

    orphans = tuple(
        path.relative_to(root)
        for path in files
        if path.name not in DEFAULT_ORPHAN_EXEMPTIONS and incoming[path.resolve()] == 0
    )

    return AuditResult(
        markdown_files=len(files),
        wikilinks=link_count,
        broken_links=tuple(broken),
        orphan_notes=orphans,
    )


def print_result(result: AuditResult) -> None:
    status = "passed" if result.passed else "failed"
    print(f"Workspace audit {status}")
    print(f"Markdown files: {result.markdown_files}")
    print(f"Wikilinks: {result.wikilinks}")
    print(f"Broken links: {len(result.broken_links)}")
    print(f"Orphan notes: {len(result.orphan_notes)}")

    for issue in result.broken_links:
        print(f"  broken: {issue.source} -> {issue.target}")
    for path in result.orphan_notes:
        print(f"  orphan: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Path to the workspace to audit")
    args = parser.parse_args()

    if not args.root.is_dir():
        parser.error(f"workspace does not exist: {args.root}")

    result = audit_workspace(args.root)
    print_result(result)
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
