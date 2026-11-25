---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T14:36:42'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# C2: primitiva 'tomar transición' en CLI y API

_Describe the incoming message with enough evidence to triage._

deskops/lifecycle.py advance hace a mano: edges_holding, apply_effects, agregar a history, escritura atómica, findings y hooks. Pedido: una primitiva de sldb que tome una transición sobre un documento (condición de la arista, efectos, append a un campo history declarado, escritura en transacción y findings), por CLI y API, con un punto donde el consumidor ejecute sus hooks. deskops conservaría solo el ejecutor de hooks (nodo P03). Plan deskops-plugin-de-sldb (deskops/desk/drawer/plans/deskops-plugin-de-sldb, decisión de JP del 25-11: deskops es un plugin sobre sldb, no una reimplementación).
