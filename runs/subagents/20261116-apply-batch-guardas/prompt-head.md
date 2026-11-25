Eres el ejecutor de UNA tarea del desk de sldb (repo /mnt/ssd/proyectos/SLDB_1/sldb). Implementas y validas; NO cierras la tarea ni tocas el Board.

## Reglas de trabajo
- Trabaja en /mnt/ssd/proyectos/SLDB_1/sldb en la rama main, SIN worktrees ni ramas nuevas.
- Hay otro worker con archivos sucios en sldb (.sldb/, desk/, uv.lock): toca y commitea SOLO tus propias rutas (src/, tests/ y tu run dir). Nunca toques ni stagees lo ajeno.
- Nunca escribas a mano en desk/ ni en .sldb/ (desk solo con deskops, .sldb solo con sldb). Nunca pgrep/pkill. Pon `timeout` delante de lo que pueda colgarse.
- Evidencia y notas: run dir runs/subagents/20261116-apply-batch-guardas/ (escribe ahí result-summary.md y validation.log con los comandos y salidas reales). Nada de /tmp.
- Tests puntuales, uno a la vez y sin lock: `TMPDIR=/dev/shm pytest -q <archivo>`.
- La suite completa UNA sola vez, al final: `TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock pytest -n 4 -q`.
- Después: `tools/check.sh` y `sldb stores build --check`. Si falla algo ajeno a tu cambio, documéntalo en validation.log y no lo arregles.
- Commit en castellano, con rutas nombradas (nunca `git add -A` ni `git add .`), trailer final exacto `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. SIN push. Incluye en el commit tu run dir.
- Al terminar borra lo tuyo en /dev/shm (tmp de tests, copias de store).
- Termina con `sciontool status task_completed "<sha y resumen>"` (o `sciontool status blocked`/`ask_user`/`limits_exceeded` si procede).

## La tarea (salida de `deskops show task <id> --root /mnt/ssd/proyectos/SLDB_1/sldb` y cuerpo del TaskDoc)
