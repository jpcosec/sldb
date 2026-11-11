# dbltrack-worker: un documento en el glob de un modelo padre y en los paths de un modelo hijo se trackea una sola vez

TaskDoc: `desk/tasks/task-un-documento-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-una-sola-vez.md` (task.debug).
Rama `wt/dbltrack`, base `5e55de42`. Fecha: 2026-11-11.
Reproducción del coordinador: `~/proyectos/SLDB_1/coord2-ccconfig/dbltrack/repro.log`.

## Causa raíz

`src/sldb/api/stores/declared_files.py::declared_files` devuelve la concatenación de las filas
`(model, path, name)` de cada regla `include`, regla por regla, sin mirar si otra regla ya nombra
el mismo path. Con `model: TaskDoc, glob: desk/tasks/task-*.md` y la misma tarea en los `paths`
de `TaskCodeDoc`, salen dos filas para un path: `(TaskDoc, p, n)` y `(TaskCodeDoc, p, n)`.

`apply_declaration.apply_includes` trackea toda fila que no esté ya en `tracked_rows`, así que en
un build en limpio (sin caché, sin índice) el archivo se trackea bajo los dos modelos.
`undeclared` tampoco lo detecta, porque las dos filas están declaradas. `stores check` no tiene
ninguna regla sobre paths repetidos, así que el store pasa.

El síntoma en deskops viene de `resolve_indexed_document._family_hits`. `TaskDoc:<name>` busca el
nombre en `TaskDoc` y en cada modelo cuyas `base_models` incluyen `TaskDoc`. Encuentra dos filas
con el mismo path, y deskops responde `Ambiguous task selector`. Con una caché vieja no se ve: el
store ya tenía la fila del hijo y el glob se añadió después. La fila del padre solo aparece en un
build desde cero (clon nuevo o CI).

## Fix (t1-t3)

