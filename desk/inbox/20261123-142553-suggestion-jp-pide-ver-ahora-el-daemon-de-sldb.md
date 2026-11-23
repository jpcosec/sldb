---
sldb:
  by: agent
  at: '2026-11-23T17:40:12Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-23T14:25:53'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T14:39:49'
# why the note was acknowledged; empty when no reason was given
ack_reason: convertida en task-plan-del-drawer-motor-datalog-duenio-de-las-aristas-revierte-d5-y-daemon-residente-de-sldb-con-prueb
  junto con la nota del motor Datalog (prioridad 4 de JP); las decisiones de diseno
  van como task.decision
# conversation thread/message the note came from, e.g. #hilo/1234
---

# JP pide ver ahora el daemon de sldb

_Describe the incoming message with enough evidence to triage._

JP (2026-11-23) pide ver ahora el daemon de sldb, que estaba diferido (2026-11-15: .sldb al día por hooks, daemon después). Va junto con la decisión del motor Datalog (nota de hoy): un proceso residente que mantenga cargado el índice de aristas y el store, para que el CLI, sldb serve, deskops y specir no recompongan el índice en cada invocación. Pedido: plan en el drawer con alcance (qué queda residente, cómo lo encuentra el CLI, qué pasa sin daemon en contenedores de ejecutor y en tests, cómo se invalida con git), relación con sldb serve y con los hooks actuales, y consumo de memoria en robocop2 (tope de 8 GB libres). Las decisiones de diseño van a JP como task.decision.
