---
sldb:
  by: agent
  at: '2026-11-16T10:14:41Z'
  authority: generated
  via: create_document
id: materialization-sections-missing-section-sync
title: sections-missing section_sync
source_atoms:
- atom-una-reconstrucción-de-secciones-con-documentos-trackeados-ausentes-avisa-una-vez-por-modelo-con-el-n
target_kind: code
target_identity: src/sldb/store/section_sync.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_semantic_rebuild.py
tags:
- system:sldb
- topic:store
---

# sections-missing section_sync

## Intent

materializa en src/sldb/store/section_sync.py el atom atom-una-reconstrucción-de-secciones-con-documentos-trackeados-ausentes-avisa-una-vez-por-modelo-con-el-n
