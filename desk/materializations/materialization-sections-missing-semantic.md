---
sldb:
  by: agent
  at: '2026-11-16T10:15:07Z'
  authority: generated
  via: create_document
id: materialization-sections-missing-semantic
title: sections-missing semantic
source_atoms:
- atom-una-reconstrucción-de-secciones-con-documentos-trackeados-ausentes-avisa-una-vez-por-modelo-con-el-n
target_kind: code
target_identity: src/sldb/store/semantic.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_semantic_rebuild.py
tags:
- system:sldb
- topic:store
---

# sections-missing semantic

## Intent

materializa en src/sldb/store/semantic.py el atom atom-una-reconstrucción-de-secciones-con-documentos-trackeados-ausentes-avisa-una-vez-por-modelo-con-el-n
