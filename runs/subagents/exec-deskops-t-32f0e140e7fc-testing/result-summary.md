FALLA

# Tester deskops-t-32f0e140e7fc: resultado

Task: `task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do`
Commit revisado: `9fbb1b776ee4a0f8e8d2c2b10c378af52d5258f2` — `docs list marks documents docs show cannot resolve`
Archivos del commit: `src/sldb/api/stores/unresolvable_documents.py` (nuevo), `src/sldb/cli/commands/docs.py`, `tests/test_cli_v2.py`, `CHANGELOG.md`.

## Veredicto

**FALLA.** Los comandos de Validation y `check.sh --fast` pasan, pero el caso que originó la tarea sigue sin cumplir el Goal: en el store real de `UIs/sldb-ui`, `docs list --format json` sigue listando `edge-task-v8-link-resolver-scan-classify-resolve-recover-execution-to-activate` sin marca, y `docs show` de ese nombre sigue dando `Unknown document target`. El diagnóstico del ejecutor (archivo borrado) no es el del caso reportado: el `.md` y el YAML del documento existen. La causa observada es que el modelo `EdgeDoc` no se puede importar, y la función nueva no juzga ese caso.

## Validation ejecutada

Se corrieron de a un archivo. El `.venv` del repo tiene symlinks rotos a `/home/robocop/...`; usé el intérprete 3.13.18 de uv (recreó el `.venv` del repo) con `TMPDIR=/dev/shm`.

| Comando | rc | Resultado |
|---|---|---|
| `uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py` | 0 | 44 passed |
| `uv run --frozen --extra code --extra dev pytest -q tests/api/test_select_documents.py` | 0 | 19 passed |
| `uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py` | 0 | 1211 passed |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

No existe `tests/test_unresolvable_documents.py`; el test del módulo nuevo es el que el propio commit agrega en `tests/test_cli_v2.py`. No se corrió la suite completa.

## Reproducción del caso reportado (falla)

Store: `/workspace/UIs/sldb-ui` (el del inbox `20261116-222911`).

- `docs list --format json` incluye la entrada:
  `{"name": "edge-task-v8-link-resolver-scan-classify-resolve-recover-execution-to-activate", "model": "EdgeDoc", "path": "desk/primitives/edges/edge-task-v8-link-resolver-scan-classify-resolve-recover-execution-to-activate.md"}`
- Esa entrada **no** lleva `unresolvable` (el listado real tiene 0 entradas marcadas).
- `docs show edge-task-v8-link-resolver-scan-classify-resolve-recover-execution-to-activate --store .sldb --pythonpath ...` termina rc 1 con `Unknown document target: ...`.
- El `.md` y el YAML del índice existen:
  `desk/primitives/edges/edge-task-v8-link-resolver-scan-classify-resolve-recover-execution-to-activate.md`
  `.sldb/core/documents/EdgeDoc/edge-task-v8-link-resolver-scan-classify-resolve-recover-execution-to-activate.yaml`
  Por tanto no es `file-missing`, `store/symlink-not-read` ni `store/path-outside-root`.
- Causa observada: `resolve_model_ref("deskops.models:EdgeDoc", ...)` falla con `SLDBModelError: Attribute 'EdgeDoc' not found in 'deskops.models'`; `load_runtime_documents` carga 37 documentos y **ninguno** de `EdgeDoc`. `docs show` no encuentra el nombre porque el modelo no importa, no porque falte el archivo.

El test nuevo (`test_docs_list_marks_what_docs_show_cannot_find`) solo simula borrar `roadmap.md`; cubre `file-missing`, pero no el bloqueo real (`model-not-importable`) ni nombres ambiguos. El propio `result-summary.md` del ejecutor reconoce: “Not reproduced against the real sldb-ui store (cause inferred; confirmed with a tmp store with a deleted tracked file)”.

## Por qué FALLA

El Goal pide que todo nombre listado se pueda mostrar o quede marcado como no resoluble con su causa. En el store que motivó la tarea, el nombre sigue listado sin marca y sigue sin poder mostrarse. El fix solo marca ausencias/lecturas denegadas de archivos; no cubre el caso observado (modelo que no importa), que es el que deja el nombre fantasma en `docs list` y el `Unknown document target` en `docs show`.

Sugerencia para el ejecutor: reproducir sobre `UIs/sldb-ui` o un store de prueba con un `model_ref` no importable, y marcar esa causa (por ejemplo `model-not-importable`) usando el mismo entorno/PYTHONPATH con el que corre `docs show`; agregar el caso al test.
