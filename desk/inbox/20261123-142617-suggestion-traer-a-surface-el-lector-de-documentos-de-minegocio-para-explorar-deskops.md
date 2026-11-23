---
sldb:
  by: agent
  at: '2026-11-23T17:39:13Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-23T14:26:17'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T14:38:50'
# why the note was acknowledged; empty when no reason was given
ack_reason: convertida en task-surface-trae-el-lector-de-documentos-de-minegocio-indice-por-carpeta-o-semantica-lectura-ficha-refer
  (prioridad 3 de JP; agrupado por semantica espera la tarea de tags de deskops)
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Traer a surface el lector de documentos de minegocio para explorar deskops

_Describe the incoming message with enough evidence to triage._

JP (2026-11-23) pide traer a sldb/surface el lector de documentos que quedó en la copia de surface de su proyecto minegocio (WebProjects/minegocio/superficie, commit ab8fac2; copia partió de sldb 562847e2 y surface no cambió en main desde entonces). Uso que le interesa: explorar el store de deskops. Fuente copiada en robocop2: /mnt/ssd/proyectos/SLDB_1/reports/lector-minegocio-20261123/superficie (sin node_modules, dist ni dev/). Diferencias contra sldb/surface: nuevos src/core/{doc-ref,wiki-index,rechazo,imagenes}.ts con sus tests y fixture rechazos-sldb.json, src/workbench/{WikiIndex,WikiLectura.test,Ficha,NuevaPagina,AvisoGuardado}.tsx; modificados WorkbenchShell, workbench.test, core/client.ts, core/layout.ts, main.tsx, react/{context,DocumentSurface,useDocumentEditor}, paper-tokens.css, ComposerView, ProsaWorkbenchView (+test), vite.config.ts. Ojo: esa copia se adaptó a la wiki de un negocio; hay que traer lo genérico (índice por carpeta o semántica, lectura, ficha, referencias entre documentos, rechazos legibles) y dejar fuera lo específico del negocio. Validación: tsc, vitest y check-layers de surface, y probarlo contra sldb serve sobre el store real de deskops midiendo tiempos de cada pantalla. Depende de que deskops ordene sus tags semánticos (nota de hoy en el desk de deskops): el índice del lector agrupa por semántica.
