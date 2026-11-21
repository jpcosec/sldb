---
sldb:
  by: agent
  at: '2026-11-21T14:28:09Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/sldb/api/documents/transaction_state.py

  src/sldb/store/documents_dirty.py

  src/sldb/store/documents_dirty_persist.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes@sha256:ce88129bccde4e084f425e487c4e688e2dc5cb97695416a86f8cf861f81ad698
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: af7dfa0add76abbcff89e814cc91c24f9872a20a865a9c7e1128e4980e0f26ec
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/sldb/api/documents/transaction_state.py

  src/sldb/store/documents_dirty.py

  src/sldb/store/documents_dirty_persist.py'
# ISO 8601 timestamp
created_at: '2026-11-21T14:28:06.978423+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T14:28:06.978423+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/sldb/api/documents/transaction_state.py, src/sldb/store/documents_dirty.py, src/sldb/store/documents_dirty_persist.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/sldb/api/documents/transaction_state.py
src/sldb/store/documents_dirty.py
src/sldb/store/documents_dirty_persist.py
