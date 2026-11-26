# result-summary
run_id: exec-deskops-e-e53642222cf7
session: n/a (claude executor)  session_sha256: n/a

Write journal of batches (sldb.store.write_journal, .sldb/core/write_journal/*.json): apply_batch/apply_batches record per batch id, order, actor, per document before-image (incl. provenance) and after_hash, and inverse. New sldb.api.undo_batches (steps, batch_id): reverts last unreverted batches in one transaction under lock; conflict -> ConflictError, nothing written; batch_id only if last unreverted. Provenance of before-images is pinned on undo so store hash returns to the prior value. MCP undo_changes now uses it (works across processes; accepts batch_id).
Files: contracts/layers.toml, docs/architecture/journal-authority.md, src/sldb/api/{__init__,documents/apply_batch,batch_inverse,batch_report,provenance_stamp,undo_batches,nothing_to_undo,undo_report}.py, src/sldb/mcp/{server,write/apply,write/undo}.py, src/sldb/store/write_journal.py, tests/mcp/test_write_tools.py (undo tests use own copy; "someone else" writes bypass batches), tests/test_mcp_undo_across_sessions.py (new).
Review: the journal is store-wide (an undo reverts another actor's last batch too); the 4 other full-suite failures look pre-existing (not verified on main).
Code commit made without Task-Id per instructions.
