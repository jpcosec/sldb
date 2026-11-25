---
sldb:
  by: agent
  at: '2026-11-25T22:25:04Z'
  authority: generated
  via: create_document
id: materialization-py-call-args-src-sldb-code-py-calls-py
title: py-call-args src-sldb-code-py_calls-py
source_atoms:
- atom-los-hechos-de-llamada-de-python-traen-sus-argumentos-literales
target_kind: code
target_identity: src/sldb/code/py_calls.py
validation:
- pytest -q tests/code/test_py_call_args.py tests/selfdoc/test_fingerprints.py
tags:
- system:sldb
- topic:py-call-args
---

# py-call-args src-sldb-code-py_calls-py

## Intent

materializa en src/sldb/code/py_calls.py el atom atom-los-hechos-de-llamada-de-python-traen-sus-argumentos-literales
