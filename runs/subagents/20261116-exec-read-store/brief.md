# Ejecutor deskops-e-ec3e43f4e6ca: task-lectura-pública-sin-migrar-read-store-abre-una-operación-fresca-de-solo-lectura-y-rechaza-un-store-n

Eres el **ejecutor** (rol sldb-executor) de una sola tarea del desk de sldb. El coordinador no implementa; tú sí, y solo esto.

## Contrato
Lee la tarea completa: `/mnt/ssd/proyectos/SLDB_1/sldb/desk/tasks/task-lectura-pública-sin-migrar-read-store-abre-una-operación-fresca-de-solo-lectura-y-rechaza-un-store-n.md` (secciones Rationale, Goal, Scope con Precisiones y Convenciones, Implementation Path, Validation, Done When). Lee también el frontmatter: references, depends_on y pills. Pills atados: ninguno; léelos en `desk/contexts/` (o con `deskops show pill <id> --root /mnt/ssd/proyectos/SLDB_1/sldb`). Cuando un pill y el contrato choquen, manda el pill del bundle (precisión posterior), y lo anotas. El ritual es `desk/rituals/execution.md`.
Archivos del contrato: src/sldb/api/stores/read_store.py, src/sldb/api/documents/extract_payload.py, src/sldb/api/__init__.py, src/sldb/store/migration.py, tests/api/test_api_stores.py, CHANGELOG.md. Toca solo esos, más los que el Scope o el pill autorizan explícitamente.

## Entorno de tests
El `.venv` del checkout puede estar vacío. Corre cada test con `cd /mnt/ssd/proyectos/SLDB_1/sldb && TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q <archivo>`: sincroniza `.venv` (sin trackear) y no modifica `uv.lock`. Si `uv` falla, anótalo en el informe y usa `TMPDIR=/dev/shm uvx --from "pytest>=8" --with-editable . pytest -q <archivo>`. Si un comando de Validation es `bash tools/check.sh ...` o `sldb ...`, córrelo dentro de `uv run --frozen --extra code --extra dev`.

## Árbol compartido
En el árbol hay cambios ajenos sin commitear (`src/sldb/api/documents/apply_batch.py`, `src/sldb/store/io/lock.py`, `tests/api/test_apply_batch_lock.py`, `uv.lock`, `desk/runtimes/`, `.herdr-coordination.md`, `runs/subagents/2026110*`). **No los toques, no los stagees, no los revises.** Si un test falla por esos cambios ajenos, anótalo con la evidencia y no lo "arregles".

## Prohibido
`git add -A`, `--autostash`, `git commit`, `git push`, `git stash`, `pkill`, `pgrep`, editar `desk/` o `.sldb/`. `TMPDIR=/dev/shm` siempre. Nada de suite completa: solo los comandos de Validation.

## Entrega (en `runs/subagents/20261116-exec-read-store/`)
- `validation.log`: la salida completa de cada comando de Validation, con su rc.
- `result-summary.md`: qué cambiaste (archivo y función), cómo se cumple cada punto de Done When, los comandos corridos con su rc, la lista exacta de archivos tocados y cualquier desvío o duda.
- Si el contrato no alcanza o el código no cuadra con él, te detienes y lo escribes; no improvises fuera del alcance.
- Al terminar, responde en una línea: `LISTO <rc>` o `BLOQUEADO <motivo>`.
