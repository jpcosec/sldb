---
sldb:
  by: agent
  at: '2026-11-16T09:21:57Z'
  authority: generated
  via: create_document
id: atom-los-imports-anidados-de-un-módulo-python-son-un-hecho-aparte-de-los-de-nivel-superior-y-el-spec-de-c
title: Los imports anidados de un módulo Python son un hecho aparte de los de nivel
  superior y el spec de componentes dibuja los dos
five_wh_one_plus: what
tags:
- system:sldb
- topic:code-facts
provenance: src/sldb/code/imports.py
---

# Los imports anidados de un módulo Python son un hecho aparte de los de nivel superior y el spec de componentes dibuja los dos

## Answer

sldb.code.scan_tree guarda en attrs.imports solo las sentencias import del nivel superior del módulo (las que alimentan relations) y en attrs.nested_imports las que están dentro de def, class, if (incluido TYPE_CHECKING), try o with. component_spec_from_python dibuja una arista imports por par (módulo fuente, módulo destino) con las dos listas, deduplicada después de resolver los relativos; un from-import apunta al módulo del que se importa, no al nombre importado.
