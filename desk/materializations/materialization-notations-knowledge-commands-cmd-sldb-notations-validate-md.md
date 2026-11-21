---
sldb:
  by: agent
  at: '2026-11-21T03:52:54Z'
  authority: generated
  via: create_document
id: materialization-notations-knowledge-commands-cmd-sldb-notations-validate-md
title: notations knowledge-commands-cmd-sldb-notations-validate-md
source_atoms:
- atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
target_kind: docs
target_identity: knowledge/commands/cmd-sldb-notations-validate.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_notations_validate_cli.py
tags:
- system:sldb
- topic:notations
---

# notations knowledge-commands-cmd-sldb-notations-validate-md

## Intent

materializa en knowledge/commands/cmd-sldb-notations-validate.md el atom atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
