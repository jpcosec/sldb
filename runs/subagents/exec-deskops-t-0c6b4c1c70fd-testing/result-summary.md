FALLA

# Testing — matching: attach_atom_edges deja de recomponer live-stale y los mapas del índice federado

No existe trabajo del ejecutor que verificar y la meta de rendimiento no se cumple en el árbol
actual (HEAD `498afcda`).

## Por qué FALLA

1. **No hay commit del ejecutor.** `git log -1 --format=%H --grep "Task-Id: <tarea>"` no devuelve
   nada; `git log --all --grep` tampoco. No hay rama `deskops/...` ni worktree del ejecutor
   (`git branch -a`, `git worktree list`), y `git status --porcelain tests/ src/ CHANGELOG.md` está
   vacío. Solo existe el run `runs/subagents/exec-deskops-t-0c6b4c1c70fd-testing` del tester; no hay run ni `result-summary.md` del ejecutor.
2. **Falta el test contador exigido.** No hay ningún test en `tests/matching/` que cuente
   `load_edge_index` o `stale_of_facts`; `grep -rn load_edge_index tests/matching/` no da nada.
3. **El código sigue en el estado "antes".** Un test temporal (creado y borrado tras la corrida,
   con la fixture `matching_store` de `tests/matching/conftest.py` y monkeypatch de
   `sldb.api.edges.edge_reading.load_edge_index`) llamó a `attach_atom_edges` con 10 referencias de
   un mismo store: **20 llamadas a `load_edge_index`** (2 por referencia: `edges_from` +
   `edges_to`), cuando el contrato exige como máximo 2. Assert `20 <= 2` → falló.
4. **Sin cambios en `store_reader.py` ni en `composed_reading.py`, sin entrada en CHANGELOG.md y sin
   la medición antes/después del `specir catalog build` de IR** (el "después" debía quedar bajo
   60 s en el informe del ejecutor).

## Comprobaciones que sí pasan (línea base)

- `TMPDIR=/tmp pytest -q tests/matching/` → 32 passed, rc=0.
- `TMPDIR=/tmp pytest -q tests/api/test_api_edges.py` → 17 passed, rc=0.
- `TMPDIR=/tmp pytest -q tests/store/test_live_stale_security.py` → 8 passed, rc=0.
- Gate rápido `bash tools/check.sh --fast` → rc=1. Única puerta que falla: `identidad`, por el
  directorio versionado sin clasificar `workbench_demo`; es una condición preexistente del árbol,
  no atribuible a un cambio del ejecutor (no hay cambio). Según la regla del encargo, rc≠0 ya
  implica FALLA; además de que la evaluación de la tarea no puede hacerse sin el trabajo.

## Entorno

`/tmp/ws-venv` no existe en este host; se usó `/workspace/sldb/.venv` (Python 3.13.18, pytest
9.1.1), con `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-0c6b4c1c70fd*`.

Detalle de comandos y salidas en `validation.log`.
