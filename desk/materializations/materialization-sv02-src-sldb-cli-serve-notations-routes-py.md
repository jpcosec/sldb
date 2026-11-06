---
id: materialization-sv02-src-sldb-cli-serve-notations-routes-py
title: 'SV02: src/sldb/cli/serve/notations_routes.py'
source_atoms:
- atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
target_kind: code
target_identity: src/sldb/cli/serve/notations_routes.py
validation:
- pytest -q tests/notations/test_notation_view_and_routes.py
tags:
- system:sldb
- task:sv02
---

# SV02: src/sldb/cli/serve/notations_routes.py

## Intent

src/sldb/cli/serve/notations_routes.py materializa la decision de SV02 (atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve).
