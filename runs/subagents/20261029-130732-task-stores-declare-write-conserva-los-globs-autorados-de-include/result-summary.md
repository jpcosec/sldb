# result-summary: task-stores-declare-write-conserva-los-globs-autorados-de-include

run_id: see directory name · session: scion claude agent, no child session recorded · session_sha256: n/a (no subagent session file)

## What changed
`declare_store` (used by `sldb stores declare` and `--write`) now keeps the authored `include:` rules of an
existing `.sldb/store.yaml` verbatim and appends only what no rule covers. Before, it always rebuilt
`include` from the index (`declared_includes`), which turned every `glob:` whose match set equalled the
tracked set into a glob only when it was exact and into a `paths:` enumeration otherwise (the 93 lines in deskops).

Rules:
- Store with no declaration yet: unchanged (`declared_includes`, derived from the index).
- Store with a declaration: every existing include rule (glob or paths) is copied as is. Tracked documents
  that no rule names (`declared_files`) are appended to the model's own `paths:` rule (created at the end if
  the model has none; a glob rule is never appended to). Links, models and predicates still come from the index
  (a new link added with `stores add` therefore appears); generators/derived were already kept.
- No format change to store.yaml; `stores build` untouched. No `--flatten` flag added (nothing flattens any more).

## Files changed
- `src/sldb/api/stores/declare_store.py` (`_include`, docstring)
- `src/sldb/api/stores/merged_includes.py` (new; split out because of the clean-code rules: functions <=10 lines, files <80)
- `tests/store/test_stores_build.py` (2 tests)
- Not touched: desk/, deskops, board. `.deskops.log` shows modified by the deskops CLI itself (not mine to edit). Nothing committed.

## Tests added (tests/store/test_stores_build.py)
- `test_declare_write_keeps_an_authored_glob_and_adds_only_what_is_missing`: store.yaml with
  `glob: notes/*.md` + `paths: [task.md]`, a new linked store (`stores add`) and a new tracked doc no glob covers ->
  `stores declare --write` keeps the glob verbatim, adds the link and appends only `late.md` to the paths rule; `undeclared == []`.
- `test_declare_write_is_stable_on_a_declaration_it_already_completed`: idempotent re-write.

## Validation (validation.log)
`PYTHONPATH=/workspace/sldb/.venv/lib/python3.13/site-packages /home/scion/.local/share/uv/tools/structuredlanguagedb/bin/python -m pytest -q tests -k 'declare or stores' -p no:cacheprovider`
-> 126 passed, exit code 0. (A first run failed `test_clean_code_rules[declared_includes.py]` for a 22-line function; fixed by the split above.)

## Real case, read-only (cd /workspace/deskops; `sldb stores declare --store .sldb`, no --write, output to /tmp)
Run with the working-tree code (`PYTHONPATH=/workspace/sldb/src ... python -m sldb`), because the installed `sldb` binary is the old code.
- Old installed `sldb`: output 269 lines vs the 199-line store.yaml; flattens `desk/atoms/atom-*.md` into ~43 `paths:` lines (diff block 117,159) and more (7 globs vs 10).
- New code: output 200 lines; all 10 globs and every include rule identical to the committed store.yaml; `include:` has zero diff.
  The only diff is 31 changed lines (8 hunks) of YAML re-wrapping of `predicates.*.description` strings (the committed file wraps at a
  different width than `save_declaration`'s width=100). No semantic difference. `git status` of deskops unchanged.

## Open questions for the supervisor
1. Description re-wrapping: `--write` on deskops would still produce ~31 whitespace-only lines for predicate descriptions (the file was hand-wrapped). Should `save_declaration` use a wider width, or is it acceptable?
2. Path entries that are no longer tracked in the index are now kept (verbatim policy), not pruned as the old derive did; `forget_tracked` already prunes on `docs untrack`, and `stores build` reports `missing` for gone files. Only a hand-removed index entry would stay listed. Say if you prefer pruning.
3. A glob that matches files not tracked in the index is left alone (intent wins); `build` will track them.
4. Requested "answer to deskops via `deskops message send --to deskops`" is in the task's Done When but I was told not to touch /workspace/deskops/desk; left for the supervisor.
