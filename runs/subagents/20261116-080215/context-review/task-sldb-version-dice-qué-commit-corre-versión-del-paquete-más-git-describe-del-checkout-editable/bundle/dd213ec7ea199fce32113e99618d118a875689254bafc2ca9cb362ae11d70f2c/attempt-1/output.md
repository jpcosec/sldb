REFORMULACION

El encargo es implementar en el repo sldb que `sldb --version` muestre la versión del paquete y la revisión git del checkout editable. Resultado: `sldb <versión> (<git describe> at <dir>)` desde checkout git, o `sldb <versión>` sin `.git`, con exit 0; incluye `source_revision()`, el argumento global `--version`, tests en `tests/test_cli_v2.py` y `CHANGELOG.md`. Límites: no cambiar `producer.version`, no decidir la instalación de referencia ni limpiar review dirs; el commit lo hace el coordinador, sin push.

AMBIGUEDADES

1. Ubicación del parser: el Scope dice “en src/sldb/cli/parser.py el argumento global --version”, pero la pill dice “El parser raíz se construye en src/sldb/cli/parsers/core.py (build_parser) y ahí va --version.” Obliga a inventar si se edita `parser.py` o `core.py`.

2. Flags de git: el Goal escribe “`sldb <versión> (<git describe --always --dirty> at <ruta del checkout>)`”, mientras la precisión exige “`git -C <dir> describe --tags --always --dirty` (con --tags, también en Goal)”. Obliga a decidir si el texto del Goal debe incluir `--tags` o si manda la precisión.

3. Exposición del directorio: el Scope admite “hay que hacer que también devuelva o exponga ese directorio, o buscarlo con el mismo recorrido”; la pill dice “Se agrega una función nueva _source_checkout_dir() ... sin cambiar _source_checkout_version.” Obliga a elegir entre modificar la función existente, añadir otra o duplicar el recorrido.

DRY-RUN

Lecturas: `src/sldb/store/package_version.py`, `src/sldb/cli/parsers/core.py`, `src/sldb/cli/parser.py`, `tests/test_cli_v2.py`, `CHANGELOG.md`. Cambios previstos: añadir `_source_checkout_dir()` y `source_revision()` con `subprocess.run(..., timeout=2, check=False)` y retorno `None` ante fallo; añadir la acción `--version` al parser raíz usando `package_version()`; tests con `monkeypatch`; línea de CHANGELOG. Dependencias: git disponible, `subprocess`, `argparse`, fixtures de test existentes. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py`, `TMPDIR=/dev/shm pytest -q tests/test_cli_envelope.py`, `PYTHONPATH=src python -m sldb --version`.

FUTURO

El coordinador hace `deskops closeout commit` con el título corto, no hace push y envía el aviso al repo o lo deja en `result-summary.md` si no está registrado. Un humano decide cualquier conflicto entre el código real y la pill o el contrato que el ejecutor reporte.
