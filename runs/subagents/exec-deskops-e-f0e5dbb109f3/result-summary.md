# Result: apply_batch dry_run
run_id: exec-deskops-e-f0e5dbb109f3
session: n/a (executor Claude session, no child session file)
session_sha256: n/a

## Changes
- src/sldb/api/documents/apply_batch.py: `dry_run=False` param; under the lock, prevalidates and returns before opening the transaction. `apply_batches` unchanged.
- src/sldb/api/documents/batch_report.py: BatchReport gains `applied` (True default) and `planned` (ids in apply order, dry run only). Dry run: applied=False, saved=[], inverse=[].
- tests/api/test_apply_batch_dry_run.py (new): store/project byte-identical, same errors as real apply.
- CHANGELOG.md.

## Notes for the supervisor
- p3: propose_changes (sldb.mcp.write) does not reimplement prevalidation nor call prevalidate_changes; left as is, so docs/architecture/mcp.md unchanged.
- The dry run does not evaluate on_write rules (stated in docstring/CHANGELOG).
- Inbox note 20261115-022430 NOT closed by me (desk doc; not hand-edited) — coordinator to close.
- sldb.api already exports apply_batch; BatchReport shape documented in Field descriptions.
- Validation: tests/api 602 passed; tests/mcp 59 passed (needed mcp extra in venv); check.sh --fast rc 0. See validation.log.
