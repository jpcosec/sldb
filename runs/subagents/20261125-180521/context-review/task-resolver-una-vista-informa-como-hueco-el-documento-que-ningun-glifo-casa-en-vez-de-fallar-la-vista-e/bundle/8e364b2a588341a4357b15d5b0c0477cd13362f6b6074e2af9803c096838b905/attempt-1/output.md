## REFORMULACION

Propósito: que `resolve_view` deje de abortar cuando un documento del store no casa con ningún GlyphDoc, para poder medir qué parte de un store cubre una notación (UML, BPMN, IFML, ORCA). Resultado: la vista se resuelve con los documentos que casan y lista aparte los no casados con id y modelo; un modo estricto explícito conserva el fallo actual. Repo: `sldb`. Superficies: `sldb.api.notations` (`resolve_view`, `evaluate_projection_view`, `ViewError`), la ruta de `sldb serve` que los expone, y `docs/architecture/notations-and-views.md`. Límites: fuera cambiar el formato de `NotationDoc` y `graph_ui`; `sldb notations validate` no cambia.

## AMBIGUEDADES

1. "Los huecos van en un campo propio del resultado": no se define nombre, tipo ni forma (¿lista de objetos, mapa id→modelo?). Obliga a inventar el contrato de salida.
2. "un llamador que quiera el comportamiento estricto lo pide de forma explícita": no se nombra parámetro ni valor por defecto. Obliga a inventar la API pública y su compatibilidad.
3. "con su id y su modelo": "modelo" no se define (¿GlyphDoc, tipo de documento, modelo de dominio?). Obliga a inventar qué se serializa.
4. "la ruta de sldb serve que los expone": no se identifica endpoint ni cómo se propaga el nuevo campo. Obliga a inventar el contrato HTTP.
5. "Dentro: sldb.api.notations (resolve_view, evaluate_projection_view y ViewError)" frente a "sigue fallando con el mismo error que hoy": no queda claro si `ViewError` se modifica o solo se conserva. Obliga a inventar el alcance del cambio en el error.

## DRY-RUN

Lecturas: `docs/architecture/notations-and-views.md`, implementación de `resolve_view`/`evaluate_projection_view`/`ViewError`, ruta de `sldb serve`, tests de notación/vista existentes. Cambios previstos: añadir campo de huecos al resultado; flag estricto con default permisivo; recolectar documentos sin glifo en lugar de lanzar; propagar el campo en la ruta serve; nuevo test `tests/test_view_reports_unmatched_documents.py`; nota en docs. Dependencias: mecanismo de matching GlyphDoc↔documento, `ViewError`, pills/átomos ligados. Validaciones futuras: los dos `pytest` citados en Validación.

## FUTURO

Decisión humana: nombre y forma del campo de huecos, nombre/default del flag estricto, definición de "modelo" y alcance sobre `ViewError`. Otro nodo (Board/deskops) enruta pills y átomos; closeout produce el commit y retira la tarea del Board. La ruta serve concreta puede requerir confirmación de su dueño.
