---
sldb:
  by: agent
  at: '2026-11-17T01:22:45Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-sldb-api-expone-los-facts-de-código-de-un-archivo-o-de-un-árbol-con-span-y-source-hash-y-write-ancho-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-b2-test-anchors

  materialization-b2sql-c1-test-anchors

  materialization-k1-anchors-init

  materialization-k1-test-anchors

  materialization-store-layout-changelog-md'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-api-expone-los-facts-de-código-de-un-archivo-o-de-un-árbol-con-span-y-source-hash-y-write-ancho@sha256:9681b4f932387fca0828fdb21e202e047ebc523475e2be09458239cd7c4f45b9
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: bda4aafef87102bc4f5028b7ac06a4b1b6eb757e8bdfea734ac9e6b5e68a3fbc
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-b2-test-anchors

  materialization-b2sql-c1-test-anchors

  materialization-k1-anchors-init

  materialization-k1-test-anchors

  materialization-store-layout-changelog-md'
# ISO 8601 timestamp
created_at: '2026-11-17T01:21:51.174648+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T01:21:51.174648+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-sldb-api-expone-los-facts-de-código-de-un-archivo-o-de-un-árbol-con-span-y-source-hash-y-write-ancho

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-b2-test-anchors, materialization-b2sql-c1-test-anchors, materialization-k1-anchors-init, materialization-k1-test-anchors, materialization-store-layout-changelog-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-b2-test-anchors
materialization-b2sql-c1-test-anchors
materialization-k1-anchors-init
materialization-k1-test-anchors
materialization-store-layout-changelog-md
