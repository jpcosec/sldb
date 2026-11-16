---
sldb:
  by: agent
  at: '2026-11-16T11:03:02Z'
  authority: generated
  via: create_document
id: materialization-sldb-version-test-cli-v2
title: sldb-version test_cli_v2
source_atoms:
- atom-sldb-version-dice-la-versión-del-paquete-y-desde-un-checkout-git-el-describe-y-la-ruta-del-checkout
target_kind: test
target_identity: tests/test_cli_v2.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
tags:
- system:sldb
- topic:cli
---

# sldb-version test_cli_v2

## Intent

materializa en tests/test_cli_v2.py el atom atom-sldb-version-dice-la-versión-del-paquete-y-desde-un-checkout-git-el-describe-y-la-ruta-del-checkout
