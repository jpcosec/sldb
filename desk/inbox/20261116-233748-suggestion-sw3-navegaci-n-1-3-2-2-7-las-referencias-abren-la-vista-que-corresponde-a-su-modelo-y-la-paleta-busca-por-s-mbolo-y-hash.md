---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T23:37:48'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# SW3 · Navegación (§1.3, §2.2, §7): las referencias abren la vista que corresponde a su modelo y la paleta busca por símbolo y hash.

_Describe the incoming message with enough evidence to triage._

1. Las fichas de referencia de parseDocRef (workbench/ProsaWorkbenchView.tsx:553-563) llaman siempre a onSelectDoc y abren prosa, aunque apunten a un SpecDoc o a una fuente. §2.2: un ref a un diagrama abre el Inspector y un ref a una fuente abre Extracción y Anclaje. Los bloques de diagrama y el árbol ya rutean bien (TopologyMindmap.tsx:238, :303; ProsaWorkbenchView.tsx:856, :893): falta el mismo criterio en las fichas y en los refs del Inspector (Spec2VizInspectorView.tsx:295, :346).
2. Clic en un nodo del árbol reemplaza el documento (TopologyMindmap.tsx:237-245). §1.3 pide que enfoque el documento o la sección en la prosa: cuando el nodo es una pieza del documento abierto, se enfoca su bloque en vez de navegar.
3. La paleta ⌘K (app/WorkbenchShell.tsx:170-185, :454-568) busca por id, título y modelo. §7 pide además símbolo y hash.
4. La tecla 3 y la pestaña Esquema necesitan un modelo activo (WorkbenchShell.tsx:139-142, :161-164) y no tienen salida si no lo hay: definir el caso (deshabilitada con el motivo).
5. El modo legacy se decide una sola vez al cargar (main.tsx:15-16): cambiar el hash a o desde #/legacy no cambia la app hasta recargar.
Regla: qué vista corresponde a un modelo se decide con lo que sldb ya entrega (familia o bases de describe_model), no con una lista de nombres en la UI; si falta el dato, nota a sldb en vez de una tabla local.
done_when sugerido: tests de ruteo por tipo de destino, de foco de sección y de búsqueda por símbolo y hash.
Toca ProsaWorkbenchView.tsx, TopologyMindmap.tsx, Spec2VizInspectorView.tsx y WorkbenchShell.tsx: en serie con SW2.

Pedido del dueño (JP) del 2026-11-16 vía la sesión supervisora local: retomar la UI @sldb/surface (el Workbench de papel) y dejarla lista para un repaso de UI. Base: commit df3903db en origin/main de sldb (el rediseño del Workbench, que estaba sin commitear en el checkout local; check-layers, tsc y vitest 29 archivos / 396 tests en verde). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (secciones citadas como §n) y maquetas en docs/ui-workbench/screens/. Rutas relativas a surface/src salvo que se diga otra cosa. Serie SW1..SW9: las que tocan los mismos archivos van en serie. Validación mínima de toda tarea de la serie: en surface/, npm test (corre check-layers y vitest) y npx tsc -b --noEmit. La evidencia viene de una lectura estática del árbol; confirmar cada línea antes de escribir el TaskDoc.
