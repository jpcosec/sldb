---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-06T15:28:34'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# SpecDoc: el modelo local docs.models:SpecDoc colisiona con el builtin sldb.models.notation_models:SpecDoc tras SV01

_Describe the incoming message with enough evidence to triage._

Desde SV01 (6b80df36, 2026-11-06) sldb.models exporta un SpecDoc builtin (sldb.models.notation_models:SpecDoc, absorbido de spec2viz). El store de este repo (.sldb/store.yaml) sigue enlazando el nombre SpecDoc a docs.models:SpecDoc, un modelo local de docs/models.py. deskops doctor lo reporta como alerta: 'SpecDoc: another class under the name of the model the store linked as pron owns'. La alerta ya existia antes de SV01, pero ahora la colision es entre un modelo local y uno builtin de sldb, y cualquier consumidor que resuelva SpecDoc por nombre (sldb serve, graph_ui, deskops view) puede recibir la clase equivocada segun el orden de registro. Hay que decidir una de tres: (a) renombrar el modelo local (por ejemplo DocsSpecDoc o ArchSpecDoc) y migrar sus documentos; (b) retirar docs.models:SpecDoc y migrar sus documentos al SpecDoc builtin si el contrato coincide; (c) definir en sldb una regla de precedencia explicita local-sobre-builtin y que doctor la reporte como decision, no como alerta. No se toco en Ola 1. Detectado por la sesion Claude de SLDB_1 al verificar la integracion de SV01+SV04; registro pedido por el supervisor deskops-sobre-sldb-config.
