---
sldb:
  by: agent
  at: '2026-11-16T21:25:37Z'
  authority: generated
  via: create_document
id: atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
title: sldb.code lee TS, TSX, JS y JSX con un mismo reader y ancla sus símbolos
five_wh_one_plus: what
tags:
- system:sldb
- topic:code
provenance: tarea B2 (IR08), ejecutor deskops-e-640c751d7c12, tester deskops-t-9d06b59a722f
  PASA
---

# sldb.code lee TS, TSX, JS y JSX con un mismo reader y ancla sus símbolos

## Answer

Con el extra code (tree-sitter-typescript), sldb.code escanea .ts con la gramática typescript y .tsx, .js y .jsx con la gramática tsx, en un mismo reader (lang_ts, ts_readers, ts_fingerprints). Publica hechos con la forma de los de Python: component (nombre en mayúscula con JSX en el cuerpo, incluidos memo y forwardRef), hook (use + mayúscula), type (type o interface, solo TS), function y module, con docstring JSDoc adyacente. Las anclas code:<ruta>.<ext>::<símbolo> pasan por intact, changed, lost y reconnected. Sin la gramática, el escaneo de .py sigue igual; find_files no recorre node_modules.
