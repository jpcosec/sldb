---
sldb:
  by: agent
  at: '2026-11-17T06:46:58Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl-bundle-4
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl@sha256:c9868bb25f7dfe00e38e9bcf620e1070832225165a0f1ca780e3f005bf877c36
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261117-064444/context-review/task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl/bundle/6cdb2bae6fa39ddd1fc3cdc42602ffe7a49ac25a40b0c141dc29a0cf56f58d97/attempt-1
input_sha256: 6cdb2bae6fa39ddd1fc3cdc42602ffe7a49ac25a40b0c141dc29a0cf56f58d97
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 9a0002428edd29ccd04f5ceb7e9774ce1b732e6825929eb51be2e5accf80391e
output_sha256: 8af319f8b007b7ac1ec83e70da670831ab5bba0c64e8568d72c6c46845a778f5
# pending | accepted | rejected | incomplete
verdict: accepted
reason: Contrato con pglast. Las dudas se resuelven en el brief del ejecutor. Sin
  el extra se usa la lectura de tree-sitter de HEAD, sin lectura textual de claves;
  attrs.keys_partial va solo en el hecho de la tabla, cuando la sentencia tuvo nodos
  ERROR o pglast no la parseó. Los bordes son los de runs/subagents/20261116-test-k2,
  test-k2-c1 y test-k2-c2. references conserva el esquema como viene escrito y la
  relación apunta al hecho de la tabla con ese qualified_name. El sufijo ~N cuenta
  por tipo dentro de la tabla. La entrada del CHANGELOG se reescribe a mano. El parche
  existe en el run-dir citado y se aplica con git apply.
# ISO 8601 timestamp
created_at: '2026-11-17T06:44:57.963744+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T06:46:31.691162+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-064444/context-review/task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl/bundle/6cdb2bae6fa39ddd1fc3cdc42602ffe7a49ac25a40b0c141dc29a0cf56f58d97/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Contrato con pglast. Las dudas se resuelven en el brief del ejecutor. Sin el extra se usa la lectura de tree-sitter de HEAD, sin lectura textual de claves; attrs.keys_partial va solo en el hecho de la tabla, cuando la sentencia tuvo nodos ERROR o pglast no la parseó. Los bordes son los de runs/subagents/20261116-test-k2, test-k2-c1 y test-k2-c2. references conserva el esquema como viene escrito y la relación apunta al hecho de la tabla con ese qualified_name. El sufijo ~N cuenta por tipo dentro de la tabla. La entrada del CHANGELOG se reescribe a mano. El parche existe en el run-dir citado y se aplica con git apply.
