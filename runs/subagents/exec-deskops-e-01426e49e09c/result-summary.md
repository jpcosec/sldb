# Result
Files: src/sldb/api/documents/lossy_overwrite.py, tests/api/test_lossy_overwrite_content.py, CHANGELOG.md
refuse_lossy_overwrite now drops from the lost headings those whose body text (whitespace-normalized) appears in the new rendered text; lost content still refused. Two tests (kept / lost). tests/api: 645 passed. check.sh --fast: only identidad red (workbench_demo, authorized).
Commit made in worktree branch deskops/deskops-e-01426e49e09c with Task-Id trailer.
