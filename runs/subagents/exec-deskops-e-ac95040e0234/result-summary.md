# Result: anchors_resolve
run_id: exec-deskops-e-ac95040e0234 (session path/sha256: not available to this executor)

Commit (branch deskops/deskops-e-ac95040e0234), no Task-Id as the review asked.
Files: contracts/layers.toml (needs/needed_by +1 for persistencia/operacion, as measured), src/sldb/api/__init__.py, src/sldb/api/anchors/__init__.py, src/sldb/api/anchors/resolve_pointers.py (new), src/sldb/api/anchors/tag_reach.py (new), src/sldb/mcp/read/tools.py, src/sldb/mcp/registry.py, src/sldb/models/code_anchor_doc.py, tests/mcp/test_read_tools.py, tests/test_where_pointers_resolve.py (new).

What: one operation `sldb.api.anchors_resolve(store, target|document|tag)` and MCP read tool `anchors_resolve`. target (path or path::Symbol) -> documents [{doc, via: direct|tag:<t>}]; document=Model:id -> code [{path,symbol,via}]; tag -> documents + code. Coverage via tags: doc's payload tags/semantic_tags, descendants in the DAG plus equivalences. Unknown tag -> `unresolved` [{tag, doc}], not an error. Read-only. Composes check-anchors refs (CodeAnchorDoc), load_semantic_dag, semantic_dag_graph.under.

Review points:
- CodeAnchorDoc had no tags field, so anchors could not carry categories: added optional `tags` (template line optrev). Needed for the tag path.
- A third argument `tag` was added beside target/document, to resolve "the parent tag" from Done When.
- Model-level __semantics__ are not counted as pointers, only payload tags.
- Proposal for docs/architecture/command-taxonomy.md: that file does not exist; name `anchors_resolve` (read, level 0) goes there when the taxonomy is written.
- Env: tests/mcp cannot run in this venv (mcp 'Client' import); 2 unrelated failures (test_cli_docs_create_names_the_document, treesitter ts types) are environment.

## Advance
`deskops advance task` was blocked (not by my work): [rules/rule-activation-task-code] requires accepted, intact preflight/bundle receipts; the bundle review has anchor_state "changed".
