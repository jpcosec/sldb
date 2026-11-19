# Result
Phantom name: `docs list` reads only the indexes (`indexed_documents`: store_index -> models index -> documents index). `docs show` uses `runtime_document` -> `load_runtime_documents`, which silently drops an indexed document whose file is missing or that the read guard refuses (symlink / outside root). The name lives in the model's documents index, not in `store_index.yaml`, so it is listed but not found.
Fix: `docs list` marks such entries `unresolvable: <cause>` (file-missing, store/path-outside-root, store/symlink-not-read); text shows `[unresolvable: ...]`. Resolvable entries unchanged. Model-not-importable deliberately not judged (list has no --pythonpath).
Files: src/sldb/api/stores/unresolvable_documents.py (new), src/sldb/cli/commands/docs.py, tests/test_cli_v2.py, CHANGELOG.md.
Validation: see validation.log (both rc 0).
To do by coordinator: notify sldb-ui. Not reproduced against the real sldb-ui store (cause inferred; confirmed with a tmp store with a deleted tracked file).
