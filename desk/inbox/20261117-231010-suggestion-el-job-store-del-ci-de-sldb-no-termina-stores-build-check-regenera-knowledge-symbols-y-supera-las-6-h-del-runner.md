---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-17T23:10:10'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# El job store del CI de sldb no termina: stores build --check regenera knowledge/symbols y supera las 6 h del runner

_Describe the incoming message with enough evidence to triage._

Desde 6d87f126 los pasos del job store que fallaban (store de deskops y make world de pron) ya pasan en CI. Ahora el paso 'Rebuild sldb's store from its sources' (sldb stores build --check) lleva más de 5 h 45 min en el runner (run 44169114744, job 134343092734) y va a cortar en el límite de 6 h. Lo reproduje en local con el layout del runner: clones de GitHub de sldb 40d399e4, deskops a6bb2591 y pron a0c4100, sin scion y sin knowledge/symbols (gitignored y generado). stores build --check dio rc 0 en 110 min, con 100 % de CPU en un solo proceso todo el tiempo y solo alertas (anchors/doc_lost, doc_changed, rules). Con knowledge/symbols ya presente tarda unos 55 min, así que la mitad del tiempo es regenerar los símbolos. El runner es varias veces más lento que robocop2, por eso no entra en 6 h. Opciones: (a) cachear knowledge/symbols en CI con actions/cache, con clave en el hash de las fuentes que lo generan; (b) paralelizar o acotar la generación de símbolos; (c) separar build --check en un workflow aparte con timeout explícito. Es lo único que falta para el verde de main (prioridad b de la pausa). Integrador wA:p1.
