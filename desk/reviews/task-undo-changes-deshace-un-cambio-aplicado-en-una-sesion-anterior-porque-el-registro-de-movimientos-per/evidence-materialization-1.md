---
sldb:
  by: agent
  at: '2026-11-26T01:15:52Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior-porque-el-registro-de-movimientos-per-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-anchors-resolve-contracts-layers-toml

  materialization-anchors-resolve-src-sldb-api-init-py

  materialization-cache-contracts-layers-toml

  materialization-carga-tolerante-init

  materialization-filas-de-documentos-en-disco-contracts-layers-toml

  materialization-gd24-documents-apply-batch

  materialization-gd24-documents-batch-report

  materialization-guardas-apply-batch

  materialization-inverso-apply-batch

  materialization-inverso-batch-inverse

  materialization-inverso-batch-report

  materialization-k1-layers

  materialization-lk-md-layers

  materialization-mcp-gancho-server

  materialization-move-src-sldb-api-init-py

  materialization-propose-changes-valida-src-sldb-api-documents-apply-batch-py

  materialization-propose-changes-valida-src-sldb-api-documents-batch-report-py

  materialization-propose-changes-valida-src-sldb-mcp-write-apply-py

  materialization-propose-changes-valida-tests-mcp-test-write-tools-py

  materialization-read-store-init

  materialization-store-contracts-layers-toml

  materialization-store-layout-docs-architecture-journal-authority-md

  materialization-sv01-src-sldb-api-init-py

  materialization-sv02-src-sldb-api-init-py

  materialization-sv04-src-sldb-api-init-py

  materialization-template-anchors-init

  materialization-undo-apply

  materialization-undo-changes-sesiones-contracts-layers-toml

  materialization-undo-changes-sesiones-docs-architecture-journal-authority-md

  materialization-undo-changes-sesiones-src-sldb-api-documents-apply-batch-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-batch-inverse-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-batch-report-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-nothing-to-undo-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-provenance-stamp-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-undo-batches-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-undo-report-py

  materialization-undo-changes-sesiones-src-sldb-api-init-py

  materialization-undo-changes-sesiones-src-sldb-mcp-server-py

  materialization-undo-changes-sesiones-src-sldb-mcp-write-apply-py

  materialization-undo-changes-sesiones-src-sldb-mcp-write-undo-py

  materialization-undo-changes-sesiones-src-sldb-store-write-journal-py

  materialization-undo-changes-sesiones-tests-mcp-test-write-tools-py

  materialization-undo-changes-sesiones-tests-test-mcp-undo-across-sessions-py

  materialization-undo-server

  materialization-undo-test-write-tools

  materialization-undo-undo'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior-porque-el-registro-de-movimientos-per@sha256:81a2dbc0164b97e81b7c9a2b6dcba3f79a88c5b95740847e3968bed70e50f383
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 7908fe9485c393b1a3bc02b61aa03f448d48f933e8009240383a032e020c1166
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-anchors-resolve-contracts-layers-toml

  materialization-anchors-resolve-src-sldb-api-init-py

  materialization-cache-contracts-layers-toml

  materialization-carga-tolerante-init

  materialization-filas-de-documentos-en-disco-contracts-layers-toml

  materialization-gd24-documents-apply-batch

  materialization-gd24-documents-batch-report

  materialization-guardas-apply-batch

  materialization-inverso-apply-batch

  materialization-inverso-batch-inverse

  materialization-inverso-batch-report

  materialization-k1-layers

  materialization-lk-md-layers

  materialization-mcp-gancho-server

  materialization-move-src-sldb-api-init-py

  materialization-propose-changes-valida-src-sldb-api-documents-apply-batch-py

  materialization-propose-changes-valida-src-sldb-api-documents-batch-report-py

  materialization-propose-changes-valida-src-sldb-mcp-write-apply-py

  materialization-propose-changes-valida-tests-mcp-test-write-tools-py

  materialization-read-store-init

  materialization-store-contracts-layers-toml

  materialization-store-layout-docs-architecture-journal-authority-md

  materialization-sv01-src-sldb-api-init-py

  materialization-sv02-src-sldb-api-init-py

  materialization-sv04-src-sldb-api-init-py

  materialization-template-anchors-init

  materialization-undo-apply

  materialization-undo-changes-sesiones-contracts-layers-toml

  materialization-undo-changes-sesiones-docs-architecture-journal-authority-md

  materialization-undo-changes-sesiones-src-sldb-api-documents-apply-batch-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-batch-inverse-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-batch-report-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-nothing-to-undo-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-provenance-stamp-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-undo-batches-py

  materialization-undo-changes-sesiones-src-sldb-api-documents-undo-report-py

  materialization-undo-changes-sesiones-src-sldb-api-init-py

  materialization-undo-changes-sesiones-src-sldb-mcp-server-py

  materialization-undo-changes-sesiones-src-sldb-mcp-write-apply-py

  materialization-undo-changes-sesiones-src-sldb-mcp-write-undo-py

  materialization-undo-changes-sesiones-src-sldb-store-write-journal-py

  materialization-undo-changes-sesiones-tests-mcp-test-write-tools-py

  materialization-undo-changes-sesiones-tests-test-mcp-undo-across-sessions-py

  materialization-undo-server

  materialization-undo-test-write-tools

  materialization-undo-undo'
