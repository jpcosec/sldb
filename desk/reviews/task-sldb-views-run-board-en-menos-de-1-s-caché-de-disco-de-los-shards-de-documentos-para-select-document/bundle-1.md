---
sldb:
  by: agent
  at: '2026-11-12T03:40:21Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document@sha256:9c1cc3517ad9216b28e4845adc37b6476ebd2e169ba42ccd8d8790a13e42a57e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261112-033918/context-review/task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document/bundle/313d62d58027e1102a8e3f756cf031bb16eb87a70d98296d082da9c469fbc38e/attempt-1
input_sha256: 313d62d58027e1102a8e3f756cf031bb16eb87a70d98296d082da9c469fbc38e
output_sha256: 3351ed2f03b811339759678078fe56ea89e7cae92165053dd0f2c1496b8a4793
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Ruta
  y esquema: el archivo vive en el .sldb_cache del store que llama, en una carpeta
  documents junto a la composed de H11, con un archivo por petición; el esquema es
  un JSON con un campo version (entero constante en el código) y lo que select_documents
  necesita de cada shard de documentos. Los campos los fija el worker leyendo qué
  lee select_documents, los enumera en el informe y los documenta en views.md. (2)
  Garantía de invalidación: la clave usa mtime_ns y tamaño de cada shard de core/documents,
  más la versión de la caché y el contrato de cada modelo, el mismo criterio que la
  caché de composición de H11. Un cambio que preserve a la vez mtime_ns y tamaño no
  se detecta: es un límite conocido, el mismo de H11, y se documenta; stores build,
  docs update y cualquier escritura de sldb cambian el mtime. ''Se nota en la siguiente
  corrida'' vale con ese límite. (3) El benchmark es tests/perf/h11_bench_run_view.sh,
  en sldb main una vez integrada H11. (4) ''Orden de los efectos'' son los imports
  con efectos al cargarse (registro de modelos, de predicados o de plugins): el recorte
  perezoso no cambia qué se registra ni cuándo para quien usa la API; lo fijan los
  tests existentes y el check de superficie de tools/check.sh --fast. (5) Versión:
  el campo version del JSON; si no coincide o el archivo no se puede leer, se ignora
  y se lee como antes. (6) revision es la que define views.md en su sección The revision.
  (7) Frío es sin .sldb_cache y con XDG_CACHE_HOME vacío; caliente es el store construido
  con una corrida previa en otro proceso. La meta de menos de 1 s aplica en caliente.
  (8) Los 7 pasos del workflow de sldb: tools/check.sh --fast, pytest, stores build,
  make world, el store de deskops, stores build --check y selfdoc; los corre el coordinador.
  (9) El informe es runs/subagents/h11b-worker-report.md. (10) Precondición: H11 está
  en sldb main; si no, el worker para y avisa.'
# ISO 8601 timestamp
created_at: '2026-11-12T03:39:30.649410+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-12T03:40:21.006232+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261112-033918/context-review/task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document/bundle/313d62d58027e1102a8e3f756cf031bb16eb87a70d98296d082da9c469fbc38e/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Ruta y esquema: el archivo vive en el .sldb_cache del store que llama, en una carpeta documents junto a la composed de H11, con un archivo por petición; el esquema es un JSON con un campo version (entero constante en el código) y lo que select_documents necesita de cada shard de documentos. Los campos los fija el worker leyendo qué lee select_documents, los enumera en el informe y los documenta en views.md. (2) Garantía de invalidación: la clave usa mtime_ns y tamaño de cada shard de core/documents, más la versión de la caché y el contrato de cada modelo, el mismo criterio que la caché de composición de H11. Un cambio que preserve a la vez mtime_ns y tamaño no se detecta: es un límite conocido, el mismo de H11, y se documenta; stores build, docs update y cualquier escritura de sldb cambian el mtime. 'Se nota en la siguiente corrida' vale con ese límite. (3) El benchmark es tests/perf/h11_bench_run_view.sh, en sldb main una vez integrada H11. (4) 'Orden de los efectos' son los imports con efectos al cargarse (registro de modelos, de predicados o de plugins): el recorte perezoso no cambia qué se registra ni cuándo para quien usa la API; lo fijan los tests existentes y el check de superficie de tools/check.sh --fast. (5) Versión: el campo version del JSON; si no coincide o el archivo no se puede leer, se ignora y se lee como antes. (6) revision es la que define views.md en su sección The revision. (7) Frío es sin .sldb_cache y con XDG_CACHE_HOME vacío; caliente es el store construido con una corrida previa en otro proceso. La meta de menos de 1 s aplica en caliente. (8) Los 7 pasos del workflow de sldb: tools/check.sh --fast, pytest, stores build, make world, el store de deskops, stores build --check y selfdoc; los corre el coordinador. (9) El informe es runs/subagents/h11b-worker-report.md. (10) Precondición: H11 está en sldb main; si no, el worker para y avisa.
