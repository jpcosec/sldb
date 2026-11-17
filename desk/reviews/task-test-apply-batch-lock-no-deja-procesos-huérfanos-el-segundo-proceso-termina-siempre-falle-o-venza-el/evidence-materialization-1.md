---
sldb:
  by: agent
  at: '2026-11-17T14:00:47Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-test-apply-batch-lock-no-deja-procesos-huérfanos-el-segundo-proceso-termina-siempre-falle-o-venza-el-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-guardas-test-apply-batch-lock

  materialization-orph-test-apply-batch-lock'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-test-apply-batch-lock-no-deja-procesos-huérfanos-el-segundo-proceso-termina-siempre-falle-o-venza-el@sha256:751cc7a5d72b7f031432a48f3ad726cc3fd5119fe68afb64d890b2a3cbc09a43
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 47a20807b3e1067254a2aeb88aa53a57520407170ca2bccb3c1c78b223762005
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-guardas-test-apply-batch-lock

  materialization-orph-test-apply-batch-lock'
# ISO 8601 timestamp
created_at: '2026-11-17T14:00:16.593695+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T14:00:16.593695+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-test-apply-batch-lock-no-deja-procesos-huérfanos-el-segundo-proceso-termina-siempre-falle-o-venza-el

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-guardas-test-apply-batch-lock, materialization-orph-test-apply-batch-lock

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-guardas-test-apply-batch-lock
materialization-orph-test-apply-batch-lock
