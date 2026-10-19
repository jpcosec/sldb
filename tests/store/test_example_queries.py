"""The five example queries in contracts/queries/sldb, run over the pinned semantic export.

They were checked against the executor of the separate graph package that became
`sldb.store.graph` (same ids, query by query); the ids it agreed on are pinned here instead.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sldb.store.graph import StructuredQuery, execute_query, sldb_semantic_export_to_snapshot
from sldb.store.graph.convert import index_from_snapshot

ROOT = Path(__file__).resolve().parents[2] / "contracts"
EXPECTED = {
    "documents_near_domain_workflow_task_tag.json": [
        "sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload"
    ],
    "documents_near_taskdoc_model.json": [
        "sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload"
    ],
    "documents_tagged_domain_contract.json": [
        "sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload"
    ],
    "sections_for_taskdoc_document.json": [
        "sldb://section/TaskDoc:001-define-kgdb-semantic-export-payload#define-kgdb-semantic-export-payload"
    ],
    "semantic_neighborhood_integration_kgdb.json": [
        "sldb://semantic_tag/integration",
        "sldb://semantic_tag/knowledge_graph.kgdb"
    ]
}


@pytest.mark.parametrize("query", sorted(EXPECTED))
def test_each_example_query_returns_the_ids_it_always_did(query):
    index = index_from_snapshot(sldb_semantic_export_to_snapshot(json.loads((ROOT / "fixtures" / "sldb_kgdb_semantic_export.v1.json").read_text(encoding="utf-8"))))
    found = execute_query(index, StructuredQuery.model_validate(json.loads((ROOT / "queries" / "sldb" / query).read_text(encoding="utf-8"))))
    assert sorted(n.id if hasattr(n, "id") else n.identity.node_id for n in found) == EXPECTED[query]
