---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T19:43:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Cómo instala un plugin sus modelos y semillas en un store

_Describe the incoming message with enough evidence to triage._

Pedido de specIR (plan IR/desk/drawer/plans/specir-plugin-de-sldb/, decisión IR/docs/decisiones/specir-es-un-plugin-de-sldb.md). specIR y deskops son plugins sobre sldb. Hoy cada uno trae su instalador: specIR tiene src/specir/install.py (122 líneas) que registra sus modelos y copia relation_types.yaml y rules.yaml al store. Es código genérico repetido en cada plugin. Qué se pide: una forma de sldb para que un paquete declare qué modelos, tipos de relación, reglas, notaciones y documentos semilla aporta, y un comando de sldb que los instale y los actualice en un store, diciendo qué cambió. Se da por cumplido cuando specIR puede borrar install.py y un store nuevo queda con sus modelos y semillas usando solo ese comando. Relacionado: el pedido C1 de deskops (aplicar reglas y relaciones de un store enlazado, para no copiar semillas). No bloquea nada hoy: de esto depende el nodo S4 del plan.
