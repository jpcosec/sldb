---
id: atom-una-vista-de-todo-el-store-no-puede-depender-de-que-importen-todos-sus-modelos
title: Una vista de todo el store no puede depender de que importen todos sus modelos
five_wh_one_plus: why
tags:
- system:sldb
---

# Una vista de todo el store no puede depender de que importen todos sus modelos

## Answer

Un store registra modelos de varios paquetes (deskops, pron, el propio repo) y no todos están instalados en cada entorno. Una vista que recorre todos los modelos (el AST del store en src/sldb/api/records/build_ast.py) tiene que registrar el que no importa como no resuelto, con su error, y seguir: si aborta, cualquier consulta de otro modelo cae con él.
