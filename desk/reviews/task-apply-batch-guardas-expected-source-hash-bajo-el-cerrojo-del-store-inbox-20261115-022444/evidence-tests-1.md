---
sldb:
  by: agent
  at: '2026-11-16T19:48:00Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'tests/api/test_apply_batch_lock.py

  tests/test_clean_code_rules.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444@sha256:1720d8d63930021c16a3c898d44afca067dd2a40517490492da0351fd282b96f
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: aba0ab43aafd846715063176e4fa60615fb7137e05aca7ec52873131a318d39f
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/api/test_apply_batch_lock.py

  tests/test_clean_code_rules.py'
# ISO 8601 timestamp
created_at: '2026-11-16T19:47:58.086665+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T19:47:58.086665+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/api/test_apply_batch_lock.py, tests/test_clean_code_rules.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/api/test_apply_batch_lock.py
tests/test_clean_code_rules.py
