## REFORMULACION
Nodo ejecutable, no agregado. Propósito: hacer tolerante la carga masiva pública de documentos y estructurar los problemas de `EdgeIndex`, tras un fallo total causado por un único Markdown inválido. Resultado: `load_runtime_documents(..., on_invalid="skip")` devuelve `RuntimeDocuments(documents, invalid)` con `InvalidDocument(path, model, error)`; `on_invalid="raise"` conserva la lista y relanza como `SLDBValidationError` con la ruta; `EdgeIndex.problem_details` añade `EdgeProblem(kind, document, detail)` manteniendo `problems`. Repo: `sldb`, cwd actual. Límites: no cambiar `resolve_runtime_doc` —solo medirlo y anotarlo—, no quitar `problems`, no tocar `graph_ui`; números de línea orientativos; el commit y push corresponden al coordinador, no al ejecutor.

## AMBIGUEDADES
1. «hay que recoger en `_load_accepted` (src/sldb/store/query.py)» frente a `files`, que no incluye `src/sldb/store/query.py`. Obliga a inventar si editar `query.py` está autorizado pese a no figurar en los archivos del encargo.
2. «más la lista de rechazados, que hay que recoger en `_load_accepted`» no define cómo devolverla ni cómo afecta a sus llamadores. Obliga a inventar la firma y el contrato de `_load_accepted`.
3. «la excepción que hoy sale se relanza como `SLDBValidationError`» no aclara si se envuelve cualquier excepción, incluida una `SLDBValidationError` previa. Obliga a inventar la política de envoltura.

## DRY-RUN
Lecturas: TaskDoc, rituales, átomo, `runtime_documents.py`, `query.py`, `edge_index.py`, tests nombrados y `CHANGELOG.md`. Cambios previstos: parámetro `on_invalid`, dataclasses y exportación, recogida de rechazados, relanzamiento con ruta, `EdgeProblem`/`problem_details`, tests de ambos comportamientos y entrada de changelog. Dependencias: `accepted_only` existente, `SLDBValidationError`, fixtures de tests, puntos actuales de `problems.append`. Validaciones futuras: los tres `pytest` indicados y `stores build --check`; informe con medición en frío de `resolve_runtime_doc`.

## FUTURO
El coordinador ejecuta `deskops closeout commit`, decide el aviso al repo y valida el informe. Un humano decide si la medición exige otra tarea para `resolve_runtime_doc`.
