---
sldb:
  by: agent
  at: '2026-11-17T03:11:51Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T23:39:57'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T00:11:22'
---

# SW8 · Decisión de JP (task.decision): qué queda de la superficie anterior de surface y de sus stores demo.

_Describe the incoming message with enough evidence to triage._

Lo que hay que decidir:
A. Vistas legacy: retirarlas, o declarar cuáles sobreviven dentro del Workbench. Salud y Bandeja no tienen equivalente en las cuatro vistas nuevas; Lector y Destilación quedaron cubiertas en parte por Extracción y Anclaje y por Model Studio.
B. Stores demo y código del caso Levira en core/: conservar como fixture de desarrollo (hay una tarea en draft que los toca: task-surface-dev-prosa-generada-con-marca-y-hash-de-sus-átomos-de-origen-...) o retirar con la maqueta.
C. T8, identidad de sección: sigue como tarea de sldb, o se descarta.
Hasta que JP decida no se borra nada. La decisión se escribe y de ella salen las tareas de retiro.

Pedido del dueño (JP) del 2026-11-16 vía la sesión supervisora local: retomar la UI @sldb/surface (el Workbench de papel) y dejarla lista para un repaso de UI. Base: commit df3903db en origin/main de sldb (el rediseño del Workbench, que estaba sin commitear en el checkout local; check-layers, tsc y vitest 29 archivos / 396 tests en verde). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (secciones citadas como §n) y maquetas en docs/ui-workbench/screens/. Rutas relativas a surface/src salvo que se diga otra cosa. Serie SW1..SW9: las que tocan los mismos archivos van en serie. Validación mínima de toda tarea de la serie: en surface/, npm test (corre check-layers y vitest) y npx tsc -b --noEmit. La evidencia viene de una lectura estática del árbol; confirmar cada línea antes de escribir el TaskDoc.