- **t1, resolution** (`src/sldb/api/stores/include_resolution.py`). When several rules name a
  path, `resolved_rows` keeps one row per path:
  - same model in `paths` and `glob`: one row, no conflict (a `paths` entry gives the name);
  - `paths` rules of a single model plus `glob` rules of a single model that is among its
    bases: the `paths` row wins;
  - anything else is a conflict, and the path gets no row: two `paths` models (even parent and
    child), two `glob` models, or models with no descent between them.

  `declared_files(root, declaration, bases=None)` returns the resolved rows; `rule_rows` returns
  them raw, with their rule type.
  - **Descent:** the `base_models` of each model index (`resolve_indexed_document.indexed_model_bases`;
    for an inherited model, its owner's). That list is recorded at registration with the same
    MRO walk as `sldb.store.model_contract.base_names` (`model_lineage.model_base_names`), so no
    class is imported. A store not built yet has no bases, and the rules of a model not yet
    registered are a conflict in the plan (`build --apply=False`). In `build`, `apply_models`
    registers the models before `apply_includes`.
  - **Conflict:** the finding `store/include-conflict`, an error by default (`include-conflict` is
    added to `policy.ERRORS`; a store's `policy:` can still change it, as for any code). It names
    the path and the models, and is emitted by:
    - `build_store` under `include_conflicts`; `sldb stores build` prints it as an `error:` line
      and exits 1;
    - `stores check` from `store_surroundings`.

    `undeclared` does not report the conflicting path.
- **t2, `stores declare --write`**: `merged_includes` uses `declared_files` with the store's
  bases. The authored glob is kept as before, and nothing is added to `paths` when the child
  already lists the file.
- **t3, a store already duplicated** (`src/sldb/api/stores/include_losers.py`). `losing_rows`
  works from the declaration's rules: a tracked row that a rule names for a path whose winner is
  a different row. It reads the store only to check that the row is tracked. `untrack_losers`
  runs at the start of `update_store_indexes`, which both `sldb stores update` and
  `sldb stores build` run. It uses `forget_document`, which touches the store index, not
  `untrack_document` (whose `forget_tracked` would remove the path from every `paths` list,
  including the winner's). The file and `store.yaml` are left untouched. It is idempotent: the
  second pass finds no losers.

### CLI file outside `files` (authorized by the coordinator)

`src/sldb/cli/commands/stores_build.py`, minimal change. `build_command` exits 1 when there are
`include_conflicts`. `_summary` prints each one as `error: [store/include-conflict] <path>: ...`
and leaves it out of the counts in the `built:` line, which is unchanged. Test:
`test_models_with_no_descent_between_them_are_an_include_conflict` (rc 1 and the line).

## Tests (t4)

`tests/store/test_include_resolution.py` (5 tests, clean build, no cache):
- parent by glob and child by paths: one row under the child, and `ParentDoc:a` resolves to
  `ChildDoc` without ambiguity; `stores check` passes;
- same model in glob and paths: one row, no conflict;
- store already duplicated (glob build, then `docs track` under the child): `update_store_indexes`
  untracks the parent's row; a second `update` and a `build` change nothing; `store.yaml` and the
  file stay byte-identical;
- parent glob plus `paths` of an unrelated model: `include_conflicts` with the path, the path not
  tracked, `stores build` rc 1 with the line, `stores check` rc 1 with the code;
- two `paths` rules (parent and child): conflict.

`tests/store/test_stores_build.py`: the golden build report gains `include_conflicts: []`.

## Real reproduction (deskops 64a5bcc7, copy in /dev/shm, already deleted)

- Clean build with this branch: `tracked: 8` (before: 11). Each of the 3 tasks is tracked once,
  under `TaskCodeDoc`/`TaskDebugDoc`. `deskops view board` shows `ritual-execution (3)` with
  the 3 tasks and no `Ambiguous task selector`. `stores check` passes.
- Store duplicated with sldb `5e55de42` (495 rows, 3 TaskDoc + 3 children):
  - `stores update` with this branch leaves 492 rows, the 3 children;
  - a second `update` changes nothing, and neither does a `build` (`tracked: 0`);
  - `store.yaml` is byte-identical.

## deskops bcf090a8

**No**, it is not needed for correctness any more. With t1, the `TaskDoc` glob over
`desk/tasks/task-*.md` and the `paths` of `TaskCodeDoc`/`TaskDebugDoc`/... (all subclasses of
`TaskDoc` in `deskops/models/task_types.py`) resolve to one row per task, under the child. A
store already duplicated is fixed by the next `stores update` or `build`, with no change to
`store.yaml`.

Removing or migrating the glob is still possible as a cleanup, and is a decision for deskops:
- the glob tracks a new task with no type as `TaskDoc`, which is what it wants today;
- one case would become a conflict: the same file under `paths` of two different task types,
  or under a `TaskRefactorDoc` and a `TaskCodeDoc` listed by path. That does not happen in the
  declaration of 64a5bcc7.

## Validation

Each file was run on its own with `systemd-run MemoryMax=2G` and `TMPDIR=/dev/shm`. All green:
- new and directly affected: `tests/store/test_include_resolution.py` (5),
  `tests/store/test_stores_build.py` (27);
- `tests/api/`: `test_api_stores.py` (7), `test_policy.py` (14), `test_scaffold_store.py` (20),
  `test_model_lifecycle.py` (14), `test_resolve_indexed_document.py` (8), `test_tags.py` (34),
  `test_replace_text.py` (16);
- `tests/store/`: `test_store_context_audit.py` (2), `test_migrate_layout.py` (8),
  `test_cli_store.py` (38), `test_update_fault_tolerance.py` (5), `test_upgrade_compat.py` (5),
  `test_live_stale_security.py` (8), `test_family_follows_the_class.py` (2);
- `tests/`: `test_cli_v2.py` (40), `test_document_segments.py` (3), `test_links_batch_cli.py` (5),
  `test_runtime_cache.py` (8), `test_clean_code_rules.py` (956).

`bash tools/check.sh --fast`: PASS. Layers, identity, axes and surface report 0 violations, and
no measured unit degree changed. Every new file is under `api/stores`, a folder with an axis.
Not run: the 7 steps of the clean-clone workflow (the coordinator runs them).

Environment: pytest from `/mnt/ssd/proyectos/SLDB_1/.venv` with `PYTHONPATH=src` (the worktree).
Neither the sldb `.venv` nor the system Python has pytest.
