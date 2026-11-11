---
sldb:
  by: agent
  at: '2026-11-11T12:49:17Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1@sha256:94df178e9710826d66151a362b46c13cec8477e7ccaab04c04c06a2dc8f2b5d0
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261111-124835/context-review/task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1/bundle/6150fb6ec327663cef2f124ae0f229c40f6bd4f01ef089405c254914931bdfdd/attempt-1
input_sha256: 6150fb6ec327663cef2f124ae0f229c40f6bd4f01ef089405c254914931bdfdd
output_sha256: 2ed1f8e620811182b938e81abaa96f840776ae0e20e836f7be7b7fd82df1f383
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Fijado por el coordinador, sin cambiar el contrato:

  - Esquema de g1: ''value'' va DENTRO de anchored_by: {model, field, value?}, con
  value en {tag, bare} y tag por defecto. Con bare, un campo que ya traiga el namespace
  (''domain:a.b'') no se ancla (no coincide), y el validador de TagNamespace acepta
  las claves {model, field} o {model, field, value}.

  - Alcance de g2: tag_models filtra solo la familia builtin:tag_namespace (no otras
  reglas). Las anclas (anchors_of) NO se filtran: un documento ancla de cualquier
  modelo sigue anclando, porque CrossroadDoc no está en tag_models. Descendientes:
  un documento cuyo modelo es uno de tag_models o tiene uno de ellos en base_models.

  - tag_tree con tag_models: ''used'' y ''orphans'' solo cuentan tags de documentos
  en alcance; roots y anclas como hoy. tag_check: solo los hallazgos de documentos
  en alcance.

  - g3: sin cambio de código en tag_folder. En docs/architecture/tags.md se suma una
  línea: que tag_folder es estricto por decisión (GD27 para deskops, H3) y que el
  consumidor que acepte segmentos vacíos los filtra antes. Si el doc ya lo dice, se
  cita esa línea en el informe y no se agrega nada.

  - 7 pasos: los de .github/workflows/ci.yml de sldb (check --fast, pytest de a uno,
  build, make world en pron, store de deskops, build --check, build + selfdoc check).
  Los corre el coordinador.

  Sin ambigüedad abierta.'
# ISO 8601 timestamp
created_at: '2026-11-11T12:48:54.778800+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-11T12:49:16.754660+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261111-124835/context-review/task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1/bundle/6150fb6ec327663cef2f124ae0f229c40f6bd4f01ef089405c254914931bdfdd/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Fijado por el coordinador, sin cambiar el contrato:
- Esquema de g1: 'value' va DENTRO de anchored_by: {model, field, value?}, con value en {tag, bare} y tag por defecto. Con bare, un campo que ya traiga el namespace ('domain:a.b') no se ancla (no coincide), y el validador de TagNamespace acepta las claves {model, field} o {model, field, value}.
- Alcance de g2: tag_models filtra solo la familia builtin:tag_namespace (no otras reglas). Las anclas (anchors_of) NO se filtran: un documento ancla de cualquier modelo sigue anclando, porque CrossroadDoc no está en tag_models. Descendientes: un documento cuyo modelo es uno de tag_models o tiene uno de ellos en base_models.
- tag_tree con tag_models: 'used' y 'orphans' solo cuentan tags de documentos en alcance; roots y anclas como hoy. tag_check: solo los hallazgos de documentos en alcance.
- g3: sin cambio de código en tag_folder. En docs/architecture/tags.md se suma una línea: que tag_folder es estricto por decisión (GD27 para deskops, H3) y que el consumidor que acepte segmentos vacíos los filtra antes. Si el doc ya lo dice, se cita esa línea en el informe y no se agrega nada.
- 7 pasos: los de .github/workflows/ci.yml de sldb (check --fast, pytest de a uno, build, make world en pron, store de deskops, build --check, build + selfdoc check). Los corre el coordinador.
Sin ambigüedad abierta.
