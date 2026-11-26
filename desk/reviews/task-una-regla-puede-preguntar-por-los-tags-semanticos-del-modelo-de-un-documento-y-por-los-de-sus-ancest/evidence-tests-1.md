---
sldb:
  by: agent
  at: '2026-11-26T00:31:13Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/sldb/api/rules/rule_writes.py

  src/sldb/store/graph/backend/index_semantics.py

  src/sldb/store/graph/backend/index_view.py

  src/sldb/store/graph/language/predicate_ast.py

  src/sldb/store/graph/language/predicate_atoms.py

  src/sldb/store/graph/language/predicate_leaves.py

  src/sldb/store/graph/language/predicate_view.py

  src/sldb/store/graph/language/semantic_scope.py

  tests/test_rules_semantic_tag_predicate.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest@sha256:679b02513ee3dc81ef0bb8ccf4b7708af5a605ae5de1a888137c34aa413a2b93
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 2039126ca1810e91e0d84a60a056bdbb02109699e9cadacb395c47028665b873
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/sldb/api/rules/rule_writes.py

  src/sldb/store/graph/backend/index_semantics.py

  src/sldb/store/graph/backend/index_view.py

  src/sldb/store/graph/language/predicate_ast.py

  src/sldb/store/graph/language/predicate_atoms.py

  src/sldb/store/graph/language/predicate_leaves.py

  src/sldb/store/graph/language/predicate_view.py

  src/sldb/store/graph/language/semantic_scope.py

  tests/test_rules_semantic_tag_predicate.py'
# ISO 8601 timestamp
created_at: '2026-11-26T00:31:11.100646+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-26T00:31:11.100646+00:00'
disposed_by: sldb
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/sldb/api/rules/rule_writes.py, src/sldb/store/graph/backend/index_semantics.py, src/sldb/store/graph/backend/index_view.py, src/sldb/store/graph/language/predicate_ast.py, src/sldb/store/graph/language/predicate_atoms.py, src/sldb/store/graph/language/predicate_leaves.py, src/sldb/store/graph/language/predicate_view.py, src/sldb/store/graph/language/semantic_scope.py, tests/test_rules_semantic_tag_predicate.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/sldb/api/rules/rule_writes.py
src/sldb/store/graph/backend/index_semantics.py
src/sldb/store/graph/backend/index_view.py
src/sldb/store/graph/language/predicate_ast.py
src/sldb/store/graph/language/predicate_atoms.py
src/sldb/store/graph/language/predicate_leaves.py
src/sldb/store/graph/language/predicate_view.py
src/sldb/store/graph/language/semantic_scope.py
tests/test_rules_semantic_tag_predicate.py
