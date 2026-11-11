---
sldb:
  by: agent
  at: '2026-11-11T12:49:13Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
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
run_dir: runs/subagents/20261111-124814/context-review/task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1/preflight/fe6a1a29c5cda4bb3a5bfb1fa32f9870e6665460d945733f3b8aab2c34ed686c/attempt-1
input_sha256: fe6a1a29c5cda4bb3a5bfb1fa32f9870e6665460d945733f3b8aab2c34ed686c
output_sha256: 658c7e1f2d6bd06ff2e8dda9107820080888d6a36785f14fbb19a3dfe6470f3a
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
created_at: '2026-11-11T12:48:32.067551+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-11T12:49:13.393122+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261111-124814/context-review/task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1/preflight/fe6a1a29c5cda4bb3a5bfb1fa32f9870e6665460d945733f3b8aab2c34ed686c/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Fijado por el coordinador, sin cambiar el contrato:
- Esquema de g1: 'value' va DENTRO de anchored_by: {model, field, value?}, con value en {tag, bare} y tag por defecto. Con bare, un campo que ya traiga el namespace ('domain:a.b') no se ancla (no coincide), y el validador de TagNamespace acepta las claves {model, field} o {model, field, value}.
- Alcance de g2: tag_models filtra solo la familia builtin:tag_namespace (no otras reglas). Las anclas (anchors_of) NO se filtran: un documento ancla de cualquier modelo sigue anclando, porque CrossroadDoc no está en tag_models. Descendientes: un documento cuyo modelo es uno de tag_models o tiene uno de ellos en base_models.
- tag_tree con tag_models: 'used' y 'orphans' solo cuentan tags de documentos en alcance; roots y anclas como hoy. tag_check: solo los hallazgos de documentos en alcance.
- g3: sin cambio de código en tag_folder. En docs/architecture/tags.md se suma una línea: que tag_folder es estricto por decisión (GD27 para deskops, H3) y que el consumidor que acepte segmentos vacíos los filtra antes. Si el doc ya lo dice, se cita esa línea en el informe y no se agrega nada.
- 7 pasos: los de .github/workflows/ci.yml de sldb (check --fast, pytest de a uno, build, make world en pron, store de deskops, build --check, build + selfdoc check). Los corre el coordinador.
Sin ambigüedad abierta.
