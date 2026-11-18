---
sldb:
  by: agent
  at: '2026-11-18T08:06:30Z'
  authority: generated
  via: create_document
id: materialization-ci-keep-workflow
title: ci-keep workflow
source_atoms:
- atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un
target_kind: config
target_identity: .github/workflows/ci.yml
validation:
- gh run view 44253024186 -R jpcosec/sldb --json jobs (store, test 3.12 y test 3.13
  en success)
tags:
- system:sldb
- topic:ci
---

# ci-keep workflow

## Intent

materializa en .github/workflows/ci.yml el atom atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un
