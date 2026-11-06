---
id: materialization-gd27-rules-builtin-tag-rules
title: gd27 rules builtin_tag_rules
source_atoms:
- atom-los-namespaces-de-tags-se-declaran-en-el-store-y-un-prefijo-necesita-su-documento-ancla
target_kind: code
target_identity: src/sldb/api/rules/builtin_tag_rules.py
validation:
- pytest -q tests/api/test_tags.py tests/api/test_replace_text.py
tags:
- system:sldb
- topic:tags
- topic:rules
---

# gd27 rules builtin_tag_rules

## Intent

materializa atom-los-namespaces-de-tags-se-declaran-en-el-store-y-un-prefijo-necesita-su-documento-ancla en src/sldb/api/rules/builtin_tag_rules.py
