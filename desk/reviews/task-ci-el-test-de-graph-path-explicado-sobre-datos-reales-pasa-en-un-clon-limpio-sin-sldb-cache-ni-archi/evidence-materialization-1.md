---
sldb:
  by: agent
  at: '2026-11-16T22:18:45Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-ci-el-test-de-graph-path-explicado-sobre-datos-reales-pasa-en-un-clon-limpio-sin-sldb-cache-ni-archi-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-b3-test-api-graph-analysis

  materialization-ci1-test-api-graph-analysis'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ci-el-test-de-graph-path-explicado-sobre-datos-reales-pasa-en-un-clon-limpio-sin-sldb-cache-ni-archi@sha256:bfe8ab2379a0faf82868b576bf1995d0f4cf75e9891ee6c606c642960f606933
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: f378db39894c4f38a5850aec761e2ef40d5a02f7efadd22d14ef9e44777abe1f
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-b3-test-api-graph-analysis

  materialization-ci1-test-api-graph-analysis'
# ISO 8601 timestamp
created_at: '2026-11-16T22:18:14.584301+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T22:18:14.584301+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-ci-el-test-de-graph-path-explicado-sobre-datos-reales-pasa-en-un-clon-limpio-sin-sldb-cache-ni-archi

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-b3-test-api-graph-analysis, materialization-ci1-test-api-graph-analysis

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-b3-test-api-graph-analysis
materialization-ci1-test-api-graph-analysis
