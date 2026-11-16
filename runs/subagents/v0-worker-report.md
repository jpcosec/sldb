# V0 — benchmark fijo de velocidad: informe del worker (2026-11-16)

- **Tarea:** `task-v0-benchmark-fijo-de-velocidad-sldb-bench-y-punto-de-partida` (task.code, desk de sldb).
  Preflight `review-…-preflight-1` aceptado (5 ambigüedades resueltas en `scope`: protocolo de copia,
  frío y caliente, documento cambiado, arranque, esquema de salida). Bundle: ver al final.
- **Commits en sldb main (sin push):** `b60f0891` (verbo), `f6920a2d` (desk), `d4aeb4b1` (copia del
  árbol en vez de clon, `--sibling`), `06aef638` (build-check caliente calentado con update),
  `088c2b34` (`stderr_tail` en corridas fallidas), más el commit de desk del cierre.
- **Baseline:** `/mnt/ssd/proyectos/SLDB_1/reports/velocidad-baseline-20261115.md` (+ `.json` y
  `-build-check.json` al lado).

## Forma del benchmark

Verbo `sldb bench` (top-level, como `lint`), sin script suelto. Código en `src/sldb/cli/bench/`
(`measure` con `os.wait4`, `desks`, `operations`, `config`, `environment`, `runner`, `meta`,
`report`), handler `src/sldb/cli/commands/bench.py` (imports perezosos: no suma al arranque),
parser `src/sldb/cli/parsers/bench.py`. Tests `tests/test_bench_measure.py`, `tests/test_bench_cli.py`
(no marcados: corren en segundos sobre un repo de juguete; el bench real es el verbo).
deskops se invoca como CLI externo, nunca se importa. Referencia regenerada (`knowledge/commands/cmd-sldb-bench.md`).

Operaciones: `sldb-help`, `deskops-help`, `update-noop`, `update-one`, `check`, `doctor`, `status`
y, solo con `--ops`, `build-check`. Salida: JSON (`--output`: meta con shas, rutas sin commitear,
máquina, el sldb que importa deskops, documento tocado; `summary`; `results` por corrida con
`stderr_tail` si rc≠0) y tabla Markdown por stdout.

## Cómo correrlo

```bash
cd /mnt/ssd/proyectos/SLDB_1/sldb
export TMPDIR=/dev/shm PATH=/mnt/ssd/proyectos/SLDB_1/.venv/bin:$PATH PYTHONPATH=src
SIB="--sibling pron=../pron --sibling spec2viz=../spec2viz --sibling scion=../scion"
python -m sldb bench --desk sldb=. --desk deskops=../deskops --desk mepu=/mnt/ssd/proyectos/mepu-scion/mepu \
  $SIB --repeat 2 --deskops ~/.local/bin/deskops --workdir /dev/shm/v0-bench --output out.json
flock /dev/shm/sldb1-tests.lock python -m sldb bench --desk sldb=. --sibling deskops=../deskops $SIB \
  --ops build-check --deskops ~/.local/bin/deskops --workdir /dev/shm/v0-build --output build.json
```

## Baseline (mediana de 2; pared s, frío / caliente)

| desk | update sin cambios | update 1 doc | stores check | deskops doctor | deskops status |
|---|---|---|---|---|---|
| sldb | 42.7 / 2.7 | 40.8 / 2.9 | 48.0 / 28.0 | 64.7 / 54.4 | 64.2 / 57.5 |
| deskops | 6.9 / 1.7 | 6.9 / 2.6 | 8.4 / 6.3 | 14.1 / 14.3 | 14.1 / 13.7 |
| mepu | 42.2 / 4.9 | 41.9 / 5.2 | 51.9 / 44.0 (29 s CPU) | 72.2 / 61.3 | 73.3 / 63.0 |

Arranque: `sldb --help` 0.41 s, `deskops --help` 0.9 s. **`stores build --check` (sldb): 3281 s
frío, 3294 s caliente (≈55 min, 1.25 GB RSS, un núcleo).**

## Hallazgos (dónde se va el tiempo)

1. `build --check` no se beneficia de ninguna caché (frío = caliente ±0.4 %): reconstruye en una
   copia temporal con otra ruta.
2. `stores check` caliente sigue en ~26–29 s de CPU: cProfile muestra 6200 extracciones para ~3100
   documentos (dos por documento: `diagnose_store` y `scan_structural_noise`), y la caché en disco
   de extracciones no evita ninguna. El tiempo propio lo encabeza PyYAML en Python puro y luego markdown-it.
3. `deskops doctor`/`status` ≈ 2 × `stores check` (dos subprocess, como dice el brief); `status` es doctor.
4. Update caliente: costo fijo ~2.7 s; cambiar un documento suma ~0.2 s.
5. deskops usa el sldb de `/home/robocop/herramientas/sldb` @ `f99b9260`, **27 commits detrás** del
   main medido: las mejoras de V1/V2 en sldb no se verán en doctor hasta actualizarlo.
6. Un clon de git no sirve para medir: deja fuera `knowledge/symbols/` (ignorado, ~3300 docs) y un
   update tardó más de 20 min. El bench copia el árbol de trabajo.
7. Sin el store hermano `pron`, `build --check` sale rc 1 en 3 s (`No store is linked as 'pron'`),
   aunque un link ausente debería ser alerta según el CHANGELOG. De ahí `--sibling` y `stderr_tail`.
8. MEPU: 23 PythonSymbolDoc faltantes (update rc 1), también en el original; sus links apuntan a
   `/home/jp/...` (ausentes en esta máquina).

## Validación

- `pytest tests/test_bench_measure.py tests/test_bench_cli.py tests/test_clean_code_rules.py`: 1169 passed.
- `tests/test_cli_every_command_has_a_handler.py tests/selfdoc/test_preflight.py tests/selfdoc/test_parser.py`: 9 passed.
- `bash tools/check.sh --fast`: todas las puertas pasan. `sldb selfdoc check`: sin hallazgos.
- `contracts/layers.toml`: sin cuentas que ajustar (el código nuevo vive en `cli`, sin aristas nuevas entre capas; check_layers y check_axes pasan).
- `deskops graph missing`: rc 1 por 6 faltantes preexistentes en otras dos tareas; ninguno de V0.

## Limpieza

Borrado en `/dev/shm`: `v0-try`, `v0-smoke`, `v0-prof` (copias y perfil), `v0-bench` y `v0-build`
(los borra el propio bench), `v0-preflight.log`, `v0-graph.log`, `v0-baseline.log`, `v0-build.log`,
`v0-run2.log`, `v0-first-run.json`, `v0-first-build.json` (la primera corrida, sin hermanos,
descartada). No quedó nada con prefijo `v0-`. `~/.cache/sldb` no se tocó (cada hijo tuvo su
`XDG_CACHE_HOME` propio). Sin worktrees ni ramas. `uv.lock` y las notas de inbox ajenas quedaron sin commitear.
