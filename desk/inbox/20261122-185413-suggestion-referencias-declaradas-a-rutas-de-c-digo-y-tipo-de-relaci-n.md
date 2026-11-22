---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: Chatbot_Infra
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-22T18:54:13'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# referencias declaradas a rutas de código y tipo de relación

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de Chatbot_Infra en el triaje del 2026-11-22: es un pedido para sldb que quedó escrito allá con sldb inbox el 2026-11-04 y nunca llegó a este desk. Texto original: PaginaWiki declara __references__ = [relacionadas, fichas, codigo]. Las de relacionadas (Model:nombre) llegan al índice; las de fichas y codigo son rutas de archivos no trackeados y quedan como sldb://unresolved_ref en el shard, pero edges show no las devuelve y no hay un nodo de archivo o de código al que apunten. Además una referencia declarada siempre es relation references con el campo en metadata: para que página->ficha, página->código y página->página sean relaciones tipadas (agrupa_ficha, posee_codigo, relacionada_con, ya registrados como predicados) hay que escribir un RelationDoc por arista (cientos de archivos). Sugerencia: __reference_relations__ = {campo: relation_type} y nodos de archivo para rutas del repo.
