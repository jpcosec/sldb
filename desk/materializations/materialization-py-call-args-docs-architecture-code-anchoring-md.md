---
sldb:
  by: agent
  at: '2026-11-25T22:24:30Z'
  authority: generated
  via: create_document
id: materialization-py-call-args-docs-architecture-code-anchoring-md
title: py-call-args docs-architecture-code-anchoring-md
source_atoms:
- atom-los-hechos-de-llamada-de-python-traen-sus-argumentos-literales
target_kind: docs
target_identity: docs/architecture/code-anchoring.md
validation:
- pytest -q tests/code/test_py_call_args.py tests/selfdoc/test_fingerprints.py
tags:
- system:sldb
- topic:py-call-args
---

# py-call-args docs-architecture-code-anchoring-md

## Intent

materializa en docs/architecture/code-anchoring.md el atom atom-los-hechos-de-llamada-de-python-traen-sus-argumentos-literales
