---
sldb:
  by: agent
  at: '2026-11-20T16:33:48Z'
  authority: generated
  via: create_document
id: materialization-stores-tests-store-test-diagnostics-py
title: stores tests-store-test_diagnostics-py
source_atoms:
- atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta
target_kind: test
target_identity: tests/store/test_diagnostics.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_diagnostics.py
tags:
- system:sldb
- topic:stores
---

# stores tests-store-test_diagnostics-py

## Intent

materializa en tests/store/test_diagnostics.py el atom atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta
