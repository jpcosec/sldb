# Reconciliación: ocho tasks de diseño en `current_node: completed` sin cerrar

Run: reconcile-design-tasks-20260929
Estado: las ocho tenían su entregable commiteado. Faltaba la evidencia que los gates leen.

## Qué se encontró

Ocho tasks quedaron en `status: active` con `current_node: completed` — el último
nodo del workflow — pero sin pasar por closeout. Cada una tiene su commit:

| Task | Commit | Entregable |
|---|---|---|
| `mapear-arquitectura-real-de-sldb` | `498aae9` | `docs/architecture_map.md` (718 líneas) |
| `definir-arquitectura-objetivo-modular-de-sldb` | `8837032` | `docs/target_architecture.md` |
| `dise-ar-estrategia-de-extracci-n-y-modularizaci-n` | `445862e` | `docs/migration_strategy.md` |
| `ejecutar-refactor-base-del-n-cleo-sldb` | `ad695a1` | cortes estructurales en `src/` |
| `define-sldb-addressability-model` | `ba2ea9e` | `docs/addressability_model.md` |
| `design-sldb-ast-query-primitives` | `436376d` | `docs/ast_query_primitives.md` |
| `expand-sldb-composition-modes` | `9411866` | `docs/composition_modes.md` |
| `tighten-semantic-export-provenance-contract` | `ce8e861` | `docs/export_provenance_contract.md` |

## La contradicción de composition_modes, resuelta

Antes de este run parecía que `expand-sldb-composition-modes` estaba en `completed`
mientras `docs/composition_modes.md:42` decía que su scope "were proposals. They are
not advertised as supported operations in this checkout."

No es contradicción. La task era de **diseño** y su entregable ERA el documento de
diseño. `9411866` agregó el archivo con los cuatro modos propuestos, incluida la
composición por query y el edit-through. Un año después, `1b04515` reescribió el
encabezado del MISMO archivo para separar lo implementado de lo propuesto.

El archivo terminó con dos capas de tiempo: un encabezado que describe el estado
actual ("Two composition mechanisms are implemented") y un cuerpo que describe el
diseño original. Ambas son correctas; el archivo no dice cuál es cuál.

Queda como atom: `atom-una-task-de-diseno-entrega-un-documento-y-su-doc-puede-decir-que-lo-disenado-no-existe`.

El error de lectura era tratar "Implement task-X" en el mensaje de commit como
evidencia de que X quedó implementado. Solo dice que la task se ejecutó. Para una
task de diseño, ejecutarla significa producir el diseño.

## Qué se hizo

Se completó el campo `references` de las ocho con: commit, documento entregado,
`validation.log` de este run, un test real, y los dos atoms aplicables.

Corrección hecha durante el run: tres rutas de test escritas de memoria no existían
(`tests/test_sections.py`, `tests/test_ast.py`, `tests/test_semantic_export.py`).
Se reemplazaron por las reales (`tests/test_address_surface.py`,
`tests/test_marker_invariants.py`, `tests/store/test_semantic_export.py`) tras
verificar cada una con `-f`. Un gate que pasa citando un archivo inexistente es peor
que un gate en rojo.

## Validación

- `PYTHONPATH=src python -m pytest -q` → **1077 passed**, 0 failed (`validation.log`).
- `closeout verify` en las ocho: `atom_or_materialization_link`, `commit`, `tests` en verde.

## Nota sobre `task_type`

Las ocho tienen `task_type: ''`. El workflow no distingue diseño de implementación:
`spec/workflows/task_lifecycle.yaml` no menciona `task_type`, y los gates de closeout
tampoco lo leen. Por eso una task de diseño y una de implementación se cierran contra
la misma evidencia, y por eso la confusión de `composition_modes` no tenía cómo ser
detectada por la herramienta.
