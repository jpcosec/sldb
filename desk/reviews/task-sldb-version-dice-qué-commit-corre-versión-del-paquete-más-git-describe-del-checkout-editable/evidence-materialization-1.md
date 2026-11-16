---
sldb:
  by: agent
  at: '2026-11-16T11:04:40Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-sldb-version-dice-qué-commit-corre-versión-del-paquete-más-git-describe-del-checkout-editable-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-sldb-version-package-version

  materialization-sldb-version-parser

  materialization-sldb-version-test-cli-v2

  materialization-store-layout-changelog-md'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-version-dice-qué-commit-corre-versión-del-paquete-más-git-describe-del-checkout-editable@sha256:380190fe43fb63efd5092d6ac9352cd73b1a9062be5519e5c4c85ce3dff5d789
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 2e83291ecc5d91f7ebe715407977e37150879ec406c7ddb36f0dddc72fc1c6fb
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-sldb-version-package-version

  materialization-sldb-version-parser

  materialization-sldb-version-test-cli-v2

  materialization-store-layout-changelog-md'
# ISO 8601 timestamp
created_at: '2026-11-16T11:03:53.380217+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T11:03:53.380217+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-sldb-version-dice-qué-commit-corre-versión-del-paquete-más-git-describe-del-checkout-editable

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-sldb-version-package-version, materialization-sldb-version-parser, materialization-sldb-version-test-cli-v2, materialization-store-layout-changelog-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-sldb-version-package-version
materialization-sldb-version-parser
materialization-sldb-version-test-cli-v2
materialization-store-layout-changelog-md
