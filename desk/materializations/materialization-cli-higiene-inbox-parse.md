---
sldb:
  by: agent
  at: '2026-11-19T09:02:42Z'
  authority: generated
  via: create_document
id: materialization-cli-higiene-inbox-parse
title: cli higiene inbox_parse
source_atoms:
- atom-fields-update-y-append-aceptan-string-y-format-e-inbox-reporta-por-stderr-y-no-escribe-sin-store
target_kind: code
target_identity: src/sldb/cli/commands/inbox_parse.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_cli_v2.py
tags:
- system:sldb
- topic:cli
---

# cli higiene inbox_parse

## Intent

materializa en src/sldb/cli/commands/inbox_parse.py el atom atom-fields-update-y-append-aceptan-string-y-format-e-inbox-reporta-por-stderr-y-no-escribe-sin-store
