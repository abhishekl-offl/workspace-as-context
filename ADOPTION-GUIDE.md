# Adoption Guide

This guide helps you introduce Workspace as Context without reorganizing everything at once.

## Before you start

Choose one real use case. Examples:

- personal career planning
- research notes
- product-management work
- learning and reading notes
- a portfolio of software projects

Do not begin by migrating every file you own. A small working system is easier to judge and improve.

## Path A: Start from the template

### Step 1: Copy the starter

```bash
cp -R starter my-workspace
cd my-workspace
git init
```

### Step 2: Define the purpose

Open `_context.md` and write:

- what the workspace is for
- what is active now
- what should happen next

Keep the first version short.

### Step 3: Create one domain

Rename `domains/example/` to a real domain such as `learning/`.

Rename the MOC to match:

```text
domains/learning/learning.md
```

Update `index.md` so it links to the new MOC.

### Step 4: Adapt the agent contract

Open `AGENTS.md` and decide:

- what the agent reads first
- what files it may never rewrite
- which changes require approval
- how new notes join the graph
- how projects are handled

Delete rules that do not apply to you.

### Step 5: Add one real source

Put a document or transcript in `reference-buffer/`. Ask the agent to summarize it into a focused note and connect that note to the domain MOC.

Review the result. This first ingest will reveal which rules need improvement.

### Step 6: Run the audit

From this repository:

```bash
python3 tools/audit_workspace.py /path/to/my-workspace
```

Fix broken links and orphans before adding more material.

## Path B: Adapt an existing folder

### Step 1: Make a backup

Before moving or renaming files, create a backup or a Git commit you can return to.

### Step 2: Add control files

Add these files without moving existing content:

```text
AGENTS.md
_context.md
index.md
log.md
```

Use them to describe the current structure first.

### Step 3: Identify domains

Look for a small number of stable areas such as work, learning, finances, writing, or projects.

Create one MOC per domain. Link to existing files from the MOC before moving anything.

### Step 4: Separate raw sources

Identify files that are evidence rather than maintained knowledge. Examples include exports, PDFs, and transcripts.

Move them only after you have confirmed that links and tools will continue to work. If moving is risky, leave them in place and document the raw-source rule first.

### Step 5: Separate projects

Check whether application code is mixed with notes. If it is, plan a separate repository for each project.

Do not move all projects in one operation. Move one, verify its history and setup, then continue.

### Step 6: Introduce zero-loss editing

Add approval rules for deletion, full rewrites, and large restructures. Ask the agent to make targeted edits and preserve unrelated content.

### Step 7: Audit and simplify

Run the audit tool. Remove conventions that do not solve a real problem.

## A practical first week

### Day 1

- Create the control files.
- Define one domain.
- Write a short context file.

### Day 2

- Ingest one source.
- Review the note and links.
- Improve the contract.

### Day 3

- Use the workspace for a real question.
- Observe which files the agent needed.
- Remove unnecessary startup context.

### Day 4

- Add a second domain only if required.
- Add one cross-domain link.

### Day 5

- Run the audit.
- Review the log.
- Decide whether the system saved time.

## Migration rules

1. Back up before restructuring.
2. Move one domain at a time.
3. Do not rewrite raw sources.
4. Update links in the same change as a move.
5. Verify project repositories independently.
6. Stop adding structure when the current problem is solved.

## How to know it is working

After a few sessions, you should be able to answer yes to these questions:

- Can the agent begin after reading one small file?
- Can a human find each domain from `index.md`?
- Does every meaningful note have an inbound link?
- Can you trace a summary back to evidence?
- Are projects independently buildable and publishable?
- Did a recent decision get recorded without rewriting history?

If not, fix the smallest failing part before expanding the system.
