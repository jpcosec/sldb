PASA

# Tester deskops-t-32f0e140e7fc-a2: resultado

Task: `task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do`
Commit revisado: `011e0da8656616c68b5cee812f12a20f73657208` — `docs list marks documents whose model does not import` (incluye el intento 1 `9fbb1b77`).
Archivos del commit: `src/sldb/api/stores/unresolvable_documents.py`, `src/sldb/cli/commands/docs.py`, `src/sldb/cli/parsers/docs2.py`, `tests/test_cli_v2.py`, `CHANGELOG.md`.

## Veredicto

**PASA.** El caso que motivó la tarea queda alineado: en el store real de `UIs/sldb-ui`, el nombre `edge-task-v8-link-resolver-scan-classify-resolve-recover-execution-to-activate` ahora sale de `docs list` con `unresolvable: model-not-importable`, y `docs show` de ese nombre sigue dando `Unknown document target`; es decir, `list` ya no ofrece el nombre como si fuera mostrable. Además, la comprobación completa del store da coincidencia exacta entre lo marcado y lo que `load_runtime_documents` no carga.

## Validation ejecutada

Comandos de la tarea, de a un archivo, con `TMPDIR=/dev/shm` y `uv` (el `.venv` del repo, Python 3.13.18):

| Comando | rc | Resultado |
|---|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py` | 0 | 45 passed |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_select_documents.py` | 0 | 19 passed |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py` | 0 | 1211 passed |
| `PATH=/workspace/sldb/.venv/bin:$PATH bash tools/check.sh --fast` | 0 | `TODAS LAS PUERTAS PASAN` |

No existe `tests/test_unresolvable_documents.py`; el test del módulo nuevo es el que agrega el commit en `tests/test_cli_v2.py`. No corrí la suite completa.

También corrí en aislamiento los dos tests de docs list del commit; ambos pasan:
`test_docs_list_marks_what_docs_show_cannot_find` y `test_docs_list_marks_a_document_whose_model_does_not_import`.
El segundo cubre exactamente el caso pedido: con `--pythonpath` el documento no lleva marca; sin `--pythonpath`, con el módulo del modelo fuera de `sys.path` y `sys.modules`, `docs list` marca `model-not-importable` y `docs show` falla con `Unknown document target`.

## Reproducción en el store real de sldb-ui

Store: `/mnt/ssd/proyectos/SLDB_1/UIs/sldb-ui/.sldb` (mismo inodo que `/workspace/UIs/sldb-ui/.sldb`; cwd `UIs/sldb-ui`, `PYTHONPATH=/workspace/sldb/src:/mnt/ssd/proyectos/SLDB_1/deskops`, sin `--pythonpath`, como lo ejecuta la API de sldb-ui).

- `docs list --format json`: la entrada del nombre reportado lleva
  `"unresolvable": "model-not-importable"`.
- `docs show edge-task-v8-link-resolver-scan-classify-resolve-recover-execution-to-activate ...`: rc 1, `Unknown document target: ...`.
- Marcas: 339 de 769 documentos, todas de modelos que ya no existen en `deskops.models`: `EdgeDoc` (120), `ConditionDoc` (80), `ChecklistDoc` (60), `OperatorDoc` (60), `RoutineDoc` (19). Comprobado importando `deskops.models`: esos cinco atributos no están exportados (por eso `resolve_model_ref("deskops.models:EdgeDoc", ...)` da `SLDBModelError: Attribute 'EdgeDoc' not found`). El `.md` y el YAML del índice del documento existen; la causa no es archivo ausente.

Comprobación cruzada en el mismo store con `load_runtime_documents(..., on_invalid="skip")`:
- 769 indexados; 430 cargados; 0 documentos inválidos; 0 nombres duplicados.
- Exactamente los mismos 339 indexados que no se cargan son los 339 que `docs list` marca (`indexed-not-loaded == marked`), y no hay ningún marcado que sí se cargue.
- `docs show` de un documento resoluble (p. ej. `AtomDoc`) responde rc 0 con el detalle.

## De dónde salía el nombre fantasma

`docs list` leía solo los índices (`indexed_documents`); `docs show` usa `load_runtime_documents`, que descarta en silencio los documentos de un modelo cuyo `model_ref` no importa (o cuyo archivo falta/no se lee). En sldb-ui el modelo `deskops.models:EdgeDoc` no importa, así que su nombre quedaba listado y `show` no lo encontraba. El commit agrega la causa `model-not-importable` y resuelve el `model_ref` con los mismos candidatos que `load_runtime_documents` (`store/query.py::_resolve_model_type`): el `--pythonpath` de quien llama y luego la raíz del store; `docs list` gana `--pythonpath`. Las entradas resolubles no cambian (el test lo verifica).

## Observaciones para el cierre

- El aviso a sldb-ui sigue pendiente (el propio `result-summary.md` del ejecutor lo dice). Además, `src/lib/cli/contracts.ts::normalizeDocsListResponse` de sldb-ui hoy reconstruye solo `name`, `model`, `path` y `status`, así que descarta el campo `unresolvable`: la UI seguirá mostrando el nombre hasta que sldb-ui consuma el campo o filtre los no resolubles. Es un cambio fuera de este repo (el scope de la tarea lo excluye), pero debe quedar en el aviso/closeout.
- La API de sldb-ui pasa el pythonpath por la variable de entorno `PYTHONPATH`, no por `--pythonpath`; el arreglo funciona igual porque la importación respeta `sys.path`, pero el flag nuevo queda disponible para invocaciones directas.
