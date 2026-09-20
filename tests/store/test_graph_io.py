"""Node-link JSON round-trip and the semantic export ingest route, without networkx."""

from __future__ import annotations

import json
from pathlib import Path

from sldb.store.graph import load_graph, save_graph, sldb_semantic_export_to_snapshot

FIXTURE = Path(__file__).resolve().parents[2] / "contracts" / "fixtures" / "sldb_kgdb_semantic_export.v1.json"


def _snapshot():
    return sldb_semantic_export_to_snapshot(json.loads(FIXTURE.read_text(encoding="utf-8")))


def test_ingest_sldb_builds_the_structural_nodes():
    snapshot = _snapshot()
    by_id = {n.identity.node_id: n for n in snapshot.nodes}
    assert by_id["sldb://store"].identity.node_type == "sldb_store"
    document = by_id["sldb://document/TaskDoc:001-define-kgdb-semantic-export-payload"]
    assert document.identity.node_type == "sldb_document"
    assert document.semantics.hash_c == "hash-doc-index-001"
    assert document.source.store["hash_a"] == "hash-store-001"
    assert any(e.relation_type == "tagged_as" and e.target_id == "sldb://semantic_tag/domain.contract" for e in document.edges)


def test_save_and_load_round_trip(tmp_path):
    snapshot = _snapshot()
    path = tmp_path / "kgdb.graph.json"
    save_graph(snapshot, path)
    reloaded = load_graph(path)
    assert [n.identity.node_id for n in reloaded.nodes] == [n.identity.node_id for n in snapshot.nodes]
    assert {e.target_id for n in reloaded.nodes for e in n.edges} == {e.target_id for n in snapshot.nodes for e in n.edges}


def test_load_graph_reads_a_native_snapshot(tmp_path):
    snapshot = _snapshot()
    path = tmp_path / "snapshot.json"
    path.write_text(json.dumps(snapshot.model_dump(mode="json"), indent=2), encoding="utf-8")
    reloaded = load_graph(path)
    assert len(reloaded.nodes) == len(snapshot.nodes)
