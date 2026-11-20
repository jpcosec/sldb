---
sldb:
  by: agent
  at: '2026-11-20T16:05:25Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-sldb-notations-from-graph-elige-el-campo-del-label-el-campo-que-da-kind-o-estilo-y-un-campo-de-agrup-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/sldb/api/notations/component_spec_fields.py

  src/sldb/api/notations/component_spec_graph.py

  src/sldb/cli/commands/notations_from_graph.py

  src/sldb/cli/parsers/notations.py

  tests/notations/test_notations_from_graph_cli.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-notations-from-graph-elige-el-campo-del-label-el-campo-que-da-kind-o-estilo-y-un-campo-de-agrup@sha256:ef105f4820b0ec9a88998e7bdadac62b3a8ee69e4fc70980f2ad9d7cdfb2fcb3
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 8a404ccacf368c70032572d75121f3a122032240d6a07bddead6b7c010c64769
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/sldb/api/notations/component_spec_fields.py

  src/sldb/api/notations/component_spec_graph.py

  src/sldb/cli/commands/notations_from_graph.py

  src/sldb/cli/parsers/notations.py

  tests/notations/test_notations_from_graph_cli.py'
# ISO 8601 timestamp
created_at: '2026-11-20T16:05:22.782961+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T16:05:22.782961+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-sldb-notations-from-graph-elige-el-campo-del-label-el-campo-que-da-kind-o-estilo-y-un-campo-de-agrup

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/sldb/api/notations/component_spec_fields.py, src/sldb/api/notations/component_spec_graph.py, src/sldb/cli/commands/notations_from_graph.py, src/sldb/cli/parsers/notations.py, tests/notations/test_notations_from_graph_cli.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/sldb/api/notations/component_spec_fields.py
src/sldb/api/notations/component_spec_graph.py
src/sldb/cli/commands/notations_from_graph.py
src/sldb/cli/parsers/notations.py
tests/notations/test_notations_from_graph_cli.py
