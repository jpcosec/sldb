---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T19:46:44'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# code_facts: argumentos de las llamadas dentro del cuerpo de una función

_Describe the incoming message with enough evidence to triage._

Para que specir extract reconozca comandos de CLI armados en funciones (argparse: sub.add_parser('run'), p.set_defaults(func=h); registros tipo Command(path=..., handler=...)), attrs.calls de una función trae solo {name, line}. Pedido: que cada entrada traiga también args y kwargs como texto, igual que call_parts en las llamadas de módulo. Sin eso, deskops (cuyo parser y registro viven en funciones) no muestra sus comandos; specIR los reporta como desconocidos. No bloquea la tarea.
