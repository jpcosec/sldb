PASA

# Tester deskops-t-04a7e510ab49: resultado

Task: `task-selfdoc-genera-distinto-la-referencia-de-stores-merge-driver-segun-la-version-de-python-required-del`
Commit revisado: `dbb314cecade242a4cda6e7f767490774ca010e5` — `selfdoc: normalize required for nargs=* positionals across python versions`
Archivos del commit: `src/sldb/selfdoc/arguments.py`, `tests/selfdoc/test_argument_required.py`.

## Veredicto

**PASA.** `argument_record` deja de copiar `action.required` en crudo para un posicional `nargs="*"` sin default: lo normaliza a `True`, que es lo que producen las versiones de Python donde `argparse` marcaba ese caso como requerido y lo que ya contenía `knowledge/commands/cmd-sldb-stores-merge-driver.md`. El resto de los argumentos conserva `bool(action.required)`. Con eso la referencia generada para `stores merge-driver` no depende del parche de Python.

## Reproducción y verificación de la normalización

- En el intérprete disponible 3.13.18, `add_argument("files", nargs="*")` deja `action.required == False`.
- Bajo la regla histórica de `argparse` (3.11 y los 3.12 que motivaron la task) el mismo argumento queda con `action.required == True`.
- Simulé la regla antigua sobre 3.13 (monkeypatch de `_get_positional_kwargs`) y comparé los 157 registros completos de `ParserScanner().scan(build_parser())`: **idénticos byte a byte** con y sin la normalización.
- Para `stores merge-driver` en concreto, el registro de `files` queda igual en ambos escenarios: `required=True`, `default="null"`, `nargs="*"`, `action="argparse._StoreAction"`.

## Validación ejecutada (detalle en validation.log)

Todo con `PATH=/tmp/ws-venv/bin:$PATH`, `TMPDIR=/tmp` y `PYTHONPATH=src` donde aplica. `/tmp/ws-venv` no existía; lo enlacé al `.venv` del repo (Python 3.13.18), que es el intérprete con las dependencias instaladas.

| Comando (de a uno) | rc | Resultado |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider tests/selfdoc/test_argument_required.py` | 0 | 2 passed |
| `python -m pytest -q -p no:cacheprovider tests/selfdoc/test_parser.py` | 0 | 4 passed |
| `python -m pytest -q -p no:cacheprovider tests/selfdoc/test_sync.py` | 0 | 5 passed |
| `python -m pytest -q -p no:cacheprovider tests/selfdoc/test_preflight.py` | 0 | 4 passed |
| `python -m pytest -q -p no:cacheprovider tests/selfdoc/test_fingerprints.py` | 0 | 4 passed |
| `python -m pytest -q -p no:cacheprovider tests/selfdoc/test_import_context.py` | 0 | 3 passed |
| `PYTHONPATH=src python -m sldb selfdoc check` | 0 | `ok: true`, 164 documentos, `changed: []`, `errors: []` |
| `bash tools/check.sh --fast` | 0 | `TODAS LAS PUERTAS PASAN` |

No existe `tests/test_arguments.py`; los tests del módulo tocado son los de `tests/selfdoc/` listados arriba. No se corrió la suite completa.

## Comprobaciones adicionales

- **Alcance:** el commit solo toca `src/sldb/selfdoc/arguments.py` y agrega `tests/selfdoc/test_argument_required.py`; no toca el parser de `stores merge-driver` ni la referencia generada, que ya tenía `required: true`.
- **Caso con default:** `nargs="*"` con `default` explícito sigue dando `required=False`, y una opción (`--x`) sigue dando `False`. Ambos cubiertos por el test nuevo.
- **Sin cambios colaterales:** `git status` de `src/`, `tests/` y `knowledge/` limpio tras la validación.

## Observaciones no bloqueantes

- La normalización cubre `nargs="*"`. Un posicional con `nargs=argparse.REMAINDER` también cambió de requerido a no requerido entre versiones de Python y no está normalizado; ningún parser de sldb usa `REMAINDER`, así que no afecta a ninguna referencia actual. El test de equivalencia de los 157 registros confirma que hoy no hay otra diferencia.
- Un `nargs="*"` con `default=None` explícito se normaliza a `required=True` (en el Python antiguo era `False` por haber default explícito). No hay ningún parser de sldb en ese caso y el valor sigue siendo estable entre versiones.
