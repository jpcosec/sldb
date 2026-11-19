---
sldb:
  by: agent
  at: '2026-11-19T06:26:13Z'
  authority: generated
  via: create_document
id: atom-docs-list-marca-con-su-causa-los-documentos-que-docs-show-no-puede-resolver
title: docs list marca con su causa los documentos que docs show no puede resolver
five_wh_one_plus: how
tags:
- system:sldb
- topic:cli
---

# docs list marca con su causa los documentos que docs show no puede resolver

## Answer

docs list y docs show no leen la misma fuente: list recorre las entradas declaradas e indexadas del store, y show resuelve por los documentos cargados en tiempo de ejecución, que solo existen si el modelo se importa. Por eso docs list marca en cada entrada que show no puede resolver 'unresolvable' con la causa (src/sldb/api/stores/unresolvable_documents.py): file-missing, store/symlink-not-read, store/path-outside-root o model-not-importable. Esta última es cuando el model_ref no se importa con el mismo pythonpath que usa show (caso real: deskops.models:EdgeDoc en el store de sldb-ui). Con el modelo importable, la entrada no lleva marca y show la encuentra.
