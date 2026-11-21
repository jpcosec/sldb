---
sldb:
  by: agent
  at: '2026-11-21T10:24:54Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/sldb/cli/commands/selfdoc.py

  src/sldb/selfdoc/cli_tree.py

  src/sldb/selfdoc/report.py

  src/sldb/selfdoc/report_findings.py

  tests/selfdoc/test_parser.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a@sha256:212b10f65d3321608feb155a22811af40e71526cf103baf36965f4347f096219
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 70321f4eaecbb8ac3a07261b344ae6589fd8186c0582fbad4d9e3c062c2269ba
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/sldb/cli/commands/selfdoc.py

  src/sldb/selfdoc/cli_tree.py

  src/sldb/selfdoc/report.py

  src/sldb/selfdoc/report_findings.py

  tests/selfdoc/test_parser.py'
# ISO 8601 timestamp
created_at: '2026-11-21T10:24:52.872211+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T10:24:52.872211+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/sldb/cli/commands/selfdoc.py, src/sldb/selfdoc/cli_tree.py, src/sldb/selfdoc/report.py, src/sldb/selfdoc/report_findings.py, tests/selfdoc/test_parser.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/sldb/cli/commands/selfdoc.py
src/sldb/selfdoc/cli_tree.py
src/sldb/selfdoc/report.py
src/sldb/selfdoc/report_findings.py
tests/selfdoc/test_parser.py
