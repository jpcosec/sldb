---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T23:40:23'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# SW9 · Aceptación sobre el desk real (§2.4) y capturas para el repaso de UI con JP.

_Describe the incoming message with enough evidence to triage._

Qué se hace, en robocop2 y sin interfaz (playwright con chromium), con sldb serve sobre el store real del repo y surface en el puerto 5174:
1. Las cuatro vistas (#/workbench, #/diagram, #/source, #/studio) con las lentes lectura y fierros, cada una sobre documentos reales: tiempo de carga, tiempo de cada llamada /sldb y captura. La carga inicial pide /graph completo (app/WorkbenchShell.tsx:81-108): medirla sobre el store real.
2. Los cuatro flujos del manual §6 de punta a punta, escribiendo en una copia desechable del store en /dev/shm y nunca en el desk real: editar un campo, editar un bloque transcluido, abrir un diagrama y un nodo, anclar un átomo, validar y promover un borrador de modelo.
3. Los atajos de §7.
4. Los colores de papel de §1 contra src/styles/paper-tokens.css (#FAF9F6, #F4F3EF, #1A1A1A, #73726E), los hex escritos a mano en TopologyMindmap.tsx:281-296 y ModelStudioView.tsx:328-346, y que #/legacy sigue renderizando con el CSS separado.
5. El enlace desde la UI de deskops (UIs/graph_ui/frontends/desk) a #/workbench?doc=TaskDoc:<id>&lens=fierros con un id real: si el id no existe, el shell cae en silencio al primer documento (WorkbenchShell.tsx:154-158) y eso debe reportarse como falla.
Entregable: runs/ con un índice (matriz por vista y flujo: PASA o FALLA con severidad), tiempos y capturas con nombre por vista y lente, para que JP las recorra. Las fallas nuevas van como notas a este desk, no se arreglan en esta tarea.
Depende de SW1-SW7. Conviene además una primera pasada antes de SW2, solo las capturas y tiempos del punto 1 sobre df3903db, para que JP vea el estado de partida.

Pedido del dueño (JP) del 2026-11-16 vía la sesión supervisora local: retomar la UI @sldb/surface (el Workbench de papel) y dejarla lista para un repaso de UI. Base: commit df3903db en origin/main de sldb (el rediseño del Workbench, que estaba sin commitear en el checkout local; check-layers, tsc y vitest 29 archivos / 396 tests en verde). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (secciones citadas como §n) y maquetas en docs/ui-workbench/screens/. Rutas relativas a surface/src salvo que se diga otra cosa. Serie SW1..SW9: las que tocan los mismos archivos van en serie. Validación mínima de toda tarea de la serie: en surface/, npm test (corre check-layers y vitest) y npx tsc -b --noEmit. La evidencia viene de una lectura estática del árbol; confirmar cada línea antes de escribir el TaskDoc.
