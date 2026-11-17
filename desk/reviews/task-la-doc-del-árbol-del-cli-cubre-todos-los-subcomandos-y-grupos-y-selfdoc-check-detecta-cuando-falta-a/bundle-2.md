---
sldb:
  by: agent
  at: '2026-11-17T15:10:52Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a-bundle-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a@sha256:e82eab592fdde1b1fcf9cbe167719b4ef030db2bded3d957cc23415e9aa64155
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261117-150536/context-review/task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a/bundle/ba68bcaab1da63cb599d1a184185f1f9609aa771dc0f9666db9191605d28a827/attempt-1
input_sha256: ba68bcaab1da63cb599d1a184185f1f9609aa771dc0f9666db9191605d28a827
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 4d59666d0ed690d2d52026d880c02132389463962e0c1379bf176bcf0bca33eb
output_sha256: 619f238d32d1f3b386c461d10c412cb6e5b619d2fe20da6f839d4c71c442ddb2
# pending | accepted | rejected | incomplete
verdict: rejected
reason: 'Error del coordinador en bundle-1: la doc usa un bloque de árbol, no spans
  `sldb ...`. Se corrige en scope.'
# ISO 8601 timestamp
created_at: '2026-11-17T15:05:53.037888+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T15:10:26.311080+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-150536/context-review/task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a/bundle/ba68bcaab1da63cb599d1a184185f1f9609aa771dc0f9666db9191605d28a827/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict rejected: Error del coordinador en bundle-1: la doc usa un bloque de árbol, no spans `sldb ...`. Se corrige en scope.
