---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: gemini_test
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-09-16T09:55:07'
# open | closed
status: open
# project identity that acknowledged the note
acknowledged_by: ⸢rev•acknowledged_by⸥
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: ⸢rev•acknowledged_at⸥
---

# relpaths de layout hardcodean '.sldb': stores con otro nombre quedan invisibles

_Describe the incoming message with enough evidence to triage._

Bug de sldb: layout relpaths hardcodean el nombre del directorio del store ('.sldb'). models_index_relpath/documents_index_relpath/sections_index_relpath devuelven '.sldb/core/...' relativo al project root, mientras que shards y rebuilds usan rutas relativas al store real. Reproducción mínima: stores init --path kb; mv kb/.sldb kb/.sldb_custom; models add AtomDoc --store kb/.sldb_custom; docs create x2 --store kb/.sldb_custom (dice 'Created and tracked'); docs list --store kb/.sldb_custom -> documents: []. El docs track escribe kb/.sldb_custom/core/documents/AtomDoc/x2.yaml pero toda lectura (docs list/show, load_runtime_documents, stores update) resuelve los índices contra un '.sldb' fantasma recreado por models add (kb/.sldb/core/models/AtomDoc.yaml). Afecta cualquier store con nombre distinto a .sldb (p.ej. .sldb_custom/.sldb_test): el store parece vacío y los duplicados no se detectan. Detalle completo en /home/jp/AntonIA/repos/AWS_Infra_worktrees/x-fixtests/docs/sldb-bug-store-name-relpaths.md
