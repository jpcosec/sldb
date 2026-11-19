PASA

# Verificación

Commit del ejecutor: `1c6d26eeecafd6a00101ba247e8a43a4fa4c3722` (Task-Id en el mensaje).
Archivos de código revisados: `src/sldb/cli/parsers/fields.py`, `src/sldb/cli/commands/fields_mutate.py`, `fields_save.py`, `inbox_core.py`, `inbox_show.py`, `help_texts_find.py`; tests en `tests/test_cli_v2.py`, más CHANGELOG y la referencia selfdoc.

# Tests ejecutados

- `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/test_cli_v2.py` → **50 passed**.
- No existen `tests/test_<modulo>.py` para los módulos tocados; el test del commit es `tests/test_cli_v2.py`.
- Verificación adicional de regresiones relacionadas:
  - `tests/test_address_surface.py tests/test_clean_code_rules.py` → **1220 passed**.
  - `tests/test_cli_format_coverage.py tests/api/test_write_paths_validate.py tests/store/test_shard_cache_copies.py tests/test_cli_every_command_has_a_handler.py` → **14 passed**.

# Comportamiento comprobado

- `fields update ... --string` guarda `"Uno: dos"` como texto literal (test y valor exacto en `fields show`).
- `fields append ... --string` guarda el valor literal.
- `fields update/append` aceptan `--format text|json|yaml`; json/yaml emiten `{document, model, field, action, saved}`.
- `inbox --show <nota inexistente>` escribe `Unknown inbox note: ...` por stderr, stdout vacío y exit != 0.
- `inbox <msg> --store <dir sin .sldb>` falla con `No .sldb store at ...` por stderr, exit 1 y no crea `desk/` ni escribe nada (comprobado también manualmente con un directorio temporal).

# Gates rápidos

`/tmp/ws-venv` no existe en este entorno; se usó el venv del repo (`.venv`), con `PYTHONPATH=src` y `TMPDIR=/tmp`:

- `bash tools/check.sh --fast` → **RC=0**, todas las puertas pasan.
- `sldb selfdoc check` (referencia CLI exigida por la tarea) → **RC=0**, `ok: true`, sin cambios ni errores.

# Observaciones

El commit regeneró además las referencias selfdoc de `docs-list` y `stores-merge-driver`; no afecta el veredicto y `selfdoc check` queda en 0.
