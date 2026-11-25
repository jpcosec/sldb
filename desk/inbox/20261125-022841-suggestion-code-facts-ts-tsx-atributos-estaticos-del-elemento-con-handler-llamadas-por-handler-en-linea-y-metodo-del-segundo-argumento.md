---
sldb:
  by: agent
  at: '2026-11-25T05:33:47Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T02:28:41'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-25T02:33:23'
# why the note was acknowledged; empty when no reason was given
ack_reason: '3 tareas: atributos estaticos de handler JSX, llamadas por handler en
  linea, options del segundo argumento'
# conversation thread/message the note came from, e.g. #hilo/1234
---

# code_facts TS/TSX: atributos estaticos del elemento con handler, llamadas por handler en linea y metodo del segundo argumento

_Describe the incoming message with enough evidence to triage._

Pedido de IR (T4 del plan graph_ui, IR/desk/drawer/plans/graph-ui-diccionario-de-componentes/README.md, medido sobre graph_ui 36adfbb). specIR solo lee facts de sldb.api.code.code_facts y le faltan tres cosas para el diccionario de componentes: (1) atributos estaticos (literales) del elemento JSX que lleva el handler: data-testid, aria-label, role, name, type, para derivar un localizador; (2) en un componente con varios handlers en linea, que llamadas pertenecen a cada handler (hoy 84 no derivados por 'mas de un handler; no se sabe que llamadas son suyas'); (3) el segundo argumento de una llamada cuando es un objeto literal, al menos la clave method de fetch/request(path, {method:'POST'}), porque hoy los facts solo dan el primero. Desbloquea T5 (localizador) y T6 (envoltorios HTTP) en IR. Respuesta esperada: tarea en sldb o nota de vuelta a IR.
