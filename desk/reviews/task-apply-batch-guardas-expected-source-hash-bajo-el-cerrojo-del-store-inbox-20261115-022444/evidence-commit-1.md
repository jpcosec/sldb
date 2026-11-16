---
sldb:
  by: agent
  at: '2026-11-16T19:48:10Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: 014335ff9fb255a1bbffb653788f1092ce6763a0
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444@sha256:1720d8d63930021c16a3c898d44afca067dd2a40517490492da0351fd282b96f
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: fdffd640eae808ec43d1292c6328929edbe643d9872ff006c24f6ebe7aed3929
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 014335ff9fb255a1bbffb653788f1092ce6763a0'
# ISO 8601 timestamp
created_at: '2026-11-16T19:47:58.086665+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T19:47:58.086665+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 014335ff9fb255a1bbffb653788f1092ce6763a0

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 014335ff9fb255a1bbffb653788f1092ce6763a0
