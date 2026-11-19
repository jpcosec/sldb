---
sldb:
  by: agent
  at: '2026-11-19T04:40:48Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430-evidence-tests-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: tests/api/test_apply_batch_dry_run.py
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430@sha256:b89e4fa1a04ec92cc504e4a26665e01f75f1ac424f2b0080e680beaa2b92d841
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 9e8883558eed12611d07d534debd60006bcf0b7fa7cca200bc7a93936ae3412d
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/api/test_apply_batch_dry_run.py'
# ISO 8601 timestamp
created_at: '2026-11-19T04:40:44.056844+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T04:40:44.056844+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/api/test_apply_batch_dry_run.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/api/test_apply_batch_dry_run.py
