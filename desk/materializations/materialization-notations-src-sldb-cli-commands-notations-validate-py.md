---
sldb:
  by: agent
  at: '2026-11-21T03:21:44Z'
  authority: generated
  via: create_document
id: materialization-notations-src-sldb-cli-commands-notations-validate-py
title: notations src-sldb-cli-commands-notations_validate-py
source_atoms:
- atom-notations-validate-respeta-las-reglas-de-codigo-limpio
target_kind: code
target_identity: src/sldb/cli/commands/notations_validate.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_clean_code_rules.py
tags:
- system:sldb
- topic:notations
---

# notations src-sldb-cli-commands-notations_validate-py

## Intent

materializa en src/sldb/cli/commands/notations_validate.py el atom atom-notations-validate-respeta-las-reglas-de-codigo-limpio
