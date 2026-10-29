---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-19T01:10:09'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-29T10:44:59'
---

# Decisión del dueño: qué mecanismo guarda el pasado del árbol del store (journal)

_Describe the incoming message with enough evidence to triage._

Bloquea la implementación del journal como vista. El diseño está entregado en docs/architecture/journal-authority.md (4a5a6b4f); la task de diseño task-congelar-journal-autoridad-arbol se cierra con ese documento.

Decisión exacta: qué mecanismo guarda el pasado del árbol Merkle del store, para que el journal se reduzca a una lista de punteros entre raíces.
(a) snapshots propios contenido-direccionados en .sldb/ (más fiel; agrega almacenamiento y poda);
(b) la historia de git de los shards (depende de que .sldb/core/ siga en git, lo opuesto a la nota 20261007-133032);
(c) descartar el journal y dejar la auditoría en git del markdown.

Mientras no se decida, el journal queda congelado: sin campos ni escritores nuevos.
