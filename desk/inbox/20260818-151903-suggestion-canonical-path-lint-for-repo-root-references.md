---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: AntonIA
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-08-18T15:19:03'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T13:10:54'
---

# canonical path lint for repo-root references

_Describe the incoming message with enough evidence to triage._

## Resolución

Resuelto (2026-10-18, sldb-04). `sldb lint [target] [--repo-root R] [--format text|json|yaml]` (src/sldb/cli/commands/lint.py) es el lint de paths canónicos de referencias a la raíz del repo, con `lint_path` y `lint_text`.
