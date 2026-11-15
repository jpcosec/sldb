"""Cobertura de atomos por vista desde un snapshot de grafo con nodos `view`.

Portado de spec2viz (`test_build_coverage_by_view_projects_snapshot_payload` de
`tests/test_deskops.py`) contra `sldb.api.matching.build_coverage_by_view`, con la vista como
`SpecView`; mas los casos sin snapshot y con snapshot ilegible (findings `matching/coverage-*`).
"""
import json

from sldb.api.matching import SpecView, build_coverage_by_view

ELEMENT = "diagram_element:view-1:node:runtime"


def _snapshot(tmp_path):
    view = {"identity": {"node_id": "view:view-1", "node_type": "view"},
            "semantics": {"view_id": "view-1", "diagram_type": "component", "title": "Projected View", "source_ref": "docs/view.html#d1"},
            "edges": [{"target_id": ELEMENT, "relation_type": "contains", "metadata": {}}]}
    covers = {"atom_id": "runtime", "facet": "what", "score": 1.0, "match_basis": "title", "evidence": 'label="Runtime" matched atom.title="Runtime"'}
    element = {"identity": {"node_id": ELEMENT, "node_type": "diagram_element"},
               "semantics": {"view_id": "view-1", "diagram_type": "component", "element_id": "node:runtime", "element_kind": "node", "label": "Runtime"},
               "edges": [{"target_id": "facet:what", "relation_type": "expects_facet", "metadata": {"facet": "what", "source_field": "label"}},
                         {"target_id": "atom:runtime", "relation_type": "covers_facet", "metadata": covers}]}
    facet = {"identity": {"node_id": "facet:what", "node_type": "facet"}, "semantics": {"facet": "what"}, "edges": []}
    path = tmp_path / ".sldb/runtime/knowledge_graph.kg.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"nodes": [view, element, facet]}), encoding="utf-8")
    return path


def _view(tmp_path):
    return SpecView(key="view-1", id="view-1", source="docs/view.html#d1", base_dir=str(tmp_path),
                    diagram_type="component", title="View 1", scope="demo/project")


def test_build_coverage_by_view_projects_snapshot_payload(tmp_path):
    payload, findings = build_coverage_by_view([_view(tmp_path)], snapshot_path=_snapshot(tmp_path))
    assert findings == []
    assert payload["view-1"]["summary"]["elements_fully_covered"] == 1
    assert payload["view-1"]["elements"][0]["covered_facets"][0]["atom_id"] == "runtime"
    assert payload["view-1"]["elements"][0]["missing_facets"] == []
    assert payload["view-1"]["title"] == "Projected View" and payload["view-1"]["summary"]["avg_coverage_ratio"] == 1.0


def test_snapshot_is_discovered_upwards_from_the_view(tmp_path):
    _snapshot(tmp_path)
    payload, findings = build_coverage_by_view([_view(tmp_path)])
    assert findings == [] and payload["view-1"]["summary"]["total_elements"] == 1


def test_missing_or_unreadable_snapshot_leaves_empty_coverage_and_a_finding(tmp_path):
    payload, findings = build_coverage_by_view([_view(tmp_path)], snapshot_path=tmp_path / "nope.json")
    assert [(f.level, f.code) for f in findings] == [("warning", "matching/coverage-snapshot-missing")]
    assert payload["view-1"]["elements"] == [] and payload["view-1"]["view_node_id"] is None
    assert payload["view-1"]["scope"] == "demo/project"
    bad = tmp_path / "bad.json"
    bad.write_text("{no json", encoding="utf-8")
    _payload, findings = build_coverage_by_view([_view(tmp_path)], snapshot_path=bad)
    assert [f.code for f in findings] == ["matching/coverage-snapshot-unreadable"]
