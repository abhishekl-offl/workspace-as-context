# Workspace Instructions

## Session start

Before answering a workspace question:

1. Read `_context.md`.
2. Identify the relevant domain.
3. Read that domain's map of content.
4. Open only the focused notes required for the task.

Do not scan the entire workspace by default.

## Workspace layers

1. `reference-buffer/` contains raw evidence. Read it but never rewrite it.
2. `domains/` contains maintained and linked knowledge.
3. `projects/` points to independent project repositories.

## Ingest workflow

When new information arrives:

1. Preserve the raw source in `reference-buffer/`.
2. Create or update one focused knowledge note.
3. Link the note from its domain map and from related notes.
4. Append a meaningful entry to `log.md`.
5. Update `_context.md` only when an active decision or status changed.

## Linking

- Use `[[path/note|Display text]]` wikilinks.
- Omit `.md` inside wikilinks.
- Use paths when filenames could be ambiguous.
- Do not create orphan notes.

## Editing safety

- Prefer targeted edits over full rewrites.
- Never delete a file without human approval.
- Never rewrite a raw source.
- Preserve unrelated content.
- Ask before moving folders or changing the workspace architecture.

## Projects

Keep each software project in an independent Git repository. Commit project code inside that repository, not in the knowledge workspace.

## Verification

After creating or moving a note, verify that:

- all wikilinks resolve
- the note has an inbound link
- the relevant domain map is current
- `log.md` records meaningful structural changes
