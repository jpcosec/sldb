---
sldb:
  by: agent
  at: '2026-11-17T03:11:15Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T23:39:31'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T00:10:38'
---

# SW7 · Flujo 4 (§6, §4 Studio): Model Studio edita campos existentes, crea modelos y confirma antes de promover.

_Describe the incoming message with enough evidence to triage._

1. La tabla de FieldDecl solo agrega y quita campos (:452-540); no edita el tipo ni la descripción de un campo existente. El selector de tipos es una lista fija (model-studio-logic.ts:9-18) que no cubre DocRef[SpecDoc] ni list[DocRef] como pide §6.
2. "+ Nuevo Modelo" está deshabilitado (:379-386) con un motivo que ya no vale: sldb serve expone POST /models/create (src/sldb/cli/serve/models_routes.py:60) y core/client.ts no tiene el método.
3. No se comprueba que cada campo tenga su slot en __template__ (§6 Flujo 4); los marcadores solo se muestran (:461-469). Esa comprobación es de sldb: usar lo que devuelve POST /models/validate o pedirla por nota, no parsear la plantilla en la UI (model-studio-logic.ts:31-78 ya parsea marcadores localmente: revisar si duplica a sldb).
4. Promover aplica al primer clic. El plan de backfill está en pantalla (:593-601) y el botón exige una validación limpia de la revisión vigente (model-studio-logic.ts:172-184), pero §4 pide mostrar siempre el plan antes de aplicar: paso de confirmación con el plan.
5. ⌘↵ no guarda la plantilla; solo el botón (§7).
done_when sugerido: tests de vista para editar un campo existente, crear un modelo, promover con confirmación y guardar con ⌘↵, contra el cliente inyectable; verificación en SW9 sobre un modelo del store local (los builtin de sldb y deskops siguen en solo lectura).
Independiente de SW2-SW6 en archivos; puede ir en paralelo.

Pedido del dueño (JP) del 2026-11-16 vía la sesión supervisora local: retomar la UI @sldb/surface (el Workbench de papel) y dejarla lista para un repaso de UI. Base: commit df3903db en origin/main de sldb (el rediseño del Workbench, que estaba sin commitear en el checkout local; check-layers, tsc y vitest 29 archivos / 396 tests en verde). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (secciones citadas como §n) y maquetas en docs/ui-workbench/screens/. Rutas relativas a surface/src salvo que se diga otra cosa. Serie SW1..SW9: las que tocan los mismos archivos van en serie. Validación mínima de toda tarea de la serie: en surface/, npm test (corre check-layers y vitest) y npx tsc -b --noEmit. La evidencia viene de una lectura estática del árbol; confirmar cada línea antes de escribir el TaskDoc.
