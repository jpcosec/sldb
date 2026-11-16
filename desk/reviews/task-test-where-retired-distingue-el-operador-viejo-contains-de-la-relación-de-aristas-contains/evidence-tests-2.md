---
sldb:
  by: agent
  at: '2026-11-16T09:14:01Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains-evidence-tests-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: tests/store/test_where_retired.py
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains@sha256:a0e2763e42e3375c77f193ac3cdc28090ffa47f53d8d972ff5e5257dfbec3abc
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: fe713d1a0ae180264355db0b7908983b0bfb7786433bc5e1b63495476f4189d8
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/store/test_where_retired.py'
# ISO 8601 timestamp
created_at: '2026-11-16T09:13:52.934359+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T09:13:52.934359+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/store/test_where_retired.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/store/test_where_retired.py
