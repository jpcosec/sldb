# Result summary
run_id: exec-deskops-e-97dc05303d2b
Added `--reindex` to `docs track` and `reindex=` to `track_document_file`: re-indexes an already tracked doc at the same path, validating like a normal track (index untouched on failure); untracked -> plain track; `--reindex` + `--force` -> SLDBError. `--force` unchanged. Store layer needed no change (reindex passes force=True to track_document only after validation).
Note: an invalid file raises pydantic ValidationError (same as a normal track), tests accept it or SLDBValidationError.
Files: src/sldb/api/documents/track_document_file.py, src/sldb/cli/commands/doc.py, src/sldb/cli/parsers/docs1.py, tests/api/test_api_documents.py, CHANGELOG.md, knowledge/commands/cmd-sldb-docs-track.md, .sldb/core/documents/CliCommandDoc/cmd-sldb-docs-track.yaml, .sldb/core/models/CliCommandDoc.yaml (selfdoc sync).
Validation: see validation.log (all pass; selfdoc check 0).
Review: notify sldb-ui (Done When). `.sldb/core/store_index.yaml`/`store.yaml` were already dirty and not committed by me.
