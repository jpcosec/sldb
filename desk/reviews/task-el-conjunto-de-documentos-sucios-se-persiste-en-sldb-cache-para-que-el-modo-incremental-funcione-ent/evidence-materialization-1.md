---
sldb:
  by: agent
  at: '2026-11-21T12:17:38Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-cache-contracts-layers-toml

  materialization-filas-de-documentos-en-disco-contracts-layers-toml

  materialization-k1-layers

  materialization-lk-md-layers

  materialization-store-contracts-layers-toml

  materialization-store-layout-changelog-md

  materialization-store-src-sldb-store-documents-dirty-persist-py

  materialization-store-src-sldb-store-documents-dirty-py

  materialization-store-tests-store-test-merkle-operation-cache-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent@sha256:3770c013b43ad163e28bc351be7746ffdb508ce16eadf21c40ea26c23e190b03
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: b1960bdfef6d19bf5384d473a3bf9e60aa7a8a63d96bf2fcbec0d9f4516868c9
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-cache-contracts-layers-toml

  materialization-filas-de-documentos-en-disco-contracts-layers-toml

  materialization-k1-layers

  materialization-lk-md-layers

  materialization-store-contracts-layers-toml

  materialization-store-layout-changelog-md

  materialization-store-src-sldb-store-documents-dirty-persist-py

  materialization-store-src-sldb-store-documents-dirty-py

  materialization-store-tests-store-test-merkle-operation-cache-py'
# ISO 8601 timestamp
created_at: '2026-11-21T12:17:05.605559+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T12:17:05.605559+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-cache-contracts-layers-toml, materialization-filas-de-documentos-en-disco-contracts-layers-toml, materialization-k1-layers, materialization-lk-md-layers, materialization-store-contracts-layers-toml, materialization-store-layout-changelog-md, materialization-store-src-sldb-store-documents-dirty-persist-py, materialization-store-src-sldb-store-documents-dirty-py, materialization-store-tests-store-test-merkle-operation-cache-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-cache-contracts-layers-toml
materialization-filas-de-documentos-en-disco-contracts-layers-toml
materialization-k1-layers
materialization-lk-md-layers
materialization-store-contracts-layers-toml
materialization-store-layout-changelog-md
materialization-store-src-sldb-store-documents-dirty-persist-py
materialization-store-src-sldb-store-documents-dirty-py
materialization-store-tests-store-test-merkle-operation-cache-py
