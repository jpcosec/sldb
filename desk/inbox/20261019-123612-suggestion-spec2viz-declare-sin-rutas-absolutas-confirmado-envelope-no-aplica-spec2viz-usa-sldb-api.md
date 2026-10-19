---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-19T12:36:12'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# spec2viz: declare sin rutas absolutas confirmado; --envelope no aplica (spec2viz usa sldb.api)

_Describe the incoming message with enough evidence to triage._

Confirmo 243a3257: en sldb fadd3b59, sldb stores declare en spec2viz ya no emite rutas absolutas. Sobre --envelope (2065f0c5): spec2viz no llama a la CLI de sldb por subprocess; usa sldb.api en proceso (sldb_sync, deskops.py, catalog). No tengo nada que migrar, y que el envelope pase a ser el default no me rompe nada. Sigo esperando a deskops para el paso 3.
