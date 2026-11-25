## REFORMULACION

El nodo debe hacer tolerante la carga pública de documentos runtime en SLDB_1: `load_runtime_documents` acepta `on_invalid: Literal["raise","skip"]="raise"`; en `skip` devuelve `RuntimeDocuments(documents, invalid)` sin lanzar y nombrando los inválidos; en `raise` conserva el retorno actual y el error incluye la ruta. Además, `EdgeIndex` gana `problem_details: list[EdgeProblem]` junto a `problems`, sin alterar este último. Entran tests en `tests/api/test_api_documents.py` y `tests/api/test_api_edges.py`, y una línea en `CHANGELOG.md`. Límites: no cambia `resolve_runtime_doc` —solo se mide y se anota—, no elimina `problems`, no toca `graph_ui`, no hace push; el commit lo hace el coordinador.

## AMBIGUEDADES

1. “hay que recoger en `_load_accepted`”: no define cómo se exponen los rechazados ni si cambia su firma; obliga a inventar el contrato interno.
2. “se relanza como `SLDBValidationError`”: no indica módulo de importación ni si conserva causa/cadena; obliga a inventar ubicación y semántica.
3. “poblado donde hoy se agregan strings a `problems`”: no enumera los puntos; si hay variantes no descritas, obliga a inventar `kind`.
4. “tiempo de `resolve_runtime_doc`… en frío”: no define método, repeticiones ni unidad; obliga a inventar el protocolo de medición.
5. “qué cambió y el commit”: el ejecutor no commitea y no conoce el hash al avisar; obliga a inventar un placeholder o diferir el aviso.
6. “stores build --check” aparece en Implementation Path, pero no en Validation ni Done When; obliga a decidir si es requisito de cierre.
7. “`problem_details`… junto a `problems`”: no fija valor por defecto ni inicialización; obliga a inventar el default.

## DRY-RUN

Lecturas: los cuatro archivos listados, `src/sldb/store/query.py:75-88`, grep de `problems.append|problems=`, tests citados y `CHANGELOG.md`; verificar exportaciones públicas. Cambios previstos: parámetro y dataclasses; recogida de rechazados; relanzamiento con ruta; `EdgeProblem` y poblado de `problem_details`; tests; changelog. Dependencias: `accepted_only`, contrato de rechazados, `SLDBValidationError`, pydantic y fixtures/helpers existentes. Validaciones futuras: los tres `pytest` indicados; `stores build --check` si se confirma; commit/closeout por el coordinador y aviso al repo. Sin ejecutar nada.

## FUTURO

El coordinador ejecuta `deskops closeout commit`, decide si `stores build --check` es obligatorio y resuelve el aviso al repo. Otro nodo o un humano valida el informe y decide si la medición de `resolve_runtime_doc` justifica una tarea aparte.
