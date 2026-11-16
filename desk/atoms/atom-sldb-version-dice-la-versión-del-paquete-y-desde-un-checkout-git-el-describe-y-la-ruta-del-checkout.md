---
sldb:
  by: agent
  at: '2026-11-16T11:01:37Z'
  authority: generated
  via: create_document
id: atom-sldb-version-dice-la-versión-del-paquete-y-desde-un-checkout-git-el-describe-y-la-ruta-del-checkout
title: sldb --version dice la versión del paquete y, desde un checkout git, el describe
  y la ruta del checkout que corre
five_wh_one_plus: what
tags:
- system:sldb
- topic:cli
provenance: src/sldb/store/package_version.py
---

# sldb --version dice la versión del paquete y, desde un checkout git, el describe y la ruta del checkout que corre

## Answer

sldb --version imprime 'sldb <versión> (<git describe --tags --always --dirty> at <directorio del pyproject>)' cuando el sldb que corre viene de un checkout con .git, y 'sldb <versión>' cuando viene de un paquete instalado. La versión sale de package_version(); el describe, de source_revision() en src/sldb/store/package_version.py (timeout de 2 s, None si git falla). La opción está en el parser raíz, src/sldb/cli/parsers/core.py; src/sldb/cli/parser.py solo lo reexporta.
