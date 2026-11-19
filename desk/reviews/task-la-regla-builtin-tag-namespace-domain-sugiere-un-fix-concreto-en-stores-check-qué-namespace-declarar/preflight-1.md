---
sldb:
  by: agent
  at: '2026-11-19T11:47:24Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar@sha256:db6c1c3f0a9c1b441fe7b3d2350e4decfafcfe637dfb59620bef767b0d17d5ac
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261119-114418/context-review/task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar/preflight/44fabcc5eac2a58d1df70ae5e4c79e16219ab6fe42719dbcbbbfb964270a5b87/attempt-1
input_sha256: 44fabcc5eac2a58d1df70ae5e4c79e16219ab6fe42719dbcbbbfb964270a5b87
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 9de424398162069b214ebab1b9740b55ad7c28a3b852b0adea1f671792c76a39
output_sha256: ed3da1ceabfa7633efebf216b48e72bdd9e465204563d41c7e7d370dca72096f
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador: 1) Formato del fix. Si el namespace
  no está declarado: "declara el namespace ''<ns>'' en tag_namespaces de .sldb/store.yaml
  (campos de TagNamespace: name, hierarchical, folder_axis, anchored_by)". Si el namespace
  está declarado y el tag no es válido: "usa uno de los tags de ''<ns>'': <lista de
  sldb tags tree <ns>>". 2) ''Las demás reglas builtin de tags'' son toda la familia
  builtin:tag_namespace:* que define builtin_tag_rules.py; el ejecutor las enumera
  en el informe y llena el fix de las que lo tengan vacío. 3) El namespace sale del
  hallazgo (found[''node''] y namespaced_tags del payload, como _names en builtin_tag_findings.py).
  4) El test nuevo va en tests/api/test_rules_evaluation.py; tests/api/test_tags.py
  se corre como regresión. builtin_tag_rules.py entra si hace falta. 5) El aviso a
  sldb-ui lo manda el integrador. Commit con rutas nombradas y trailer ''Task-Id:
  <id>''.'
# ISO 8601 timestamp
created_at: '2026-11-19T11:44:32.750141+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T11:47:03.173977+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261119-114418/context-review/task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar/preflight/44fabcc5eac2a58d1df70ae5e4c79e16219ab6fe42719dbcbbbfb964270a5b87/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) Formato del fix. Si el namespace no está declarado: "declara el namespace '<ns>' en tag_namespaces de .sldb/store.yaml (campos de TagNamespace: name, hierarchical, folder_axis, anchored_by)". Si el namespace está declarado y el tag no es válido: "usa uno de los tags de '<ns>': <lista de sldb tags tree <ns>>". 2) 'Las demás reglas builtin de tags' son toda la familia builtin:tag_namespace:* que define builtin_tag_rules.py; el ejecutor las enumera en el informe y llena el fix de las que lo tengan vacío. 3) El namespace sale del hallazgo (found['node'] y namespaced_tags del payload, como _names en builtin_tag_findings.py). 4) El test nuevo va en tests/api/test_rules_evaluation.py; tests/api/test_tags.py se corre como regresión. builtin_tag_rules.py entra si hace falta. 5) El aviso a sldb-ui lo manda el integrador. Commit con rutas nombradas y trailer 'Task-Id: <id>'.
