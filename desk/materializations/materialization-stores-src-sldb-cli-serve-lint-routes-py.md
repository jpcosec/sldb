---
sldb:
  by: agent
  at: '2026-11-20T16:31:39Z'
  authority: generated
  via: create_document
id: materialization-stores-src-sldb-cli-serve-lint-routes-py
title: stores src-sldb-cli-serve-lint_routes-py
source_atoms:
- atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta
target_kind: code
target_identity: src/sldb/cli/serve/lint_routes.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_diagnostics.py
tags:
- system:sldb
- topic:stores
---

# stores src-sldb-cli-serve-lint_routes-py

## Intent

materializa en src/sldb/cli/serve/lint_routes.py el atom atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta
