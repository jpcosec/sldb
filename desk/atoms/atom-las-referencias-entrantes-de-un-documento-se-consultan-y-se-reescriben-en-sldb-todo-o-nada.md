---
id: atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada
title: Las referencias entrantes de un documento se consultan y se reescriben en sldb,
  todo o nada
five_wh_one_plus: what
tags:
- system:sldb
- topic:references
provenance: docs/architecture/references.md
---

# Las referencias entrantes de un documento se consultan y se reescriben en sldb, todo o nada

## Answer

sldb responde quién apunta a un documento: sldb.api.referrers(store, target) devuelve cada Referrer con source, field, index y location, y origin schema (campos de referencia del índice de aristas) o mention (menciones del grafo de proyecto de GD21). target acepta export_id, Model:name, ruta trackeada o id de nodo del grafo. sldb.api.rewrite_references(store, target, replacement | None) reemplaza o quita esas referencias conservando la forma del valor original, sin dejar huecos ni duplicados en las listas y sin borrar prosa (una mención sin reemplazo se informa en skipped), dentro de una transacción de GD24: todo o nada. Un campo __doc_anchors__ se reescribe a doc:Model:name sin hash para que sldb lo vuelva a anclar al guardar. CLI: sldb edges referrers y sldb edges rewrite --to|--remove [--dry-run]; serve: GET /edges/referrers y POST /edges/rewrite. Implementado en GD22 (plan generalizar-desde-deskops).
