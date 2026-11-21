# Result
Files (committed in worktree branch deskops/deskops-e-cc37b51d8dab):
- src/sldb/cli/commands/notations_validate.py (split validate_target into _file_or_name_kinds/_ambiguity; store code moved out)
- src/sldb/cli/commands/notations_validate_store.py (new: _STORE_MODELS, _store_has, _store_payload, _check_palette_payload, _check_store_document)
Behavior unchanged. validate_target also exceeded 10 lines and the file exceeded 80 effective lines, hence the sibling module.
Validation: see validation.log. check.sh --fast: only identidad/workbench_demo fails (authorized).
