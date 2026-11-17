---
sldb:
  by: agent
  at: '2026-11-17T16:33:04Z'
  authority: generated
  via: create_document
id: materialization-lk-md-scan-text
title: lk-md scan_text
source_atoms:
- atom-sldb-links-extrae-los-enlaces-del-árbol-de-markdown-it-y-no-cuenta-nada-que-esté-en-código-cercado-i
target_kind: code
target_identity: src/sldb/links/scan_text.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links.py
tags:
- system:sldb
- topic:links
---

# lk-md scan_text

## Intent

materializa en src/sldb/links/scan_text.py el atom atom-sldb-links-extrae-los-enlaces-del-árbol-de-markdown-it-y-no-cuenta-nada-que-esté-en-código-cercado-i
