---
sldb:
  by: agent
  at: '2026-11-16T23:09:17Z'
  authority: generated
  via: create_document
id: atom-sldb-code-lee-ddl-de-postgres-y-migraciones-de-sqlmigrate-como-hechos-de-tablas-columnas-vistas-e-ín
title: sldb.code lee DDL de Postgres y migraciones de sqlmigrate como hechos de tablas,
  columnas, vistas e índices
five_wh_one_plus: what
tags:
- system:sldb
- topic:code
provenance: tarea B2-SQL (IR09), corrección 1; ejecutor deskops-e-90f36a61abe4, tester
  deskops-t-ad9f049e2cf8 PASA
---

# sldb.code lee DDL de Postgres y migraciones de sqlmigrate como hechos de tablas, columnas, vistas e índices

## Answer

Con el extra code (tree-sitter-sql), sldb.code escanea .sql y publica hechos module (el archivo), table, column (<tabla>.<columna>), view (CREATE VIEW y CREATE MATERIALIZED VIEW) e index, también dentro de BEGIN; ... COMMIT;. Los nombres entre comillas dobles se leen sin comillas y el esquema se conserva si viene escrito (public.users). La lectura es tolerante: si el nombre se lee, la sentencia da su hecho y las columnas sin error; solo se omite la columna o constraint que la gramática no reconoce (IDENTITY, CONSTRAINT nombre UNIQUE). Repetidos llevan sufijo ~N. Las anclas code:<ruta>.sql::<nombre> pasan por intact, changed, lost y reconnected; un archivo con errores locales marca parse_errors, no has_error.
