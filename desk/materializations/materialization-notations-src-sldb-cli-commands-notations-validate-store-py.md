---
sldb:
  by: agent
  at: '2026-11-21T03:22:14Z'
  authority: generated
  via: create_document
id: materialization-notations-src-sldb-cli-commands-notations-validate-store-py
title: notations src-sldb-cli-commands-notations_validate_store-py
source_atoms:
- atom-notations-validate-respeta-las-reglas-de-codigo-limpio
target_kind: code
target_identity: src/sldb/cli/commands/notations_validate_store.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_clean_code_rules.py
tags:
- system:sldb
- topic:notations
---

# notations src-sldb-cli-commands-notations_validate_store-py

## Intent

materializa en src/sldb/cli/commands/notations_validate_store.py el atom atom-notations-validate-respeta-las-reglas-de-codigo-limpio
