---
sldb:
  by: agent
  at: '2026-11-19T15:50:54Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document-reproduction-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: reproduction
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document@sha256:9c1cc3517ad9216b28e4845adc37b6476ebd2e169ba42ccd8d8790a13e42a57e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: human
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: a1d57cce85a80a0b966bb7dbd55b02ea2c5cc2cb3e0ea0b5cdbb7dbc96ea5000
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Reproduce: mediana caliente 2,48 s contra la meta de 1 s.'
# ISO 8601 timestamp
created_at: '2026-11-19T15:50:16.563879+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T15:50:31.014861+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Reproduction review of task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document

## Summary

_Summarize what was reviewed and the evidence this receipt records._

reproduction receipt recorded by sldb; evidence: runs/subagents/20261119-repro-views-board/repro.log

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Reproduce: mediana caliente 2,48 s contra la meta de 1 s.
