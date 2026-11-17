---
sldb:
  by: agent
  at: '2026-11-17T11:10:06Z'
  authority: generated
  via: create_document
id: atom-el-spec-de-componentes-desde-python-lee-solo-archivos-py-aunque-el-árbol-tenga-otros-lenguajes
title: El spec de componentes desde Python lee solo archivos .py aunque el árbol tenga
  otros lenguajes
five_wh_one_plus: what
tags:
- system:sldb
- topic:notations
provenance: tarea de la regresión de B2 (nota de IR 213452); ejecutor deskops-e-55d271007190,
  tester PASA en runs/subagents/20261116-test-b2reg
---

# El spec de componentes desde Python lee solo archivos .py aunque el árbol tenga otros lenguajes

## Answer

component_spec_from_python arma el spec de componentes solo con los .py del árbol (find_files filtrado a Python, con un mismo Ids y su segunda pasada), así que los .js, .ts o .sql que sldb.code también sabe leer no producen hallazgos en ese spec. scan_tree no cambia para los demás consumidores (code_facts y anclas). El spec de src/sldb es idéntico al de antes de B2.
