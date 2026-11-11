---
sldb:
  by: agent
  at: '2026-11-11T12:45:17Z'
  authority: generated
  via: create_document
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-11T15:00:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# referrers y rewrite_references para un grafo armado en proceso, excluir fuentes y menciones duplicadas en frontmatter (H-a..H-c de CC35c de deskops)

_Describe the incoming message with enough evidence to triage._

Hallado por CC35c de deskops (wt/cc35c 61ad9d1a, runs/subagents/cc35c-worker-report.md, 2026-11-11). deskops compone hoy resolve_target, find_hits, rewrite_references, rewritten_line y replace_text en deskops/services/references.py porque la API pública no cubre estos casos:

- **H-a (b2).** `referrers(store, target)` y `rewrite_references(...)` no ven menciones en un proyecto cuyo grafo se arma en proceso.
  - Por qué: leen el grafo de `store.yaml` (`optional_graph` → `project_graph(store)`), y deskops no declara `project_graph`. Su `closed_document` es código (DO8; nota H2 de CC33c en sldb `61e9c7a9`).
  - Qué hace deskops mientras: compone `resolve_target` + `find_hits` y `rewrite_references` (campos) + `rewritten_line` + `replace_text` (menciones). Eso repite el bucle `_write`/`_planned_text` de `rewrite_references.py` (unas 20 líneas en `_rewrite_mentions`).
  - Propuesta: un parámetro `graph: ProjectGraph | None` (o `config`) en `referrers` y `rewrite_references`. Cuando entre, `_rewrite_mentions` se borra y las dos funciones de `references.py` llaman a la API pública. Con H2 resuelta (declarar `project_graph` en store.yaml), también.
  - Desk mínimo que lo reproduce: `deskops init` en tmp_path, un átomo `atom-a` y `desk/tasks/task-ref.md` con "Depends on atom:atom-a." `sldb.api.referrers(store, "atom-a")` devuelve `[]`; `find_hits(location, target, desk_graph(root))` devuelve la mención en `desk/tasks/task-ref.md:3`.
- **H-b.** `rewrite_references` no admite excluir fuentes.
  - En atoms merge, el átomo destino y el stub los escribe merge. deskops los excluye de las menciones, pero no puede excluirlos de los campos. Hoy `AtomDoc` no declara campos de referencia, así que no pasa.
  - Propuesta: `excluded_sources=`.
- **H-c.** Una mención de línea (`LineMentions`) también lee el frontmatter, salvo los campos de `skipped_frontmatter_fields`. Así, un campo declarado (`pills: [desk/contexts/pill-x.md]`) aparece dos veces en `find_hits`: como `schema` y como `mention`.
  - deskops descarta las menciones del frontmatter de un documento trackeado (`_in_frontmatter` en `references.py`).
  - Propuesta: que `find_hits` no devuelva como mención una línea del frontmatter que ya es un hit `schema` del mismo documento.
