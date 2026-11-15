"""What SLDB does not offer yet, and the note that asks for it. Nothing replaces it here:
every answer that depends on it says so."""

from __future__ import annotations

PENDING = {
    "dry_run": {
        "what": "a public dry run of apply_batch: propose_changes answers what would be written, but the prevalidation (model round-trip, guards, on_write rules, edge types) runs only when apply_changes calls apply_batch",
        "note": "sldb:20261115-022430-suggestion-specir-dry-run-p-blico-de-apply-batch",
    },
    "edge_validation_before_write": {
        "what": "an edge checked against its RelationTypeDoc (source and target types, cardinality, condition) before the RelationDoc is written: SLDB checks it only in check_edges, after the write, so apply_changes reports the violation instead of refusing it",
        "note": "sldb:20261115-022655-suggestion-specir-validar-aristas-antes-de-escribir-y-devolver-las-alertas-on-write-de-apply-batch",
    },
    "store_hash_precondition": {
        "what": "the store's fingerprint as an atomic precondition of apply_batch (level 2): only the per-document guards protect the apply",
        "note": "sldb:20261114-074447-suggestion-specir-brechas-api-p-blica-sldb-para-mcp",
    },
    "guards_in_transaction": {
        "what": "the guards re-checked inside apply_batch's transaction, or a store write lock: a concurrent writer between prevalidation and write is not detected",
        "note": "sldb:20261115-022444-suggestion-specir-guardas-de-apply-batch-bajo-el-cerrojo-del-store",
    },
    "on_write_alerts": {
        "what": "the on_write alerts of a write in apply_batch's answer: SLDB hands them only to in-process listeners, so apply_changes re-reads them with rules_check, which cannot take a document that is not a node of the edge index (a RelationDoc) as subject; those alerts are not reported",
        "note": "sldb:20261115-022655-suggestion-specir-validar-aristas-antes-de-escribir-y-devolver-las-alertas-on-write-de-apply-batch",
    },
    "undo": {
        "what": "undo_changes: apply_batch does not return the inverse batch with guards yet, so the MCP does not serve the tool; calling it is logged as a not_implemented signal",
        "note": "sldb:20261115-123855-suggestion-specir-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-en-sldb",
    },
}
