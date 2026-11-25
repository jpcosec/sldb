---
sldb:
  by: agent
  at: '2026-11-25T23:54:19Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/sldb/api/documents/apply_batch.py

  src/sldb/api/documents/batch_edges.py

  src/sldb/api/documents/batch_report.py

  src/sldb/mcp/write/apply.py

  src/sldb/mcp/write/findings.py

  src/sldb/mcp/write/pending.py

  src/sldb/mcp/write/pendings.py

  src/sldb/mcp/write/tools.py

  src/sldb/store/edge_index/doc_kinds.py

  src/sldb/store/edge_index/resolve.py

  tests/mcp/test_write_tools.py

  tests/test_mcp_propose_rejects_invalid_edges.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond@sha256:fdf123e910c926502b8aa78c35bac404ff6e9ebbac73c9772bbf68ffa60e4a65
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 4634f2d6d4bb60ddbfc865855ba01f4c2cea2c3024e4da9e5783c06ca94ec906
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/sldb/api/documents/apply_batch.py

  src/sldb/api/documents/batch_edges.py

  src/sldb/api/documents/batch_report.py

  src/sldb/mcp/write/apply.py

  src/sldb/mcp/write/findings.py

  src/sldb/mcp/write/pending.py

  src/sldb/mcp/write/pendings.py

  src/sldb/mcp/write/tools.py

  src/sldb/store/edge_index/doc_kinds.py

  src/sldb/store/edge_index/resolve.py

  tests/mcp/test_write_tools.py

  tests/test_mcp_propose_rejects_invalid_edges.py'
# ISO 8601 timestamp
created_at: '2026-11-25T23:54:16.556962+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T23:54:16.556962+00:00'
disposed_by: sldb
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/sldb/api/documents/apply_batch.py, src/sldb/api/documents/batch_edges.py, src/sldb/api/documents/batch_report.py, src/sldb/mcp/write/apply.py, src/sldb/mcp/write/findings.py, src/sldb/mcp/write/pending.py, src/sldb/mcp/write/pendings.py, src/sldb/mcp/write/tools.py, src/sldb/store/edge_index/doc_kinds.py, src/sldb/store/edge_index/resolve.py, tests/mcp/test_write_tools.py, tests/test_mcp_propose_rejects_invalid_edges.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/sldb/api/documents/apply_batch.py
src/sldb/api/documents/batch_edges.py
src/sldb/api/documents/batch_report.py
src/sldb/mcp/write/apply.py
src/sldb/mcp/write/findings.py
src/sldb/mcp/write/pending.py
src/sldb/mcp/write/pendings.py
src/sldb/mcp/write/tools.py
src/sldb/store/edge_index/doc_kinds.py
src/sldb/store/edge_index/resolve.py
tests/mcp/test_write_tools.py
tests/test_mcp_propose_rejects_invalid_edges.py
