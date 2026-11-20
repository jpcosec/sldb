---
sldb:
  by: agent
  at: '2026-11-20T01:44:57Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen@sha256:5166d536e09d276de8265eec08633588a104ee32252035dc98d5e436426aa47f
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261120-014304/context-review/task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen/bundle/fd7c1f32494e32fd25a3202a8a99ae64d5a4a53801a0d21813003922d568b5c0/attempt-1
input_sha256: fd7c1f32494e32fd25a3202a8a99ae64d5a4a53801a0d21813003922d568b5c0
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 5d6e04ace55021444d61009f6fb1980bd46e23697e01edb11b30b89d08edffdc
output_sha256: b8db36eb2780558a83da3683056d2670e5b2dec45fa0b3986cd40f9ad352759a
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador: 1) y 2) El diagnóstico es parte de
  la tarea: el ejecutor aísla cuál caché da la vista vieja, con la reproducción del
  p1. Si la simple no falla, usa el patrón del repro.log, que está en el repo en runs/subagents/20261120-repro-cache-recibos/repro.log
  (dentro del contenedor, en el workspace). Corre las dos sospechas y cita en el informe
  cuál falla, con la evidencia; si son las dos, arregla las dos. 3) Si el fallo está
  en deskops, lo informa en result-summary.md y en una nota con ''deskops message
  send --to deskops --kind suggestion'', sin tocar deskops. 4) El checkout es /mnt/ssd/proyectos/SLDB_1/sldb
  (en el contenedor, el workspace sldb) y la tarea es task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer.
  5) y bundle 3) La señal se elige así, en orden: primero invalidar en el camino de
  escritura (la escritura ya sabe qué documento cambió); si eso no alcanza para las
  escrituras de otro proceso, una señal barata que no lea los shards, por ejemplo
  el mtime en ns y el tamaño del índice del modelo. Nunca un hash de shards, porque
  es justo lo que la caché evita. Se elige lo más simple que pase el test y mantenga
  ''views run board'' en su tiempo; el ejecutor reporta el tiempo antes y después.
  Bundle 4) La caché no se quita ni se apaga en producción; un test puede usar un
  directorio de caché propio. El commit lleva el trailer ''Task-Id: <id de la tarea>''
  y rutas nombradas.'
# ISO 8601 timestamp
created_at: '2026-11-20T01:43:21.641166+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T01:44:35.696583+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-014304/context-review/task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen/bundle/fd7c1f32494e32fd25a3202a8a99ae64d5a4a53801a0d21813003922d568b5c0/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) y 2) El diagnóstico es parte de la tarea: el ejecutor aísla cuál caché da la vista vieja, con la reproducción del p1. Si la simple no falla, usa el patrón del repro.log, que está en el repo en runs/subagents/20261120-repro-cache-recibos/repro.log (dentro del contenedor, en el workspace). Corre las dos sospechas y cita en el informe cuál falla, con la evidencia; si son las dos, arregla las dos. 3) Si el fallo está en deskops, lo informa en result-summary.md y en una nota con 'deskops message send --to deskops --kind suggestion', sin tocar deskops. 4) El checkout es /mnt/ssd/proyectos/SLDB_1/sldb (en el contenedor, el workspace sldb) y la tarea es task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer. 5) y bundle 3) La señal se elige así, en orden: primero invalidar en el camino de escritura (la escritura ya sabe qué documento cambió); si eso no alcanza para las escrituras de otro proceso, una señal barata que no lea los shards, por ejemplo el mtime en ns y el tamaño del índice del modelo. Nunca un hash de shards, porque es justo lo que la caché evita. Se elige lo más simple que pase el test y mantenga 'views run board' en su tiempo; el ejecutor reporta el tiempo antes y después. Bundle 4) La caché no se quita ni se apaga en producción; un test puede usar un directorio de caché propio. El commit lleva el trailer 'Task-Id: <id de la tarea>' y rutas nombradas.
