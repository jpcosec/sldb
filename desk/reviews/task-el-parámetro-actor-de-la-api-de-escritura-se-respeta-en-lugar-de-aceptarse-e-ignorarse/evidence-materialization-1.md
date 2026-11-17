---
sldb:
  by: agent
  at: '2026-11-17T15:48:18Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-actor-anchor-docs

  materialization-actor-test-provenance

  materialization-store-layout-changelog-md'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse@sha256:71a79a181a28e2a85148eb417c330671de135f6a2b1e2d935f3c39af9e97b5bf
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: b90c88f2adc7d87588d8ab809ce84a98cfe3558bc44db4d23f6981ce06301a3f
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-actor-anchor-docs

  materialization-actor-test-provenance

  materialization-store-layout-changelog-md'
# ISO 8601 timestamp
created_at: '2026-11-17T15:47:47.935763+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T15:47:47.935763+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-actor-anchor-docs, materialization-actor-test-provenance, materialization-store-layout-changelog-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-actor-anchor-docs
materialization-actor-test-provenance
materialization-store-layout-changelog-md
