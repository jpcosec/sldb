---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-09-30T17:36:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# stores update no recomputa content_hash cuando el shard no tiene field_hashes

_Describe the incoming message with enough evidence to triage._

Reparando 37 desks del ecosistema aparecieron dos fallas de sldb que bloquean la migracion:

1) stores update no recomputa content_hash en shards sin field_hashes.
   Repro: kimun, TraderBot, marcado, gemini_test, matrix-shrdlu-spec. stores check
   reporta data_mutation permanente aunque el .md este intacto en git (source_hash
   coincide, content_hash no). migrate-hashes renombra hash_c/hash_d a
   source_hash/content_hash pero no recalcula, y update respeta el valor rancio.
   Workaround usado: borrar content_hash/source_hash del shard y correr stores update,
   que ahi si recomputa. Afecto ~236 documentos en 6 repos.

2) migrate_store_layout nunca corre en stores con layout viejo.
   open_store llama migrate_store_layout solo si store_exists (que reconoce
   .sldb/store_index.yaml legacy), pero migrate_store_layout arranca con
   load_store_index, que lee unicamente core/store_index.yaml y lanza
   FileNotFoundError: No store_index.yaml. El migrador muere antes de migrar.
   Repro: hum-ecosystem-worktrees/pm-surface, sldb-ui, hum-ecosystem/hum-core.
   Esos tres stores quedaron sin tocar esperando esta decision.
