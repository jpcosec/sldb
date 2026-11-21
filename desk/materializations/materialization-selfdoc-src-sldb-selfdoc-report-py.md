---
sldb:
  by: agent
  at: '2026-11-21T10:23:23Z'
  authority: generated
  via: create_document
id: materialization-selfdoc-src-sldb-selfdoc-report-py
title: selfdoc src-sldb-selfdoc-report-py
source_atoms:
- atom-selfdoc-check-compara-el-arbol-de-argparse-con-current-cli-tree-md
target_kind: code
target_identity: src/sldb/selfdoc/report.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/selfdoc/test_parser.py
tags:
- system:sldb
- topic:selfdoc
---

# selfdoc src-sldb-selfdoc-report-py

## Intent

materializa en src/sldb/selfdoc/report.py el atom atom-selfdoc-check-compara-el-arbol-de-argparse-con-current-cli-tree-md
