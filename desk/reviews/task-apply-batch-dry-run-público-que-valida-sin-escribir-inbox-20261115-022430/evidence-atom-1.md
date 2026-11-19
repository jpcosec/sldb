---
sldb:
  by: agent
  at: '2026-11-19T04:39:33Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430-evidence-atom-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: atom
# kind evidence only: what the producer verified, one item per line
value: atom-apply-batch-con-dry-run-valida-un-lote-completo-sin-escribir-y-devuelve-lo-mismo-que-una-corrida-rea
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430@sha256:b89e4fa1a04ec92cc504e4a26665e01f75f1ac424f2b0080e680beaa2b92d841
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: eb7eab1ce7ea4803ba39c26edf2f5a5fe9f615be81ff703becf7b7798218edf6
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: atom atom-apply-batch-con-dry-run-valida-un-lote-completo-sin-escribir-y-devuelve-lo-mismo-que-una-corrida-rea'
# ISO 8601 timestamp
created_at: '2026-11-19T04:39:11.035171+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T04:39:11.035171+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence atom of task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked atom: atom-apply-batch-con-dry-run-valida-un-lote-completo-sin-escribir-y-devuelve-lo-mismo-que-una-corrida-rea

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: atom atom-apply-batch-con-dry-run-valida-un-lote-completo-sin-escribir-y-devuelve-lo-mismo-que-una-corrida-rea
