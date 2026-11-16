---
sldb:
  by: agent
  at: '2026-11-16T20:17:31Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-sldb-serve-list-views-deja-de-componer-el-índice-federado-de-toda-la-máquina-y-compose-edge-index-co-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-gd25-views-list-views

  materialization-leak-compose

  materialization-leak-list-views

  materialization-leak-test-shard-cache-copies

  materialization-leak-test-views-linked

  materialization-store-layout-changelog-md'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-serve-list-views-deja-de-componer-el-índice-federado-de-toda-la-máquina-y-compose-edge-index-co@sha256:55d0a37acc66dfd67921f46dc41514508e0b6a6d314fb26faa5a3c4c2f6de59c
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 52ad94eb0ded82bfb4771956eb2a8c1c126d40a1f6069a5a9aa83b501d6ec37f
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-gd25-views-list-views

  materialization-leak-compose

  materialization-leak-list-views

  materialization-leak-test-shard-cache-copies

  materialization-leak-test-views-linked

  materialization-store-layout-changelog-md'
# ISO 8601 timestamp
created_at: '2026-11-16T20:17:03.353444+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T20:17:03.353444+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-sldb-serve-list-views-deja-de-componer-el-índice-federado-de-toda-la-máquina-y-compose-edge-index-co

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-gd25-views-list-views, materialization-leak-compose, materialization-leak-list-views, materialization-leak-test-shard-cache-copies, materialization-leak-test-views-linked, materialization-store-layout-changelog-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-gd25-views-list-views
materialization-leak-compose
materialization-leak-list-views
materialization-leak-test-shard-cache-copies
materialization-leak-test-views-linked
materialization-store-layout-changelog-md
