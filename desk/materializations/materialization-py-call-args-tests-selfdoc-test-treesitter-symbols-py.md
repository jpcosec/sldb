---
sldb:
  by: agent
  at: '2026-11-25T22:26:09Z'
  authority: generated
  via: create_document
id: materialization-py-call-args-tests-selfdoc-test-treesitter-symbols-py
title: py-call-args tests-selfdoc-test_treesitter_symbols-py
source_atoms:
- atom-los-hechos-de-llamada-de-python-traen-sus-argumentos-literales
target_kind: test
target_identity: tests/selfdoc/test_treesitter_symbols.py
validation:
- pytest -q tests/code/test_py_call_args.py tests/selfdoc/test_fingerprints.py
tags:
- system:sldb
- topic:py-call-args
---

# py-call-args tests-selfdoc-test_treesitter_symbols-py

## Intent

materializa en tests/selfdoc/test_treesitter_symbols.py el atom atom-los-hechos-de-llamada-de-python-traen-sus-argumentos-literales
