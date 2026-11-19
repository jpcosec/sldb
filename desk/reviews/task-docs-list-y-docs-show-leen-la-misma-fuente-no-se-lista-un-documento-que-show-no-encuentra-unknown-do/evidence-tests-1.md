---
sldb:
  by: agent
  at: '2026-11-19T06:27:37Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: tests/test_cli_v2.py
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do@sha256:82a0ef1cd7975ea2ca95a1be60da43e8bad02f0410dbdf5f2919174a92bc9e5d
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 7479ce8b3aa39bb686d89b465174e7edd3d1eb72a1bfc421f512ba3fc5dbb68a
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/test_cli_v2.py'
# ISO 8601 timestamp
created_at: '2026-11-19T06:27:35.352668+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T06:27:35.352668+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/test_cli_v2.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/test_cli_v2.py
