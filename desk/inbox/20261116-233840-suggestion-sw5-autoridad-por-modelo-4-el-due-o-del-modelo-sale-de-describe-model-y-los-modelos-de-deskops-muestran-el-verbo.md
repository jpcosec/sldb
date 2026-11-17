---
sldb:
  by: agent
  at: '2026-11-17T03:09:49Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T23:38:40'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T00:09:03'
---

# SW5 · Autoridad por modelo (§4): el dueño del modelo sale de describe_model y los modelos de deskops muestran el verbo.

_Describe the incoming message with enough evidence to triage._

1. core/authority.ts:13-35 decide qué modelos son de deskops con un conjunto fijo de nombres (DESKOPS_MODELS) y prefijos de model_ref (:39-45). §4 dice que el dueño se deduce del módulo de origen que devuelve describe_model. ModelDescription ya trae model_ref como modulo:Clase (src/sldb/api/model_registry/model_description.py). Confirmar si con model_ref alcanza para modelos builtin de sldb, de deskops y del store local, incluidas las especializaciones de un desk; si no alcanza, pedir el dato a sldb por nota, no ampliar la lista.
2. "gestionado por deskops" y el verbo sugerido se calculan (authority.ts:112-124) pero no se dibujan: grep de "gestionado" y "suggestedVerb" en los .tsx no da nada. Un TaskDoc se ve como prosa de solo lectura sin decir por qué ni con qué verbo se cambia (§4: mostrar "gestionado por deskops" y el verbo, por ejemplo deskops edit task <id> <campo>).
3. Model Studio usa una regla aparte (canEditModelContract, authority.ts:49-70; workbench/ModelStudioView.tsx:140-143, :426-430): debe salir de la misma fuente que el punto 1.
Fuera de alcance: ejecutar el verbo (SW6).
done_when sugerido: tests de authority con model_ref reales del store del repo (TaskDoc, PillDoc, un modelo local y uno builtin de sldb) y un test de vista que encuentra el texto y el verbo en un campo de TaskDoc.
Toca ProsaWorkbenchView.tsx: en serie con SW2 y SW3.

Pedido del dueño (JP) del 2026-11-16 vía la sesión supervisora local: retomar la UI @sldb/surface (el Workbench de papel) y dejarla lista para un repaso de UI. Base: commit df3903db en origin/main de sldb (el rediseño del Workbench, que estaba sin commitear en el checkout local; check-layers, tsc y vitest 29 archivos / 396 tests en verde). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (secciones citadas como §n) y maquetas en docs/ui-workbench/screens/. Rutas relativas a surface/src salvo que se diga otra cosa. Serie SW1..SW9: las que tocan los mismos archivos van en serie. Validación mínima de toda tarea de la serie: en surface/, npm test (corre check-layers y vitest) y npx tsc -b --noEmit. La evidencia viene de una lectura estática del árbol; confirmar cada línea antes de escribir el TaskDoc.
