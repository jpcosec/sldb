---
sldb:
  by: agent
  at: '2026-11-26T01:06:29Z'
  authority: generated
  via: create_document
id: materialization-undo-changes-sesiones-contracts-layers-toml
title: undo-changes-sesiones contracts-layers-toml
source_atoms:
- atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
target_kind: config
target_identity: contracts/layers.toml
validation:
- pytest -q tests/test_mcp_undo_across_sessions.py tests/mcp/test_write_tools.py
tags:
- system:sldb
- topic:undo-changes-sesiones
---

# undo-changes-sesiones contracts-layers-toml

## Intent

materializa en contracts/layers.toml el atom atom-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior
