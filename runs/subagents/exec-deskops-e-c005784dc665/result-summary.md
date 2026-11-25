run_id: exec-deskops-e-c005784dc665
Changed (committed on branch deskops/deskops-e-c005784dc665):
- src/sldb/cli/commands/doc.py: docs create resolves -o against process cwd.
- tests/test_docs_create_output_path.py: new test (fails before fix, passes after).
- tests/test_cli_v2.py: two linked-store tests used relative -o expecting project-root resolution; now pass absolute paths.
Note: API create_document docstring still says relative = project root (API unchanged; only CLI resolves to cwd).
Validation: see validation.log (full suite incomplete due to timeout).
