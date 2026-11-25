# Ejecutor deskops-e-f8f7d079d2e1: task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com

Eres el **ejecutor** (rol sldb-executor) de una sola tarea del desk de sldb. El coordinador no implementa; tú sí, y solo esto.

## Contrato
Lee la tarea completa: `/mnt/ssd/proyectos/SLDB_1/sldb/desk/tasks/task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com.md` (secciones Rationale, Goal, Scope con Precisiones y Convenciones, Implementation Path, Validation, Done When). Lee también el frontmatter: references, depends_on y pills. Pills atados: ninguno; léelos en `desk/contexts/` (o con `deskops show pill <id> --root /mnt/ssd/proyectos/SLDB_1/sldb`). Cuando un pill y el contrato choquen, manda el pill del bundle (precisión posterior), y lo anotas. El ritual es `desk/rituals/execution.md`.
Archivos del contrato: src/sldb/links/parser.py, tests/test_links.py, CHANGELOG.md. Toca solo esos, más los que el Scope o el pill autorizan explícitamente.

## Entorno de tests
El `.venv` del checkout puede estar vacío. Corre cada test con `cd /mnt/ssd/proyectos/SLDB_1/sldb && TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q <archivo>`: sincroniza `.venv` (sin trackear) y no modifica `uv.lock`. Si `uv` falla, anótalo en el informe y usa `TMPDIR=/dev/shm uvx --from "pytest>=8" --with-editable . pytest -q <archivo>`. Si un comando de Validation es `bash tools/check.sh ...` o `sldb ...`, córrelo dentro de `uv run --frozen --extra code --extra dev`.

**Prohibido correr la suite completa y `sldb stores build --check`, aunque figuren en Validation**: los corre el integrador (wA:p1) una vez por integración, en una copia limpia. Si Validation los nombra, anótalo en result-summary.md como 'delegado al integrador' y no los corras. `sldb stores build` (sin --check) solo si el contrato pide reconstruir el store del repo, y entonces bajo `flock /dev/shm/sldb1-tests.lock`.

**Siempre**, además de Validation y aunque no figure en el contrato: `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py` y `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast` (reglas de clean code: 1 clase por archivo, como máximo 80 líneas efectivas por archivo y 10 líneas de lógica por función, más la puerta de afirmaciones del CHANGELOG y los docs). Cualquier violación en un archivo tocado es FALLA o bloqueo, no una nota.

Si copias scripts propios al run-dir, ningún nombre puede empezar por `test_` ni terminar en `_test.py` (CI corre `pytest` a secas), y ninguno abre rutas absolutas de esta máquina.

## Árbol compartido
En el árbol hay cambios ajenos sin commitear (`src/sldb/api/documents/apply_batch.py`, `src/sldb/store/io/lock.py`, `tests/api/test_apply_batch_lock.py`, `uv.lock`, `desk/runtimes/`, `.herdr-coordination.md`, `runs/subagents/2026110*`). **No los toques, no los stagees, no los revises.** Si un test falla por esos cambios ajenos, anótalo con la evidencia y no lo "arregles".

## Prohibido
`git add -A`, `--autostash`, `git commit`, `git push`, `git stash`, `pkill`, `pgrep`, editar `desk/` o `.sldb/`. `TMPDIR=/dev/shm` siempre. Nada de suite completa: solo los comandos de Validation.

## Entrega (en `runs/subagents/20261116-exec-lk-md-c2/`)
- `validation.log`: la salida completa de cada comando de Validation, con su rc.
- `result-summary.md`: qué cambiaste (archivo y función), cómo se cumple cada punto de Done When, los comandos corridos con su rc, la lista exacta de archivos tocados y cualquier desvío o duda.
- Si el contrato no alcanza o el código no cuadra con él, te detienes y lo escribes; no improvises fuera del alcance.
- Al terminar, responde en una línea: `LISTO <rc>` o `BLOQUEADO <motivo>`.
