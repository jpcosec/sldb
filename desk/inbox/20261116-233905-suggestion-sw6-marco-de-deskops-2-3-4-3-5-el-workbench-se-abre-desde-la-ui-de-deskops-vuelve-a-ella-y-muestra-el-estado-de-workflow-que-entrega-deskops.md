---
sldb:
  by: agent
  at: '2026-11-17T03:10:32Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T23:39:05'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T00:09:58'
---

# SW6 · Marco de deskops (§2, §3.4, §3.5): el Workbench se abre desde la UI de deskops, vuelve a ella y muestra el estado de workflow que entrega deskops.

_Describe the incoming message with enough evidence to triage._

Lo que pide el manual:
1. §2.1-2.2: entrada desde el Board y la vista task, y vuelta al cascarón. Falta el enlace de regreso a la UI de deskops (a la tarea cuando el documento abierto es un TaskDoc).
2. §2.3: lo que una ficha muestra de una tarea (por ejemplo "2/2 gates ok" en el Inspector) sale de deskops view, nunca se recalcula leyendo el store. Hoy no se muestra nada.
3. §3.4: ⌘K lista los verbos de deskops con su nombre de CLI y argumentos; deskops next decide cuáles aplican; el que no aplica sale deshabilitado con el motivo.
4. §3.5: cabecera con "N cambios sin commitear" y el commit como operación aparte.
Operaciones que faltan, a pedir por nota al repo dueño y no a emular en la UI (§3.6): no hay endpoint que entregue deskops next, ni que ejecute verbos aparte de advance y del ack/promote del inbox, ni que cuente los cambios sin commitear o haga el commit (ni sldb serve ni el servidor del desk tienen nada de git).
Sugerencia de corte: (a) solo lectura con lo que ya existe: enlace de regreso y gates/evidencia de la tarea desde /desk/api/view/task; (b) notas a deskops y graph_ui por las operaciones que faltan, y los controles correspondientes deshabilitados con el motivo; (c) la paleta de verbos cuando existan las operaciones. No dibujar nada sin fuente real.
Depende de SW5 (qué documentos son de deskops). Cruza repos: el contrato es de deskops (deskops/docs/deskops-ui.md) y el servidor es de graph_ui.

Pedido del dueño (JP) del 2026-11-16 vía la sesión supervisora local: retomar la UI @sldb/surface (el Workbench de papel) y dejarla lista para un repaso de UI. Base: commit df3903db en origin/main de sldb (el rediseño del Workbench, que estaba sin commitear en el checkout local; check-layers, tsc y vitest 29 archivos / 396 tests en verde). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (secciones citadas como §n) y maquetas en docs/ui-workbench/screens/. Rutas relativas a surface/src salvo que se diga otra cosa. Serie SW1..SW9: las que tocan los mismos archivos van en serie. Validación mínima de toda tarea de la serie: en surface/, npm test (corre check-layers y vitest) y npx tsc -b --noEmit. La evidencia viene de una lectura estática del árbol; confirmar cada línea antes de escribir el TaskDoc.
