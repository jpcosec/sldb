---
sldb:
  by: agent
  at: '2026-11-17T16:37:16Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-lk-md-parser

  materialization-lk-md-test-links

  materialization-store-layout-changelog-md'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com@sha256:14a64b8b9c449b99f9718d121ab66b24406035356b1eec58f51914adc6d430ff
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: fd7b727e75dd3f25a31b16bc15996818326a86cd4b8d8adb868429b8af539b79
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-lk-md-parser

  materialization-lk-md-test-links

  materialization-store-layout-changelog-md'
# ISO 8601 timestamp
created_at: '2026-11-17T16:36:11.287243+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T16:36:11.287243+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-lk-md-parser, materialization-lk-md-test-links, materialization-store-layout-changelog-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-lk-md-parser
materialization-lk-md-test-links
materialization-store-layout-changelog-md
