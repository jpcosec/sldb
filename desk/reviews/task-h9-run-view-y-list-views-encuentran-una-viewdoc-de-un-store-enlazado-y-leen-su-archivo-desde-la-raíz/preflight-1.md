---
sldb:
  by: agent
  at: '2026-11-11T09:02:17Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-h9-run-view-y-list-views-encuentran-una-viewdoc-de-un-store-enlazado-y-leen-su-archivo-desde-la-raíz-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-h9-run-view-y-list-views-encuentran-una-viewdoc-de-un-store-enlazado-y-leen-su-archivo-desde-la-raíz@sha256:1174d91d32817153239e85584c3ef63d2b03aeac1f7a8afe302aa2ae5e29b75e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261111-090115/context-review/task-h9-run-view-y-list-views-encuentran-una-viewdoc-de-un-store-enlazado-y-leen-su-archivo-desde-la-raíz/preflight/2186a9303e38d815daf5762900fc99aa85dd34587ae478dc100c874cba56b100/attempt-1
input_sha256: 2186a9303e38d815daf5762900fc99aa85dd34587ae478dc100c874cba56b100
output_sha256: d082cd3277bd14728100f7335fa0146c9021670a9705794d6020322f3357de75
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Fijado por el coordinador, sin cambiar el contrato:

  - Guarda de seguridad: es la tarea task-seguridad-live-stale-... del desk de sldb
  (rama wt/livestale-security). Está disponible si ''from sldb.store.source_read import
  read_source_text'' importa en la base del worker. Si importa, se usa. Si no, comentario
  ''# TODO(task-seguridad-live-stale): leer por source_read.read_source_text'' en
  la lectura.

  - Evaluación: la misma que hoy hace run_view sobre A, con su índice compuesto, enlaces
  incluidos. Lo único que cambia es de dónde sale la ViewDoc.

  - contracts/layers.toml: se puede editar solo si se crea un archivo fuera de una
  carpeta ya declarada. api/views es carpeta declarada, así que un archivo nuevo ahí
  no necesita eje.

  - Pasos: el worker corre los tests que toca, tests/api de views, test_clean_code_rules
  y tools/check.sh --fast. Los 7 pasos del workflow (.github/workflows) los corre
  el coordinador.

  - serve: usa run_view y no se espera tocarlo. Si hace falta, el worker para y avisa.

  - Error ambiguo: SLDBDocumentTargetError(''Ambiguous view: <name> (linked in <store1>,
  <store2>)'').

  - Docs: el documento de docs/ que describe vistas y run_view (grep run_view en docs/),
  con un párrafo sobre ViewDoc enlazadas, más CHANGELOG.

  Sin ambigüedad abierta.'
# ISO 8601 timestamp
created_at: '2026-11-11T09:01:34.288765+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-11T09:02:16.681452+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-h9-run-view-y-list-views-encuentran-una-viewdoc-de-un-store-enlazado-y-leen-su-archivo-desde-la-raíz

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261111-090115/context-review/task-h9-run-view-y-list-views-encuentran-una-viewdoc-de-un-store-enlazado-y-leen-su-archivo-desde-la-raíz/preflight/2186a9303e38d815daf5762900fc99aa85dd34587ae478dc100c874cba56b100/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Fijado por el coordinador, sin cambiar el contrato:
- Guarda de seguridad: es la tarea task-seguridad-live-stale-... del desk de sldb (rama wt/livestale-security). Está disponible si 'from sldb.store.source_read import read_source_text' importa en la base del worker. Si importa, se usa. Si no, comentario '# TODO(task-seguridad-live-stale): leer por source_read.read_source_text' en la lectura.
- Evaluación: la misma que hoy hace run_view sobre A, con su índice compuesto, enlaces incluidos. Lo único que cambia es de dónde sale la ViewDoc.
- contracts/layers.toml: se puede editar solo si se crea un archivo fuera de una carpeta ya declarada. api/views es carpeta declarada, así que un archivo nuevo ahí no necesita eje.
- Pasos: el worker corre los tests que toca, tests/api de views, test_clean_code_rules y tools/check.sh --fast. Los 7 pasos del workflow (.github/workflows) los corre el coordinador.
- serve: usa run_view y no se espera tocarlo. Si hace falta, el worker para y avisa.
- Error ambiguo: SLDBDocumentTargetError('Ambiguous view: <name> (linked in <store1>, <store2>)').
- Docs: el documento de docs/ que describe vistas y run_view (grep run_view en docs/), con un párrafo sobre ViewDoc enlazadas, más CHANGELOG.
Sin ambigüedad abierta.
