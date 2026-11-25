REFORMULACION
Propósito: eliminar el ruido de miles de warnings “Sections rebuild: doc … missing” al escribir en el desk. Resultado: un solo aviso agregado con total, desglose por modelo y hasta tres rutas de ejemplo. Repo: `/mnt/ssd/proyectos/SLDB_1` (sldb). Nodo ejecutable, no agregado. Límites: cambiar `section_sync.py`, test y CHANGELOG; no cambiar llamadores, no limitar el rebuild a documentos de la transacción, no tocar `stores check`; el coordinador hace commit, el ejecutor no hace push.

AMBIGUEDADES
1. “emite a lo sumo una línea de aviso con el número de ausentes” frente a la pill: “si esa función se llama por modelo, sale una línea por modelo con ausentes, y eso es válido”. Obliga a decidir entre aviso global único o uno por modelo.
2. “agregar la ruta relativa al proyecto a una lista nueva report.missing_paths” (pill: `list[str]`) frente al formato “<Modelo>: <n>”. Con solo rutas no se puede calcular el desglose por modelo; obliga a inventar cómo asociar modelo y ruta.
3. Validación “TMPDIR=/dev/shm pytest -q tests/store/test_semantic_rebuild.py” frente al ritual: “stores check, tools/check.sh y tools/check_claims.py cuando … toca el store”. Obliga a decidir qué checks adicionales son exigibles.
4. “en una copia del repo en /dev/shm” frente a “en un worktree limpio”. Obliga a elegir ubicación de la comprobación manual, aunque sea opcional.

DRY-RUN
Leería `section_sync.py`, `semantic.py` (`RebuildReport`), el test, llamadores y CHANGELOG. Añadiría a `RebuildReport` una estructura para ausentes con modelo/ruta; `_missing_doc` solo acumularía; la función superior emitiría un `logger.warning` final si hay ausentes, con modelos y rutas alfabéticos. Añadiría test con `caplog` para 5 documentos borrados y una línea con 5; actualizaría CHANGELOG. Dependencias: fixtures existentes o `sldb.api`; `m_entry.name`; orden alfabético. Validaría con el pytest indicado y, según se resuelva la ambigüedad 3, checks del ritual. La comprobación manual sería opcional.

FUTURO
El coordinador decidirá checks adicionales y hará `deskops closeout commit`, sin push. El ejecutor dejará `runs/subagents/<run-dir>/result-summary.md` y el aviso al repo o su línea de fallback. Un humano resolverá contradicciones entre pill y código.
