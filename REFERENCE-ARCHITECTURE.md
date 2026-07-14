# Reference Architecture

This document explains the system design behind Workspace as Context. It describes the responsibilities of each layer, the boundaries between them, and the reasons for the main design decisions.

## System goals

The architecture is designed to optimize for five properties:

1. Low retrieval cost.
2. Clear provenance.
3. Safe incremental editing.
4. Tool independence.
5. Clean project publication.

It is not designed to maximize automation or note count.

## Logical architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                       AGENT CONTRACT                        │
│       Session rules, workflows, safety, file contracts      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────┐   ┌────────────────────┐   ┌──────────────┐
│    EVIDENCE     │ → │     KNOWLEDGE      │ → │   PROJECTS   │
│  Raw and stable │   │ Linked and current │   │ Independent  │
└─────────────────┘   └────────────────────┘   └──────────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ CONTEXT AND LOGS   │
                    │ Current state and  │
                    │ change history     │
                    └────────────────────┘
```

## Physical structure

```text
workspace/
├── AGENTS.md
├── _context.md
├── index.md
├── log.md
├── reference-buffer/
├── domains/
│   ├── domain-a/
│   │   ├── domain-a.md
│   │   └── focused-note.md
│   └── domain-b/
│       ├── domain-b.md
│       └── focused-note.md
└── projects/
    └── README.md
```

The exact domain names are intentionally left to the user.

## File contracts

### `AGENTS.md`

**Owner:** Human, with agent suggestions.

**Purpose:** Define how an agent must operate inside the workspace.

**Contains:**

- session-start behavior
- routing rules
- ingest workflow
- editing constraints
- link conventions
- approval boundaries
- project rules
- verification requirements

**Does not contain:**

- large amounts of personal context
- detailed domain knowledge
- temporary task status

**Reason:** Operating rules change more slowly than active context. Mixing them would make the contract large and unstable.

### `_context.md`

**Owner:** Agent maintains, human reviews important changes.

**Purpose:** Provide the smallest useful session pickup.

**Contains:**

- active priorities
- current project status
- recent decisions
- open loops
- routing table for deeper files
- a short last-session summary

**Does not contain:**

- all historical details
- full source summaries
- copies of every domain note

**Reason:** The file should remain cheap enough to read at the start of every session.

### `index.md`

**Owner:** Agent maintains when domains change.

**Purpose:** Give humans a stable workspace map.

**Contains:**

- links to domain MOCs
- links to operating files
- a short explanation of the workspace

**Reason:** Human navigation and agent routing are related but not identical. The human index can be more descriptive than the fast-start context.

### `log.md`

**Owner:** Agent appends after meaningful changes.

**Purpose:** Record the meaning of important changes in chronological order.

**Format:**

```text
## [YYYY-MM-DD] type | summary
```

**Reason:** Git history answers what bytes changed. The log answers what changed in the system and why it mattered.

### `reference-buffer/`

**Owner:** Human adds files. Agent reads files.

**Purpose:** Preserve raw evidence.

**Rules:**

- never rewrite raw sources
- keep private material out of public repositories
- use stable filenames
- link to sources from compiled notes when useful

**Reason:** A knowledge system needs an auditable path back to evidence.

### Domain MOCs

**Owner:** Agent maintains when notes are created or substantially changed.

**Purpose:** Route readers into a domain.

**Contains:**

- short domain description
- links to canonical notes
- links to related domains
- current gaps or next actions when useful

**Reason:** A folder listing does not explain importance or relationships.

### Focused notes

**Owner:** Human and agent.

**Purpose:** Hold one durable topic, decision, concept, or plan.

**Rules:**

- one primary topic per file
- canonical home for repeated information
- links to related notes
- targeted edits over full rewrites

**Reason:** Small notes reduce retrieval cost and edit risk.

### `projects/`

**Owner:** Each project has its own ownership and repository rules.

**Purpose:** Connect the workspace to independently shippable work.

**Reason:** Code and personal knowledge require different histories, tools, access controls, and publication choices.

## Retrieval path

The default retrieval path is deterministic:

```text
Question
  ↓
_context.md
  ↓
Relevant domain MOC
  ↓
One or more focused notes
  ↓
