---
id: atom-un-censo-de-importadores-por-substring-miente-hay-que-contarlo-sobre-el-ast
title: 'Un censo de importadores por substring miente: hay que contarlo sobre el AST'
five_wh_one_plus: how_not
tags:
- system:sldb
- topic:dead-code
- topic:refactoring
- topic:diagnostics
- layer:cli
provenance: docs/architecture/superseded-code-audit.md
---

# Un censo de importadores por substring miente: hay que contarlo sobre el AST

## Answer

Antes de borrar un modulo por 'no tiene importadores', el censo tiene que contar nodos ast.Import/ast.ImportFrom, no lineas de grep. Un grep del nombre del modulo produce falsos positivos por prefijo que invierten la conclusion: contar 'cli.graph' matcheo 20 veces 'cli.graph_ops' (el arbol VIVO que gano el refactor) y contar 'model_source' matcheo 15 veces 'api.model_drafts.model_source' (el modulo destino al que los consumidores YA migraron). En los dos casos el grep decia 'esto tiene decenas de importadores, no lo borres' mientras el censo AST daba exact=0, submodules=0. El patron es estructural, no accidental: cuando un refactor deja un modulo viejo y uno nuevo, el nombre del nuevo suele CONTENER al del viejo, asi que el grep del muerto siempre encuentra al vivo. Corolario: el falso positivo empuja al lado seguro-aparente (no borrar), por eso no se detecta solo y el codigo muerto sobrevive refactors enteros.
