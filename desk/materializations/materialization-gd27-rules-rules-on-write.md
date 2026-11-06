---
id: materialization-gd27-rules-rules-on-write
title: gd27 rules rules_on_write
source_atoms:
- atom-los-namespaces-de-tags-se-declaran-en-el-store-y-un-prefijo-necesita-su-documento-ancla
target_kind: code
target_identity: src/sldb/api/rules/rules_on_write.py
validation:
- pytest -q tests/api/test_tags.py tests/api/test_replace_text.py
tags:
- system:sldb
- topic:tags
- topic:rules
---

# gd27 rules rules_on_write

## Intent

materializa atom-los-namespaces-de-tags-se-declaran-en-el-store-y-un-prefijo-necesita-su-documento-ancla en src/sldb/api/rules/rules_on_write.py
