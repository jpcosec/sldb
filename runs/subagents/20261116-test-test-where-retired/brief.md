# Tester deskops-t-e73d2fad915b: task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains

Eres el **tester independiente** (rol deskops-tester, modo tester). Tu trabajo es entregar evidencia: no implementas, no corriges, no ruteas, no cierras.

## Qué verificar
1. Lee el contrato con `TMPDIR=/dev/shm deskops show task task-test-where-retired --root /mnt/ssd/proyectos/SLDB_1/sldb` (scope con Precisiones y Convenciones, validation, done_when).
2. Mira el cambio sin commitear con `git -C /mnt/ssd/proyectos/SLDB_1/sldb diff -- tests/store/test_where_retired.py CHANGELOG.md`. Ignora cualquier otro archivo modificado del árbol: es ajeno.
3. Corre tú mismo la validación. El `.venv` del checkout está vacío, así que usa `cd /mnt/ssd/proyectos/SLDB_1/sldb && TMPDIR=/dev/shm uvx --from "pytest>=8" pytest -q tests/store/test_where_retired.py`.
4. Comprueba cada punto de done_when por separado: que `_old_operators("sldb edges --relation contains") == []`, que `_old_operators('status contains "x"') == ["contains"]` y que el diff solo toca esos dos archivos.
5. Comprueba que el regex `PREDICATE_CONTAINS` es exactamente el del scope y que los otros siete operadores siguen contando como palabra entera. Prueba además un caso negativo que el ejecutor no cubrió: con el regex viejo, el test de la relación tiene que fallar. Hazlo en un script en /dev/shm que importe el módulo del test y reemplace el regex en memoria, **sin editar archivos del repo**.

## Reglas
- `TMPDIR=/dev/shm`. No edites nada del repo ni de `desk/`. Nada de `git add`, commit, push, `pkill` ni `pgrep`.
- Escribe la evidencia en `runs/subagents/20261116-test-test-where-retired/`: `validation.log` (salida completa) y `result-summary.md` (veredicto PASA/FALLA por punto, con la evidencia).
- Al terminar, responde en una línea: `PASA` o `FALLA <motivo>`.
