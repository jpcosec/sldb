---
sldb:
  by: agent
  at: '2026-11-11T14:47:36Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-seguridad-resto-toda-lectura-de-un-documento-trackeado-pasa-por-la-guarda-de-raíz-y-symlinks-stores-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-seguridad-resto-toda-lectura-de-un-documento-trackeado-pasa-por-la-guarda-de-raíz-y-symlinks-stores@sha256:7c56592aa99b6ed65094aa684cae6d38241360d0f58d48bbb3638ad31e9ecf5f
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261111-144653/context-review/task-seguridad-resto-toda-lectura-de-un-documento-trackeado-pasa-por-la-guarda-de-raíz-y-symlinks-stores/bundle/2fd0d7230f63ba0f2de59a6611790185a7a2a107f0bbdfdd3de0cf2c41f2035d/attempt-1
input_sha256: 2fd0d7230f63ba0f2de59a6611790185a7a2a107f0bbdfdd3de0cf2c41f2035d
output_sha256: 9ccd70b9f841b9ed8cbce4be1fb5b0c68b8712780c547ca5dae642f6b99f9a27
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Fijado por el coordinador, sin cambiar el contrato:

  - ''Documento por trackear'': un path que docs track recibe, o que un include de
  store.yaml nombra. El criterio de documento es el de sldb (declared_files / el modelo);
  no se inventa otro.

  - ''Extracción que sigue a track/update'': el alcance exacto lo fija el grep. Es
  toda llamada que lea el texto de un documento trackeado para extraer, hashear, seccionar
  o etiquetar. La lista de CAUSA es el punto de partida; el inventario final va en
  el informe.

  - Informe: runs/subagents/secrest-worker-report.md, con una tabla ''archivo:línea
  | lectura | antes | después''.

  - Hallazgos: los de source_read. Ruta que resuelve fuera de la raíz (symlink saliente
  o directorio en el camino): store/path-outside-root. Symlink dentro de la raíz:
  store/symlink-not-read. Salen por la misma vía que hoy (StoreFinding, _DOC_CODES);
  stores check los lista y build/update los reportan sin abortar.

  - Comandos: ''sldb stores check'', ''sldb stores update'', ''sldb stores build'',
  ''sldb stores build --check'' y ''sldb docs update''/''sldb docs track''.

  - Excepciones del grep: archivos que no son documentos del store (store.yaml, store_index,
  shards yaml, pyproject, .gitignore). Cada una se nombra en el informe.

  - Docs: docs/ que describe la guarda o staleness (la sección que dejó live_stale),
  más CHANGELOG.

  - 7 pasos: los de .github/workflows/ci.yml de sldb (check --fast, pytest de a uno,
  python -m build, make world en pron, store de deskops, build --check, build + selfdoc
  check). Los corre el coordinador.

  - Grados de unidad: los needs/needed_by de [[unit]] en contracts/layers.toml. Si
  tools/check.sh --fast (ejes) dice que el código difiere, se actualizan al valor
  medido con comentario fechado.

  Sin ambigüedad abierta.'
# ISO 8601 timestamp
created_at: '2026-11-11T14:47:08.471907+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-11T14:47:36.572977+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-seguridad-resto-toda-lectura-de-un-documento-trackeado-pasa-por-la-guarda-de-raíz-y-symlinks-stores

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261111-144653/context-review/task-seguridad-resto-toda-lectura-de-un-documento-trackeado-pasa-por-la-guarda-de-raíz-y-symlinks-stores/bundle/2fd0d7230f63ba0f2de59a6611790185a7a2a107f0bbdfdd3de0cf2c41f2035d/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Fijado por el coordinador, sin cambiar el contrato:
- 'Documento por trackear': un path que docs track recibe, o que un include de store.yaml nombra. El criterio de documento es el de sldb (declared_files / el modelo); no se inventa otro.
- 'Extracción que sigue a track/update': el alcance exacto lo fija el grep. Es toda llamada que lea el texto de un documento trackeado para extraer, hashear, seccionar o etiquetar. La lista de CAUSA es el punto de partida; el inventario final va en el informe.
- Informe: runs/subagents/secrest-worker-report.md, con una tabla 'archivo:línea | lectura | antes | después'.
- Hallazgos: los de source_read. Ruta que resuelve fuera de la raíz (symlink saliente o directorio en el camino): store/path-outside-root. Symlink dentro de la raíz: store/symlink-not-read. Salen por la misma vía que hoy (StoreFinding, _DOC_CODES); stores check los lista y build/update los reportan sin abortar.
- Comandos: 'sldb stores check', 'sldb stores update', 'sldb stores build', 'sldb stores build --check' y 'sldb docs update'/'sldb docs track'.
- Excepciones del grep: archivos que no son documentos del store (store.yaml, store_index, shards yaml, pyproject, .gitignore). Cada una se nombra en el informe.
- Docs: docs/ que describe la guarda o staleness (la sección que dejó live_stale), más CHANGELOG.
- 7 pasos: los de .github/workflows/ci.yml de sldb (check --fast, pytest de a uno, python -m build, make world en pron, store de deskops, build --check, build + selfdoc check). Los corre el coordinador.
- Grados de unidad: los needs/needed_by de [[unit]] en contracts/layers.toml. Si tools/check.sh --fast (ejes) dice que el código difiere, se actualizan al valor medido con comentario fechado.
Sin ambigüedad abierta.
