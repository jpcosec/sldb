"""Portado de spec2viz tests/test_view_doc.py: ViewDoc, la vista portable de la gramatica de
proyeccion (pedida por graph_ui), contra `sldb.api.ViewDoc` y `sldb.api.notations.NotationSync`.

Casos no portados: ninguno.
"""
import pytest
import yaml

import sldb.api as sldb_api
from sldb.api import ViewDoc
from sldb.api.notations import NotationSync

BASE = {"id": "atoms-by-task", "name": "atoms-by-task", "title": "Atoms by task"}


def test_defaults_and_shape():
    v = ViewDoc.model_validate(BASE)
    assert v.nodes == [] and v.relations == [] and v.direction == "both" and v.notation == "" and v.layout == {}
    v = ViewDoc.model_validate({**BASE, "nodes": [{"model": "TaskDoc"}, {"model": "AtomDoc", "where": 'five_wh_one_plus = "why"'}],
                                "relations": ["references"], "direction": "outgoing", "notation": "NotationDoc:component",
                                "layout": {"kind": "graph", "style": "rings", "ring_field": "status"}})
    assert v.nodes == [{"model": "TaskDoc", "where": ""}, {"model": "AtomDoc", "where": 'five_wh_one_plus = "why"'}]
    assert v.layout["style"] == "rings"


@pytest.mark.parametrize("changes, message", [
    ({"direction": "up"}, "direction"),
    ({"nodes": [{"where": "x"}]}, "needs a model"),
    ({"nodes": [{"model": "A", "id": "SpecNodeDoc:x"}]}, "only take model and where"),
    ({"layout": {"style": "force"}}, "layout.style"),
])
def test_invalid(changes, message):
    with pytest.raises(Exception, match=message):
        ViewDoc.model_validate({**BASE, **changes})


def test_view_doc_in_a_store_references_its_notation(tmp_path):
    sldb_api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    NotationSync(store).sync("component")  # registra los modelos de notacion, ViewDoc incluido
    payload = {**BASE, "nodes": [{"model": "SpecNodeDoc", "where": 'kind = "entry"'}], "relations": ["uses"],
               "direction": "both", "notation": "NotationDoc:component", "layout": {"style": "layered"}, "description": "entry points"}
    sldb_api.create_document(store, "ViewDoc", tmp_path / "sldb" / "views" / "atoms-by-task.md", payload, name="atoms-by-task")
    sldb_api.rebuild_edges(store)
    front = yaml.safe_load((tmp_path / "sldb" / "views" / "atoms-by-task.md").read_text(encoding="utf-8").split("---")[1])
    assert front["nodes"] == [{"model": "SpecNodeDoc", "where": 'kind = "entry"'}] and front["notation"] == "NotationDoc:component"
    targets = {r.target for r in sldb_api.edges_from(store, "ViewDoc:atoms-by-task") if r.relation == "references"}
    assert targets == {"sldb://document/NotationDoc:component"}
    assert sldb_api.check_edges(store).errors == []
