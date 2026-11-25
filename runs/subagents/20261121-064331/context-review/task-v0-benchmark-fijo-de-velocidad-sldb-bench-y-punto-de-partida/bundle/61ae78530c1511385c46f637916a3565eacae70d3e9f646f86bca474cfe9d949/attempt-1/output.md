## REFORMULACION

Propósito: fijar una medición de velocidad repetible de sldb y deskops antes de cualquier optimización (V1/V2). Resultado: verbo `sldb bench` en `src/sldb/cli/bench/` (copia de desks, frío/caliente, subprocess con `os.wait4`, JSON + tabla) más `reports/velocidad-baseline-20261115.md`. Repo: sldb (parser/handler, `tests/test_bench_*.py`, selfdoc). Límites: solo medición; sin arreglos de velocidad ni cambios en deskops o MEPU; protocolo cerrado (copias con `copytree(symlinks=True)`, purga de `.sldb_cache` y `xdg`, orden de operaciones, `--repeat`, `--timeout` 7200 s, borrado del workdir salvo `--keep`).

## AMBIGUEDADES

1. "el cambio es agregar un salto de línea al final antes de cada corrida de sldb stores update": no distingue calentamiento de muestras medidas; obliga a inventar si en caliente se re-modifica entre repeticiones (rompería el calentamiento).
2. "Orden: cli-start, update-noop…" junto a "el arranque de ambos CLI": no dice a qué `desk` se atribuye cada arranque ni si se repite por desk.
3. "deskops --help (el del PATH o --deskops)": forma y semántica de `--deskops` (ruta, ejecutable, argv) no definidas.
4. "ejecutable de deskops y el sldb que importa" (meta): obliga a inventar qué identifica al sldb importado (módulo, versión, ruta).
5. "cuyo path es .md": criterio de extensión vs subcadena no especificado.

## DRY-RUN

Lecturas: Board, TaskDoc, rituales execution/testing/closeout, `src/sldb/cli/` y registro selfdoc existentes, `git log`/`status` del origen. Cambios previstos: paquete bench (copias, purga de caché y `XDG_CACHE_HOME`, medición `os.wait4`, autodetección y `--touch`, JSON+tabla), parser/handler, tests, selfdoc sync, informe de baseline. Dependencias: Linux (`os.wait4`), git, deskops en PATH, `/dev/shm`. Validaciones futuras: los dos pytest de bench, `test_clean_code_rules.py`, `tools/check.sh --fast`, `selfdoc check`.

## FUTURO

El ejecutor cierra con commit atómico y `deskops closeout` (ritual closeout). Un humano fija rutas concretas de `--desk` y la máquina del baseline. Las tareas V1/V2 consumen el baseline; variaciones de medición entre máquinas las decide un humano, no este nodo.
