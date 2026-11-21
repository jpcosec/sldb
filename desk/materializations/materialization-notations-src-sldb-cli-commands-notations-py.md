---
sldb:
  by: agent
  at: '2026-11-21T03:53:53Z'
  authority: generated
  via: create_document
id: materialization-notations-src-sldb-cli-commands-notations-py
title: notations src-sldb-cli-commands-notations-py
source_atoms:
- atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
target_kind: code
target_identity: src/sldb/cli/commands/notations.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_notations_validate_cli.py
tags:
- system:sldb
- topic:notations
---

# notations src-sldb-cli-commands-notations-py

## Intent

materializa en src/sldb/cli/commands/notations.py el atom atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
