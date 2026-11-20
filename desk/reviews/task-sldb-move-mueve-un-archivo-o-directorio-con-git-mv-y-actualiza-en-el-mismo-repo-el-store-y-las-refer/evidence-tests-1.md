---
sldb:
  by: agent
  at: '2026-11-20T04:42:58Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/sldb/api/__init__.py

  src/sldb/api/documents/move_document.py

  src/sldb/api/documents/move_path.py

  src/sldb/api/documents/move_path_apply.py

  src/sldb/api/documents/move_path_fields.py

  src/sldb/api/documents/move_path_files.py

  src/sldb/api/documents/move_path_links.py

  src/sldb/api/documents/move_path_plan.py

  src/sldb/api/documents/move_path_remap.py

  src/sldb/api/documents/move_path_report.py

  src/sldb/api/documents/move_path_resolve.py

  src/sldb/api/documents/relocate_file.py

  src/sldb/cli/commands/help_texts_short.py

  src/sldb/cli/commands/move.py

  src/sldb/cli/dispatcher.py

  src/sldb/cli/parsers/project.py

  tests/api/test_move_path.py

  tests/cli/__init__.py

  tests/cli/move_repo.py

  tests/cli/test_move_cli.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer@sha256:f1481847df39973eb7faaabf89c2381bbb6c9a0f51c6d4362ceb640b3b06ce28
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 47e1622beb0ef1db32007447126e7d7b66725eb7b663a0fd61c16e61f343b4eb
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/sldb/api/__init__.py

  src/sldb/api/documents/move_document.py

  src/sldb/api/documents/move_path.py

  src/sldb/api/documents/move_path_apply.py

  src/sldb/api/documents/move_path_fields.py

  src/sldb/api/documents/move_path_files.py

  src/sldb/api/documents/move_path_links.py

  src/sldb/api/documents/move_path_plan.py

  src/sldb/api/documents/move_path_remap.py

  src/sldb/api/documents/move_path_report.py

  src/sldb/api/documents/move_path_resolve.py

  src/sldb/api/documents/relocate_file.py

  src/sldb/cli/commands/help_texts_short.py

  src/sldb/cli/commands/move.py

  src/sldb/cli/dispatcher.py

  src/sldb/cli/parsers/project.py

  tests/api/test_move_path.py

  tests/cli/__init__.py

  tests/cli/move_repo.py

  tests/cli/test_move_cli.py'
# ISO 8601 timestamp
created_at: '2026-11-20T04:42:56.237069+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T04:42:56.237069+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/sldb/api/__init__.py, src/sldb/api/documents/move_document.py, src/sldb/api/documents/move_path.py, src/sldb/api/documents/move_path_apply.py, src/sldb/api/documents/move_path_fields.py, src/sldb/api/documents/move_path_files.py, src/sldb/api/documents/move_path_links.py, src/sldb/api/documents/move_path_plan.py, src/sldb/api/documents/move_path_remap.py, src/sldb/api/documents/move_path_report.py, src/sldb/api/documents/move_path_resolve.py, src/sldb/api/documents/relocate_file.py, src/sldb/cli/commands/help_texts_short.py, src/sldb/cli/commands/move.py, src/sldb/cli/dispatcher.py, src/sldb/cli/parsers/project.py, tests/api/test_move_path.py, tests/cli/__init__.py, tests/cli/move_repo.py, tests/cli/test_move_cli.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/sldb/api/__init__.py
src/sldb/api/documents/move_document.py
src/sldb/api/documents/move_path.py
src/sldb/api/documents/move_path_apply.py
src/sldb/api/documents/move_path_fields.py
src/sldb/api/documents/move_path_files.py
src/sldb/api/documents/move_path_links.py
src/sldb/api/documents/move_path_plan.py
src/sldb/api/documents/move_path_remap.py
src/sldb/api/documents/move_path_report.py
src/sldb/api/documents/move_path_resolve.py
src/sldb/api/documents/relocate_file.py
src/sldb/cli/commands/help_texts_short.py
src/sldb/cli/commands/move.py
src/sldb/cli/dispatcher.py
src/sldb/cli/parsers/project.py
tests/api/test_move_path.py
tests/cli/__init__.py
tests/cli/move_repo.py
tests/cli/test_move_cli.py
