## REFORMULACION

Encargo `task.code` ejecutable: añadir a sldb el verbo `sldb bench` en `src/sldb/cli/bench/` (parser, handler y medición por subprocess con `os.wait4`), que copia desks a un workdir, mide en frío y caliente pared, CPU y RSS de `stores update`, `stores check`, `stores build --check`, `deskops doctor`, `deskops status` y arranque de CLIs, y emite JSON y tabla. Resultado: verbo operativo, tests `tests/test_bench_*.py`, selfdoc regenerado y baseline en `reports/velocidad-baseline-20261115.md`. Límites: solo medición; nada de arreglos V1/V2 ni cambios en deskops/MEPU (CLI externo y copia respectivamente); protocolo de copias, frío/caliente, orden, documento cambiado, arranque y salida fijado en el TaskDoc.

## AMBIGUEDADES

1. «el primero de sldb docs list --format json cuyo path es .md y existe»: no define orden ni interpretación de `path`; obliga a inventar criterio de selección y resolución de rutas.
2. «--touch NOMBRE=RUTA»: no explica el uso de `NOMBRE` ni si sustituye la autodetección; obliga a inventar semántica.
3. «sin .sldb_cache»: no fija exclusiones adicionales (symlinks, `.git`, permisos); obliga a inventar política de copia.
4. «Caliente: una corrida no medida… y luego --repeat N corridas medidas»: no aclara si `--repeat` aplica también al frío pese a «antes de cada corrida medida»; obliga a inventar matriz frío/caliente×N.
5. «el JSON anota sha y rutas sin commitear de cada origen»: no define cómo detectar rutas sin commitear; obliga a inventar consulta git y formato.
6. «meta (… máquina …)»: no enumera campos de máquina; obliga a inventar esquema.

## DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout, Board, pills/átomos ligados (el TaskDoc los declara vacíos) y archivos nombrados (`src/sldb/cli/bench/`, tests, `tools/check.sh`, selfdoc, `reports/`). Cambios previstos: crear paquete bench, parser/handler, utilidades de copia/medición, tests unitarios, regenerar referencia CLI y escribir informe baseline. Dependencias: `os.wait4`, `subprocess`, `$TMPDIR`/`/dev/shm`, git, deskops en PATH, pytest. Validaciones futuras: los cuatro comandos de la sección Validation, más comprobación de JSON/tabla y limpieza de workdir. Sin ejecutar nada.

## FUTURO

Otro nodo/humano decide: resolver las ambigüedades anteriores antes de implementar; aceptar el baseline y su metodología; usar esas cifras para priorizar V1/V2; decidir si deskops/MEPU requieren tareas propias.
