---
sldb:
  by: agent
  at: '2026-11-20T04:43:28Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-carga-tolerante-init

  materialization-gd24-architecture-transactions

  materialization-gd24-documents-move-document

  materialization-gd27-cli-dispatcher

  materialization-move-docs-architecture-transactions-md

  materialization-move-knowledge-commands-cmd-sldb-move-md

  materialization-move-knowledge-surfaces-surface-sldb-move-md

  materialization-move-src-sldb-api-documents-move-document-py

  materialization-move-src-sldb-api-documents-move-path-apply-py

  materialization-move-src-sldb-api-documents-move-path-fields-py

  materialization-move-src-sldb-api-documents-move-path-files-py

  materialization-move-src-sldb-api-documents-move-path-links-py

  materialization-move-src-sldb-api-documents-move-path-plan-py

  materialization-move-src-sldb-api-documents-move-path-py

  materialization-move-src-sldb-api-documents-move-path-remap-py

  materialization-move-src-sldb-api-documents-move-path-report-py

  materialization-move-src-sldb-api-documents-move-path-resolve-py

  materialization-move-src-sldb-api-documents-relocate-file-py

  materialization-move-src-sldb-api-init-py

  materialization-move-src-sldb-cli-commands-help-texts-short-py

  materialization-move-src-sldb-cli-commands-move-py

  materialization-move-src-sldb-cli-dispatcher-py

  materialization-move-src-sldb-cli-parsers-project-py

  materialization-move-tests-api-test-move-path-py

  materialization-move-tests-cli-init-py

  materialization-move-tests-cli-move-repo-py

  materialization-move-tests-cli-test-move-cli-py

  materialization-read-store-init

  materialization-store-layout-changelog-md

  materialization-sv01-src-sldb-api-init-py

  materialization-sv02-src-sldb-api-init-py

  materialization-sv04-src-sldb-api-init-py

  materialization-template-anchors-init'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer@sha256:f1481847df39973eb7faaabf89c2381bbb6c9a0f51c6d4362ceb640b3b06ce28
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 45fd0e65335be0bd0cfea75fa9d0c19eaf99dc3b945028770c7eb1ad8e30caf8
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-carga-tolerante-init

  materialization-gd24-architecture-transactions

  materialization-gd24-documents-move-document

  materialization-gd27-cli-dispatcher

  materialization-move-docs-architecture-transactions-md

  materialization-move-knowledge-commands-cmd-sldb-move-md

  materialization-move-knowledge-surfaces-surface-sldb-move-md

  materialization-move-src-sldb-api-documents-move-document-py

  materialization-move-src-sldb-api-documents-move-path-apply-py

  materialization-move-src-sldb-api-documents-move-path-fields-py

  materialization-move-src-sldb-api-documents-move-path-files-py

  materialization-move-src-sldb-api-documents-move-path-links-py

  materialization-move-src-sldb-api-documents-move-path-plan-py

  materialization-move-src-sldb-api-documents-move-path-py

  materialization-move-src-sldb-api-documents-move-path-remap-py

  materialization-move-src-sldb-api-documents-move-path-report-py

  materialization-move-src-sldb-api-documents-move-path-resolve-py

  materialization-move-src-sldb-api-documents-relocate-file-py

  materialization-move-src-sldb-api-init-py

  materialization-move-src-sldb-cli-commands-help-texts-short-py

  materialization-move-src-sldb-cli-commands-move-py

  materialization-move-src-sldb-cli-dispatcher-py

  materialization-move-src-sldb-cli-parsers-project-py

  materialization-move-tests-api-test-move-path-py

  materialization-move-tests-cli-init-py

  materialization-move-tests-cli-move-repo-py

  materialization-move-tests-cli-test-move-cli-py

  materialization-read-store-init

  materialization-store-layout-changelog-md

  materialization-sv01-src-sldb-api-init-py

  materialization-sv02-src-sldb-api-init-py

  materialization-sv04-src-sldb-api-init-py

  materialization-template-anchors-init'
# ISO 8601 timestamp
created_at: '2026-11-20T04:42:56.237069+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T04:42:56.237069+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-carga-tolerante-init, materialization-gd24-architecture-transactions, materialization-gd24-documents-move-document, materialization-gd27-cli-dispatcher, materialization-move-docs-architecture-transactions-md, materialization-move-knowledge-commands-cmd-sldb-move-md, materialization-move-knowledge-surfaces-surface-sldb-move-md, materialization-move-src-sldb-api-documents-move-document-py, materialization-move-src-sldb-api-documents-move-path-apply-py, materialization-move-src-sldb-api-documents-move-path-fields-py, materialization-move-src-sldb-api-documents-move-path-files-py, materialization-move-src-sldb-api-documents-move-path-links-py, materialization-move-src-sldb-api-documents-move-path-plan-py, materialization-move-src-sldb-api-documents-move-path-py, materialization-move-src-sldb-api-documents-move-path-remap-py, materialization-move-src-sldb-api-documents-move-path-report-py, materialization-move-src-sldb-api-documents-move-path-resolve-py, materialization-move-src-sldb-api-documents-relocate-file-py, materialization-move-src-sldb-api-init-py, materialization-move-src-sldb-cli-commands-help-texts-short-py, materialization-move-src-sldb-cli-commands-move-py, materialization-move-src-sldb-cli-dispatcher-py, materialization-move-src-sldb-cli-parsers-project-py, materialization-move-tests-api-test-move-path-py, materialization-move-tests-cli-init-py, materialization-move-tests-cli-move-repo-py, materialization-move-tests-cli-test-move-cli-py, materialization-read-store-init, materialization-store-layout-changelog-md, materialization-sv01-src-sldb-api-init-py, materialization-sv02-src-sldb-api-init-py, materialization-sv04-src-sldb-api-init-py, materialization-template-anchors-init

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-carga-tolerante-init
materialization-gd24-architecture-transactions
materialization-gd24-documents-move-document
materialization-gd27-cli-dispatcher
materialization-move-docs-architecture-transactions-md
materialization-move-knowledge-commands-cmd-sldb-move-md
materialization-move-knowledge-surfaces-surface-sldb-move-md
materialization-move-src-sldb-api-documents-move-document-py
materialization-move-src-sldb-api-documents-move-path-apply-py
materialization-move-src-sldb-api-documents-move-path-fields-py
materialization-move-src-sldb-api-documents-move-path-files-py
materialization-move-src-sldb-api-documents-move-path-links-py
materialization-move-src-sldb-api-documents-move-path-plan-py
materialization-move-src-sldb-api-documents-move-path-py
materialization-move-src-sldb-api-documents-move-path-remap-py
materialization-move-src-sldb-api-documents-move-path-report-py
materialization-move-src-sldb-api-documents-move-path-resolve-py
materialization-move-src-sldb-api-documents-relocate-file-py
materialization-move-src-sldb-api-init-py
materialization-move-src-sldb-cli-commands-help-texts-short-py
materialization-move-src-sldb-cli-commands-move-py
materialization-move-src-sldb-cli-dispatcher-py
materialization-move-src-sldb-cli-parsers-project-py
materialization-move-tests-api-test-move-path-py
materialization-move-tests-cli-init-py
materialization-move-tests-cli-move-repo-py
materialization-move-tests-cli-test-move-cli-py
materialization-read-store-init
materialization-store-layout-changelog-md
materialization-sv01-src-sldb-api-init-py
materialization-sv02-src-sldb-api-init-py
materialization-sv04-src-sldb-api-init-py
materialization-template-anchors-init
