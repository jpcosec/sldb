---
sldb:
  by: agent
  at: '2026-11-21T10:24:21Z'
  authority: generated
  via: create_document
id: materialization-selfdoc-tests-selfdoc-test-parser-py
title: selfdoc tests-selfdoc-test_parser-py
source_atoms:
- atom-selfdoc-check-compara-el-arbol-de-argparse-con-current-cli-tree-md
target_kind: test
target_identity: tests/selfdoc/test_parser.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/selfdoc/test_parser.py
tags:
- system:sldb
- topic:selfdoc
---

# selfdoc tests-selfdoc-test_parser-py

## Intent

materializa en tests/selfdoc/test_parser.py el atom atom-selfdoc-check-compara-el-arbol-de-argparse-con-current-cli-tree-md
