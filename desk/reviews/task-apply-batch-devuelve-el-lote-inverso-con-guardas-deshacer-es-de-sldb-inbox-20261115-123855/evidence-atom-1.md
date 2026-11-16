---
sldb:
  by: agent
  at: '2026-11-16T20:34:21Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855-evidence-atom-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: atom
# kind evidence only: what the producer verified, one item per line
value: atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855@sha256:a8bd1bc222432a68c341ac4d05172f4d90b096816b97396de643d1813b464046
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 68030b3e9f6f1e2f9c5bf1f17fd53a3cd629bb672914045f34800763c902fae1
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: atom atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas'
# ISO 8601 timestamp
created_at: '2026-11-16T20:33:54.985380+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T20:33:54.985380+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence atom of task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked atom: atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: atom atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
