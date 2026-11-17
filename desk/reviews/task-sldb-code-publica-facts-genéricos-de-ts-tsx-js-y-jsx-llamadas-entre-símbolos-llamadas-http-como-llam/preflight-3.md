---
sldb:
  by: agent
  at: '2026-11-17T11:41:27Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam-preflight-3
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam@sha256:cf32b1cfc08e1aa0a49eab23bd4c3087a544ba55258364751b70d02561c31967
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261117-113908/context-review/task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam/preflight/b7a73b08470af30afb6a69cae1f564b3722a4183b90bf53ddf24f4e12ccbff6e/attempt-1
input_sha256: b7a73b08470af30afb6a69cae1f564b3722a4183b90bf53ddf24f4e12ccbff6e
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 325b11a560a3295aac85f994d93d8f5d2743435f1519dfce3a1dce99ac04cf97
output_sha256: f177a4cdcf5bb694d0a5f5ac6ec1506d8f179483d7997e91b4502f982a75dfc7
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Corrección 2. La tarea Python ya cerró en HEAD (ad6f8842) y su forma es:
  attrs.calls es una lista {name, line}; la relación calls lleva name una vez por
  destino. En TS se agrega first_arg con el valor del literal sin comillas ni backticks,
  y los escapes se resuelven como los resuelve la gramática. Los módulos son los que
  ya están en el árbol (ts_calls.py, ts_jsx.py). La base de partida es el diff que
  está en el árbol.'
# ISO 8601 timestamp
created_at: '2026-11-17T11:39:23.729559+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T11:41:04.065614+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-113908/context-review/task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam/preflight/b7a73b08470af30afb6a69cae1f564b3722a4183b90bf53ddf24f4e12ccbff6e/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Corrección 2. La tarea Python ya cerró en HEAD (ad6f8842) y su forma es: attrs.calls es una lista {name, line}; la relación calls lleva name una vez por destino. En TS se agrega first_arg con el valor del literal sin comillas ni backticks, y los escapes se resuelven como los resuelve la gramática. Los módulos son los que ya están en el árbol (ts_calls.py, ts_jsx.py). La base de partida es el diff que está en el árbol.
