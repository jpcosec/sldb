# Informe del tester deskops-t-3ddb03815c4e

Tarea: `task-scan-tree-registra-los-imports-anidados-y-component-spec-from-python-dibuja-sus-aristas`. Veredicto: **PASA**.

Salida completa en `validation.log`, en esta misma carpeta. `uv run --frozen --extra code --extra dev` funcionó y no hizo falta el fallback a `uvx`.

## Validation

| Comando | Resultado | Veredicto |
|---|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q -rs tests/notations/test_component_spec_python.py` | rc 0: 4 passed, 1 skipped | PASA |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q -rs tests/selfdoc/test_treesitter_symbols.py` | rc 0: 5 passed | PASA |

El test que se salta es `test_matches_spec2viz_on_modules_classes_and_defines`, por `importorskip('spec2viz.generators.python_ast')`: spec2viz no está instalado en el `.venv`. El skip no depende de este cambio.

## Done When, punto por punto

- **Un import dentro de una función genera una arista imports: PASA.**
  - Lo cubre `test_nested_imports_draw_one_edge_per_pair`: `pkg/lazy.py` (`def f(): from pkg.sub import b`) da la arista `module_pkg_lazy → module_pkg_sub`, y `pkg/typed.py` (`def g(): from .sub.b import Thing`) da `module_pkg_sub_b`.
  - Mi script lo confirma con def anidado, función decorada, `async def` y método de clase.
- **Un import bajo `if TYPE_CHECKING` genera una arista imports: PASA.**
  - `pkg/typed.py`, con `from pkg.a import A` bajo `TYPE_CHECKING`, da `module_pkg_a`.
  - `if False: import json` da `module_json`.
- **`attrs.imports` igual que antes: PASA.**
  - Comparé `py_imports` nuevo contra el de HEAD (`git show HEAD:src/sldb/code/imports.py`) en los 1160 archivos `.py` de `src/`: 0 diferencias.
  - Comparé `facts.rels` de `scan_tree` nuevo contra un worktree detached de HEAD en /dev/shm, sobre un módulo con imports de nivel superior y anidados. Dan lo mismo: `[{'type': 'imports', 'target': 'a1,a2'}]`. Los anidados no entran en rels. Después borré el worktree (`git worktree remove` y `prune`).
  - El test viejo `test_docstrings_signatures_and_relations` no se tocó y pasa.
- **CHANGELOG con la entrada: PASA.** Es una línea en español bajo `## 0.1.13 — not released yet`, primera de la lista y con el estilo de las vecinas.
- **Commit con los archivos de Files: no aplica al tester.** Lo hace el coordinador con `deskops closeout commit`. El cambio sigue sin commitear, como corresponde.

## Desvío del ejecutor: `module_pkg_sub_b` frente a `module_pkg_sub`

Las Precisiones del contrato piden la arista `("module_pkg_lazy", "module_pkg_sub_b")`. El pill fija que el formato es el mismo que `py_imports`, y para `from pkg.sub import b` ese formato da `pkg.sub`. Lo comprobé: el mismo import en el nivel superior de `pkg/a.py` ya daba `module_pkg_sub` en HEAD.

El brief del ejecutor dice "cuando un pill y el contrato choquen, manda el pill del bundle, y lo anotas". El ejecutor aplicó el pill, mantuvo el texto exacto de `pkg/lazy.py` y anotó el desvío. Es correcto según su brief. Que la Precisión del contrato quede desfasada lo decide el coordinador; no lo cuento como falla.

## Casos no cubiertos por el ejecutor (`/dev/shm/tst-scan/edge.py`)

Todos dan OK:

- Imports anidados dentro de def anidado en def, función decorada, `async def`, `while`, `for`, `match/case`, `except`, `else` y `finally` de un `try`, y en el cuerpo de una clase.
- Los imports que solo aparecen dentro de strings o comentarios no cuentan.
- Un módulo sin imports anidados da `nested_imports == []`.
- Un módulo que importa `a2` arriba y otra vez dentro de una función tiene una sola arista a `module_a2`. No hay aristas duplicadas en todo el spec.
- `from .a import A` anidado se resuelve a `module_pkg_a`.
- `from ... import x`, que sale de la raíz, no genera una arista basura.
- Caso motivador real: `../IR/src/specir/visual/commands.py` da `nested_imports = ['specir.visual.compilers', 'specir.visual.lint_mermaid', 'specir.visual.renderers']`.

En `validation.log` aparece una línea `FAIL rels de e = solo top-level`. Es un error de mi aserción: esperaba los targets partidos por coma, y `rels` guarda `"a1,a2"` como un solo target, igual que HEAD (ver la comparación contra HEAD más arriba). No es un defecto del cambio.

## Archivos fuera del contrato

`git status --short` muestra modificados de la tarea solo los 6 archivos de Files. Los informes del ejecutor están en `runs/subagents/20261116-exec-scan-tree/`. El resto ya estaba listado como ajeno:

- `apply_batch.py`, `lock.py`, `tests/api/test_apply_batch_lock.py`
- `uv.lock`: ajeno. `uv run --frozen` no lo tocó.
- `desk/runtimes/`, `.herdr-coordination.md`

Aparecen además `.sldb/store.yaml`, `.sldb/core/store_index.yaml`, `.sldb/core/models/RunDoc.yaml` y los RunDoc `run-deskops-e-0901c0b6a455` y `run-deskops-t-3ddb03815c4e`. No figuran en la lista de ajenos del brief, pero son registros de corridas del coordinador (RunDoc de este ejecutor y de este tester), no del ejecutor. Lo dejo anotado para que el coordinador lo confirme.

No edité el repo: solo escribí en esta carpeta de run y en /dev/shm. No hice stage, commit ni stash.
