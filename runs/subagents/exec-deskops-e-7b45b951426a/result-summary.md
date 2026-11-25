# Result — merge driver auto-install

run_id: exec-deskops-e-7b45b951426a

## Done (uncommitted)
- NEW src/sldb/api/stores/ensure_merge_driver.py: `ensure_merge_driver` (idempotent; no-op outside git; git failure -> stderr warning, no raise), `missing_merge_driver`, `merge_driver_finding` (alert `merge-driver-missing`, fix `sldb stores merge-driver --install`).
- src/sldb/api/stores/init_store.py, scaffold_store.py (apply only), build_store.py (apply only): call ensure_merge_driver.
- src/sldb/api/stores/store_surroundings.py: adds the finding to `stores check`.
- NEW tests/store/test_merge_driver_auto_install.py (6 tests: init, scaffold, build twice no dup, outside git, check finding before/after install, git failure only warns).
- CHANGELOG.md entry.

## Validation
- pytest on new tests + test_stores_build + test_update_fault_tolerance: 49 passed.
- `bash tools/check.sh --fast`: rc 1. Only gate `identidad` fails: "directorio versionado sin clasificar en la raíz: workbench_demo" — pre-existing (committed in 562847e2), unrelated to this task, needs a human decision on classifying that directory. All other gates pass. Log: check-fast.log.

## Blocked
Not committed (task requires check --fast rc 0) and `deskops advance` not run. Supervisor: classify workbench_demo (or authorize commit despite it); then commit these files by name:
src/sldb/api/stores/{ensure_merge_driver,init_store,scaffold_store,build_store,store_surroundings}.py tests/store/test_merge_driver_auto_install.py CHANGELOG.md

## Update (coordinator authorization 2026-11-20T07:13Z)
`bash tools/check.sh --fast` rc 1 only because gate `identidad` fails on `workbench_demo` (pre-existing, from 562847e2, unrelated; classification goes in another task). Coordinator authorized committing with it red; every other gate passes. Committed by named files with Task-Id trailer.
