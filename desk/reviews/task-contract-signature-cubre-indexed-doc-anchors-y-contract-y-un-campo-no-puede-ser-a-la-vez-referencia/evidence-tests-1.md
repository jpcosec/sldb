---
sldb:
  by: agent
  at: '2026-11-17T01:07:02Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-contract-signature-cubre-indexed-doc-anchors-y-contract-y-un-campo-no-puede-ser-a-la-vez-referencia-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'tests/api/test_doc_anchors.py

  tests/store/test_payload_projection.py

  tests/test_clean_code_rules.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-contract-signature-cubre-indexed-doc-anchors-y-contract-y-un-campo-no-puede-ser-a-la-vez-referencia@sha256:7e28fb89fb226e2bddf128834e25d52650cf61d8281645c99e27dfacc831e109
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 8fb2326cf4407361edb1fb5edece782ec69e484d041859d020df9b5e4d1d0a07
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/api/test_doc_anchors.py

  tests/store/test_payload_projection.py

  tests/test_clean_code_rules.py'
# ISO 8601 timestamp
created_at: '2026-11-17T01:07:00.979942+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T01:07:00.979942+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-contract-signature-cubre-indexed-doc-anchors-y-contract-y-un-campo-no-puede-ser-a-la-vez-referencia

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/api/test_doc_anchors.py, tests/store/test_payload_projection.py, tests/test_clean_code_rules.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/api/test_doc_anchors.py
tests/store/test_payload_projection.py
tests/test_clean_code_rules.py
