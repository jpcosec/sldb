---
sldb:
  by: agent
  at: '2026-11-25T21:42:54Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-sldb-responde-que-documentos-aplican-a-un-archivo-o-a-un-simbolo-sea-porque-lo-anclan-directo-o-porq-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-anchors-resolve-contracts-layers-toml

  materialization-anchors-resolve-src-sldb-api-anchors-init-py

  materialization-anchors-resolve-src-sldb-api-anchors-resolve-pointers-py

  materialization-anchors-resolve-src-sldb-api-anchors-tag-reach-py

  materialization-anchors-resolve-src-sldb-api-init-py

  materialization-anchors-resolve-src-sldb-mcp-read-tools-py

  materialization-anchors-resolve-src-sldb-mcp-registry-py

  materialization-anchors-resolve-src-sldb-models-code-anchor-doc-py

  materialization-anchors-resolve-tests-mcp-test-read-tools-py

  materialization-anchors-resolve-tests-test-where-pointers-resolve-py

  materialization-cache-contracts-layers-toml

  materialization-carga-tolerante-init

  materialization-filas-de-documentos-en-disco-contracts-layers-toml

  materialization-k1-anchors-init

  materialization-k1-layers

  materialization-lk-md-layers

  materialization-move-src-sldb-api-init-py

  materialization-read-store-init

  materialization-store-contracts-layers-toml

  materialization-sv01-src-sldb-api-init-py

  materialization-sv02-src-sldb-api-init-py

  materialization-sv04-src-sldb-api-init-py

  materialization-template-anchors-init

  materialization-undo-registry'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-responde-que-documentos-aplican-a-un-archivo-o-a-un-simbolo-sea-porque-lo-anclan-directo-o-porq@sha256:96ac9f85dc85ba5b91c43e59f8a1c0d20cd20dc11dafb43105880ffb384732d7
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 7b9e3942989d0e286b5a43b0b0a450632879008c7a210c4b0d66fb5624161e6c
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-anchors-resolve-contracts-layers-toml

  materialization-anchors-resolve-src-sldb-api-anchors-init-py

  materialization-anchors-resolve-src-sldb-api-anchors-resolve-pointers-py

  materialization-anchors-resolve-src-sldb-api-anchors-tag-reach-py

  materialization-anchors-resolve-src-sldb-api-init-py

  materialization-anchors-resolve-src-sldb-mcp-read-tools-py

  materialization-anchors-resolve-src-sldb-mcp-registry-py

  materialization-anchors-resolve-src-sldb-models-code-anchor-doc-py

  materialization-anchors-resolve-tests-mcp-test-read-tools-py

  materialization-anchors-resolve-tests-test-where-pointers-resolve-py

  materialization-cache-contracts-layers-toml

  materialization-carga-tolerante-init

  materialization-filas-de-documentos-en-disco-contracts-layers-toml

  materialization-k1-anchors-init

  materialization-k1-layers

  materialization-lk-md-layers

  materialization-move-src-sldb-api-init-py

  materialization-read-store-init

  materialization-store-contracts-layers-toml

  materialization-sv01-src-sldb-api-init-py

  materialization-sv02-src-sldb-api-init-py

  materialization-sv04-src-sldb-api-init-py

  materialization-template-anchors-init

  materialization-undo-registry'
# ISO 8601 timestamp
created_at: '2026-11-25T21:42:12.623731+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T21:42:12.623731+00:00'
disposed_by: sldb
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-sldb-responde-que-documentos-aplican-a-un-archivo-o-a-un-simbolo-sea-porque-lo-anclan-directo-o-porq

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-anchors-resolve-contracts-layers-toml, materialization-anchors-resolve-src-sldb-api-anchors-init-py, materialization-anchors-resolve-src-sldb-api-anchors-resolve-pointers-py, materialization-anchors-resolve-src-sldb-api-anchors-tag-reach-py, materialization-anchors-resolve-src-sldb-api-init-py, materialization-anchors-resolve-src-sldb-mcp-read-tools-py, materialization-anchors-resolve-src-sldb-mcp-registry-py, materialization-anchors-resolve-src-sldb-models-code-anchor-doc-py, materialization-anchors-resolve-tests-mcp-test-read-tools-py, materialization-anchors-resolve-tests-test-where-pointers-resolve-py, materialization-cache-contracts-layers-toml, materialization-carga-tolerante-init, materialization-filas-de-documentos-en-disco-contracts-layers-toml, materialization-k1-anchors-init, materialization-k1-layers, materialization-lk-md-layers, materialization-move-src-sldb-api-init-py, materialization-read-store-init, materialization-store-contracts-layers-toml, materialization-sv01-src-sldb-api-init-py, materialization-sv02-src-sldb-api-init-py, materialization-sv04-src-sldb-api-init-py, materialization-template-anchors-init, materialization-undo-registry

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-anchors-resolve-contracts-layers-toml
materialization-anchors-resolve-src-sldb-api-anchors-init-py
materialization-anchors-resolve-src-sldb-api-anchors-resolve-pointers-py
materialization-anchors-resolve-src-sldb-api-anchors-tag-reach-py
materialization-anchors-resolve-src-sldb-api-init-py
materialization-anchors-resolve-src-sldb-mcp-read-tools-py
materialization-anchors-resolve-src-sldb-mcp-registry-py
materialization-anchors-resolve-src-sldb-models-code-anchor-doc-py
materialization-anchors-resolve-tests-mcp-test-read-tools-py
materialization-anchors-resolve-tests-test-where-pointers-resolve-py
materialization-cache-contracts-layers-toml
materialization-carga-tolerante-init
materialization-filas-de-documentos-en-disco-contracts-layers-toml
materialization-k1-anchors-init
materialization-k1-layers
materialization-lk-md-layers
materialization-move-src-sldb-api-init-py
materialization-read-store-init
materialization-store-contracts-layers-toml
materialization-sv01-src-sldb-api-init-py
materialization-sv02-src-sldb-api-init-py
materialization-sv04-src-sldb-api-init-py
materialization-template-anchors-init
materialization-undo-registry
