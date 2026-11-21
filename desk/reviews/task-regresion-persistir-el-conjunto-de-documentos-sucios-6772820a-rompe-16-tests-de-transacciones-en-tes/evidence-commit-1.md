---
sldb:
  by: agent
  at: '2026-11-21T14:28:20Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: 4b44a43af41c3634c78ac9a1ea106764450c9e34
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes@sha256:ce88129bccde4e084f425e487c4e688e2dc5cb97695416a86f8cf861f81ad698
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 9718bd612aeef4247f759695587abd53293ffe0ae97b02819e2aba06e3741d9f
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 4b44a43af41c3634c78ac9a1ea106764450c9e34'
# ISO 8601 timestamp
created_at: '2026-11-21T14:28:06.978423+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T14:28:06.978423+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 4b44a43af41c3634c78ac9a1ea106764450c9e34

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 4b44a43af41c3634c78ac9a1ea106764450c9e34
