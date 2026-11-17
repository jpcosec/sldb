---
sldb:
  by: agent
  at: '2026-11-17T13:17:31Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: materialization-store-layout-changelog-md
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari@sha256:d72b7a8add49d5bc6a028fbe583edabe734d7f8997b0126d92acae85d3fcf216
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 158acfa79ac3e1e9c3bfc5b64fee62b1f9d2b6e8087d724e9f4ebe6a1a6be12a
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: rejected
reason: Changed file has no atom/materialization link and no routed follow-up reference.
# ISO 8601 timestamp
created_at: '2026-11-17T13:16:57.294432+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T13:16:57.294432+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-store-layout-changelog-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict rejected: Changed file has no atom/materialization link and no routed follow-up reference.
