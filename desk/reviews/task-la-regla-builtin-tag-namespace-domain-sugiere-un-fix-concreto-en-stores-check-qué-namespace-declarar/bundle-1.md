---
sldb:
  by: agent
  at: '2026-11-19T11:48:22Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
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
run_dir: runs/subagents/20261119-114458/context-review/task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar/bundle/11cdb4f8e5f1c082250895f0721c0adaec3d442c1d191e95dde6ef4af9cf8536/attempt-1
input_sha256: 11cdb4f8e5f1c082250895f0721c0adaec3d442c1d191e95dde6ef4af9cf8536
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 9fe1e3e0daba0c5816bf7d9b5a5882d900c76f9e4c1fe14f745ae8abe6bdad06
output_sha256: b48a4aa3110675988697043b412ee4df51bb033ee52eea3c917c61a2ff18935e
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
created_at: '2026-11-19T11:45:15.756227+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T11:48:01.240461+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261119-114458/context-review/task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar/bundle/11cdb4f8e5f1c082250895f0721c0adaec3d442c1d191e95dde6ef4af9cf8536/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) Formato del fix. Si el namespace no está declarado: "declara el namespace '<ns>' en tag_namespaces de .sldb/store.yaml (campos de TagNamespace: name, hierarchical, folder_axis, anchored_by)". Si el namespace está declarado y el tag no es válido: "usa uno de los tags de '<ns>': <lista de sldb tags tree <ns>>". 2) 'Las demás reglas builtin de tags' son toda la familia builtin:tag_namespace:* que define builtin_tag_rules.py; el ejecutor las enumera en el informe y llena el fix de las que lo tengan vacío. 3) El namespace sale del hallazgo (found['node'] y namespaced_tags del payload, como _names en builtin_tag_findings.py). 4) El test nuevo va en tests/api/test_rules_evaluation.py; tests/api/test_tags.py se corre como regresión. builtin_tag_rules.py entra si hace falta. 5) El aviso a sldb-ui lo manda el integrador. Commit con rutas nombradas y trailer 'Task-Id: <id>'.
