---
sldb:
  by: agent
  at: '2026-11-19T10:09:24Z'
  authority: generated
  via: create_document
id: materialization-selfdoc-required-estable-test-argument-required
title: selfdoc required estable test_argument_required
source_atoms:
- atom-selfdoc-normaliza-el-required-de-los-posicionales-nargs-para-que-la-referencia-no-dependa-del-parche
target_kind: test
target_identity: tests/selfdoc/test_argument_required.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/selfdoc/test_argument_required.py
tags:
- system:sldb
- topic:selfdoc
---

# selfdoc required estable test_argument_required

## Intent

materializa en tests/selfdoc/test_argument_required.py el atom atom-selfdoc-normaliza-el-required-de-los-posicionales-nargs-para-que-la-referencia-no-dependa-del-parche
