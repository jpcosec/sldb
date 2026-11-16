# Resultado — executor deskops-e-95afccc5d347

Tarea: `task-sldb-version-dice-qué-commit-corre-versión-del-paquete-más-git-describe-del-checkout-editable`. Resultado: LISTO 0.

## Cambios
- `src/sldb/store/package_version.py`:
  - `_source_checkout_dir()` (nueva, según el pill): mismo recorrido que `_source_checkout_version` (que no cambia), devuelve el directorio del `pyproject.toml` de `structuredLanguageDB` o `None`.
  - `source_revision() -> str | None`: si ese directorio tiene `.git` (archivo o carpeta, `Path.exists`), corre `git -C <dir> describe --tags --always --dirty` con `subprocess.run(..., capture_output=True, text=True, timeout=2, check=False)`; `None` si returncode != 0, salida vacía, `FileNotFoundError` o `TimeoutExpired`.
  - `version_line()`: `sldb <package_version()> (<describe> at <dir>)` o `sldb <versión>`. Llama a `source_revision` por el atributo del módulo, así el monkeypatch del test funciona.
- `src/sldb/cli/parsers/core.py`: `build_parser` añade el argumento global `--version` con una `argparse.Action` propia (`_VersionAction`) que imprime `version_line()` y hace `parser.exit(0)`. `CLI._parse_args` ya convierte ese `SystemExit(0)` en rc 0.
- `tests/test_cli_v2.py`: `test_version_prints_package_version_and_exits_zero`, `test_version_without_git_has_no_parenthesis` (source_revision → None: línea exacta `sldb <versión>`, sin paréntesis), `test_version_with_git_shows_describe_in_parenthesis` (source_revision → `'v0.1.13-1-gabc'`: contiene `(v0.1.13-1-gabc at `).
- `CHANGELOG.md`: una línea en español bajo `## 0.1.13 — not released yet (no tag, not on PyPI)`, primera de la lista.

## Done When
- Los tests pasan: `tests/test_cli_v2.py` 43 passed (rc 0); `tests/test_cli_envelope.py` 10 passed (rc 0).
- `PYTHONPATH=src python -m sldb --version` desde el checkout imprime `sldb 0.1.13 (archive/wt/h47-70-gf4d7c828-dirty at /mnt/ssd/proyectos/SLDB_1/sldb)` (rc 0): versión con el describe entre paréntesis.
- CHANGELOG: hecho. Commit: lo hace el coordinador con `deskops closeout commit` (no commiteé, según el brief).

## Comandos (salida completa en validation.log)
| comando | rc |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py` | 0 |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_envelope.py` | 0 |
| `TMPDIR=/dev/shm PYTHONPATH=src uv run --frozen --extra code --extra dev python -m sldb --version` | 0 |

`uv` funcionó; no hizo falta el fallback de uvx. `uv.lock` ya figuraba modificado por cambios ajenos antes de empezar; no lo toqué ni lo revisé.

## Archivos tocados
- `src/sldb/store/package_version.py`
- `src/sldb/cli/parsers/core.py`
- `tests/test_cli_v2.py`
- `CHANGELOG.md`
- `runs/subagents/20261116-exec-sldb-version/validation.log`, `result-summary.md` (entrega)

## Desvíos y dudas
1. **Pill sobre contrato**: el contrato nombra `src/sldb/cli/parser.py`, pero ese archivo solo reexporta `build_parser` de `src/sldb/cli/parsers/core.py`. El pill (precisión posterior) manda poner `--version` en `parsers/core.py` y lo autoriza en su Where; así se hizo. `src/sldb/cli/parser.py` no se tocó.
2. **Añadí `version_line()`** en `package_version.py`, que no está en el contrato, para no meter la composición de la línea en el parser. Es un helper interno dentro de los archivos del contrato.
3. **`--tags` elige tags de archivo**: con el comando exacto que manda el contrato, `--tags` incluye tags ligeros como `archive/wt/h47`, así que el describe sale `archive/wt/h47-70-gf4d7c828-dirty` y no `v0.1.13-363-gf4d7c828-dirty` (lo que da `git describe --always --dirty` sin `--tags`). El hash del commit sí es correcto y la salida cumple el contrato, pero la parte legible confunde. Si se quiere `v0.1.13-…`, haría falta `--match 'v*'` (tarea aparte o decisión del coordinador); no lo cambié porque las Precisiones fijan el comando exacto.
4. El sufijo `-dirty` sale por los cambios ajenos sin commitear y por los míos, que aún no están commiteados; es lo esperado.
