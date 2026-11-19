---
sldb:
  by: agent
  at: '2026-11-19T12:43:30Z'
  authority: generated
  via: create_document
id: materialization-fix-tag-namespace-builtin-tag-findings
title: fix tag_namespace builtin_tag_findings
source_atoms:
- atom-los-hallazgos-builtin-tag-namespace-traen-un-fix-accionable
target_kind: code
target_identity: src/sldb/api/rules/builtin_tag_findings.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_tags.py
tags:
- system:sldb
- topic:tags
---

# fix tag_namespace builtin_tag_findings

## Intent

materializa en src/sldb/api/rules/builtin_tag_findings.py el atom atom-los-hallazgos-builtin-tag-namespace-traen-un-fix-accionable
