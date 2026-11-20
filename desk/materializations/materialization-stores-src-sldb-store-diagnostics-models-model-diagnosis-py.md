---
sldb:
  by: agent
  at: '2026-11-20T16:33:14Z'
  authority: generated
  via: create_document
id: materialization-stores-src-sldb-store-diagnostics-models-model-diagnosis-py
title: stores src-sldb-store-diagnostics_models-model_diagnosis-py
source_atoms:
- atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta
target_kind: code
target_identity: src/sldb/store/diagnostics_models/model_diagnosis.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_diagnostics.py
tags:
- system:sldb
- topic:stores
---

# stores src-sldb-store-diagnostics_models-model_diagnosis-py

## Intent

materializa en src/sldb/store/diagnostics_models/model_diagnosis.py el atom atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta
