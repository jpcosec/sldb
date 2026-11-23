---
sldb:
  by: agent
  at: '2026-11-23T01:43:47Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: Chatbot_Infra
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-22T18:54:39'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-22T22:43:23'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en dos tareas. Puntos 3 y 4 (los slugs pierden las tildes
  en _slugify; inbox escribe antes de trackear): task-los-ids-de-seccion-conservan-las-letras-con-tilde-y-sldb-inbox-no-deja-una-nota-sin-trackear-cuando.
  Puntos 1 y 2 (no existen stores check --model ni docs update --merge en 6ab01b80):
  task-stores-check-filtra-por-modelo-y-docs-update-acepta-un-payload-parcial-que-se-mezcla-con-el-document.'
---

# stores check filtrado por modelo y docs update parcial

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de Chatbot_Infra en el triaje del 2026-11-22: es un pedido para sldb que quedó escrito allá con sldb inbox el 2026-11-04 y nunca llegó a este desk. Texto original: (1) sldb stores check no tiene --model: para chequear solo los modelos de la wiki hay que filtrar el JSON por subject, porque el resto del store (deskops) trae sus propios hallazgos. (2) sldb docs update exige el payload completo (un payload parcial falla con campos requeridos); sería útil un --merge. (3) Los ids de sección pierden las letras con tilde (#qu-hace-y-para-qui-n). (4) sldb inbox sin --pythonpath a deskops falla (Failed to import module deskops.models) pero igual deja escrita la nota sin trackear.
