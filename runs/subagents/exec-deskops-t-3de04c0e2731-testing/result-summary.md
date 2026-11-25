PASA

# Tester deskops-t-3de04c0e2731: 422 de POST /save con `details`

Task: `task-el-422-de-post-save-de-sldb-serve-devuelve-exc-errors-como-details`
Commit revisado: `373bb14d7ac41eba27aeeb2dd91f64446938e63e` — `POST /save 422 devuelve exc.errors() como details` (trailer `Task-Id` correcto).

Archivos del commit:
- `src/sldb/cli/serve/save_routes.py` (+13/−1)
- `tests/test_serve_save_422.py` (nuevo, 25 líneas)

## Veredicto

**PASA.** Cuando un cambio de `POST /save` es rechazado por validación pydantic, la respuesta
sigue siendo 422 con `ok: false` y `error`, y ahora incluye `details` como lista de errores de
pydantic. La ruta delega en `validation_body`, que obtiene el `ValidationError` de
`exc.__cause__` y llama `errors(include_url=False, include_context=False, include_input=False)`,
dejando entradas serializables con `loc`, `msg` y `type`. Los errores que no son de pydantic
conservan su comportamiento anterior (409).

## Validación ejecutada (detalle en validation.log)

Ejecutada de a un archivo, con `TMPDIR=/tmp` y
`PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-3de04c0e2731`:

| Comando | rc | Resultado |
|---|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_serve_save_422.py` | 0 | 1 passed |
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_serve.py` | 0 | 63 passed |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

El test nuevo comprueba: status 422, `body["ok"] is False`, `"validation error"` en `error`,
`details` es lista no vacía, cada entrada tiene `loc`/`msg`/`type`, algún `loc` nombra el campo
`title`, y `json.dumps(details)` funciona. `tests/test_serve.py` incluye además el test
preexistente `test_batch_save_invalid_payload_422`, que sigue pasando.

No existe `tests/test_save_routes.py`. Por tratarse del módulo de la ruta modificada se corrió
la suite específica de serve (`tests/test_serve.py`), no la suite completa.

## Nota de entorno

`/tmp/ws-venv` no existe en este host. Usé `/workspace/sldb/.venv/bin/python` (CPython 3.13.18,
pydantic 2.13.4, pytest 9.1.1), que es el mismo directorio que
`/mnt/ssd/proyectos/SLDB_1/sldb/.venv` (mismo inode). `tools/check.sh --fast` se corrió con ese
`.venv/bin` primero en `PATH`. El `/workspace/.venv` de nivel superior es un Python 3.11.2 sin
las dependencias del proyecto y no se usó.

## Observaciones no bloqueantes

- El alcance se respeta: solo se tocaron la ruta `save_routes.py` y su test.
- El single-save (`save_single`) no se modifica; el encargo y el test apuntan al flujo batch de
  `/save`, que es donde `apply_batch` propaga `SLDBValidationError`.
- `details` omite `input`, `url` y `ctx` de pydantic para garantizar JSON serializable; conserva
  exactamente la información exigida (`loc`, `msg`, `type`).
