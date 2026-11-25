## REFORMULACION

Encargo ejecutable (`task.code`, no agregado): hacer que `sldb --version` diga qué commit corre. Propósito: hoy dos instalaciones decían `0.1.13` aunque `git describe` daba `v0.1.13-283-gb965c62d`. Resultado observable: una línea `sldb <versión> (<describe> at <dir>)` desde checkout git, y `sldb <versión>` sin `.git`; exit 0. Repo: checkout editable de sldb (`src/sldb/...`, `tests/`, `CHANGELOG.md`). Límites: no toca `producer.version`, no decide instalación de referencia, no limpia review dirs; el ejecutor no hace push.

## AMBIGUEDADES

1. «en `src/sldb/cli/parser.py` el argumento global `--version`» — pero ese archivo solo hace `from sldb.cli.parsers.core import build_parser`; el parser raíz se construye en `core`. Obliga a inventar si se edita `parser.py` o `parsers/core.py`.
2. «hay que hacer que también devuelva o exponga ese directorio, o buscarlo con el mismo recorrido» — dos alternativas sin criterio; obliga a elegir entre cambiar la firma de `_source_checkout_version` (y sus llamadores) o duplicar el recorrido.
3. «con un valor fijo aparece entre paréntesis» junto a «`sldb <versión> (<describe> at <dir>)`» — si se parchea `source_revision` a un string fijo, no queda claro si ese string incluye ya `at <dir>` o si el `dir` sale de otra función; obliga a inventar el contrato de retorno y el formato del paréntesis.
4. «una línea en español bajo el encabezado "## 0.1.13 — not released yet"» — si el encabezado no existe en `CHANGELOG.md`, obliga a inventar si se crea.

## DRY-RUN

Lecturas: `src/sldb/store/package_version.py`, `src/sldb/cli/parser.py`, `src/sldb/cli/parsers/core.py` (construcción real del parser), `tests/test_cli_v2.py` (fixtures/helpers), `CHANGELOG.md`. Cambios previstos: `source_revision()` con `subprocess.run(["git","-C",dir,"describe","--tags","--always","--dirty"], capture_output=True, text=True, timeout=2, check=False)` y `None` ante `returncode!=0`, salida vacía, `FileNotFoundError` o `TimeoutExpired`; exposición del directorio del pyproject; `argparse.Action` que imprime la línea y sale 0; tres tests con `monkeypatch` sobre `sldb.store.package_version.source_revision` y `cli_main(["--version"])`; entrada de CHANGELOG. Dependencias: binario `git`, `subprocess`, `argparse`, `capsys`/`monkeypatch`. Validaciones futuras: los tres comandos de la sección de validación, sin ejecutarlos aquí.

## FUTURO

El coordinador ejecuta `deskops closeout commit` (mensaje = título corto) y no hay push. El aviso `deskops message send --to <repo>` lo emite el flujo, con fallback a línea en el informe. La decisión sobre qué instalación es de referencia ya la tomó un humano.
