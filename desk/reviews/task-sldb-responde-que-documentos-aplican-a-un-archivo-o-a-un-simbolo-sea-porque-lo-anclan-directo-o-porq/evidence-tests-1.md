---
sldb:
  by: agent
  at: '2026-11-25T21:42:15Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-sldb-responde-que-documentos-aplican-a-un-archivo-o-a-un-simbolo-sea-porque-lo-anclan-directo-o-porq-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'src/sldb/api/__init__.py

  src/sldb/api/anchors/__init__.py

  src/sldb/api/anchors/resolve_pointers.py

  src/sldb/api/anchors/tag_reach.py

  src/sldb/mcp/read/tools.py

  src/sldb/mcp/registry.py

  src/sldb/models/code_anchor_doc.py

  tests/mcp/test_read_tools.py

  tests/test_where_pointers_resolve.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-sldb-responde-que-documentos-aplican-a-un-archivo-o-a-un-simbolo-sea-porque-lo-anclan-directo-o-porq@sha256:96ac9f85dc85ba5b91c43e59f8a1c0d20cd20dc11dafb43105880ffb384732d7
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 943e564a0c32d8cc21791356ca5bbd5e8a40ee04ce909b3f0230fc96d1c67a7a
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests src/sldb/api/__init__.py

  src/sldb/api/anchors/__init__.py

  src/sldb/api/anchors/resolve_pointers.py

  src/sldb/api/anchors/tag_reach.py

  src/sldb/mcp/read/tools.py

  src/sldb/mcp/registry.py

  src/sldb/models/code_anchor_doc.py

  tests/mcp/test_read_tools.py

  tests/test_where_pointers_resolve.py'
# ISO 8601 timestamp
created_at: '2026-11-25T21:42:12.623731+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T21:42:12.623731+00:00'
disposed_by: sldb
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-sldb-responde-que-documentos-aplican-a-un-archivo-o-a-un-simbolo-sea-porque-lo-anclan-directo-o-porq

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: src/sldb/api/__init__.py, src/sldb/api/anchors/__init__.py, src/sldb/api/anchors/resolve_pointers.py, src/sldb/api/anchors/tag_reach.py, src/sldb/mcp/read/tools.py, src/sldb/mcp/registry.py, src/sldb/models/code_anchor_doc.py, tests/mcp/test_read_tools.py, tests/test_where_pointers_resolve.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests src/sldb/api/__init__.py
src/sldb/api/anchors/__init__.py
src/sldb/api/anchors/resolve_pointers.py
src/sldb/api/anchors/tag_reach.py
src/sldb/mcp/read/tools.py
src/sldb/mcp/registry.py
src/sldb/models/code_anchor_doc.py
tests/mcp/test_read_tools.py
tests/test_where_pointers_resolve.py
