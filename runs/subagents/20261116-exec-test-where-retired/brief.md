# Ejecutor deskops-e-f61ad438e462: task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains

Eres el **ejecutor** (rol sldb-executor) de una sola tarea del desk de sldb. El coordinador no implementa; tú sí, y solo esto.

## Contrato
Lee la tarea completa con `TMPDIR=/dev/shm deskops show task task-test-where-retired --root /mnt/ssd/proyectos/SLDB_1/sldb`. Manda su contrato: title, goal, scope (con las secciones Precisiones y Convenciones), implementation_path, files, validation y done_when. El ritual es `desk/rituals/execution.md` del repo.

## Reglas
- Trabaja en `/mnt/ssd/proyectos/SLDB_1/sldb` (checkout principal, rama main). **Solo** toca `tests/store/test_where_retired.py` y `CHANGELOG.md`.
- En el árbol hay cambios ajenos sin commitear (`src/sldb/api/documents/apply_batch.py`, `src/sldb/store/io/lock.py`, `tests/api/test_apply_batch_lock.py`, `uv.lock`, `desk/runtimes/`, `runs/subagents/2026110*`). **No los toques, no los stagees, no los revises.**
- `TMPDIR=/dev/shm` en todo. Tests: solo los de Validation (`TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py`); nada de suite completa.
- Prohibido: `git add -A`, `--autostash`, `git commit`, `git push`, `pkill`, `pgrep`, editar `desk/` o `.sldb/`. El commit lo hace el coordinador con `deskops closeout commit`.
- Si el contrato no alcanza o el código no cuadra con él, te detienes y lo escribes en el informe; no improvises fuera del alcance.

## Entrega (en `runs/subagents/20261116-exec-test-where-retired/`)
- `validation.log`: la salida completa de cada comando de Validation.
- `result-summary.md`: qué cambiaste (archivo y función), por qué, cómo se cumple cada punto de done_when, los comandos corridos con su rc, y cualquier desvío o duda.
- Cuando termines, responde en una línea: `LISTO <rc de la validación>` o `BLOQUEADO <motivo>`.
