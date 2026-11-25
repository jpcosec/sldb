---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T17:26:48'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Que una máquina de estados se haga respetar: el campo de estado solo cambia tomando una arista

_Describe the incoming message with enough evidence to triage._

Pedido de deskops (25-11, decisión de JP: deskops es un plugin de sldb; el mecanismo es de sldb y deskops solo declara su workflow como dato). Diagnóstico de deskops (deskops/desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md): el workflow declarado no se hace cumplir; se puede cerrar una tarea sin pasar por testing porque nada impide escribir status y current_node fuera de una arista. Busqué en rules.md y edges.md de sldb y no hay forma de declarar que un campo de estado solo cambia tomando una RelationDoc. Pedido genérico, para cualquier modelo: (1) declarar en el modelo (o en una RuleDoc) que ciertos campos (status, current_node, history) solo se escriben tomando una arista válida desde el valor actual, y que cualquier otra escritura por sldb se rechace; (2) como no todo pasa por sldb (un agente puede editar el Markdown a mano), una comprobación apta para CI que recorra el historial de git de cada documento con máquina de estados y verifique que cada cambio de esos campos corresponde a una arista válida (deskops exige git en cada desk, decisión de JP del 25-11); (3) que una regla pueda exigir, como gate local antes del CI, un recibo de los tests que corresponden a lo que mutó. Relacionado con C2 (tomar transición) y C3 (último elemento de una lista) de las notas 20261125-1436*. La pregunta de diseño de cuál combinación usar queda para sldb y JP; deskops la usa.
