---
sldb:
  by: agent
  at: '2026-11-16T10:14:16Z'
  authority: generated
  via: create_document
id: atom-una-reconstrucción-de-secciones-con-documentos-trackeados-ausentes-avisa-una-vez-por-modelo-con-el-n
title: Una reconstrucción de secciones con documentos trackeados ausentes avisa una
  vez por modelo, con el número y hasta tres ejemplos
five_wh_one_plus: what
tags:
- system:sldb
- topic:store
provenance: src/sldb/store/section_sync.py
---

# Una reconstrucción de secciones con documentos trackeados ausentes avisa una vez por modelo, con el número y hasta tres ejemplos

## Answer

src/sldb/store/section_sync.py acumula en RebuildReport.missing_paths (src/sldb/store/semantic.py) las rutas de los documentos trackeados que no están en disco, por ejemplo los PythonSymbolDoc generados en un checkout limpio. process_model_sections emite un solo logger.warning por modelo con el formato 'Sections rebuild: <n> documents missing on disk (<Modelo>: <n>); e.g. <r1>, <r2>, <r3>' (missing_summary), en lugar de una línea por documento. report.verbose sigue con una entrada por ausente.
