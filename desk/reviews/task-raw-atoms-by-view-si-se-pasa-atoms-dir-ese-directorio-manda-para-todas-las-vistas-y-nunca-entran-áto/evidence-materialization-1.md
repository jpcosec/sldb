---
sldb:
  by: agent
  at: '2026-11-20T15:31:24Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas-y-nunca-entran-áto-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-matching-src-sldb-api-matching-atoms-by-view-py

  materialization-matching-tests-matching-test-matching-refs-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas-y-nunca-entran-áto@sha256:b592fd17f2509f122f2936532a169f786be89efbd641b1f527c759030640ce67
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: bcf72f1aff6062faf8d74dc2c9ade646ee2704b25a1a72bcca7dd528d59713ab
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-matching-src-sldb-api-matching-atoms-by-view-py

  materialization-matching-tests-matching-test-matching-refs-py'
# ISO 8601 timestamp
created_at: '2026-11-20T15:30:55.335850+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T15:30:55.335850+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas-y-nunca-entran-áto

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-matching-src-sldb-api-matching-atoms-by-view-py, materialization-matching-tests-matching-test-matching-refs-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-matching-src-sldb-api-matching-atoms-by-view-py
materialization-matching-tests-matching-test-matching-refs-py
