---
sldb:
  by: agent
  at: '2026-11-25T20:45:24Z'
  authority: generated
  via: create_document
id: materialization-docs-create-cwd-tests-test-cli-v2-py
title: docs-create-cwd tests-test_cli_v2-py
source_atoms:
- atom-sldb-docs-create-o-resuelve-la-ruta-relativa-contra-el-cwd
target_kind: test
target_identity: tests/test_cli_v2.py
validation:
- pytest -q tests/test_docs_create_output_path.py
tags:
- system:sldb
- topic:docs-create-cwd
---

# docs-create-cwd tests-test_cli_v2-py

## Intent

materializa en tests/test_cli_v2.py el atom atom-sldb-docs-create-o-resuelve-la-ruta-relativa-contra-el-cwd
