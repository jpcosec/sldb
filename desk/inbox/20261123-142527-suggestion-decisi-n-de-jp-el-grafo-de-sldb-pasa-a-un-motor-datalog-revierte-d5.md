---
sldb:
  by: agent
  at: '2026-11-23T17:39:43Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-23T14:25:27'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T14:39:19'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'convertida en task-plan-del-drawer-motor-datalog-duenio-de-las-aristas-revierte-d5-y-daemon-residente-de-sldb-con-prueb
  junto con la nota del daemon (prioridad 4 de JP): plan del drawer con prueba de
  concepto medida y task.decision por cada decision; no bloquea la tarea de attach_atom_edges'
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Decisión de JP: el grafo de sldb pasa a un motor Datalog (revierte D5)

_Describe the incoming message with enough evidence to triage._

JP (2026-11-23) revierte D5 del plan grafo-operable (desk/drawer/plans/grafo-operable/decisiones.md): el grafo de sldb pasa a un motor Datalog estable y probado, que sea dueño del almacenamiento y la consulta de aristas, no solo del análisis. JP descartó Cypher/Neo4j en favor de Datalog (coherente con D6: reglas en Datalog estratificado). Motivo: hoy la costura GraphBackend (src/sldb/store/graph/backend/protocol.py) solo cubre eval/analyze sobre networkx; componer el índice de aristas, federar stores y calcular live stale quedan fuera, hechos a mano sobre YAML en .sldb_cache/edges, y ahí se va el tiempo (acta de IR docs/spec2viz/acta-de-retiro.md: 28 s la primera carga del índice federado; specir catalog build no termina en 280 s el 2026-11-22). Los documentos y git siguen siendo la verdad; el motor es un índice derivado reconstruible. Primer paso propuesto por el supervisor (no decidido por JP): prueba de concepto que cargue el índice federado real en un motor Datalog embebido (Datalevin es el candidato de docs/architecture/graph-backend.md; verificar alternativas con cliente Python) y mida aristas de un nodo, recorrido, emparejamiento de átomos y stale. El motor concreto no está elegido. No reemplaza el arreglo chico de task-matching-attach-atom-edges-deja-de-recomponer-live-stale..., que sigue primero porque destraba el retiro de spec2viz.
