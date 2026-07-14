# Repository Instructions

## Purpose

This is a document-first public repository that explains and implements the Workspace as Context pattern.

## Editing rules

- Keep the English direct and easy to understand.
- Do not use em dashes anywhere in repository content.
- Preserve the distinction between inspiration and original contribution.
- Never add private workspace content, employer information, credentials, or real personal data.
- Prefer small targeted edits over broad rewrites.
- Do not add dependencies unless a verified need cannot be met by the standard library.
- Keep the starter small enough for a new user to understand in one sitting.

## Verification

Before a change is complete, run:

```bash
python3 tools/audit_workspace.py starter
python3 -m unittest discover -s tests -v
python3 tools/validate_repository.py
```

All checks must pass.

## Publication

Do not publish, release, or push changes without explicit human approval.
