---
sldb:
  by: agent
  at: '2026-11-22T13:19:04Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-heading-scan-scan-heading-bodies-baja-a-10-lineas-de-logica-regla-de-codigo-limpio-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: materialization-api-src-sldb-api-documents-heading-scan-py
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-heading-scan-scan-heading-bodies-baja-a-10-lineas-de-logica-regla-de-codigo-limpio@sha256:a5b8c7ad43b120e0ae40802466ca7a73e0c1a561c475a52c06142fb88061d496
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 2869ff7b53d8c6e8fb34878b20317a7b04287a3499aa80d508b9262dd58f6d14
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-api-src-sldb-api-documents-heading-scan-py'
# ISO 8601 timestamp
created_at: '2026-11-22T13:18:31.232532+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T13:18:31.232532+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-heading-scan-scan-heading-bodies-baja-a-10-lineas-de-logica-regla-de-codigo-limpio

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-api-src-sldb-api-documents-heading-scan-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-api-src-sldb-api-documents-heading-scan-py
