---
id: materialization-gd27-tags-tag-check
title: gd27 tags tag_check
source_atoms:
- atom-los-namespaces-de-tags-se-declaran-en-el-store-y-un-prefijo-necesita-su-documento-ancla
target_kind: code
target_identity: src/sldb/api/tags/tag_check.py
validation:
- pytest -q tests/api/test_tags.py tests/api/test_replace_text.py
tags:
- system:sldb
- topic:tags
- topic:rules
---

# gd27 tags tag_check

## Intent

materializa atom-los-namespaces-de-tags-se-declaran-en-el-store-y-un-prefijo-necesita-su-documento-ancla en src/sldb/api/tags/tag_check.py
