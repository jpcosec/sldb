---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-18T23:31:52'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T23:33:47'
---

# pron atoms v1 → sldb: anti-patrón de endpoints monolíticos en sldb serve

_Describe the incoming message with enough evidence to triage._

Movido desde pron/knowledge/atoms/atom-anti-pattern-monolithic-api-endpoints-in-sldb-viewer.md (limpieza de los atoms v1 que el merge 49c647a trajo a pron; pron no tiene modelo de átomo, spec 08:48). Es un principio de diseño de la superficie de sldb serve, no de pron. El código ya lo cumple (una ruta por superficie en src/sldb/cli/serve/*_routes.py), pero no encontré dónde lo dice sldb; si quieres conservarlo, va a tus docs o atoms; si ya está cubierto, ciérrala.

--- texto original ---

# Anti-pattern: monolithic API endpoints in SLDB Viewer

## Answer

SLDB surfaces (AST, StructuredDocModel, fields, markdown frontmatter) must be queried via independent commands (sldb ast show, sldb fields), not through a single monolithic UI endpoint. Markdown frontmatter must be preserved on save. No mocked 'coming soon' states for unbuilt surfaces are acceptable.
