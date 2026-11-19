---
sldb:
  by: agent
  at: '2026-11-19T10:08:55Z'
  authority: generated
  via: create_document
id: materialization-selfdoc-required-estable-arguments
title: selfdoc required estable arguments
source_atoms:
- atom-selfdoc-normaliza-el-required-de-los-posicionales-nargs-para-que-la-referencia-no-dependa-del-parche
target_kind: code
target_identity: src/sldb/selfdoc/arguments.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/selfdoc/test_argument_required.py
tags:
- system:sldb
- topic:selfdoc
---

# selfdoc required estable arguments

## Intent

materializa en src/sldb/selfdoc/arguments.py el atom atom-selfdoc-normaliza-el-required-de-los-posicionales-nargs-para-que-la-referencia-no-dependa-del-parche
