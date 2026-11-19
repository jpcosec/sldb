---
sldb:
  by: agent
  at: '2026-11-19T11:46:55Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización@sha256:7801bdaf8fa97e47299f7923f44ab8604480a0fcdc66253342012128ce9587a8
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261119-114252/context-review/task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización/preflight/7417c2253b47c87c26f0596feb05d5259d91104beb92b7916e0206675721be30/attempt-1
input_sha256: 7417c2253b47c87c26f0596feb05d5259d91104beb92b7916e0206675721be30
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 669ae92039686b546b9ec0600bc10d8632a44e8df3ffd355259535daf97cf8a7
output_sha256: 34cbef638d03bf35916c6d8ffdf93e47893d60c6f914e6baf2c888e62b3bae70
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador: 1) Se reusa FileNode (src/sldb/api/edges/project_graph/file_node.py,
  id ''kind:path'') con file_kind ''directory'' y el kind que da la regla; no hay
  clase nueva, y por eso file_node.py entra en el alcance. 2) Ver 1. 3) La ruta se
  resuelve como la de los archivos declarados (declared_file_targets.py), relativa
  a la raíz del proyecto. Un directorio existente dentro de la raíz, también vía symlink,
  genera nodo; fuera de la raíz o inexistente sigue missing. Aplican las FileExclusions
  como a los archivos. 4) Lo missing sale de missing_project_target.py y missing_target_kind.py
  del mismo paquete; deskops lo reporta como missing_declared_target (deskops/graph/checks.py:117).
  Con el nodo de directorio presente deja de aparecer. 5) CHANGELOG: una viñeta en
  la sección sin publicar. Commit con rutas nombradas y trailer ''Task-Id: <id>''.
  6) El aviso a deskops lo manda el integrador tras integrar.'
# ISO 8601 timestamp
created_at: '2026-11-19T11:43:10.194061+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T11:46:33.488638+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261119-114252/context-review/task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización/preflight/7417c2253b47c87c26f0596feb05d5259d91104beb92b7916e0206675721be30/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) Se reusa FileNode (src/sldb/api/edges/project_graph/file_node.py, id 'kind:path') con file_kind 'directory' y el kind que da la regla; no hay clase nueva, y por eso file_node.py entra en el alcance. 2) Ver 1. 3) La ruta se resuelve como la de los archivos declarados (declared_file_targets.py), relativa a la raíz del proyecto. Un directorio existente dentro de la raíz, también vía symlink, genera nodo; fuera de la raíz o inexistente sigue missing. Aplican las FileExclusions como a los archivos. 4) Lo missing sale de missing_project_target.py y missing_target_kind.py del mismo paquete; deskops lo reporta como missing_declared_target (deskops/graph/checks.py:117). Con el nodo de directorio presente deja de aparecer. 5) CHANGELOG: una viñeta en la sección sin publicar. Commit con rutas nombradas y trailer 'Task-Id: <id>'. 6) El aviso a deskops lo manda el integrador tras integrar.
