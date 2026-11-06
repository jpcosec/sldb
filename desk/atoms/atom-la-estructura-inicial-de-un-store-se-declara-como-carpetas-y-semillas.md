---
id: atom-la-estructura-inicial-de-un-store-se-declara-como-carpetas-y-semillas
title: La estructura inicial de un store se declara como carpetas y semillas
five_wh_one_plus: what
tags:
- system:sldb
- topic:store-declaration
- topic:scaffold
provenance: docs/architecture/store-declaration.md
---

# La estructura inicial de un store se declara como carpetas y semillas

## Answer

La estructura inicial de un store (carpetas y archivos semilla) se declara como datos en StoreDeclaration, con folders y seeds, y no se escribe a mano en el código del consumidor. Una semilla es text, un file relativo a template_root, un pkg:modulo/ruta resuelto con importlib.resources o un document {model, name, payload} que se renderiza con el modelo y se puede trackear. mode if_missing nunca sobrescribe; managed reescribe lo que difiere. sldb.api.scaffold_store(store, declaration=None, apply=False, template_root=None) es idempotente: sin apply informa created, rewritten, present y conflicts, y con apply escribe todo dentro de una transacción (GD24). Un conflicto (la ruta es un archivo donde va una carpeta, o al revés, incluso en un ancestro) no escribe nada. sldb.api.build_store agrega el scaffold al build, y la CLI es sldb stores scaffold [--apply] y la sección scaffold de stores build. Una semilla trackeada se declara en include como todo tracking, así que un consumidor que no quiere cambiar su store.yaml declara antes un include glob que la cubra. Implementado en GD26 (plan generalizar-desde-deskops).
