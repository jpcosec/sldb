---
sldb:
  by: agent
  at: '2026-11-20T10:18:52Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-merge-driver-automatico-intento-nuevo-se-instala-desde-los-comandos-cli-de-stores-no-desde-la-api-qu-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-ci-keep-stores-build

  materialization-gd26-commands-stores-build

  materialization-gd26-commands-stores-scaffold

  materialization-j02-store-init

  materialization-link-missing-commands-stores-build

  materialization-store-layout-changelog-md

  materialization-stores-src-sldb-api-stores-ensure-merge-driver-py

  materialization-stores-src-sldb-api-stores-store-surroundings-py

  materialization-stores-src-sldb-cli-commands-store-init-py

  materialization-stores-src-sldb-cli-commands-stores-build-py

  materialization-stores-src-sldb-cli-commands-stores-scaffold-py

  materialization-stores-tests-api-test-gitignore-policy-py

  materialization-stores-tests-store-test-merge-driver-auto-install-py

  materialization-stores-tests-store-test-migrate-layout-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-merge-driver-automatico-intento-nuevo-se-instala-desde-los-comandos-cli-de-stores-no-desde-la-api-qu@sha256:f4fb380490a0ff0040bfdbd79cd6a8a959ae24a01cbb380665fa07ed2477807c
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 05af9d2ade430aa677b3af6507b7698c67d39b3420b5e89f4a7c970d13a4209b
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-ci-keep-stores-build

  materialization-gd26-commands-stores-build

  materialization-gd26-commands-stores-scaffold

  materialization-j02-store-init

  materialization-link-missing-commands-stores-build

  materialization-store-layout-changelog-md

  materialization-stores-src-sldb-api-stores-ensure-merge-driver-py

  materialization-stores-src-sldb-api-stores-store-surroundings-py

  materialization-stores-src-sldb-cli-commands-store-init-py

  materialization-stores-src-sldb-cli-commands-stores-build-py

  materialization-stores-src-sldb-cli-commands-stores-scaffold-py

  materialization-stores-tests-api-test-gitignore-policy-py

  materialization-stores-tests-store-test-merge-driver-auto-install-py

  materialization-stores-tests-store-test-migrate-layout-py'
# ISO 8601 timestamp
created_at: '2026-11-20T10:18:23.376334+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T10:18:23.376334+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-merge-driver-automatico-intento-nuevo-se-instala-desde-los-comandos-cli-de-stores-no-desde-la-api-qu

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-ci-keep-stores-build, materialization-gd26-commands-stores-build, materialization-gd26-commands-stores-scaffold, materialization-j02-store-init, materialization-link-missing-commands-stores-build, materialization-store-layout-changelog-md, materialization-stores-src-sldb-api-stores-ensure-merge-driver-py, materialization-stores-src-sldb-api-stores-store-surroundings-py, materialization-stores-src-sldb-cli-commands-store-init-py, materialization-stores-src-sldb-cli-commands-stores-build-py, materialization-stores-src-sldb-cli-commands-stores-scaffold-py, materialization-stores-tests-api-test-gitignore-policy-py, materialization-stores-tests-store-test-merge-driver-auto-install-py, materialization-stores-tests-store-test-migrate-layout-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-ci-keep-stores-build
materialization-gd26-commands-stores-build
materialization-gd26-commands-stores-scaffold
materialization-j02-store-init
materialization-link-missing-commands-stores-build
materialization-store-layout-changelog-md
materialization-stores-src-sldb-api-stores-ensure-merge-driver-py
materialization-stores-src-sldb-api-stores-store-surroundings-py
materialization-stores-src-sldb-cli-commands-store-init-py
materialization-stores-src-sldb-cli-commands-stores-build-py
materialization-stores-src-sldb-cli-commands-stores-scaffold-py
materialization-stores-tests-api-test-gitignore-policy-py
materialization-stores-tests-store-test-merge-driver-auto-install-py
materialization-stores-tests-store-test-migrate-layout-py
