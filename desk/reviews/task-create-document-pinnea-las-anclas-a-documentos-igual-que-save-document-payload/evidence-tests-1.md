---
sldb:
  by: agent
  at: '2026-11-16T11:11:40Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: tests/api/test_doc_anchors.py
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload@sha256:cbc510344b2d66390dc7bb7f9d8489c1d97fd6ecb4834e045f02bc77a01668c4
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: f2087c5c80d43e87154c56998c0c7110a42e932438be028b3029c205b072645b
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/api/test_doc_anchors.py'
# ISO 8601 timestamp
created_at: '2026-11-16T11:11:31.725935+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T11:11:31.725935+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/api/test_doc_anchors.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/api/test_doc_anchors.py
