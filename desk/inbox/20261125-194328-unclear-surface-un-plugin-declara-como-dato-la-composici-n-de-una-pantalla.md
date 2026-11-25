---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T19:43:28'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# surface: un plugin declara como dato la composición de una pantalla

_Describe the incoming message with enough evidence to triage._

Pedido de specIR para sldb/surface (plan IR/desk/drawer/plans/specir-plugin-de-sldb/; ADR de sldb surface-is-an-editor-contract.md). JP decidió el 2026-11-25 que specIR no tiene interfaz y que su pantalla, el catálogo de diagramas, la aporta el plugin como dato: una lista de diagramas por categoría a la izquierda, el editor de grafo al centro y el editor de texto con el documento del nodo seleccionado. Qué se pide: que el compositor de surface lea una composición guardada en el store (qué componentes van, en qué zona, a qué consulta o documento se enlaza cada uno y cómo pasa la selección de uno a otro) y arme la pantalla sin código por plugin. specIR entrega el documento de composición; los componentes son de surface. Se da por cumplido cuando la pantalla del catálogo de specIR se abre desde un documento del store y specIR puede borrar src/specir/visual/catalog/ (1.054 líneas). De esto dependen los nodos S5 y R4 del plan.
