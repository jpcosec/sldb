---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T23:38:13'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# SW4 · Flujo 3 (§6, §4): anclar de verdad. Hoy "Crear AtomDoc y Anclar" no guarda un anclaje y el estado del anclaje se calcula en la UI.

_Describe the incoming message with enough evidence to triage._

1. workbench/SourceAnchoringView.tsx:442-450 crea el átomo con un POST /docs cuyo payload lleva quote, text, body, source y title, pero no los offsets. No queda anclaje guardado: la rama aparece después solo si indexOf(quote) encuentra la cita en la fuente (:241-273). Una cita repetida o editada pierde su anclaje.
2. El estado del anclaje, incluido "changed", se recalcula en la UI con indexOf y slice (:241-273), la cobertura se arma en workbench/anchoring-coverage.ts:16-36 y la pertenencia átomo-fuente con heurísticas sobre llaves del payload (:146-162). sldb ya tiene esto: write_anchor en src/sldb/api/anchors/anchor_docs.py:50 y anchor_state en src/sldb/store/edge_index/doc_anchor_states.py:44. sldb serve no tiene ninguna ruta de anclaje (grep de "anchor" en src/sldb/cli/serve/ solo da comentarios). Los consumidores no reimplementan sldb.
3. Duplicados: el umbral de duplicado es 0.85 (core/similarity.ts:8) y §6 dice 75 %; los parecidos salen como texto (:689-694) y §6 pide el enlace al átomo existente; el mensaje "✓ Nuevo en el store (máx. similitud NN%)" sale sin porcentaje (:478).
4. §4: editar un átomo anclado deja el anclaje en changed y la UI lo muestra como alerta ruidosa en la ficha, en la lente Fierros y en el panel de cobertura de la vista 03. Hoy es una ficha neutra "cita alterada" (:555-557) solo en la vista 03, y editar el cuerpo de un átomo transcluido desde un informe (ProsaWorkbenchView.tsx:731) no muestra nada.
Son dos tareas en orden: (a) sldb serve expone la escritura de un anclaje y la lectura del estado de anclaje y la cobertura por fuente, sobre la API pública que ya existe; (b) surface las usa, borra el cálculo local, corrige umbral, enlace y porcentaje, y muestra changed como alerta en los tres lugares. changed es una alerta, no un error, y no bloquea.
done_when sugerido: tras crear un átomo desde una selección, sldb reporta el anclaje con sus offsets; al editar la fuente o el átomo, la UI muestra changed leyendo el estado de sldb, sin indexOf en surface.

Pedido del dueño (JP) del 2026-11-16 vía la sesión supervisora local: retomar la UI @sldb/surface (el Workbench de papel) y dejarla lista para un repaso de UI. Base: commit df3903db en origin/main de sldb (el rediseño del Workbench, que estaba sin commitear en el checkout local; check-layers, tsc y vitest 29 archivos / 396 tests en verde). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (secciones citadas como §n) y maquetas en docs/ui-workbench/screens/. Rutas relativas a surface/src salvo que se diga otra cosa. Serie SW1..SW9: las que tocan los mismos archivos van en serie. Validación mínima de toda tarea de la serie: en surface/, npm test (corre check-layers y vitest) y npx tsc -b --noEmit. La evidencia viene de una lectura estática del árbol; confirmar cada línea antes de escribir el TaskDoc.
