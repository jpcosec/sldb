---
sldb:
  by: agent
  at: '2026-11-16T11:02:19Z'
  authority: generated
  via: create_document
id: materialization-sldb-version-core
title: sldb-version core
source_atoms:
- atom-sldb-version-dice-la-versión-del-paquete-y-desde-un-checkout-git-el-describe-y-la-ruta-del-checkout
target_kind: code
target_identity: src/sldb/cli/parsers/core.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
tags:
- system:sldb
- topic:cli
---

# sldb-version core

## Intent

materializa en src/sldb/cli/parsers/core.py el atom atom-sldb-version-dice-la-versión-del-paquete-y-desde-un-checkout-git-el-describe-y-la-ruta-del-checkout
