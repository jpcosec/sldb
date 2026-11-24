---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-24T02:37:54'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T23:38:31'
# why the note was acknowledged; empty when no reason was given
ack_reason: una sola falla de la suite por timeout de test_serve bajo carga alta del
  host (load 16); integrate reencolado
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Semantica del store: padres declarados solo en el cache, namespace sin padre y migracion de tags en bloque

_Describe the incoming message with enough evidence to triage._

Desde deskops (tarea un-solo-vocabulario-de-tags). Tres huecos en sldb: (1) 'sldb semantic parent add' y 'equivalent add' escriben en .sldb_cache/semantic_dag.yaml, que esta en .gitignore: los padres declarados no se versionan ni sobreviven a un clon nuevo ni a borrar el cache; hace falta guardarlos en el store trackeado (por ejemplo .sldb/core). (2) 'parent add TAG PARENT' rechaza un PARENT que ningun documento o modelo lleva ('Unknown semantic tag'), asi que no se puede declarar el padre de topic:atoms, system:deskops, host:robocop2, pill-type:* (149 tags planos con dos puntos siguen sin padre). Propuesta: que ns:valor tenga como padre implicito el namespace ns, o que parent add pueda crear el nodo padre. (3) Falta una operacion de migracion de tags en bloque (renombrar/quitar un tag en todos los documentos) y una consulta por tag que liste descendientes explicitos; hoy deskops migra con su propio 'deskops tags migrate' reescribiendo cada documento por su modelo (1083 documentos tardaron unas 3 horas por una transaccion por documento).
