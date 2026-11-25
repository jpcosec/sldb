---
sldb:
  by: agent
  at: '2026-11-25T06:29:02Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T03:25:12'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-25T03:28:34'
# why the note was acknowledged; empty when no reason was given
ack_reason: convertida en tarea de sldb
# conversation thread/message the note came from, e.g. #hilo/1234
---

# sldb serve: la cobertura de atomos de cada spec o vista en el payload de /notations y /views

_Describe the incoming message with enough evidence to triage._

Pedido de IR (U2 de la UI de specIR, paridad con la pagina de spec2viz, que mostraba n/m de atomos cubiertos por diagrama). Ni views_payloads.py ni notations_payloads.py traen cobertura; la UI no calcula, asi que hoy muestra '—'. Pedido: que cada spec/vista del listado traiga su cobertura de atomos (cubiertos/total, y si se puede la lista) calculada por sldb. Respuesta esperada: tarea en sldb o nota de vuelta a IR.
