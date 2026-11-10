---
sldb:
  by: agent
  at: '2026-11-10T04:52:23Z'
  authority: generated
  via: create_document
id: materialization-link-missing-commands-stores-link-alert
title: link-missing commands stores_link_alert
source_atoms:
- atom-un-store-enlazado-ausente-es-alerta-en-stores-build-y-build-check
target_kind: code
target_identity: src/sldb/cli/commands/stores_link_alert.py
validation:
- pytest -q tests/store/test_stores_build.py
tags:
- system:sldb
- topic:stores
---

# link-missing commands stores_link_alert

## Intent

materializa atom-un-store-enlazado-ausente-es-alerta-en-stores-build-y-build-check en src/sldb/cli/commands/stores_link_alert.py
