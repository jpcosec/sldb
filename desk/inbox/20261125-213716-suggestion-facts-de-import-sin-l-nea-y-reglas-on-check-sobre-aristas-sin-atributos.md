---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T21:37:16'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Facts de import sin línea y reglas on_check sobre aristas sin atributos

_Describe the incoming message with enough evidence to triage._

specIR extrae dependencias entre piezas (depends_on) de attrs.imports y attrs.nested_imports de los hechos de módulo. Faltan dos cosas genéricas: (1) los hechos de import no traen la línea del import (solo el nombre del módulo importado); specIR la lee hoy con ast del archivo como parche. Pedido: span o línea por import en attrs (p. ej. imports_at: [{module, line}]). (2) Una regla on_check no puede tener como sujeto un RelationDoc ('sin proyección para RelationDoc:...', no es nodo del índice) y la cláusula/seen de un cuantificador sobre rel:<tipo> solo lee campos del nodo testigo, no los attributes de la arista. Así un hallazgo 'graph_ui depende de pron' no puede mostrar archivo:línea del import, que vive en attributes.sitios de la arista. Pedido: poder leer atributos de la arista en el seen (o un paso de camino que devuelva la arista).
