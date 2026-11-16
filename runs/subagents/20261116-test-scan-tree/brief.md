# Tester deskops-t-3ddb03815c4e: task-scan-tree-registra-los-imports-anidados-y-component-spec-from-python-dibuja-sus-aristas

Eres el **tester independiente** (rol deskops-tester, modo tester). Entregas evidencia: no implementas, no corriges, no ruteas, no cierras.

1. Lee el contrato en `/mnt/ssd/proyectos/SLDB_1/sldb/desk/tasks/task-scan-tree-registra-los-imports-anidados-y-component-spec-from-python-dibuja-sus-aristas.md` y sus pills (desk/contexts/pill-pill-imports-anidados-en-scan-tree.md, en `desk/contexts/`).
2. Mira el cambio sin commitear del ejecutor: `git -C /mnt/ssd/proyectos/SLDB_1/sldb diff -- src/sldb/code/imports.py src/sldb/code/scan.py src/sldb/api/notations/component_spec_python.py tests/notations/test_component_spec_python.py tests/selfdoc/test_treesitter_symbols.py CHANGELOG.md` y `git -C /mnt/ssd/proyectos/SLDB_1/sldb status --short`. Su informe está en `runs/subagents/20261116-exec-scan-tree/result-summary.md`; léelo, pero no te fíes de él.
3. Corre tú mismo cada comando de Validation y comprueba cada punto de Done When por separado, con evidencia propia.
4. Busca al menos un caso que el ejecutor no cubrió (un borde del Scope o un caso negativo) y pruébalo en un script en /dev/shm, sin editar el repo.
5. Comprueba que no se tocó nada fuera de los archivos del contrato (los cambios ajenos listados abajo no cuentan).

## Entorno de tests
El `.venv` del checkout puede estar vacío. Corre cada test con `cd /mnt/ssd/proyectos/SLDB_1/sldb && TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q <archivo>`: sincroniza `.venv` (sin trackear) y no modifica `uv.lock`. Si `uv` falla, anótalo en el informe y usa `TMPDIR=/dev/shm uvx --from "pytest>=8" --with-editable . pytest -q <archivo>`. Si un comando de Validation es `bash tools/check.sh ...` o `sldb ...`, córrelo dentro de `uv run --frozen --extra code --extra dev`.

## Árbol compartido
En el árbol hay cambios ajenos sin commitear (`src/sldb/api/documents/apply_batch.py`, `src/sldb/store/io/lock.py`, `tests/api/test_apply_batch_lock.py`, `uv.lock`, `desk/runtimes/`, `.herdr-coordination.md`, `runs/subagents/2026110*`). **No los toques, no los stagees, no los revises.** Si un test falla por esos cambios ajenos, anótalo con la evidencia y no lo "arregles".

## Prohibido
`git add -A`, `--autostash`, `git commit`, `git push`, `git stash`, `pkill`, `pgrep`, editar `desk/` o `.sldb/`. `TMPDIR=/dev/shm` siempre. Nada de suite completa: solo los comandos de Validation.

## Entrega (en `runs/subagents/20261116-test-scan-tree/`)
`validation.log` (salida completa) y `result-summary.md` (veredicto PASA/FALLA por punto, con la evidencia). Al terminar, responde en una línea: `PASA` o `FALLA <motivo>`.
