Nodo ejecutable (`task.code`), no agregado.

**REFORMULACION**

Propósito: que `load_runtime_documents` de la API pública tolere un store con documentos inválidos y nombre los rechazados, y que `EdgeIndex` exponga los problemas estructurados. Resultado: parámetro `on_invalid: Literal["raise","skip"]="raise"` (con `RuntimeDocuments`/`InvalidDocument` y `SLDBValidationError` con la ruta en modo raise), `EdgeProblem` + `problem_details` junto a `problems` intacto, tests en `tests/api/test_api_documents.py` y `tests/api/test_api_edges.py`, y una línea en `CHANGELOG.md` bajo "## 0.1.13 — not released yet". Repo: sldb. Límites: no entra `resolve_runtime_doc` focalizado (solo se mide su tiempo), no se quita `problems`, no se toca graph_ui.

**AMBIGUEDADES**

1. "el comportamiento por defecto (on_invalid=\"raise\") no cambia salvo que el mensaje nombra la ruta" frente a "En modo raise, la excepción que hoy sale se relanza como SLDBValidationError"; obliga a inventar si el tipo de excepción cambia o solo el texto.
2. "kind es \"endpoint-not-a-node\" para los problemas que hoy se agregan como strings (son todos de ese tipo según la descripción del campo problems)"; obliga a inventar `kind` si el grep revela otros orígenes.
3. "path: str relativo al proyecto" frente al pill "(ruta, modelo, mensaje)" sin base declarada; obliga a inventar si es relativo a la raíz del proyecto o al store.
4. "se mide en esta tarea y se anota el tiempo... en frío"; obliga a inventar qué cuenta como frío (primer import, proceso nuevo) y no hay umbral ni formato.
5. "5) stores build --check" frente al pill "stores build --check no es requisito de cierre"; obliga a inventar si es obligatorio.

**DRY-RUN**

Lecturas: `runtime_documents.py`, `query.py:75-88`, `edge_index.py`, grep `problems.append\|problems=` en `edge_index`, ambos tests, `CHANGELOG.md`, `sldb/api/__init__.py` (export). Cambios previstos: `query._load_accepted` con lista `rejected` opcional; envoltorio público con `on_invalid`, dataclasses y `SLDBValidationError` con `raise ... from exc`; `EdgeProblem` y `problem_details` en cada punto que hoy agrega string; tests; CHANGELOG. Dependencias: pydantic, `sldb.core.exceptions`. Validaciones futuras: los tres `pytest` de la sección, `stores build --check` (ver ambigüedad 5), y dejar en `result-summary.md` la medición de `resolve_runtime_doc`.

**FUTURO**

El coordinador hace `deskops closeout commit` y el aviso `deskops message send` (o su línea en el informe); decide sobre la tarea aparte de `resolve_runtime_doc` y sobre el cambio en graph_ui.
