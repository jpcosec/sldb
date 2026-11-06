---
id: materialization-sv04-src-sldb-cli-commands-models-validate-py
title: 'SV04: src/sldb/cli/commands/models_validate.py'
source_atoms:
- atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill
target_kind: code
target_identity: src/sldb/cli/commands/models_validate.py
validation:
- pytest -q tests/api/test_model_metadata_drafts.py
tags:
- system:sldb
- task:sv04
---

# SV04: src/sldb/cli/commands/models_validate.py

## Intent

src/sldb/cli/commands/models_validate.py materializa la decision de SV04 (atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill).
