---
sldb:
  by: agent
  at: '2026-11-19T04:39:23Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: 29c0a85725c47cb27ec460d13be6e54210b3f38e
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430@sha256:b89e4fa1a04ec92cc504e4a26665e01f75f1ac424f2b0080e680beaa2b92d841
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 1a04d670220d75002e2dfc7e6af618b18be888597c5e921db6a6666b7f67e546
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 29c0a85725c47cb27ec460d13be6e54210b3f38e'
# ISO 8601 timestamp
created_at: '2026-11-19T04:39:11.035171+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T04:39:11.035171+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 29c0a85725c47cb27ec460d13be6e54210b3f38e

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 29c0a85725c47cb27ec460d13be6e54210b3f38e
