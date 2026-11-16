"""Portado de spec2viz tests/test_catalog_resolved_views.py: el catalogo HTML dibuja cada vista desde la
vista resuelta (`resolve_view`), con la notacion de la vista.

Todos los casos del original ejercitan `spec2viz.renderers.view_mermaid.view_to_mermaid` o
`spec2viz catalog build` (`spec2viz.catalog_views`): son renderers y el constructor del catalogo
HTML, que no viven en sldb (son de specIR) y quedan fuera del alcance de la tarea. Lo unico que
sldb aporta a esos casos es la vista resuelta que reciben; eso se porta como un caso, con las
aserciones del original que dependen solo de la vista (glifo, keyword, estilo del lado oscuro,
nesting, color y rotulo de link), sin la sintaxis Mermaid.

Casos no portados, con su motivo:
- test_view_to_mermaid_uses_glyph_shape_keyword_style_nesting_and_links: renderer Mermaid (specIR);
  su parte de vista resuelta queda en test_view_under_the_view_notation_carries_what_the_catalog_draws.
- test_view_to_mermaid_compartments_and_pseudonodes: renderer Mermaid (specIR).
- test_view_to_mermaid_refuses_non_graph_layouts: renderer Mermaid (specIR).
- test_view_to_mermaid_is_accepted_by_the_real_engine: renderer Mermaid + mmdc (specIR).
- test_catalog_build_draws_graph_views_from_the_view_notation: `catalog build` (HTML de specIR).
- test_catalog_build_uses_the_builtin_notation_without_the_field: `catalog build` (specIR).
- test_catalog_build_prefers_the_project_store_when_the_spec_is_synced: `catalog build` y
  `spec2viz.catalog_views` (specIR).
- test_catalog_build_falls_back_to_src_without_sldb: `catalog build` sin sldb (specIR).
"""
import shutil
from pathlib import Path

import yaml

import sldb.api as sldb_api
from sldb.api.notations import SpecSync, resolve_view

FIXTURES = Path(__file__).parent.parent / "fixtures" / "specs"
NOTATION = {
    "name": "infra-own", "title": "Infra", "diagram_type": "deployment", "layout": {"kind": "graph", "direction": "LR"},
    "glyphs": [
        {"id": "db", "model": "SpecNodeDoc", "where": 'kind = "database"', "shape": "cylinder", "keyword": "«{kind}»", "fill": {"light": "#fff1c2", "dark": "#3d3200"}},
        {"id": "node", "model": "SpecNodeDoc", "where": 'collection = "nodes"', "shape": "node-box", "keyword": "«node»"},
        {"id": "any", "model": "SpecNodeDoc", "shape": "rounded-box"},
    ],
    "links": [
        {"id": "contains", "relation": "contains", "draw": "nest"},
        {"id": "deploy", "relation": "deploy", "line": "dashed", "label": "«deploy»"},
        {"id": "any", "relation": "*", "color": "#0072b2", "target_end": "none", "label": "{data.protocol}"},
    ],
}


def _view(tmp_path, spec=FIXTURES / "deployment.nested.yml", notation=None):
    root = tmp_path / "scratch"
    sldb_api.init_store(root)
    (root / "docs").mkdir()
    copy = Path(shutil.copy(spec, root / "docs" / spec.name))
    report = SpecSync(root / ".sldb").sync(copy, notation=notation)
    return resolve_view(root / ".sldb", report.spec_id)


def _notation(tmp_path):
    path = tmp_path / "infra-own.yml"
    path.write_text(yaml.safe_dump(NOTATION, allow_unicode=True), encoding="utf-8")
    return path


def test_view_under_the_view_notation_carries_what_the_catalog_draws(tmp_path):
    view = _view(tmp_path, notation=_notation(tmp_path))
    assert view["notation"] == "NotationDoc:infra-own" and view["layout"] == {"kind": "graph", "direction": "LR"} and view["skipped"] == []
    nodes = {n["element"]: n for n in view["nodes"]}
    # el nodo que contiene lleva su keyword; la base de datos, cilindro con el kind interpolado
    assert nodes["vpc"]["glyph"] == "GlyphDoc:infra-own.node" and (nodes["vpc"]["keyword"], nodes["vpc"]["label"]) == ("«node»", "VPC")
    assert nodes["db"]["glyph"] == "GlyphDoc:infra-own.db" and (nodes["db"]["keyword"], nodes["db"]["label"]) == ("«database»", "Postgres")
    # el par de color del glifo llega con su lado oscuro
    assert nodes["db"]["style"]["fill"]["dark"] == "#3d3200"
    links = [(l["source"].split(".")[-1], l["target"].split(".")[-1], l) for l in view["links"]]
    assert any(s == "vpc" and l["draw"] == "nest" for s, _, l in links)
    deploy = next(l for _, _, l in links if l["relation"] == "deploy")
    assert deploy["line"] == "dashed" and deploy["label"] == "«deploy»"
    https = next(l for s, t, l in links if (s, t) == ("edge", "cluster"))
    assert https["label"] == "HTTPS" and https["target_end"] == "none" and https["color"]["light"] == "#0072b2"
