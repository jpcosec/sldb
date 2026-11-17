---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T23:36:46'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# SW1 · Documentación y arranque de surface al día con el Workbench.

_Describe the incoming message with enough evidence to triage._

Puerto: la UI de deskops (UIs/graph_ui/frontends/desk/app.js, cambio sin commitear de JP) enlaza a http://127.0.0.1:5174/#/workbench?doc=TaskDoc:<id>&lens=fierros. workbench-router.ts ya entiende esa ruta, pero vite arranca en 5173 salvo que esté ocupado.
Resultado esperado: README de surface que describe lo que hay (cuatro vistas, lentes, #/legacy, proxies /sldb y /desk, contrato de capas, cómo levantarla contra un sldb serve real y contra el store demo de scripts/setup_workbench_demo_store.py); referencias a la maqueta corregidas o marcadas como históricas; docs/surface/tasks/README.md con el estado real de T7, T8 y T9; server.port fijo en 5174 con strictPort, documentado. Sin cambios de comportamiento fuera del puerto.
Sin dependencias. Puede ir primera.

Pedido del dueño (JP) del 2026-11-16 vía la sesión supervisora local: retomar la UI @sldb/surface (el Workbench de papel) y dejarla lista para un repaso de UI. Base: commit df3903db en origin/main de sldb (el rediseño del Workbench, que estaba sin commitear en el checkout local; check-layers, tsc y vitest 29 archivos / 396 tests en verde). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (secciones citadas como §n) y maquetas en docs/ui-workbench/screens/. Rutas relativas a surface/src salvo que se diga otra cosa. Serie SW1..SW9: las que tocan los mismos archivos van en serie. Validación mínima de toda tarea de la serie: en surface/, npm test (corre check-layers y vitest) y npx tsc -b --noEmit. La evidencia viene de una lectura estática del árbol; confirmar cada línea antes de escribir el TaskDoc.
