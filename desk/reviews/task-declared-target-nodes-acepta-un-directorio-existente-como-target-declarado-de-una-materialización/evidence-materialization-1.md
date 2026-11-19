---
sldb:
  by: agent
  at: '2026-11-19T12:13:35Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-directorio-declarado-declared-target-nodes

  materialization-directorio-declarado-test-project-graph

  materialization-gd21-api-test-project-graph

  materialization-store-layout-changelog-md'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización@sha256:7801bdaf8fa97e47299f7923f44ab8604480a0fcdc66253342012128ce9587a8
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 370f947b7b1a0e2d3edd3d2289a34dc88760be7c4ac1cb0dd187b70eba087777
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-directorio-declarado-declared-target-nodes

  materialization-directorio-declarado-test-project-graph

  materialization-gd21-api-test-project-graph

  materialization-store-layout-changelog-md'
# ISO 8601 timestamp
created_at: '2026-11-19T12:13:02.368923+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T12:13:02.368923+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-directorio-declarado-declared-target-nodes, materialization-directorio-declarado-test-project-graph, materialization-gd21-api-test-project-graph, materialization-store-layout-changelog-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-directorio-declarado-declared-target-nodes
materialization-directorio-declarado-test-project-graph
materialization-gd21-api-test-project-graph
materialization-store-layout-changelog-md
