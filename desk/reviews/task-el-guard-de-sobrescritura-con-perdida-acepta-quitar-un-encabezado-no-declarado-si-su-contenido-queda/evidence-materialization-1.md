---
sldb:
  by: agent
  at: '2026-11-22T13:59:10Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-api-src-sldb-api-documents-heading-scan-py

  materialization-api-src-sldb-api-documents-lossy-overwrite-py

  materialization-api-tests-api-test-lossy-overwrite-content-py

  materialization-guard-sin-perdida-lossy-overwrite

  materialization-store-layout-changelog-md'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda@sha256:aec627d411ec21dc15f44553dc70c5e8763579389465abfccfade872c812bd74
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: b0bd152f1b581cee97ae79a645fc4c1533c5bd04a5de0d68dbd90c4c12566f88
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-api-src-sldb-api-documents-heading-scan-py

  materialization-api-src-sldb-api-documents-lossy-overwrite-py

  materialization-api-tests-api-test-lossy-overwrite-content-py

  materialization-guard-sin-perdida-lossy-overwrite

  materialization-store-layout-changelog-md'
# ISO 8601 timestamp
created_at: '2026-11-22T13:58:37.208002+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T13:58:37.208002+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-api-src-sldb-api-documents-heading-scan-py, materialization-api-src-sldb-api-documents-lossy-overwrite-py, materialization-api-tests-api-test-lossy-overwrite-content-py, materialization-guard-sin-perdida-lossy-overwrite, materialization-store-layout-changelog-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-api-src-sldb-api-documents-heading-scan-py
materialization-api-src-sldb-api-documents-lossy-overwrite-py
materialization-api-tests-api-test-lossy-overwrite-content-py
materialization-guard-sin-perdida-lossy-overwrite
materialization-store-layout-changelog-md
