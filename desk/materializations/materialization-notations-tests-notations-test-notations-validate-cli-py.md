---
sldb:
  by: agent
  at: '2026-11-21T03:54:26Z'
  authority: generated
  via: create_document
id: materialization-notations-tests-notations-test-notations-validate-cli-py
title: notations tests-notations-test_notations_validate_cli-py
source_atoms:
- atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
target_kind: test
target_identity: tests/notations/test_notations_validate_cli.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_notations_validate_cli.py
tags:
- system:sldb
- topic:notations
---

# notations tests-notations-test_notations_validate_cli-py

## Intent

materializa en tests/notations/test_notations_validate_cli.py el atom atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
