---
sldb:
  by: agent
  at: '2026-11-21T10:25:24Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-selfdoc-docs-architecture-current-cli-tree-md

  materialization-selfdoc-src-sldb-cli-commands-selfdoc-py

  materialization-selfdoc-src-sldb-selfdoc-cli-tree-py

  materialization-selfdoc-src-sldb-selfdoc-report-findings-py

  materialization-selfdoc-src-sldb-selfdoc-report-py

  materialization-selfdoc-tests-selfdoc-test-parser-py

  materialization-store-layout-changelog-md'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a@sha256:212b10f65d3321608feb155a22811af40e71526cf103baf36965f4347f096219
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: f47691480cb6d5fc8e69403c9dcfa939dd69316a65f8935680a9eee2319f55c8
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-selfdoc-docs-architecture-current-cli-tree-md

  materialization-selfdoc-src-sldb-cli-commands-selfdoc-py

  materialization-selfdoc-src-sldb-selfdoc-cli-tree-py

  materialization-selfdoc-src-sldb-selfdoc-report-findings-py

  materialization-selfdoc-src-sldb-selfdoc-report-py

  materialization-selfdoc-tests-selfdoc-test-parser-py

  materialization-store-layout-changelog-md'
# ISO 8601 timestamp
created_at: '2026-11-21T10:24:52.872211+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T10:24:52.872211+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-selfdoc-docs-architecture-current-cli-tree-md, materialization-selfdoc-src-sldb-cli-commands-selfdoc-py, materialization-selfdoc-src-sldb-selfdoc-cli-tree-py, materialization-selfdoc-src-sldb-selfdoc-report-findings-py, materialization-selfdoc-src-sldb-selfdoc-report-py, materialization-selfdoc-tests-selfdoc-test-parser-py, materialization-store-layout-changelog-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-selfdoc-docs-architecture-current-cli-tree-md
materialization-selfdoc-src-sldb-cli-commands-selfdoc-py
materialization-selfdoc-src-sldb-selfdoc-cli-tree-py
materialization-selfdoc-src-sldb-selfdoc-report-findings-py
materialization-selfdoc-src-sldb-selfdoc-report-py
materialization-selfdoc-tests-selfdoc-test-parser-py
materialization-store-layout-changelog-md