Raw source only when verification is required
```

This path avoids two extremes:

- loading the entire workspace
- relying on opaque semantic search for every question

Search can still be added later. It becomes a fallback and discovery tool instead of the only navigation system.

## Write path

New information follows this path:

```text
Raw source arrives
  ↓
Source is preserved
  ↓
Relevant knowledge is extracted
  ↓
Focused notes are created or updated
  ↓
MOCs and cross-links are updated
  ↓
log.md records the change
  ↓
_context.md changes only if active state changed
```

This ensures that new information joins the graph and does not become an orphan file.

## Why Markdown

Markdown is used because it is:

- readable without a special application
- easy for AI tools to parse and edit
- friendly to Git history
- compatible with Obsidian wikilinks
- portable across operating systems and editors

A database can offer stronger queries and schemas. It also creates more setup, migration, and tooling dependence. Markdown is the simplest useful default for a personal workspace.

## Why MOCs instead of one global index

One global index works for a small workspace. As domains grow, it becomes either too long or too shallow.

MOCs create a two-level routing system:

```text
Global index → domain map → focused note
```

This structure is easy to understand and keeps the common read path short.

## Why both folders and links

Folders answer ownership and broad category. Links answer relationships.

A note can live in one folder but relate to several domains. Cross-links preserve those relationships without copying the note.

## Why an append-only log

The knowledge layer evolves. Readers need a simple way to understand recent changes without comparing file versions.

The log is intentionally selective. Recording every edit would create noise. It should capture new decisions, status changes, major ingests, and structural changes.

## Why project isolation

A software project should be able to answer these questions independently:

- What does it do?
- How is it installed?
- How is it tested?
- What changed over time?
- Who can access it?
- How is it released?

Those questions become harder when the project is only a folder inside a private knowledge repository.

Submodules are one option, not a requirement. A plain link or sibling repository may be simpler. The invariant is independent history.

## Scaling thresholds

Add tooling only when the current structure has a measured problem.

| Workspace state | Recommended response |
|---|---|
| Fewer than 50 notes | Use index, MOCs, and normal search |
| Links begin breaking | Run the audit tool in continuous integration |
| Hundreds of notes | Add full-text search or metadata queries |
| Large media archive | Store media outside Git and keep references |
| Multiple contributors | Add ownership, review, and access-control rules |
| Repeated ingest work | Add a small scripted or skill-based workflow |

These are guidance, not hard limits.

## Failure modes

### The context file becomes a database

**Symptom:** `_context.md` grows until it contains full histories and domain detail.

**Fix:** Move durable detail to focused notes. Keep links and current state in context.

### The schema becomes generic advice

**Symptom:** `AGENTS.md` says to be careful, clear, and helpful but gives no file-specific rules.

**Fix:** Replace vague guidance with observable workflows and approval boundaries.

### Notes become orphans

**Symptom:** New files exist but no MOC or related note links to them.

**Fix:** Make linking part of the same change that creates a note. Run the audit tool.

### The raw layer becomes editable

**Symptom:** Summaries overwrite sources or source files are cleaned up in place.

**Fix:** Treat the raw layer as immutable and write interpretation in the knowledge layer.

### Projects leak into the workspace history

**Symptom:** Application dependencies and generated files appear in the knowledge repository.

**Fix:** move the project to an independent repository and connect it by reference.

## Security boundary

The architecture separates information for a reason. Public projects should never inherit the privacy level of the workspace by accident.

Before publishing any repository:

1. Inspect tracked files.
2. Search for secrets and personal identifiers.
3. Replace real data with synthetic examples.
4. Confirm every referenced source is safe to share.
5. Review Git history, not only the current files.

## Technology choices

| Choice | Selected | Reason |
|---|---|---|
| Knowledge format | Markdown | Portable, readable, versionable |
| Relationship format | Obsidian wikilinks | Simple backlinks and graph navigation |
| History | Git plus `log.md` | Byte history plus semantic history |
| Agent configuration | `AGENTS.md` | Local, inspectable operating contract |
| Audit implementation | Python standard library | No dependency setup for a small check |
| Project boundary | Independent repositories | Clean history and publication control |

The architecture favors boring, durable tools. Complexity must prove that it reduces a real cost.
