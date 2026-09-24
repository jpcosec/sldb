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
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: 2026-09-23T19:30:00
---

# relpaths de layout hardcodean '.sldb': stores con otro nombre quedan invisibles

_Describe the incoming message with enough evidence to triage._

Bug de sldb: layout relpaths hardcodean el nombre del directorio del store ('.sldb'). models_index_relpath/documents_index_relpath/sections_index_relpath devuelven '.sldb/core/...' relativo al project root, mientras que shards y rebuilds usan rutas relativas al store real. Reproducción mínima: stores init --path kb; mv kb/.sldb kb/.sldb_custom; models add AtomDoc --store kb/.sldb_custom; docs create x2 --store kb/.sldb_custom (dice 'Created and tracked'); docs list --store kb/.sldb_custom -> documents: []. El docs track escribe kb/.sldb_custom/core/documents/AtomDoc/x2.yaml pero toda lectura (docs list/show, load_runtime_documents, stores update) resuelve los índices contra un '.sldb' fantasma recreado por models add (kb/.sldb/core/models/AtomDoc.yaml). Afecta cualquier store con nombre distinto a .sldb (p.ej. .sldb_custom/.sldb_test): el store parece vacío y los duplicados no se detectan. Detalle completo en /home/jp/AntonIA/repos/AWS_Infra_worktrees/x-fixtests/docs/sldb-bug-store-name-relpaths.md

## Resolution

Commit 76c19b2 "fix(store): index relpaths derive from the real store directory name, not a hardcoded '.sldb'": `src/sldb/store/layout.py` deriva los relpaths del nombre real del directorio del store (via `_index_relpath`), de modo que un store renombrado a `.sldb_custom` queda legible y `models add` ya no recrea un `.sldb` fantasma. Regresion en `tests/store/test_store_name_relpaths.py`.
