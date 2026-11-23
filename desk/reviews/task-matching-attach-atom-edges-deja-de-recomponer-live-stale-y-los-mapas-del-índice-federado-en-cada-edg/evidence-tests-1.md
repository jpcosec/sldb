---
sldb:
  by: agent
  at: '2026-11-23T22:30:02Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/sldb/api/matching/store_edges.py

  src/sldb/api/matching/store_reader.py

  tests/matching/test_matching_refs.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg@sha256:d5c5e5be318f916e9957d3d7561678dd292981f37fd7a4d482fd2f76705d5a25
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 2b659cd8724f33af7be2d1c72a2ed5986a2f9c7f204a78fbe1b3fe5f87b7f149
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/sldb/api/matching/store_edges.py

  src/sldb/api/matching/store_reader.py

  tests/matching/test_matching_refs.py'
# ISO 8601 timestamp
created_at: '2026-11-23T22:30:00.563955+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T22:30:00.563955+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/sldb/api/matching/store_edges.py, src/sldb/api/matching/store_reader.py, tests/matching/test_matching_refs.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/sldb/api/matching/store_edges.py
src/sldb/api/matching/store_reader.py
tests/matching/test_matching_refs.py
