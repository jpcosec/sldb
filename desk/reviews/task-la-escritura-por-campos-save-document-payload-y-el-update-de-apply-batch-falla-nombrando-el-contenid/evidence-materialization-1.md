---
sldb:
  by: agent
  at: '2026-11-19T07:58:53Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-la-escritura-por-campos-save-document-payload-y-el-update-de-apply-batch-falla-nombrando-el-contenid-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-gd24-api-test-transaction

  materialization-inverso-test-transaction

  materialization-store-layout-changelog-md'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-escritura-por-campos-save-document-payload-y-el-update-de-apply-batch-falla-nombrando-el-contenid@sha256:58369861ff3c11497e48f3b55813f45dfc07146be418290de7500a3ef7dc3145
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: f125dcd4ce77829a97844dbd7f1bc944ce329467a268fa4befb68de9d49b94ba
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: rejected
reason: Changed file has no atom/materialization link and no routed follow-up reference.;
  Changed file has no atom/materialization link and no routed follow-up reference.;
  Changed file has no atom/materialization link and no routed follow-up reference.
# ISO 8601 timestamp
created_at: '2026-11-19T07:58:21.034465+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T07:58:21.034465+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-la-escritura-por-campos-save-document-payload-y-el-update-de-apply-batch-falla-nombrando-el-contenid

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-gd24-api-test-transaction, materialization-inverso-test-transaction, materialization-store-layout-changelog-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict rejected: Changed file has no atom/materialization link and no routed follow-up reference.; Changed file has no atom/materialization link and no routed follow-up reference.; Changed file has no atom/materialization link and no routed follow-up reference.
