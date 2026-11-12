---
sldb:
  by: agent
  at: '2026-11-12T02:31:22Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru@sha256:afadd17917c7df577c5f7178d2028eda238be6757610d0de0b914fac710310e8
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261112-022646/context-review/task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru/preflight/19ded5d45ae2cc5483952b32ff0b047a3903324404d557bd8dd0934989117e27/attempt-1
input_sha256: 19ded5d45ae2cc5483952b32ff0b047a3903324404d557bd8dd0934989117e27
output_sha256: 83cfde4a7d30dec9f31f8477db5aff67e4cb39aac307ee5225a459ec6e402551
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Umbrales:
  menos de 1 s aplica con el store construido y un proceso nuevo (caliente = la caché
  de disco que stores build deja); en frío (sin ninguna caché de disco) no más lento
  que la línea base. La línea base la mide el benchmark h1 del worker el mismo día
  sobre el mismo layout (la reproducción del coordinador dio 9,4 s y 9,7 s de deskops
  view board y 10,89 s de run_view bajo cProfile). (2) Premisa corregida: include_linked
  es una clave de select (views.md), así que una vista puede seleccionar documentos
  enlazados; el board de deskops no la usa, pero no todas las vistas son locales.
  Criterio de h2, conservador: una sección necesita un store enlazado solo si su select
  trae include_linked verdadero o un ref o prefix con prefijo de enlace; si alguna
  sección lo necesita, se leen todos los enlazados como hoy, sin análisis más fino.
  El worker verifica en el ViewDoc semilla de deskops que board y task no lo usan.
  (3) views.md manda: la vista se evalúa sobre el store que llama; no se cambia. (4)
  Clave de h3: la firma por store que sldb ya calcula para saber si un store cambió
  (la de _stale_documents y documents_hash en shard_reading); el worker reutiliza
  esa firma y no inventa otra. Formato y lugar: un archivo en el .sldb_cache del store
  que llama, que es la caché de disco que ya existe; se invalida por firma. (5) Un
  store enlazado cambiado: si la vista usa include_linked, su firma entra a la clave
  y se nota en la siguiente corrida; si no lo usa, un cambio ahí no afecta ni el resultado
  ni la revision. (6) Revision: la firma de shards de la revision es la del store
  que llama y no cambia; el test del worker fija que, para una vista sin include_linked,
  la revision es idéntica leyendo o no los enlazados, y que para una con include_linked
  sigue incluyendo lo enlazado. (7) Los 7 pasos del workflow de sldb son: tools/check.sh
  --fast, pytest, stores build, make world, el store de deskops, stores build --check
  y selfdoc; los corre el coordinador. (8) pills y atoms vacíos: no hay ninguno que
  ligar. (9) Layout: el benchmark arma el layout con origin/main de cada repo al día
  y registra los SHA en el informe. (10) h3 solo si h2 medido no baja de 1 s en el
  layout; h4 solo si h2 y h3 no alcanzan.'
# ISO 8601 timestamp
created_at: '2026-11-12T02:27:01.109885+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-12T02:31:21.793854+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261112-022646/context-review/task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru/preflight/19ded5d45ae2cc5483952b32ff0b047a3903324404d557bd8dd0934989117e27/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Umbrales: menos de 1 s aplica con el store construido y un proceso nuevo (caliente = la caché de disco que stores build deja); en frío (sin ninguna caché de disco) no más lento que la línea base. La línea base la mide el benchmark h1 del worker el mismo día sobre el mismo layout (la reproducción del coordinador dio 9,4 s y 9,7 s de deskops view board y 10,89 s de run_view bajo cProfile). (2) Premisa corregida: include_linked es una clave de select (views.md), así que una vista puede seleccionar documentos enlazados; el board de deskops no la usa, pero no todas las vistas son locales. Criterio de h2, conservador: una sección necesita un store enlazado solo si su select trae include_linked verdadero o un ref o prefix con prefijo de enlace; si alguna sección lo necesita, se leen todos los enlazados como hoy, sin análisis más fino. El worker verifica en el ViewDoc semilla de deskops que board y task no lo usan. (3) views.md manda: la vista se evalúa sobre el store que llama; no se cambia. (4) Clave de h3: la firma por store que sldb ya calcula para saber si un store cambió (la de _stale_documents y documents_hash en shard_reading); el worker reutiliza esa firma y no inventa otra. Formato y lugar: un archivo en el .sldb_cache del store que llama, que es la caché de disco que ya existe; se invalida por firma. (5) Un store enlazado cambiado: si la vista usa include_linked, su firma entra a la clave y se nota en la siguiente corrida; si no lo usa, un cambio ahí no afecta ni el resultado ni la revision. (6) Revision: la firma de shards de la revision es la del store que llama y no cambia; el test del worker fija que, para una vista sin include_linked, la revision es idéntica leyendo o no los enlazados, y que para una con include_linked sigue incluyendo lo enlazado. (7) Los 7 pasos del workflow de sldb son: tools/check.sh --fast, pytest, stores build, make world, el store de deskops, stores build --check y selfdoc; los corre el coordinador. (8) pills y atoms vacíos: no hay ninguno que ligar. (9) Layout: el benchmark arma el layout con origin/main de cada repo al día y registra los SHA en el informe. (10) h3 solo si h2 medido no baja de 1 s en el layout; h4 solo si h2 y h3 no alcanzan.
