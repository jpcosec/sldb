## REFORMULACION

Encargo ejecutable (nodo TaskDoc, no agregado): en el repo SLDB_1 (`/mnt/ssd/proyectos/SLDB_1`, checkout editable) hacer que `sldb --version` identifique qué commit corre. Resultado: `source_revision()` en `src/sldb/store/package_version.py` que ejecute `git -C <dir> describe --tags --always --dirty` (timeout 2 s, `check=False`), devolviendo `None` si falla; argumento global `--version` en `src/sldb/cli/parser.py` que imprima `sldb <versión> (<describe> at <dir>)` o `sldb <versión>`, exit 0; tres tests en `tests/test_cli_v2.py`; línea en `CHANGELOG.md`; informe en `runs/subagents/<run-dir>/result-summary.md`. Límites: no tocar `producer.version`, no decidir instalación de referencia, no limpiar review dirs, no push; el commit lo hace el coordinador.

## AMBIGUEDADES

1. "hay que hacer que también devuelva o exponga ese directorio, o buscarlo con el mismo recorrido": dos alternativas de API sin elegir; obliga a inventar si se cambia la firma de `_source_checkout_version`, se crea otra función o se duplica el recorrido, y cómo lo consume la CLI.
2. "con un valor fijo aparece entre paréntesis": no dice qué `<dir>` se imprime ni cómo hacerlo determinista si solo se parchea `source_revision`; obliga a inventar el stubbing del directorio o aceptar la ruta real del checkout.
3. "sldb <versión>": no especifica de dónde sale `<versión>` en el caso sin `.git` (¿`package_version()`? ¿pyproject instalado?); obliga a asumir la fuente.
4. "Un aviso con deskops message send --to <repo>": `<repo>` no está concretado; obliga a asumir el identificador.
5. "una línea" no fija salto final ni espaciado exacto; menor, pero obliga a asumir.

## DRY-RUN

Lecturas: `package_version.py`, `cli/parser.py`, `tests/test_cli_v2.py`, `tests/test_cli_envelope.py`, `CHANGELOG.md` y nota de inbox. Cambios previstos: `source_revision()` + exposición de `<dir>`; `--version` con `argparse.Action` propia; tres tests con `monkeypatch` y captura de stdout; entrada de CHANGELOG. Dependencias: `subprocess`, `pathlib`, `argparse`, `_source_checkout_version` y helpers/fixtures existentes del test. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py`, `TMPDIR=/dev/shm pytest -q tests/test_cli_envelope.py`, `PYTHONPATH=src python -m sldb --version`. Sin ejecutar nada.

## FUTURO

El coordinador hace `deskops closeout commit` (sin push) y envía el aviso o lo anota en el informe; un humano valida estilo del CHANGELOG y la línea impresa.
