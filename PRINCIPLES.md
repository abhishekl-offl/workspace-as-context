# Workspace as Context: Principles

This document is the center of the project.

The folder template and audit tool are useful, but they are implementations. The principles explain why the system has this shape and how to make decisions when the template no longer fits.

## 1. Compile knowledge once

### The idea

When a source contains durable information, turn that information into a maintained knowledge note. Do not reconstruct the same understanding from raw material every time a related question appears.

### Why

Reading the same long document repeatedly wastes time and context. It also creates inconsistent answers because each reading may emphasize something different.

A compiled note gives the knowledge a stable home. New sources can strengthen, qualify, or contradict that note over time.

### Failure mode

A workspace contains hundreds of PDFs and transcripts but almost no maintained knowledge. Every question triggers a new search through raw material.

### Operating rule

Raw sources remain unchanged. Durable takeaways are integrated into focused notes that can be updated and linked.

## 2. Make retrieval cheap

### The idea

The common path should require very little reading. More detail should be available through links when it is needed.

### Why

An agent has a limited context window and a human has limited attention. Loading a whole workspace for every question reduces both speed and accuracy.

The solution is progressive disclosure:

```text
Fast context → domain map → focused note → raw evidence
```

Each layer is more detailed than the previous layer.

### Failure mode

The agent starts every session by scanning many folders, or the user pastes a large master prompt containing information unrelated to the task.

### Operating rule

Begin with `_context.md`. Read the relevant domain MOC next. Open focused notes only when required.

## 3. Separate evidence, knowledge, and execution

### The idea

Raw evidence, maintained knowledge, and shippable projects have different lifecycles. Give them different places.

### Why

Evidence should preserve provenance. Knowledge should evolve. Projects should be independently testable and publishable.

Mixing the three makes every operation harder. A public code repository should not accidentally include personal source material. A private workspace should not become the only home for project code.

### Failure mode

Raw documents are rewritten as summaries, project code is committed to a personal wiki, or private context leaks into a public repository.

### Operating rule

Use three clear layers:

1. Evidence: read-only raw sources.
2. Knowledge: linked and maintained Markdown.
3. Execution: independent project repositories.

## 4. Give the agent a contract

### The idea

Durable behavior belongs in a versioned file near the work, not only in a chat message.

### Why

Chats end. Models change. Different tools may work on the same folder. A written contract makes expectations inspectable and repeatable.

The contract should describe structure, workflows, approval boundaries, and definitions of done.

### Failure mode

The agent behaves differently in every session because the important rules exist only in the user's memory.

### Operating rule

Keep a concise `AGENTS.md` at the workspace root. Update it when a repeated mistake reveals a missing rule.

## 5. Prefer append and link

### The idea

Make the smallest change that preserves existing useful information. Add context and connections before considering a full rewrite.

### Why

AI systems are good at producing clean summaries. They are also capable of removing details that look minor but matter later.

Targeted edits are easier to review and less likely to cause silent loss.

### Failure mode

A note becomes shorter and cleaner, but a decision, caveat, or historical fact disappears.

### Operating rule

Use targeted edits. Append new sections when appropriate. Require explicit approval before full rewrites or destructive operations.

## 6. Keep the graph connected

### The idea

A note that cannot be reached from a map or related note is effectively lost.

### Why

Folder search can find files by name, but it does not explain relationships. Links carry meaning and help both humans and agents move through the workspace.

MOCs create stable hubs. Cross-links reveal relationships between domains.

### Failure mode

New notes accumulate as isolated files. Search still works, but the knowledge base no longer helps the reader understand how ideas connect.

### Operating rule

Every meaningful note must be linked from a domain MOC or another canonical note in the same change that creates it.

## 7. Isolate what you ship

### The idea

Every software project or public artifact should have its own repository and history.

### Why

Projects need clean commits, issue tracking, tests, releases, and collaboration boundaries. The knowledge workspace has a different purpose and often a different privacy level.

The workspace may track project status and decisions. It should not absorb the project's code.

### Failure mode

One large repository contains personal notes, unrelated applications, experiments, secrets, and deployment configuration.

### Operating rule

Keep projects independent. Connect them to the workspace with links, submodules, or status notes, but commit project code inside the project repository.

## How the principles work together

The principles are not independent tips.

- Compilation creates durable knowledge.
- Cheap retrieval makes that knowledge practical to use.
- Layer separation preserves provenance and publication boundaries.
- The agent contract makes maintenance consistent.
- Append-first editing protects information.
- Graph connectivity keeps knowledge discoverable.
- Project isolation turns learning into clean, shippable work.

Together they create a workspace that can grow without requiring every future session to start from zero.

## Decision test

When deciding whether a new convention belongs in the workspace, ask:

1. Does it reduce repeated work?
2. Does it make retrieval cheaper?
3. Does it preserve provenance?
4. Can a human understand it from the files alone?
5. Can an agent follow it without hidden context?
6. Does it reduce the chance of silent information loss?
7. Does it keep public projects independent and safe to publish?

If the answer is mostly no, the convention is probably adding structure without value.
