---
sldb:
  by: agent
  at: '2026-11-17T13:22:16Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari-evidence-commit-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: d49f6ddc96d0081642fddd70769f50bfb26c5b3c
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari@sha256:d72b7a8add49d5bc6a028fbe583edabe734d7f8997b0126d92acae85d3fcf216
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: bca2a25478a5b0801312c73447396009ec28428f1f4b8a4f494b22e23e4fba1f
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit d49f6ddc96d0081642fddd70769f50bfb26c5b3c'
# ISO 8601 timestamp
created_at: '2026-11-17T13:21:55.248635+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T13:21:55.248635+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: d49f6ddc96d0081642fddd70769f50bfb26c5b3c

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit d49f6ddc96d0081642fddd70769f50bfb26c5b3c
