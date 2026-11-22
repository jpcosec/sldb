---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: Chatbot_Infra
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-22T18:53:16'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# selfdoc python-scan: módulos sin símbolos, imports anidados, reexportes y repos hermanos

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de Chatbot_Infra en el triaje del 2026-11-22: es un pedido para sldb que quedó escrito allá con sldb inbox el 2026-11-04 y nunca llegó a este desk. Texto original: Al armar el mapa de código de la wiki del desk (ops/wiki_desk.py) con sldb selfdoc python-scan faltó: (1) un módulo sin clases ni funciones (p. ej. un __init__ que solo reexporta) no aparece en la salida, así que no se ven sus imports; (2) solo se ven los imports de nivel de módulo, no los de dentro de una función; (3) no resuelve reexportes: from data import SqlStore queda como uso de data/__init__ y no de data/store.py, ni los reexportes perezosos por un mapa de nombres; (4) --source-root tiene que estar dentro del proyecto del store: un repo hermano (../labchile_chatbots) se escanea con su propio store; (5) para tener el grafo node-link hay que usar python-sync, que trackea un documento por símbolo (miles). Sugerencia: python-scan --graph-output sin trackear, con nodos de módulo para todo archivo .py y aristas resueltas a través de reexportes. Mientras tanto la herramienta lo completa con ast.
