---
sldb:
  by: agent
  at: '2026-11-17T16:33:39Z'
  authority: generated
  via: create_document
id: materialization-lk-md-parser
title: lk-md parser
source_atoms:
- atom-sldb-links-extrae-los-enlaces-del-árbol-de-markdown-it-y-no-cuenta-nada-que-esté-en-código-cercado-i
target_kind: code
target_identity: src/sldb/links/parser.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links.py
tags:
- system:sldb
- topic:links
---

# lk-md parser

## Intent

materializa en src/sldb/links/parser.py el atom atom-sldb-links-extrae-los-enlaces-del-árbol-de-markdown-it-y-no-cuenta-nada-que-esté-en-código-cercado-i
