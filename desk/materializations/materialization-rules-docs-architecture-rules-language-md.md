---
sldb:
  by: agent
  at: '2026-11-21T10:44:13Z'
  authority: generated
  via: create_document
id: materialization-rules-docs-architecture-rules-language-md
title: rules docs-architecture-rules-language-md
source_atoms:
- atom-la-cabecera-de-rules-language-md-describe-la-semantica-bivaluada
target_kind: docs
target_identity: docs/architecture/rules-language.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_rules_language_spec.py
tags:
- system:sldb
- topic:rules
---

# rules docs-architecture-rules-language-md

## Intent

materializa en docs/architecture/rules-language.md el atom atom-la-cabecera-de-rules-language-md-describe-la-semantica-bivaluada
