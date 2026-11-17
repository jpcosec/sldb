---
sldb:
  by: agent
  at: '2026-11-17T11:41:58Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam-bundle-3
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
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
run_dir: runs/subagents/20261117-113952/context-review/task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam/bundle/615e8e4a0dc0084394c1bbf1a8e1b8a334df41b6dfd791f6aa84804683481ea7/attempt-1
input_sha256: 615e8e4a0dc0084394c1bbf1a8e1b8a334df41b6dfd791f6aa84804683481ea7
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: a855355309e402f735bead8f939abe7ca30dfe6d90d8161423c32eae28fd6bdc
output_sha256: 7551b3d5c660030f33b38c6493ae00421f02136e455620afbab47a87e9eabcf9
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Corrección 2. La tarea Python ya cerró en HEAD (ad6f8842) y su forma es:
  attrs.calls es una lista {name, line}; la relación calls lleva name una vez por
  destino. En TS se agrega first_arg con el valor del literal sin comillas ni backticks,
  y los escapes se resuelven como los resuelve la gramática. Los módulos son los que
  ya están en el árbol (ts_calls.py, ts_jsx.py). La base de partida es el diff que
  está en el árbol.'
# ISO 8601 timestamp
created_at: '2026-11-17T11:40:10.189219+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T11:41:35.526645+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-113952/context-review/task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam/bundle/615e8e4a0dc0084394c1bbf1a8e1b8a334df41b6dfd791f6aa84804683481ea7/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Corrección 2. La tarea Python ya cerró en HEAD (ad6f8842) y su forma es: attrs.calls es una lista {name, line}; la relación calls lleva name una vez por destino. En TS se agrega first_arg con el valor del literal sin comillas ni backticks, y los escapes se resuelven como los resuelve la gramática. Los módulos son los que ya están en el árbol (ts_calls.py, ts_jsx.py). La base de partida es el diff que está en el árbol.
