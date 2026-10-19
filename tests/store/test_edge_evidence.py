"""Evidence on edges: the target's hash, the source's contract, the engine or actor, no time."""
from __future__ import annotations

import json
import sys

import pytest

from sldb.cli import main as cli_main
from sldb.store.edge_index.edge_evidence import stamp
from sldb.store.models import EdgeRecord

from .test_semantic_export import _build_tracked_store

ENGINE = {"name": "sldb", "version": "9.9"}
HASHES = {"sldb://document/TaskDoc:alpha": "hd", "sldb://model/TaskDoc": "hm", "sldb://document/other:TaskDoc:beta": "hq"}
CONTRACTS = {"TaskDoc": "hc"}


def _edge(target: str, **metadata) -> EdgeRecord:
    return EdgeRecord(source="sldb://document/TaskDoc:alpha", target=target, relation="r", metadata={"origin": "structural", **metadata})


@pytest.fixture(autouse=True)
def _forget_the_tmp_model_package():
    yield
    for name in [m for m in sys.modules if m == "tmpdocs" or m.startswith("tmpdocs.")]:
        del sys.modules[name]


def test_a_structural_edge_names_its_engine_and_the_states_it_was_derived_from():
    [edge] = stamp([_edge("sldb://model/TaskDoc")], HASHES, CONTRACTS, ENGINE)
    assert edge.metadata["evidence"] == {"ref_hash": "hm", "contract": "hc", "engine": ENGINE}
    assert "timestamp" not in json.dumps(edge.metadata)


def test_an_authored_edge_names_its_actor():
    [edge] = stamp([_edge("sldb://document/TaskDoc:alpha", origin="relation_doc", relation_doc="links")], HASHES, CONTRACTS, ENGINE)
    assert edge.metadata["evidence"] == {"ref_hash": "hd", "contract": "hc", "actor": "relation_doc:links"}


def test_a_section_target_stands_on_its_documents_hash_and_says_so():
    [edge] = stamp([_edge("sldb://section/TaskDoc:alpha#overview")], HASHES, CONTRACTS, ENGINE)
    assert edge.metadata["evidence"]["ref_hash"] == "hd" and edge.metadata["evidence"]["ref"] == "document"


def test_a_linked_stores_document_is_found_by_its_qualified_id():
    [edge] = stamp([_edge("sldb://document/other:TaskDoc:beta")], HASHES, CONTRACTS, ENGINE)
    assert edge.metadata["evidence"]["ref_hash"] == "hq"


def test_edges_show_adds_evidence_only_when_asked(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)
    assert cli_main(["edges", "show", "TaskDoc:task", "--store", str(store)]) == 0
    assert all("evidence" not in e["metadata"] for e in json.loads(capsys.readouterr().out))
    assert cli_main(["edges", "show", "TaskDoc:task", "--store", str(store), "--evidence"]) == 0
    edges = json.loads(capsys.readouterr().out)
    assert edges and all(e["metadata"]["evidence"]["engine"]["name"] == "sldb" for e in edges)
    assert all(e["metadata"]["evidence"]["contract"] for e in edges)
