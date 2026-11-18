---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-17T23:26:08'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# CI store: build --check pasa en CI; lo que corta las 6 h es el segundo stores build del paso de referencia CLI

_Describe the incoming message with enough evidence to triage._

Seguimiento de la nota 20261117-231010. El run 44169114744 (sldb 6d87f126) terminó cancelado a las 6 h 0 min. Resultado de cada paso del job store: el store de deskops, el make world de pron y 'Rebuild sldb's store from its sources' (sldb stores build --check) dieron success. El que se canceló fue 'Check generated CLI reference', que corre 'sldb stores build && sldb selfdoc check': construye el store completo por segunda vez porque --check no deja el store escrito. Es decir, el job construye el store dos veces y la segunda no entra en el tiempo. El arreglo más barato es construir una sola vez. Opciones: (a) que el paso de referencia CLI reuse el store, con un build --check que deje el store escrito o un build normal seguido de una comprobación de no-cambios; (b) cachear knowledge/symbols, como dice la nota anterior; (c) las dos. Los jobs test 3.12 y 3.13 están en verde. Integrador wA:p1.
