PASA

# Tester deskops-t-1390ab24e897: resultado

Task: `task-render-y-fields-de-sldb-sin-fricciones-none-en-rev-y-optrev-tablas-vacias-dict-de-basemodel-y-rutas`
Commit revisado: `b3dd710632c1ecdb09ce3bd5086093ff175c0d00` — `rev None renders null; fields update sets a None optrev` (con el trailer `Task-Id` correcto).
Archivos del commit: `src/sldb/cli/commands/fields_mutate.py`, `src/sldb/core/renderer_engine/base.py`, `src/sldb/runtime/validation.py`, `tests/test_rev_optrev_none.py`.

## Veredicto

**PASA.** El contrato del alcance se cumple: un marcador `rev` con valor `None` renderiza `null`, la extracción devuelve `None` (el campo opcional queda ausente del payload, por lo que `get` da `None`) y el round-trip de validación es `True`. Un campo `optrev` que vale `None` deja la línea fuera del documento, y `fields update docs/a/nota x --string` vuelve a ponerlo y persiste `nota: x`.

No se evaluaron tablas, dicts con `BaseModel` ni `docs create` relativos: el propio apartado **Scope** de la task los declara fuera de alcance.

## Validación ejecutada

Se corrieron de a un archivo, con `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-1390ab24e897`.

| Comando | rc | Resultado |
|---|---|---|
| `python -m pytest -q tests/test_rev_optrev_none.py` | 0 | 2 passed |
| `python -m pytest -q tests/test_validation_semantics.py` | 0 | 2 passed |
| `python -m pytest -q tests/test_marker_invariants.py` | 0 | 4 passed |
| `python -m pytest -q tests/test_field_corpus.py` | 0 | 7 passed |
| `python -m pytest -q tests/test_campo_con_default.py` | 0 | 1 passed |
| `python -m pytest -q tests/test_cli_v2.py` | 0 | 50 passed |
| `python -m pytest -q tests/test_address_surface.py` | 0 | 8 passed |
| `python -m pytest -q tests/test_list_items_round_trip.py` | 0 | 24 passed |
| `python -m pytest -q tests/store/test_optional_field_hash_neutral.py` | 0 | 12 passed |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

No existen `tests/test_fields_mutate.py`, `tests/test_base.py` ni `tests/test_validation.py`; para los módulos tocados corrí los tests existentes que ejercitan esas superficies (`fields update`/CLI, render y extracción de marcadores, validación y campos opcionales). No se corrió la suite completa.

## Comprobación adicional

- `render_model_markdown(NoneDoc, {"title": "T", "owner": None})` produce `# T\n\nowner: null` (sin marcadores crudos).
- `extract_model_data` da `{'title': 'T'}`; `payload.get("owner") is None`.
- `validate_model_data_roundtrip(NoneDoc, {"title": "T", "owner": None})` devuelve `True`.

## Nota de entorno

`/tmp/ws-venv` no existe en este contenedor. Usé `/workspace/sldb/.venv` (Python 3.13.18, pytest 9.1.1), que es el `.venv` del propio repo y tiene todas las dependencias del proyecto. Los temporales de pytest quedaron bajo `/tmp`.

## Observación no bloqueante

`_is_null_literal` interpreta el texto `null` como `None` en cualquier campo opcional, no sólo en `rev`. Es lo que permite el round-trip de `rev`/`optrev`, pero implica que un valor literal `"null"` en un campo opcional se lee como `None`. No afecta a los dos tests exigidos ni al alcance declarado.
