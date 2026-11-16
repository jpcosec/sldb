# Resultado — tester deskops-t-f7923f75b516

Tarea: `task-clean-code-tras-carga-tolerante-edge-index-py-y-runtime-documents-py-con-una-clase-cada-uno-y-query` (pills: ninguno).
Veredicto global: **PASA** (con la salvedad del punto 4: el comando completo de clean code sale rc 1 solo por violaciones ajenas, fuera de Scope).

Salida completa de todo lo de abajo: `validation.log` en esta carpeta.

## Validation (corrido por mí, árbol de trabajo)

| # | comando | rc | veredicto |
|---|---|---|---|
| 1 | `pytest -q tests/api/test_api_documents.py` | 0 (13 passed) | PASA |
| 2 | `pytest -q tests/api/test_api_edges.py` | 0 (16 passed) | PASA |
| 3 | `pytest -q tests/store/test_doc_invalid_check.py` | 0 (2 passed) | PASA |
| 4 | `pytest -q tests/test_clean_code_rules.py` | 1 (7 failed, 1159 passed) | PASA en alcance (ver abajo) |
| 5 | `bash tools/check.sh --fast` | 0 | PASA |

Todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`; `uv` funcionó sin problemas.

Punto 4 en detalle:
- Los 6 archivos de la tarea (3 originales + 3 nuevos) pasan, verificados por `-k`: `edge_index.py`, `edge_problem.py`, `runtime_documents.py`, `invalid_document.py`, `store/query.py`, `query_engine/accepted_load.py` → 6 passed.
- Base HEAD (`git archive HEAD` en `/dev/shm/tc1-base`, con `uvx --with-editable`): 9 fallos = los 3 de esta tarea (`edge_index.py`, `runtime_documents.py`, `query.py`) + 6 ajenos (`mcp/write/tools.py`, `api/edges/referrers.py`, `api/edges/rewrite_references.py`, `api/documents/create_document.py`, `store/package_version.py`, `store/section_sync.py`).
- Árbol de trabajo: 7 fallos = esos 6 ajenos preexistentes + `store/io/lock.py`, que en HEAD pasa y falla por el cambio ajeno sin commitear en `lock.py` (no es de esta tarea; anotado, no tocado).
- Por lo tanto la violación de task-carga-tolerante ya no está y no aparece ninguna nueva en los archivos tocados. El Done When literal ("todos los comandos de Validation pasan") no se cumple con rc 0 en el comando 4, pero el Scope deja fuera de manera explícita las otras violaciones.

## Done When, punto por punto

- Comandos de Validation: PASA (1, 2, 3 y 5 en rc 0; 4 limpio en los archivos de la tarea, como se explica arriba).
- git diff no toca tests de comportamiento: PASA. `git diff --stat HEAD -- tests` sale vacío; el único archivo de tests sin trackear es `tests/api/test_apply_batch_lock.py`, que es ajeno.
- CHANGELOG: PASA. Hay una línea bajo `## 0.1.13 — not released yet` que dice que es un arreglo de clean code sin cambio de comportamiento, y check.sh --fast (que incluye la puerta del CHANGELOG) sale en rc 0.
- Commit: pendiente. Al ejecutor y al tester se les prohíbe commitear; queda para el closeout.

## Caso no cubierto por el ejecutor (`/dev/shm/tc1-probe/probe.py`, sin tocar el repo): PASA
- Identidad de los reexports: `edge_index.EdgeProblem is edge_problem.EdgeProblem`, lo mismo con `edge_problem` y `ENDPOINT_NOT_A_NODE`; `runtime_documents.InvalidDocument is invalid_document.InvalidDocument is sldb.api.InvalidDocument`; `__all__` de runtime_documents sin cambios.
- `edge_problem` en el caso negativo (un texto que no coincide da `document=""`) y en el positivo (`RelationDoc:r1`).
- `InvalidDocument` sigue siendo frozen.
- `on_invalid="bogus"` sigue lanzando `ValueError` antes de cualquier IO (es el borde de la nueva extracción `_raising`).
- `load_accepted`: un error que no es `ValidationError` se propaga (no se traga); con `rejected=None` se calla; con lista agrega `(path, model, msg)`; si no hay error devuelve el valor.
- Import en un intérprete limpio de cada módulo nuevo y de `sldb.store.query` por separado: no hay import circular.
- Nota menor, no es falla: `sldb.store.edge_index` (con un `__init__` vacío, igual que en HEAD) ahora tiene un submódulo `edge_problem` con el mismo nombre que la función `edge_problem`. La API de la función se importa desde `edge_index.edge_index` como antes.

## Fuera del contrato: PASA
Cambios de la tarea: `CHANGELOG.md`, `edge_index.py`, `runtime_documents.py`, `query.py` y los 3 módulos nuevos que el Scope autoriza. Hay un desvío justificado: el helper de `query.py` quedó en `store/query_engine/accepted_load.py` y no al lado de `query.py`, porque el eje de `contracts/layers.toml` rechaza un archivo suelto nuevo en `store/`, y check.sh --fast lo confirma en rc 0. Además se extrajo `_raising` en `runtime_documents.py` para cumplir la regla de 10 líneas; el comportamiento queda igual (probado). El resto de los cambios del árbol (`apply_batch.py`, `io/lock.py`, `uv.lock`, `.sldb/`, `desk/`, `runs/`) son ajenos.

## Regresiones vecinas: PASA
Busqué con grep en `tests/` los archivos que importan runtime_documents, InvalidDocument, edge_index, EdgeProblem, edge_problem, query, load_runtime_documents, accepted_load e invalid_document: son 44 archivos. Corrí cada uno por separado y los 44 salen en rc 0, sin ningún fallo (la lista con conteos está en `validation.log` → "REGRESIONES VECINAS"). No hizo falta comparar contra HEAD porque no hubo fallos.
