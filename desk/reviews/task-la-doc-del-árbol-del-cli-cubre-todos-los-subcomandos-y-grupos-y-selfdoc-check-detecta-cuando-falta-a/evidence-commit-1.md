---
sldb:
  by: agent
  at: '2026-11-21T10:25:06Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: b8e564c2956f1bf7f0ba8d1d942862231a85bf1f
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a@sha256:212b10f65d3321608feb155a22811af40e71526cf103baf36965f4347f096219
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: b04c03848931c77f8944275565e97f754e87a230307a684bb3314abc001c16b9
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit b8e564c2956f1bf7f0ba8d1d942862231a85bf1f'
# ISO 8601 timestamp
created_at: '2026-11-21T10:24:52.872211+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T10:24:52.872211+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: b8e564c2956f1bf7f0ba8d1d942862231a85bf1f

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit b8e564c2956f1bf7f0ba8d1d942862231a85bf1f
