# Result
Existing pieces reused: check_edges' validator (`validate_edge_index_by_store`), the composed edge index, `apply_batch(dry_run=True)`, `rejected()` structure of mcp/write.
- New `sldb/api/documents/batch_edges.py`: applies the batch in memory on the composed edge index (relation types, relations, new docs, in batch order) and runs the same validator; reports only violations the batch adds. Not read at all when the batch touches no RelationDoc/RelationTypeDoc.
- `apply_batch(dry_run=True)` -> `BatchReport.rejections` (code types|cardinality|condition|endpoint, relation {source,type,target}, relation_doc, message). Real apply unchanged.
- propose_changes and apply_changes call the dry run first; violation -> `rejected("edges", ..., findings=rejections)`, nothing written, store hash unchanged.
- pendings: removed `edge_validation_before_write` and `edge_pending`.
- Pure parts extracted: `doc_kinds.relation_edge`, `relation_type_contribution`, `resolve.resolve_authored`.
- Tests: new tests/test_mcp_propose_rejects_invalid_edges.py; tests/mcp/test_write_tools.py: replaced the xfail/"reported after write" edge tests (now refused before).
Review: a cardinality violation yields one entry per batch relation behind it. session/run_id/session_sha256: not available to this agent.
Files: src/sldb/api/documents/{apply_batch,batch_report,batch_edges}.py src/sldb/mcp/write/{apply,findings,pending,pendings,tools}.py src/sldb/store/edge_index/{doc_kinds,resolve}.py tests/mcp/test_write_tools.py tests/test_mcp_propose_rejects_invalid_edges.py

Commit de codigo: b5a008670 en la rama deskops/deskops-e-2757adcb50b7 (sin Task-Id, segun la aclaracion de la revision).
`deskops advance task`: BLOQUEADO — error: [rules/rule-activation-task-code] ... recibos preflight y bundle aceptados e intactos (ReviewDoc ...-bundle-1 anchor_state "changed"). La tarea sigue en ritual-execution.
