## REFORMULACION
Propósito: que `resolve_view` deje de fallar entera cuando un documento no casa con ningún `GlyphDoc` de la notación y lo reporte como hueco. Resultado: la vista resuelve los documentos que sí casan y lista aparte los no casados con id y modelo; el modo estricto conserva el fallo actual; `sldb notations validate` no cambia. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: dentro, `sldb.api.notations` (`resolve_view`, `evaluate_projection_view`, `ViewError`) y la ruta de `sldb serve`; fuera, el formato de `NotationDoc` y `graph_ui`. Es una tarea ejecutable, no un agregado.

## AMBIGUEDADES
1. «Los huecos van en un campo propio del resultado»: no se define nombre, tipo ni serialización del campo; obligaría a inventar el contrato del resultado.
2. «un llamador que quiera el comportamiento estricto lo pide de forma explícita»: no se indica parámetro, valor por defecto, ni cómo se expone en `sldb serve`; obligaría a inventar la API.
3. «lista ese documento como hueco con id y modelo»: «modelo» no se precisa (modelo del documento, de la notación o detalle de error); obligaría a inventar el contenido.
4. «la ruta de sldb serve que los expone»: no se nombra archivo, endpoint ni forma de respuesta; obligaría a inventar la superficie HTTP.
5. «evaluate_projection_view y ViewError»: no se concreta si `ViewError` cambia, se conserva solo en estricto o mantiene mensaje; obligaría a inventar compatibilidad.

## DRY-RUN
Lecturas previstas: `docs/architecture/notations-and-views.md`, `sldb/api/notations`, ruta de `sldb serve`, tests de notación/vista. Cambios previstos: recoger documentos sin glifo en vez de abortar; añadir campo de huecos al resultado; parámetro explícito de modo estricto; serializar huecos en la ruta. Dependencias: `NotationDoc`, `GlyphDoc`, `ViewError` y fixtures de store. Validaciones futuras: `python -m pytest -q tests/test_view_reports_unmatched_documents.py` y `python -m pytest -q tests -k "notation or view"`, más comprobar que `sldb notations validate` no cambia. Sin ejecutar nada.

## FUTURO
Un humano debe aprobar el contrato del campo de huecos y el modo estricto. Otro nodo podría implementar la ruta `serve` o los tests. La aceptación final decide si el resultado cumple «Done When».
