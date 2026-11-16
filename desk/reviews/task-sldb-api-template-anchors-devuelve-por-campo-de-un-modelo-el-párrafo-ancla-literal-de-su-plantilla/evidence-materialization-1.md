---
sldb:
  by: agent
  at: '2026-11-16T11:21:05Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-sldb-api-template-anchors-devuelve-por-campo-de-un-modelo-el-párrafo-ancla-literal-de-su-plantilla-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-carga-tolerante-init

  materialization-read-store-init

  materialization-store-layout-changelog-md

  materialization-sv01-src-sldb-api-init-py

  materialization-sv02-src-sldb-api-init-py

  materialization-sv04-src-sldb-api-init-py

  materialization-template-anchors-init

  materialization-template-anchors-template-anchors

  materialization-template-anchors-template-extractor

  materialization-template-anchors-test-literal-paragraph-anchor'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-api-template-anchors-devuelve-por-campo-de-un-modelo-el-párrafo-ancla-literal-de-su-plantilla@sha256:58c997196b65e55ce46ab063388c48c2a66684e839364aa1eb8e245555db655c
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: b9dcf548fef4e24c5c5f6ffb14dade1becd438eecd8151132143d1384b7a79c6
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-carga-tolerante-init

  materialization-read-store-init

  materialization-store-layout-changelog-md

  materialization-sv01-src-sldb-api-init-py

  materialization-sv02-src-sldb-api-init-py

  materialization-sv04-src-sldb-api-init-py

  materialization-template-anchors-init

  materialization-template-anchors-template-anchors

  materialization-template-anchors-template-extractor

  materialization-template-anchors-test-literal-paragraph-anchor'
# ISO 8601 timestamp
created_at: '2026-11-16T11:20:19.928938+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T11:20:19.928938+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-sldb-api-template-anchors-devuelve-por-campo-de-un-modelo-el-párrafo-ancla-literal-de-su-plantilla

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-carga-tolerante-init, materialization-read-store-init, materialization-store-layout-changelog-md, materialization-sv01-src-sldb-api-init-py, materialization-sv02-src-sldb-api-init-py, materialization-sv04-src-sldb-api-init-py, materialization-template-anchors-init, materialization-template-anchors-template-anchors, materialization-template-anchors-template-extractor, materialization-template-anchors-test-literal-paragraph-anchor

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-carga-tolerante-init
materialization-read-store-init
materialization-store-layout-changelog-md
materialization-sv01-src-sldb-api-init-py
materialization-sv02-src-sldb-api-init-py
materialization-sv04-src-sldb-api-init-py
materialization-template-anchors-init
materialization-template-anchors-template-anchors
materialization-template-anchors-template-extractor
materialization-template-anchors-test-literal-paragraph-anchor
