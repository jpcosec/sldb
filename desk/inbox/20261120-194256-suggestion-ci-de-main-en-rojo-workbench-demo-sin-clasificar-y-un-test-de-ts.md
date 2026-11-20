---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-20T19:42:56'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# CI de main en rojo: workbench_demo sin clasificar y un test de TS

_Describe the incoming message with enough evidence to triage._

Visto al integrar jpcosec/sldb#3 (2026-11-20): la compuerta estructural identidad falla en main con «directorio versionado sin clasificar en la raíz: workbench_demo» (entró en 562847e2), así que el job no llega a correr pytest. Además tests/selfdoc/test_treesitter_symbols.py::test_ts_types_only_in_ts_and_same_module_names_take_a_suffix falla en main en local (scan_tree devuelve vacío). El #3 se integró con ese rojo, que no era suyo.
