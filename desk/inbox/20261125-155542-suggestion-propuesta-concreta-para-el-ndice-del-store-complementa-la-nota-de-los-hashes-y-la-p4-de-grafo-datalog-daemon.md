---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T15:55:42'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Propuesta concreta para el índice del store (complementa la nota de los hashes y la P4 de grafo-datalog-daemon)

_Describe the incoming message with enough evidence to triage._

Complementa la nota 20261125-152845 (propósito de los hashes). Decisión de JP del 25-11: deskops exige git en cada desk, así que sldb puede apoyarse en git para los stores de deskops. Medido en deskops: leer las 2 233 hojas YAML de .sldb/core tarda 493 ms con libyaml; el mismo contenido en un JSON 11 ms y en sqlite 14 ms (una fila por clave 0,05 ms); stat de todas 3 ms. Encima del caché YAML ya hay otras dos capas para evitar leerlo: ~6 900 YAML por documento en .sldb_cache (edges, sections, semantic) y 1,7 GB de JSON en ~/.cache/sldb. Propuesta: (1) el índice en una base embebida de un archivo en .sldb_cache (sqlite, o el Cozo con almacenamiento sqlite de la P1), una fila por documento con source_hash, content_hash, field_hashes, extracted_with = contract_hash bajo el que se extrajo, y firma de stat completa (mtime_ns, size, inode, ctime) con manejo de filas indexadas en el mismo instante (el problema racy de git); agregados roster_hash y store_hash como hash de contenido, calculables al leer. (2) Sin daemon obligatorio: cada proceso hace stat contra las filas o, mejor, pregunta a git: git status --porcelain (70 ms en deskops) y git diff --name-only <commit indexado> HEAD (35 ms); el índice guarda el commit y el árbol con que se construyó. (3) source_hash = blob id de git: git ls-files -s da el de todos los rastreados en 14 ms sin leerlos; es seguro porque lo que se fija de forma persistente en las anclas es el contract_hash (models/doc_anchor_value.py), y source_hash solo se usa transitoriamente (concurrencia optimista, revision de vistas). (4) Caché de extracción direccionado por contenido con clave (blob id, contract_hash): compartible entre ramas, worktrees y clones, y el CI lo podría bajar hecho; de paso, docs history por campo se puede calcular desde git log de los blob ids más ese caché cuando el modelo no cambió, sin versionar core/. Límite: un store fuera de git necesita el stat propio como respaldo.
