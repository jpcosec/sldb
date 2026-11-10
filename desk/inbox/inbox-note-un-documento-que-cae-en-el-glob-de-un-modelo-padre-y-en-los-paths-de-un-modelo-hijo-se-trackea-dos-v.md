---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-10T14:20:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Un documento que cae en el glob de un modelo padre y en los paths de un modelo hijo se trackea dos veces

_Describe the incoming message with enough evidence to triage._

Visto en deskops el 2026-11-10 con sldb@main. El .sldb/store.yaml de deskops declara TaskDoc con el glob desk/tasks/task-*.md (desde 376fdcce) y además los paths explícitos de TaskCodeDoc y TaskDebugDoc, que son hijos de TaskDoc. sldb stores build trackea los 5 tasks dos veces: bajo su modelo hijo y otra vez bajo TaskDoc. sldb stores build --check da rc 0 igual, y los selectores por nombre quedan ambiguos porque el mismo id resuelve a dos documentos.

Además, sldb stores declare --write conserva el glob autorado, y no hay CLI para quitar una entrada include de store.yaml. Editar .sldb a mano está prohibido, así que el desk no puede corregirse solo.

Esperado: (a) cuando un archivo cae en el glob de un modelo y en los paths de un descendiente, gana el modelo más específico y se trackea una sola vez, o build --check lo marca como error (store/duplicate-tracking); (b) una vía de CLI para quitar o reemplazar una entrada include (sldb stores undeclare o declare --write con --drop-glob). Tarea consumidora en el drawer de deskops: quitar o migrar el glob TaskDoc cuando exista la vía.
