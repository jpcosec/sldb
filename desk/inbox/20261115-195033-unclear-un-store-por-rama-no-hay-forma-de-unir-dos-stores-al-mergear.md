---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: mepu
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T19:50:33'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# un store por rama: no hay forma de unir dos stores al mergear

_Describe the incoming message with enough evidence to triage._

Caso real en el repo mepu (2026-11-15). El store .sldb/ nació en una rama de trabajo (wt/ontologia-licitaciones, en un worktree de git) con 5 modelos y 31 documentos de ontología. Después hubo que inicializar deskops, que según la regla de uso va en el checkout principal sobre dev. Ahí no existía .sldb/, así que deskops init habría creado un segundo store independiente en dev. Los dos stores escriben los mismos archivos (.sldb/store.yaml, .sldb/core/store_index.yaml, .sldb/core/models/*.yaml) con contenido distinto, y al mergear la rama chocarían: son índices generados, con hashes, que no se pueden fusionar a mano. No se llegó a producir el choque: se evitó inicializando deskops dentro del worktree, sobre el store existente, a costa de que el desk queda en una rama sin mergear. Lo que no está claro: 1) si sldb tiene una forma soportada de unir o reconstruir un store después de un merge de git (reindexar desde los documentos y los modelos, en vez de fusionar los YAML del índice); 2) si no la tiene, cómo se espera trabajar con un store cuando hay varias ramas o worktrees que agregan modelos y documentos en paralelo. Nota: esto es una previsión a partir de qué archivos escribe cada store; no se probó el merge.
