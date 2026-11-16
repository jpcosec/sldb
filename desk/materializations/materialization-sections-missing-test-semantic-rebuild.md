---
sldb:
  by: agent
  at: '2026-11-16T10:15:32Z'
  authority: generated
  via: create_document
id: materialization-sections-missing-test-semantic-rebuild
title: sections-missing test_semantic_rebuild
source_atoms:
- atom-una-reconstrucción-de-secciones-con-documentos-trackeados-ausentes-avisa-una-vez-por-modelo-con-el-n
target_kind: test
target_identity: tests/store/test_semantic_rebuild.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_semantic_rebuild.py
tags:
- system:sldb
- topic:store
---

# sections-missing test_semantic_rebuild

## Intent

materializa en tests/store/test_semantic_rebuild.py el atom atom-una-reconstrucción-de-secciones-con-documentos-trackeados-ausentes-avisa-una-vez-por-modelo-con-el-n
