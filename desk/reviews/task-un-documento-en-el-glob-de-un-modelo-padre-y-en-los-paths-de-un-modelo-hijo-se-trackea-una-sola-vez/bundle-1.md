---
sldb:
  by: agent
  at: '2026-11-11T09:32:47Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-un-documento-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-una-sola-vez-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-un-documento-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-una-sola-vez@sha256:d84f9e9662ec3d31946304a45d707a4fbfeca4bfccdd74a7306cbdd676d4fedc
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261111-093204/context-review/task-un-documento-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-una-sola-vez/bundle/c6ffa719d114f72c81372e4672004824259dfbdd4a5d4a210c24c672210ba2ea/attempt-1
input_sha256: c6ffa719d114f72c81372e4672004824259dfbdd4a5d4a210c24c672210ba2ea
output_sha256: fdf08d65a5b703469e76e78ecda7dd6c7fff352c62d57dee726946663fa9d3a7
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Fijado por el coordinador, sin cambiar el contrato:

  - Descendencia: la de sldb.store.model_contract.base_names. El modelo de paths desciende
  del de glob si el nombre del modelo del glob está en base_names(clase del modelo
  de paths), cargada por el store.

  - Mismo modelo en paths y glob: no hay conflicto, es la misma fila; queda una.

  - Paths cuyo modelo no desciende del glob, o dos globs o dos paths de modelos distintos:
  conflicto.

  - Error: la misma vía que los demás hallazgos de store (StoreFinding con code ''store/include-conflict'',
  severity error, el path y los modelos en el mensaje). Lo emiten build y stores check;
  build sale con rc distinto de 0 como con los demás errores de store.

  - Fila perdedora en un store duplicado: se reconoce por las reglas de la declaración,
  no por la caché. Una fila trackeada (modelo, path) que la resolución t1 no produce
  se destrackea. Lo hacen build y stores update (los dos); idempotente.

  - Informe: runs/subagents/<worker>-report.md, sección ''deskops bcf090a8'' con sí
  o no y la razón (con t1, ¿el glob TaskDoc sigue duplicando?).

  - Entrega del worker: tests que toca, tests/store y tests/api de stores, test_clean_code_rules
  y tools/check.sh --fast. Los 7 pasos de .github/workflows los corre el coordinador.

  - Docs: el documento de docs/ que describe includes y declaración del store, más
  CHANGELOG.

  Sin ambigüedad abierta.'
# ISO 8601 timestamp
created_at: '2026-11-11T09:32:23.353075+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-11T09:32:47.119764+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-un-documento-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-una-sola-vez

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261111-093204/context-review/task-un-documento-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-una-sola-vez/bundle/c6ffa719d114f72c81372e4672004824259dfbdd4a5d4a210c24c672210ba2ea/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Fijado por el coordinador, sin cambiar el contrato:
- Descendencia: la de sldb.store.model_contract.base_names. El modelo de paths desciende del de glob si el nombre del modelo del glob está en base_names(clase del modelo de paths), cargada por el store.
- Mismo modelo en paths y glob: no hay conflicto, es la misma fila; queda una.
- Paths cuyo modelo no desciende del glob, o dos globs o dos paths de modelos distintos: conflicto.
- Error: la misma vía que los demás hallazgos de store (StoreFinding con code 'store/include-conflict', severity error, el path y los modelos en el mensaje). Lo emiten build y stores check; build sale con rc distinto de 0 como con los demás errores de store.
- Fila perdedora en un store duplicado: se reconoce por las reglas de la declaración, no por la caché. Una fila trackeada (modelo, path) que la resolución t1 no produce se destrackea. Lo hacen build y stores update (los dos); idempotente.
- Informe: runs/subagents/<worker>-report.md, sección 'deskops bcf090a8' con sí o no y la razón (con t1, ¿el glob TaskDoc sigue duplicando?).
- Entrega del worker: tests que toca, tests/store y tests/api de stores, test_clean_code_rules y tools/check.sh --fast. Los 7 pasos de .github/workflows los corre el coordinador.
- Docs: el documento de docs/ que describe includes y declaración del store, más CHANGELOG.
Sin ambigüedad abierta.
