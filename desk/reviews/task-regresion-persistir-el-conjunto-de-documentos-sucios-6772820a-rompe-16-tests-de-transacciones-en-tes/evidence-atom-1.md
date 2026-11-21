---
sldb:
  by: agent
  at: '2026-11-21T14:28:29Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes-evidence-atom-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: atom
# kind evidence only: what the producer verified, one item per line
value: atom-el-rollback-de-una-transaccion-restaura-el-conjunto-sucio-persistido
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes@sha256:ce88129bccde4e084f425e487c4e688e2dc5cb97695416a86f8cf861f81ad698
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: ec21ee89254e353c95d64b9113ffd251a048ce6f37e8869410a4e858a9a89383
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: atom atom-el-rollback-de-una-transaccion-restaura-el-conjunto-sucio-persistido'
# ISO 8601 timestamp
created_at: '2026-11-21T14:28:06.978423+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T14:28:06.978423+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence atom of task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked atom: atom-el-rollback-de-una-transaccion-restaura-el-conjunto-sucio-persistido

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: atom atom-el-rollback-de-una-transaccion-restaura-el-conjunto-sucio-persistido
