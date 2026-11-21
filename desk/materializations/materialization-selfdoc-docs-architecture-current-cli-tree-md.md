---
sldb:
  by: agent
  at: '2026-11-21T10:21:54Z'
  authority: generated
  via: create_document
id: materialization-selfdoc-docs-architecture-current-cli-tree-md
title: selfdoc docs-architecture-current-cli-tree-md
source_atoms:
- atom-selfdoc-check-compara-el-arbol-de-argparse-con-current-cli-tree-md
target_kind: docs
target_identity: docs/architecture/current-cli-tree.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/selfdoc/test_parser.py
tags:
- system:sldb
- topic:selfdoc
---

# selfdoc docs-architecture-current-cli-tree-md

## Intent

materializa en docs/architecture/current-cli-tree.md el atom atom-selfdoc-check-compara-el-arbol-de-argparse-con-current-cli-tree-md
