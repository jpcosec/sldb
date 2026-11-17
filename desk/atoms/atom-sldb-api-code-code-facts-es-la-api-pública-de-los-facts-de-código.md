---
sldb:
  by: agent
  at: '2026-11-17T01:17:30Z'
  authority: generated
  via: create_document
id: atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código
title: sldb.api.code.code_facts es la API pública de los facts de código
five_wh_one_plus: what
tags:
- system:sldb
- topic:code
provenance: tarea C1 (nota IR 211648), ejecutor deskops-e-7f02ec7518c9, tester deskops-t-69a960ddb28e
  PASA
---

# sldb.api.code.code_facts es la API pública de los facts de código

## Answer

code_facts(root, paths=None) devuelve {facts, skipped}: los facts de .py, .ts, .tsx, .js, .jsx y .sql de las rutas dadas (archivos o directorios, relativas a root) o de todo el árbol, con los mismos ids que scan_tree. Cada fact trae path relativo, span {start_line, end_line} base 1 inclusivo y source_hash sha256 del archivo; si un reader no los da, lanza RuntimeError. skipped lista los archivos sin gramática disponible. Rutas inexistentes, absolutas o fuera de root dan ValueError antes de escanear. write_anchor se importa desde sldb.api.anchors. Es la frontera que consume specIR; no se usa sldb.code por dentro.
