---
sldb:
  by: agent
  at: '2026-11-20T02:58:29Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/sldb/api/stores/build_store.py

  src/sldb/store/edge_index/cache_keys.py

  src/sldb/store/edge_index/composed_disk.py

  src/sldb/store/layout.py

  tests/api/test_select_documents_disk.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen@sha256:24aeda8cbd7345c18287e275ee55e1a0424cd0f04b156d025f8cbd586adbb678
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 22198b817bde6bf8cac69836ba450f15b8bc63f8f9a838e7d9c9a048724e4a72
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/sldb/api/stores/build_store.py

  src/sldb/store/edge_index/cache_keys.py

  src/sldb/store/edge_index/composed_disk.py

  src/sldb/store/layout.py

  tests/api/test_select_documents_disk.py'
# ISO 8601 timestamp
created_at: '2026-11-20T02:58:27.295484+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T02:58:27.295484+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-el-sldb-cache-del-repo-deja-a-deskops-con-una-vista-vieja-de-los-reviewdoc-recibos-aceptados-no-cuen

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/sldb/api/stores/build_store.py, src/sldb/store/edge_index/cache_keys.py, src/sldb/store/edge_index/composed_disk.py, src/sldb/store/layout.py, tests/api/test_select_documents_disk.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/sldb/api/stores/build_store.py
src/sldb/store/edge_index/cache_keys.py
src/sldb/store/edge_index/composed_disk.py
src/sldb/store/layout.py
tests/api/test_select_documents_disk.py
