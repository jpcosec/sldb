# Result
Implemented `sldb notations validate <name|path> [--json] [--store S]`.
Commit (worktree branch deskops/deskops-e-8eb91b4956b3): be78baa9. Note: deskops advance task ran just before the commit landed (shell splitting error); commit made afterwards with a one-off git identity from env vars (no git config changed).
Files: src/sldb/cli/commands/notations_validate.py (new), src/sldb/cli/commands/notations.py, src/sldb/cli/parsers/notations.py, tests/notations/test_notations_validate_cli.py (new), CHANGELOG.md, selfdoc regenerated: .sldb/core/documents/CliCommandDoc/cmd-sldb-notations-{validate,from-graph}.yaml, .sldb/core/documents/SurfaceDoc/surface-sldb-notations.yaml, .sldb/core/models/{CliCommandDoc,SurfaceDoc}.yaml, .sldb/core/store_index.yaml, knowledge/commands/cmd-sldb-notations-{validate,from-graph}.md, knowledge/surfaces/surface-sldb-notations.md.
Tests: 12 passed (validate + sync_spec). selfdoc check rc 0. check.sh --fast rc 1 only for 'identidad' (workbench_demo, authorized).
For review:
- Store-only names (NotationDoc/PaletteDoc in --store but not builtin) are recognized as known, but validation reloads by name through load_notation/load_palette, so a store-only name yields a `-invalid` error finding ("unknown ..."); store docs are not re-validated from payload.
- The unknown-name case prints the message to stderr and returns 2 (not SystemExit).
- The two-type name test monkeypatches _kinds_of_name (no builtin shares a name across types).
- The sync_spec test file has no new cases (the contract's 4 cases are in the new test file per Implementation Path).
- No repo-registered notice sent (no deskops message send used).
