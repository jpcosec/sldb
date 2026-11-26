---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-26T00:56:27'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# deskops add task tarda cerca de 90 segundos cuando otra sesión usa el mismo store

_Describe the incoming message with enough evidence to triage._

Medido el 2026-11-25 en robocop2, en el desk de IR: cada deskops add task --from-yaml tardó entre 80 y 100 segundos (seis tareas seguidas pasaron de 120 s en total y la tanda se fue a segundo plano), mientras el despacho corría cierres sobre el mismo store. En johanes, sin otra sesión, un deskops message ack sobre el mismo desk tarda 22 segundos. scion confirmó en la sala (sala/2026-11-25-planificacion/scion.md) que no es su lock de tests sino contención del store de sldb. No sé cuánto es espera del cerrojo y cuánto es carga y reescritura de índices; eso es lo que se pide medir. Se da por atendido cuando sldb dice dónde se va el tiempo de una escritura de un documento en un store de este tamaño y si la espera por el cerrojo se informa al usuario.
