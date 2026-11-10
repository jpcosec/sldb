---
sldb:
  by: agent
  at: '2026-11-10T04:52:19Z'
  authority: generated
  via: create_document
id: materialization-link-missing-commands-stores-build-check
title: link-missing commands stores_build_check
source_atoms:
- atom-un-store-enlazado-ausente-es-alerta-en-stores-build-y-build-check
target_kind: code
target_identity: src/sldb/cli/commands/stores_build_check.py
validation:
- pytest -q tests/store/test_stores_build.py
tags:
- system:sldb
- topic:stores
---

# link-missing commands stores_build_check

## Intent

materializa atom-un-store-enlazado-ausente-es-alerta-en-stores-build-y-build-check en src/sldb/cli/commands/stores_build_check.py
