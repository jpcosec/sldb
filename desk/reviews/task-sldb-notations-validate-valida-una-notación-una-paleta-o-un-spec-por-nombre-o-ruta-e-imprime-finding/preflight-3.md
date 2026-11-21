---
sldb:
  by: agent
  at: '2026-11-21T02:17:19Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding-preflight-3
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding@sha256:b770e3dd0684cff0c7d65a4baea0f68fe0dcf06a21d0016f973e5eb7e3d1b156
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-021501/context-review/task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding/preflight/7cfc8192d326d04549fbb44055babc485dfaf7384cc49224b36f52e3f42699d5/attempt-1
input_sha256: 7cfc8192d326d04549fbb44055babc485dfaf7384cc49224b36f52e3f42699d5
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: e4432a8d7c60223f5d30f9d98fac74798c97816d15419eff7472ba1cd81ab97d
output_sha256: 391a7582b0b98cccb8f0adf113c9227985ecc95fead37903fb556eeb3fd49865
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador (mandan sobre Scope, Convenciones
  y el pill donde choquen). Preflight 1) y bundle 1) Los tests nuevos van en tests/notations/test_notations_validate_cli.py;
  test_notations_sync_spec_cli.py se corre solo como regresión. 2) Commitea el ejecutor
  desde su worktree con ''git commit -- <rutas>'' y el trailer Task-Id; la frase vieja
  de Convenciones sobre el coordinador queda superada (el coordinador hace solo el
  closeout). 3) Una ruta existente con otra extensión, o un directorio, da un finding
  error ''notations/unsupported-path'' y exit 1. 4) --store: opcional, como en los
  demás comandos de notations (args.store, ruta o alias, sin default); sin --store
  se usan solo las builtin, como dice el pill. Bundle 2) El conjunto mínimo son los
  casos enumerados en el Implementation Path paso 4; ''los cuatro casos'' del Done
  When viejo queda reemplazado por esa lista. 3) Ver 4. 4) Una notación es inválida
  si load_notation lanza una excepción, por ejemplo con un campo requerido ausente
  o mal tipado; el finding lleva code ''notations/notation-invalid'', el mensaje de
  la excepción y la ruta. 5) La detección de spec mira si la raíz tiene clave ''type''.
  Después load_spec decide si es válida, y un ''type'' que load_spec rechaza da finding
  ''notations/spec-invalid'', no se toma como notación.'
# ISO 8601 timestamp
created_at: '2026-11-21T02:15:16.706828+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T02:16:57.103957+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-021501/context-review/task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding/preflight/7cfc8192d326d04549fbb44055babc485dfaf7384cc49224b36f52e3f42699d5/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador (mandan sobre Scope, Convenciones y el pill donde choquen). Preflight 1) y bundle 1) Los tests nuevos van en tests/notations/test_notations_validate_cli.py; test_notations_sync_spec_cli.py se corre solo como regresión. 2) Commitea el ejecutor desde su worktree con 'git commit -- <rutas>' y el trailer Task-Id; la frase vieja de Convenciones sobre el coordinador queda superada (el coordinador hace solo el closeout). 3) Una ruta existente con otra extensión, o un directorio, da un finding error 'notations/unsupported-path' y exit 1. 4) --store: opcional, como en los demás comandos de notations (args.store, ruta o alias, sin default); sin --store se usan solo las builtin, como dice el pill. Bundle 2) El conjunto mínimo son los casos enumerados en el Implementation Path paso 4; 'los cuatro casos' del Done When viejo queda reemplazado por esa lista. 3) Ver 4. 4) Una notación es inválida si load_notation lanza una excepción, por ejemplo con un campo requerido ausente o mal tipado; el finding lleva code 'notations/notation-invalid', el mensaje de la excepción y la ruta. 5) La detección de spec mira si la raíz tiene clave 'type'. Después load_spec decide si es válida, y un 'type' que load_spec rechaza da finding 'notations/spec-invalid', no se toma como notación.
