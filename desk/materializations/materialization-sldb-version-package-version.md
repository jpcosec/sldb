---
sldb:
  by: agent
  at: '2026-11-16T11:01:58Z'
  authority: generated
  via: create_document
id: materialization-sldb-version-package-version
title: sldb-version package_version
source_atoms:
- atom-sldb-version-dice-la-versión-del-paquete-y-desde-un-checkout-git-el-describe-y-la-ruta-del-checkout
target_kind: code
target_identity: src/sldb/store/package_version.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
tags:
- system:sldb
- topic:cli
---

# sldb-version package_version

## Intent

materializa en src/sldb/store/package_version.py el atom atom-sldb-version-dice-la-versión-del-paquete-y-desde-un-checkout-git-el-describe-y-la-ruta-del-checkout
