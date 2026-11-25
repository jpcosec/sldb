---
sldb:
  by: agent
  at: '2026-11-25T22:25:36Z'
  authority: generated
  via: create_document
id: materialization-py-call-args-tests-code-test-py-call-args-py
title: py-call-args tests-code-test_py_call_args-py
source_atoms:
- atom-los-hechos-de-llamada-de-python-traen-sus-argumentos-literales
target_kind: test
target_identity: tests/code/test_py_call_args.py
validation:
- pytest -q tests/code/test_py_call_args.py tests/selfdoc/test_fingerprints.py
tags:
- system:sldb
- topic:py-call-args
---

# py-call-args tests-code-test_py_call_args-py

## Intent

materializa en tests/code/test_py_call_args.py el atom atom-los-hechos-de-llamada-de-python-traen-sus-argumentos-literales
