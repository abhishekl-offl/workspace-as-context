# Acknowledgements and Attribution

Workspace as Context combines ideas from existing work with lessons from operating a real long-running workspace.

Clear attribution matters because the goal is to extend useful ideas, not to rename them.

## Andrej Karpathy's LLM Wiki

Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) describes a pattern in which an LLM maintains a persistent, interlinked Markdown wiki between raw sources and user questions. It also describes an agent schema that records structure and workflows.

This project adopts those foundational ideas:

- raw sources remain available
- knowledge is compiled into maintained Markdown
- links make the knowledge navigable
- an agent-facing schema guides maintenance

Karpathy's document is intentionally abstract about the exact implementation.

## Karpathy-Inspired Claude Code Guidelines

The community-maintained [Karpathy-Inspired Claude Code Guidelines](https://github.com/multica-ai/andrej-karpathy-skills) distill common AI-coding failure modes into practical rules about assumptions, simplicity, surgical changes, and verification.

This project applies similar discipline to knowledge maintenance, especially targeted editing, explicit approval boundaries, and verifiable graph health.

The guidelines repository is community-authored and inspired by Andrej Karpathy's observations. It is not presented here as a repository authored by Karpathy.

## Original contribution of this project

Workspace as Context is a concrete workspace architecture built around these additions:

- `_context.md` as a deliberately small agent fast-start file
- separate human and agent entry points
- domain MOCs as a progressive retrieval layer
- retrieval cost as a system-design constraint
- explicit zero-loss editing discipline
- a no-orphan rule for graph health
- an append-only semantic change log
- independent project repositories as a publication boundary
- a small audit tool that checks broken links and orphans

The wording, starter files, diagrams, system explanation, and audit implementation in this repository are original to this project.

## Reuse policy

This repository does not copy the source documents. It explains the resulting architecture in new language, links to its influences, and provides an independently written implementation under the MIT License.
