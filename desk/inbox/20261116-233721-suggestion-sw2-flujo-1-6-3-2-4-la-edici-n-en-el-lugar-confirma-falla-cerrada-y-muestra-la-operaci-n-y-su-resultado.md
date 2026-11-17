---
sldb:
  by: agent
  at: '2026-11-17T03:07:12Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T23:37:21'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T00:06:33'
---

# SW2 · Flujo 1 (§6, §3.2, §4): la edición en el lugar confirma, falla cerrada y muestra la operación y su resultado.

_Describe the incoming message with enough evidence to triage._

1. Enter no confirma. InlineEditableProse (workbench/ProsaWorkbenchView.tsx:1022-1064) usa textarea para todo campo; Enter inserta salto de línea y solo Ctrl/⌘+↵ o el blur guardan. §6 Flujo 1 pide "Enter o ⌘↵": Enter debe confirmar en campos de una línea y ⌘↵ en los de bloque.
2. La autoridad falla abierta en el documento principal: ProsaWorkbenchView.tsx:107 hace modelDetail?.authority ?? "authored", así que mientras describe_model carga o si falla todo queda editable. El servidor usa "generated" por defecto (src/sldb/api/model_registry/model_description.py:28) y el camino de transclusiones ya falla cerrado (:648-656). Deben coincidir: sin autoridad conocida, solo lectura.
3. La etiqueta de operación de la lente Fierros (POST /save · expected <hash>) aparece solo en campos y líneas (:339, :419, :512). Falta en el título (:198-202) y en la edición de un bloque transcluido (:683-731).
4. Tras guardar solo se ve "✓ sincronizado" (:216-217). §3.2 pide el resultado de la operación: hash nuevo, o el error accionable.
5. El hash que muestra la etiqueta queda viejo: documents se carga una vez (app/WorkbenchShell.tsx:81-108) y no se refresca tras un guardado de prosa, así que la etiqueta puede no coincidir con el expected que se envía (react/useDocumentEditor.ts:64-82).
Fuera de alcance: verbos de deskops y "gestionado por deskops" (SW5, SW6).
done_when sugerido: tests de vitest que prueban cada uno de los cinco puntos contra el cliente inyectable (sin mocks de módulo, como exige check-layers), más la verificación manual del Flujo 1 sobre un store real en SW9.
Toca ProsaWorkbenchView.tsx y WorkbenchShell.tsx: en serie con SW3 y SW5.

Pedido del dueño (JP) del 2026-11-16 vía la sesión supervisora local: retomar la UI @sldb/surface (el Workbench de papel) y dejarla lista para un repaso de UI. Base: commit df3903db en origin/main de sldb (el rediseño del Workbench, que estaba sin commitear en el checkout local; check-layers, tsc y vitest 29 archivos / 396 tests en verde). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (secciones citadas como §n) y maquetas en docs/ui-workbench/screens/. Rutas relativas a surface/src salvo que se diga otra cosa. Serie SW1..SW9: las que tocan los mismos archivos van en serie. Validación mínima de toda tarea de la serie: en surface/, npm test (corre check-layers y vitest) y npx tsc -b --noEmit. La evidencia viene de una lectura estática del árbol; confirmar cada línea antes de escribir el TaskDoc.
