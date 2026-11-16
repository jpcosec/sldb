---
sldb:
  by: agent
  at: '2026-11-16T20:34:34Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-gd24-api-test-transaction

  materialization-gd24-documents-apply-batch

  materialization-gd24-documents-batch-report

  materialization-guardas-apply-batch

  materialization-inverso-apply-batch

  materialization-inverso-batch-report

  materialization-inverso-test-transaction

  materialization-store-layout-changelog-md'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855@sha256:a8bd1bc222432a68c341ac4d05172f4d90b096816b97396de643d1813b464046
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: f35c1f0ccdbb3f87e7f4f0a294fd9b4b389736fb87769805f89b667f1ed4417f
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-gd24-api-test-transaction

  materialization-gd24-documents-apply-batch

  materialization-gd24-documents-batch-report

  materialization-guardas-apply-batch

  materialization-inverso-apply-batch

  materialization-inverso-batch-report

  materialization-inverso-test-transaction

  materialization-store-layout-changelog-md'
# ISO 8601 timestamp
created_at: '2026-11-16T20:33:54.985380+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T20:33:54.985380+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-gd24-api-test-transaction, materialization-gd24-documents-apply-batch, materialization-gd24-documents-batch-report, materialization-guardas-apply-batch, materialization-inverso-apply-batch, materialization-inverso-batch-report, materialization-inverso-test-transaction, materialization-store-layout-changelog-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-gd24-api-test-transaction
materialization-gd24-documents-apply-batch
materialization-gd24-documents-batch-report
materialization-guardas-apply-batch
materialization-inverso-apply-batch
materialization-inverso-batch-report
materialization-inverso-test-transaction
materialization-store-layout-changelog-md
