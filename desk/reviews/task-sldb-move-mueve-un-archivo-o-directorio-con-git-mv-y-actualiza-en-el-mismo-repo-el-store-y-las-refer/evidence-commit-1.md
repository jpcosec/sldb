---
sldb:
  by: agent
  at: '2026-11-20T04:43:10Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: bc05f2ab4d1fccca0f3dc22d0a2f7b201ad382c0
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer@sha256:f1481847df39973eb7faaabf89c2381bbb6c9a0f51c6d4362ceb640b3b06ce28
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 43edfb9e4514c299c23854bb8336541500a580159497835b19d85ff5968f26f2
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit bc05f2ab4d1fccca0f3dc22d0a2f7b201ad382c0'
# ISO 8601 timestamp
created_at: '2026-11-20T04:42:56.237069+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T04:42:56.237069+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence commit of task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: bc05f2ab4d1fccca0f3dc22d0a2f7b201ad382c0

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit bc05f2ab4d1fccca0f3dc22d0a2f7b201ad382c0
