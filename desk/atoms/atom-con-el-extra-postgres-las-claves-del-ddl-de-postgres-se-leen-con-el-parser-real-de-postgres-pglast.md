---
sldb:
  by: agent
  at: '2026-11-17T08:06:21Z'
  authority: generated
  via: create_document
id: atom-con-el-extra-postgres-las-claves-del-ddl-de-postgres-se-leen-con-el-parser-real-de-postgres-pglast
title: Con el extra postgres, las claves del DDL de Postgres se leen con el parser
  real de Postgres (pglast)
five_wh_one_plus: what
tags:
- system:sldb
- topic:code
provenance: tarea C4 de IR (nota 211648), decisión del supervisor 2026-11-17 de usar
  pglast; ejecutor deskops-e-67dedd6aa01e-a2, tester PASA en runs/subagents/20261116-test-k2-pg-c1
---

# Con el extra postgres, las claves del DDL de Postgres se leen con el parser real de Postgres (pglast)

## Answer

Con el extra postgres (pglast, libpg_query), sldb.code lee de cada CREATE TABLE y ALTER TABLE las claves PRIMARY KEY, FOREIGN KEY y UNIQUE (de columna y de tabla, con nombre o sin él) como hechos constraint con constraint_type, columns y references {table, columns}, con columns vacía para la PK de la tabla referenciada, y marca en cada columna type, primary_key, unique, identity y references. Los nombres salen tal como están escritos, sin comillas y con '' leído como '. Tablas, columnas, spans y anclas siguen viniendo de tree-sitter-sql; sin el extra se usa solo tree-sitter y una tabla con errores de parseo lleva keys_partial. Los offsets son exactos aunque el archivo no sea UTF-8 (surrogateescape). Límites: CHECK y EXCLUDE no son claves; un BOM queda avisado con keys_partial.
