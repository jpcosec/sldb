---
sldb:
  by: agent
  at: '2026-11-19T06:27:48Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: '011e0da8656616c68b5cee812f12a20f73657208

  9fbb1b776ee4a0f8e8d2c2b10c378af52d5258f2'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do@sha256:82a0ef1cd7975ea2ca95a1be60da43e8bad02f0410dbdf5f2919174a92bc9e5d
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 94b7a6ea69deaed81f42734047db8065233fd12af32f96db49d851ba9e3f193c
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 011e0da8656616c68b5cee812f12a20f73657208

  9fbb1b776ee4a0f8e8d2c2b10c378af52d5258f2'
# ISO 8601 timestamp
created_at: '2026-11-19T06:27:35.352668+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T06:27:35.352668+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 011e0da8656616c68b5cee812f12a20f73657208, 9fbb1b776ee4a0f8e8d2c2b10c378af52d5258f2

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 011e0da8656616c68b5cee812f12a20f73657208
9fbb1b776ee4a0f8e8d2c2b10c378af52d5258f2
