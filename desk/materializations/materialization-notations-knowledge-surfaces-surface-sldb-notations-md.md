---
sldb:
  by: agent
  at: '2026-11-21T03:53:23Z'
  authority: generated
  via: create_document
id: materialization-notations-knowledge-surfaces-surface-sldb-notations-md
title: notations knowledge-surfaces-surface-sldb-notations-md
source_atoms:
- atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
target_kind: docs
target_identity: knowledge/surfaces/surface-sldb-notations.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_notations_validate_cli.py
tags:
- system:sldb
- topic:notations
---

# notations knowledge-surfaces-surface-sldb-notations-md

## Intent

materializa en knowledge/surfaces/surface-sldb-notations.md el atom atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
