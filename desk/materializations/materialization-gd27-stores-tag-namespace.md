---
id: materialization-gd27-stores-tag-namespace
title: gd27 stores tag_namespace
source_atoms:
- atom-los-namespaces-de-tags-se-declaran-en-el-store-y-un-prefijo-necesita-su-documento-ancla
target_kind: code
target_identity: src/sldb/api/stores/tag_namespace.py
validation:
- pytest -q tests/api/test_tags.py tests/api/test_replace_text.py
tags:
- system:sldb
- topic:tags
- topic:rules
---

# gd27 stores tag_namespace

## Intent

materializa atom-los-namespaces-de-tags-se-declaran-en-el-store-y-un-prefijo-necesita-su-documento-ancla en src/sldb/api/stores/tag_namespace.py
