REFORMULACION
Propósito: cerrar el punto 1 de IR13 — el test de paridad D2 se salta sin spec2viz por el `importorskip` en vivo.
Resultado: `tests/notations/test_component_spec_python.py` compara contra un golden congelado `tests/notations/goldens/component_spec_python_spec2viz.json` (modules, classes, defines y `_source` con el commit), sin importar spec2viz en ninguna rama; entrada en CHANGELOG.
Repo: `/mnt/ssd/proyectos/SLDB_1` (sldb).
Límites: no tocar vistas.yml, identity.toml ni otros usos de spec2viz; no modificar `component_spec_from_python`; si la paridad difiere, se reporta y no se retoca el golden; solo módulos, clases y defines, no imports.

AMBIGUEDADES
1. "la lista ordenada de pares [from, to]": no fija criterio de orden. Obligaría a inventar la clave de ordenación.
2. "comparar contra _defined(spec) convertido a la misma forma": no describe la conversión (sets/tuplas a listas, orden). Obligaría a inventar la normalización.
3. "deskops message send --to <repo>" y "Aviso a <repo>: ...": `<repo>` sin concretar. Obligaría a inventar el destinatario.
4. "«_source»: la salida de `git -C .../spec2viz rev-parse HEAD`": si se usa un spec2viz instalado distinto de ese checkout, no dice qué commit anotar. Obligaría a decidir.
5. "falla en el entorno de la suite, o bien ... con PYTHONPATH=src": "entorno de la suite" y "src" no se definen. Obligaría a asumir layout.
6. "mensaje «<título corto de la tarea>»": sin longitud ni formato. Obligaría a inventar el texto.

DRY-RUN
Lecturas: `tests/notations/test_component_spec_python.py` (línea 43, fixture tree, `_defined`, `test_matches_spec2viz_on_modules_classes_and_defines`), el TREE y el encabezado de CHANGELOG. Cambios previstos: crear `goldens/component_spec_python_spec2viz.json` generado una vez con PYTHONPATH al checkout; editar el test para leer el golden y normalizar `_defined`; quitar el `importorskip`; añadir la línea de CHANGELOG. Dependencias: checkout o instalación de spec2viz, pytest, git. Validaciones futuras: `pytest -q` del archivo con `TMPDIR=/dev/shm`; grep sin imports de spec2viz; `python -c "import spec2viz"` debe fallar; revisar `_source`. Nada ejecutado.

FUTURO
El commit lo hace el coordinador (`deskops closeout commit`); el ejecutor no hace push. El aviso `deskops message send` al repo, o su línea en el informe, queda para el ejecutor; `runs/subagents/<run-dir>/result-summary.md` lo consume el nodo de revisión. Si la paridad difiere del golden, decide un humano: reportar, no ajustar.