# ISO 8601 timestamp
created_at: '2026-11-26T01:15:17.611792+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-26T01:15:17.611792+00:00'
disposed_by: sldb
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior-porque-el-registro-de-movimientos-per

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-anchors-resolve-contracts-layers-toml, materialization-anchors-resolve-src-sldb-api-init-py, materialization-cache-contracts-layers-toml, materialization-carga-tolerante-init, materialization-filas-de-documentos-en-disco-contracts-layers-toml, materialization-gd24-documents-apply-batch, materialization-gd24-documents-batch-report, materialization-guardas-apply-batch, materialization-inverso-apply-batch, materialization-inverso-batch-inverse, materialization-inverso-batch-report, materialization-k1-layers, materialization-lk-md-layers, materialization-mcp-gancho-server, materialization-move-src-sldb-api-init-py, materialization-propose-changes-valida-src-sldb-api-documents-apply-batch-py, materialization-propose-changes-valida-src-sldb-api-documents-batch-report-py, materialization-propose-changes-valida-src-sldb-mcp-write-apply-py, materialization-propose-changes-valida-tests-mcp-test-write-tools-py, materialization-read-store-init, materialization-store-contracts-layers-toml, materialization-store-layout-docs-architecture-journal-authority-md, materialization-sv01-src-sldb-api-init-py, materialization-sv02-src-sldb-api-init-py, materialization-sv04-src-sldb-api-init-py, materialization-template-anchors-init, materialization-undo-apply, materialization-undo-changes-sesiones-contracts-layers-toml, materialization-undo-changes-sesiones-docs-architecture-journal-authority-md, materialization-undo-changes-sesiones-src-sldb-api-documents-apply-batch-py, materialization-undo-changes-sesiones-src-sldb-api-documents-batch-inverse-py, materialization-undo-changes-sesiones-src-sldb-api-documents-batch-report-py, materialization-undo-changes-sesiones-src-sldb-api-documents-nothing-to-undo-py, materialization-undo-changes-sesiones-src-sldb-api-documents-provenance-stamp-py, materialization-undo-changes-sesiones-src-sldb-api-documents-undo-batches-py, materialization-undo-changes-sesiones-src-sldb-api-documents-undo-report-py, materialization-undo-changes-sesiones-src-sldb-api-init-py, materialization-undo-changes-sesiones-src-sldb-mcp-server-py, materialization-undo-changes-sesiones-src-sldb-mcp-write-apply-py, materialization-undo-changes-sesiones-src-sldb-mcp-write-undo-py, materialization-undo-changes-sesiones-src-sldb-store-write-journal-py, materialization-undo-changes-sesiones-tests-mcp-test-write-tools-py, materialization-undo-changes-sesiones-tests-test-mcp-undo-across-sessions-py, materialization-undo-server, materialization-undo-test-write-tools, materialization-undo-undo

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-anchors-resolve-contracts-layers-toml
materialization-anchors-resolve-src-sldb-api-init-py
materialization-cache-contracts-layers-toml
materialization-carga-tolerante-init
materialization-filas-de-documentos-en-disco-contracts-layers-toml
materialization-gd24-documents-apply-batch
materialization-gd24-documents-batch-report
materialization-guardas-apply-batch
materialization-inverso-apply-batch
materialization-inverso-batch-inverse
materialization-inverso-batch-report
materialization-k1-layers
materialization-lk-md-layers
materialization-mcp-gancho-server
materialization-move-src-sldb-api-init-py
materialization-propose-changes-valida-src-sldb-api-documents-apply-batch-py
materialization-propose-changes-valida-src-sldb-api-documents-batch-report-py
materialization-propose-changes-valida-src-sldb-mcp-write-apply-py
materialization-propose-changes-valida-tests-mcp-test-write-tools-py
materialization-read-store-init
materialization-store-contracts-layers-toml
materialization-store-layout-docs-architecture-journal-authority-md
materialization-sv01-src-sldb-api-init-py
materialization-sv02-src-sldb-api-init-py
materialization-sv04-src-sldb-api-init-py
materialization-template-anchors-init
materialization-undo-apply
materialization-undo-changes-sesiones-contracts-layers-toml
materialization-undo-changes-sesiones-docs-architecture-journal-authority-md
materialization-undo-changes-sesiones-src-sldb-api-documents-apply-batch-py
materialization-undo-changes-sesiones-src-sldb-api-documents-batch-inverse-py
materialization-undo-changes-sesiones-src-sldb-api-documents-batch-report-py
materialization-undo-changes-sesiones-src-sldb-api-documents-nothing-to-undo-py
materialization-undo-changes-sesiones-src-sldb-api-documents-provenance-stamp-py
materialization-undo-changes-sesiones-src-sldb-api-documents-undo-batches-py
materialization-undo-changes-sesiones-src-sldb-api-documents-undo-report-py
materialization-undo-changes-sesiones-src-sldb-api-init-py
materialization-undo-changes-sesiones-src-sldb-mcp-server-py
materialization-undo-changes-sesiones-src-sldb-mcp-write-apply-py
materialization-undo-changes-sesiones-src-sldb-mcp-write-undo-py
materialization-undo-changes-sesiones-src-sldb-store-write-journal-py
materialization-undo-changes-sesiones-tests-mcp-test-write-tools-py
materialization-undo-changes-sesiones-tests-test-mcp-undo-across-sessions-py
materialization-undo-server
materialization-undo-test-write-tools
materialization-undo-undo
