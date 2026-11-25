---
sldb:
  by: agent
  at: '2026-11-25T23:54:52Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-c5-mcp-tools

  materialization-gd24-documents-apply-batch

  materialization-gd24-documents-batch-report

  materialization-guardas-apply-batch

  materialization-inverso-apply-batch

  materialization-inverso-batch-report

  materialization-mcp-gancho-tools

  materialization-propose-changes-valida-src-sldb-api-documents-apply-batch-py

  materialization-propose-changes-valida-src-sldb-api-documents-batch-edges-py

  materialization-propose-changes-valida-src-sldb-api-documents-batch-report-py

  materialization-propose-changes-valida-src-sldb-mcp-write-apply-py

  materialization-propose-changes-valida-src-sldb-mcp-write-findings-py

  materialization-propose-changes-valida-src-sldb-mcp-write-pending-py

  materialization-propose-changes-valida-src-sldb-mcp-write-pendings-py

  materialization-propose-changes-valida-src-sldb-mcp-write-tools-py

  materialization-propose-changes-valida-src-sldb-store-edge-index-doc-kinds-py

  materialization-propose-changes-valida-src-sldb-store-edge-index-resolve-py

  materialization-propose-changes-valida-tests-mcp-test-write-tools-py

  materialization-propose-changes-valida-tests-test-mcp-propose-rejects-invalid-edges-py

  materialization-undo-apply

  materialization-undo-pending

  materialization-undo-test-write-tools

  materialization-undo-tools'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond@sha256:fdf123e910c926502b8aa78c35bac404ff6e9ebbac73c9772bbf68ffa60e4a65
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 52078fe84965ec059ae9d339c75a80e783f4a514fafd261ffc98cde17b47b4af
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-c5-mcp-tools

  materialization-gd24-documents-apply-batch

  materialization-gd24-documents-batch-report

  materialization-guardas-apply-batch

  materialization-inverso-apply-batch

  materialization-inverso-batch-report

  materialization-mcp-gancho-tools

  materialization-propose-changes-valida-src-sldb-api-documents-apply-batch-py

  materialization-propose-changes-valida-src-sldb-api-documents-batch-edges-py

  materialization-propose-changes-valida-src-sldb-api-documents-batch-report-py

  materialization-propose-changes-valida-src-sldb-mcp-write-apply-py

  materialization-propose-changes-valida-src-sldb-mcp-write-findings-py

  materialization-propose-changes-valida-src-sldb-mcp-write-pending-py

  materialization-propose-changes-valida-src-sldb-mcp-write-pendings-py

  materialization-propose-changes-valida-src-sldb-mcp-write-tools-py

  materialization-propose-changes-valida-src-sldb-store-edge-index-doc-kinds-py

  materialization-propose-changes-valida-src-sldb-store-edge-index-resolve-py

  materialization-propose-changes-valida-tests-mcp-test-write-tools-py

  materialization-propose-changes-valida-tests-test-mcp-propose-rejects-invalid-edges-py

  materialization-undo-apply

  materialization-undo-pending

  materialization-undo-test-write-tools

  materialization-undo-tools'
# ISO 8601 timestamp
created_at: '2026-11-25T23:54:16.556962+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T23:54:16.556962+00:00'
disposed_by: sldb
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-c5-mcp-tools, materialization-gd24-documents-apply-batch, materialization-gd24-documents-batch-report, materialization-guardas-apply-batch, materialization-inverso-apply-batch, materialization-inverso-batch-report, materialization-mcp-gancho-tools, materialization-propose-changes-valida-src-sldb-api-documents-apply-batch-py, materialization-propose-changes-valida-src-sldb-api-documents-batch-edges-py, materialization-propose-changes-valida-src-sldb-api-documents-batch-report-py, materialization-propose-changes-valida-src-sldb-mcp-write-apply-py, materialization-propose-changes-valida-src-sldb-mcp-write-findings-py, materialization-propose-changes-valida-src-sldb-mcp-write-pending-py, materialization-propose-changes-valida-src-sldb-mcp-write-pendings-py, materialization-propose-changes-valida-src-sldb-mcp-write-tools-py, materialization-propose-changes-valida-src-sldb-store-edge-index-doc-kinds-py, materialization-propose-changes-valida-src-sldb-store-edge-index-resolve-py, materialization-propose-changes-valida-tests-mcp-test-write-tools-py, materialization-propose-changes-valida-tests-test-mcp-propose-rejects-invalid-edges-py, materialization-undo-apply, materialization-undo-pending, materialization-undo-test-write-tools, materialization-undo-tools

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-c5-mcp-tools
materialization-gd24-documents-apply-batch
materialization-gd24-documents-batch-report
materialization-guardas-apply-batch
materialization-inverso-apply-batch
materialization-inverso-batch-report
materialization-mcp-gancho-tools
materialization-propose-changes-valida-src-sldb-api-documents-apply-batch-py
materialization-propose-changes-valida-src-sldb-api-documents-batch-edges-py
materialization-propose-changes-valida-src-sldb-api-documents-batch-report-py
materialization-propose-changes-valida-src-sldb-mcp-write-apply-py
materialization-propose-changes-valida-src-sldb-mcp-write-findings-py
materialization-propose-changes-valida-src-sldb-mcp-write-pending-py
materialization-propose-changes-valida-src-sldb-mcp-write-pendings-py
materialization-propose-changes-valida-src-sldb-mcp-write-tools-py
materialization-propose-changes-valida-src-sldb-store-edge-index-doc-kinds-py
materialization-propose-changes-valida-src-sldb-store-edge-index-resolve-py
materialization-propose-changes-valida-tests-mcp-test-write-tools-py
materialization-propose-changes-valida-tests-test-mcp-propose-rejects-invalid-edges-py
materialization-undo-apply
materialization-undo-pending
materialization-undo-test-write-tools
materialization-undo-tools
