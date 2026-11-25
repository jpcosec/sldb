## REFORMULACION
Encargo: hacer que `sldb --version` informe no solo la versión del paquete sino también el commit del checkout desde el que se ejecuta. Resultado observable: una línea `sldb <versión> (<git describe --always --dirty> at <ruta del checkout>)` cuando hay checkout git, y `sldb <versión>` cuando no lo hay; exit 0. Repo: `/mnt/ssd/proyectos/SLDB_1`, rutas relativas `src/sldb/...`, `tests/...`, `CHANGELOG.md`. Límites: no tocar `producer.version` de sellos de procedencia, no decidir instalación de referencia, no limpiar review dirs huérfanos.

## AMBIGUEDADES
1. Goal: `"git describe --always --dirty"` frente a Scope: `` `git -C <dir> describe --tags --always --dirty` ``. Obliga a inventar si se pasa `--tags`.
2. Goal: `"at <ruta del checkout>"`; Scope: `"si el pyproject encontrado por _source_checkout_version está en un directorio con .git"`. No se define qué ruta imprimir (directorio del pyproject, raíz git o cwd); obliga a inventarla.
3. Tests: `"con source_revision parcheada a None"` y `"con un valor fijo aparece entre paréntesis"`. No se indica destino del parcheo ni cadena exacta esperada; obliga a inventar import y formato.
4. Scope: `"corre ... con subprocess (timeout 2 s)"`. No se especifica `check`, captura de stderr ni decodificación; obliga a elegir comportamiento ante salida parcial.
5. `"CHANGELOG.md"`: sin sección, formato ni texto; obliga a inventar la entrada.
6. `_source_checkout_version` se cita como existente sin firma ni contrato; obliga a asumir qué devuelve.

## DRY-RUN
Lecturas: `src/sldb/store/package_version.py`, `src/sldb/cli/parser.py`, `tests/test_cli_v2.py`, `tests/test_cli_envelope.py`, `CHANGELOG.md`, `pyproject.toml`. Cambios previstos: añadir `source_revision()` con detección de `.git` (archivo/carpeta) y `git -C ... describe`; añadir `--version` global con `argparse.Action` que imprime y sale; tres tests; entrada de changelog. Dependencias: binario `git`, `subprocess`, construcción del parser raíz. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py`, `... tests/test_cli_envelope.py`, `PYTHONPATH=src python -m sldb --version`.

## FUTURO
Un ejecutor implementa; otro nodo corre las validaciones; un humano aprueba texto del CHANGELOG, formato final y commit.
