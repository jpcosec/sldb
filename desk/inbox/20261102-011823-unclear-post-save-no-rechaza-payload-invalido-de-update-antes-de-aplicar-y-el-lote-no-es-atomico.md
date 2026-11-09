---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-02T01:18:23'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# POST /save no rechaza payload invalido de update antes de aplicar y el lote no es atomico

_Describe the incoming message with enough evidence to triage._

Gap observado por lectura estática de sldb 77bd6d00; no reproducido en runtime. En src/sldb/cli/serve/save_plan.py, update_target devuelve payload_error(...) en la primera posición de la tupla, la de target/path (línea 53 aprox.: return payload_error(...), None), mientras create_target lo devuelve como error. prepare_step en save_routes.py:61-69 solo rechaza el segundo valor. apply_change(update) no usa ese path (save_routes.py:101-106). Consecuencia probable: un payload inválido de update no se rechaza en la prevalidación. Además apply_batch (save_routes.py:79-87) aplica en secuencia y ante fallo devuelve ok false con lo ya completado: el lote no es atómico. Los tests de payload inválido citados en deskops cubren creación. Origen: revisión root de WS12, deskops runs/subagents/20261102-ws12-correccion/review-source.md, hallazgo 2. Es intake, no una propuesta de reparación: deskops no hará workaround. Decide el repo dueño.
