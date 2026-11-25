## REFORMULACION
Propósito: que sldb.code publique facts sintácticos genéricos (sin conocer frameworks) de TS/TSX/JS/JSX para desbloquear IR09: llamadas entre símbolos, llamadas HTTP como llamadas y handlers JSX. Resultado: readers nuevos en sldb.code, fixture en tests/fixtures/treesitter/frontend/src/, tests en tests/selfdoc/test_treesitter_symbols.py, CHANGELOG y commit atómico. Repo: /mnt/ssd/proyectos/SLDB_1. Límites: fuera interpretar REST/frameworks, resolver imports y Python; los readers nuevos están autorizados aunque no figuren en files; los facts y anclas TS existentes deben quedar idénticos a HEAD.

## AMBIGUEDADES
1. Clave del item: "attrs.calls con {func, line, first_arg}" frente a "name en attrs.calls". Obliga a inventar si la clave es func o name (Python usa name).
2. Punto de partida: "El diff de los intentos anteriores está en el árbol o en runs/subagents/20261116-exec-k4-c1/" frente a "El punto de partida es el diff guardado en runs/subagents/20261116-exec-k4-c2/executor-diff-c3ts-c2.patch". Dos rutas alternativas.
3. Estado: "BLOQUEADA 2026-11-17... necesita OK del supervisor" frente a "Decisión del supervisor (2026-11-17, prevalece)". No aclara si ya se puede ejecutar.
4. "Mismas convenciones... que la tarea de Python (si esa ya cerró, seguir su forma exacta)": si no cerró, no dice qué forma usar.
5. "en los tres frontends reales del workspace (solo lectura)": no los nombra; obliga a inventar rutas.
6. "Los readers nuevos van en módulos nuevos del paquete sldb.code" pero files lista lang_ts.py y ts_readers.py; no aclara si se extienden o se crean otros.
7. No canónicos: "cada tramo de espacios en blanco colapsado a un solo espacio (no borrado)" y "sin await ni type args"; no define si los saltos de línea cuentan como espacio ni qué pasa con paréntesis internos.

## DRY-RUN
No es un agregado: es una tarea task.code ejecutable. Un ejecutor futuro leería TaskDoc, rituales, átomo, lang_ts.py, ts_readers.py, ts_fingerprints.py, test/fixture y el patch c2. Cambiaría: módulos nuevos en src/sldb/code (calls, canonización, handlers), attrs.calls/handlers y relaciones calls en lang_ts, fixture, tests y CHANGELOG. Depende del patch de partida, del extra code, de la forma de la tarea Python y del OK del supervisor. Validaría los cinco comandos y los criterios de Done When (tres frontends, destinos canónicos, anclas TS intactas).

## FUTURO
El supervisor confirma el diff de partida y desbloquea; alguien aporta la forma de la tarea Python o confirma su cierre; se nombran los tres frontends. IR09 consume los facts; el tester ejecuta la validación.
