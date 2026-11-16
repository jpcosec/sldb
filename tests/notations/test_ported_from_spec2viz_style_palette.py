"""Portado de spec2viz tests/test_style_palette.py: formas builtin, paleta accesible como documento
del store, colores e iconos en glifos y links, style.kinds del spec y una sola precedencia
(glifo > spec > paleta), contra `sldb.notations` y `sldb.api.notations`.

Las fixtures de spec2viz/tests/fixtures que usa (component.kinds.yml, component.styled.yml,
deployment.runtime.yml) ya existian identicas en tests/fixtures/specs/.

Casos no portados (o portados en parte), con su motivo:
- test_notation_validate_gives_typed_errors, parte CLI (`spec2viz notation validate <ruta>`):
  sldb no tiene `sldb notations validate` (primer pedido de la nota de inbox 20261115-192054,
  otra tarea). Se porta la parte de `load_notation` con el error tipado.
- test_palette_validation_is_typed, parte CLI (`spec2viz palette validate <ruta>`): mismo
  motivo; se porta la parte de `check_palette`.
- test_mermaid_class_defs_from_style_kinds_and_plantuml_block_untouched y
  test_mermaid_takes_the_light_side_of_a_spec_pair: prueban renderers (Mermaid, PlantUML,
  compile_ir) de spec2viz, que son de specIR, no de sldb (fuera de alcance segun la tarea).
- test_palette_cli_sync_writes_the_store_document, salida de texto "Synced palette default":
  `sldb notations sync --palette` imprime el SyncReport en JSON; se comprueba el JSON.
"""
import copy
import json
import shutil
from pathlib import Path

import pytest
import yaml

import sldb.api as sldb_api
import sldb.notations as notations_pkg
from sldb.api.notations import SpecSync, load_spec, resolve_documents, resolve_view, validate_spec
from sldb.cli import main
from sldb.notations import SHAPES, PaletteSpec, builtin_notations, check_palette, contrast, load_notation, load_palette, resolve_color, resolve_style
from sldb.notations.exceptions import InvalidColorError, UnknownIconError, UnknownKindError, UnknownShapeError, ValidationError

FIXTURES = Path(__file__).parent.parent / "fixtures" / "specs"
DEFAULT_PALETTE_YAML = Path(notations_pkg.__file__).parent / "palettes" / "default.yml"
STYLED = {
    "name": "infra", "title": "Infra", "diagram_type": "component", "layout": {"kind": "graph"},
    "glyphs": [
        {"id": "db", "model": "SpecNodeDoc", "where": 'kind = "database"', "shape": "cylinder", "kind": "database"},
        {"id": "api", "model": "SpecNodeDoc", "where": 'kind = "backend"', "shape": "box", "fill": "#fafafa"},
        {"id": "any", "model": "SpecNodeDoc", "shape": "rounded-box"},
    ],
    "links": [{"id": "any", "relation": "*", "color": "database-stroke", "label": "{relation_type}"}],
}


def _write(tmp_path, notation, name="infra.yml"):
    path = tmp_path / name
    path.write_text(yaml.safe_dump(notation), encoding="utf-8")
    return path


# --- formas y validacion tipada de notaciones --------------------------------------------------

def test_new_builtin_shapes_are_accepted(tmp_path):
    assert {"cylinder", "queue", "cloud", "package", "note"} <= set(SHAPES)
    notation = copy.deepcopy(STYLED)
    notation["glyphs"] = [{"id": s, "model": "SpecNodeDoc", "where": f'kind = "{s}"', "shape": s} for s in ("cylinder", "queue", "cloud", "package", "note")]
    notation["glyphs"].append({"id": "any", "model": "SpecNodeDoc", "shape": "box"})
    load_notation(_write(tmp_path, notation))


@pytest.mark.parametrize("mutate, error", [
    (lambda n: n["glyphs"][2].update(shape="hexagon"), UnknownShapeError),
    (lambda n: n["glyphs"][0].update(kind="mainframe"), UnknownKindError),
    (lambda n: n["glyphs"][1].update(fill="red"), InvalidColorError),
    (lambda n: n["glyphs"][1].update(stroke="#12345"), InvalidColorError),
    (lambda n: n["links"][0].update(color="url(#x)"), InvalidColorError),
    (lambda n: n["glyphs"][1].update(icon="https://example.com/x.svg"), UnknownIconError),
    (lambda n: n["glyphs"][1].update(icon="rocket"), UnknownIconError),
])
def test_notation_validate_gives_typed_errors(tmp_path, mutate, error):
    notation = copy.deepcopy(STYLED)
    mutate(notation)
    path = _write(tmp_path, notation)
    with pytest.raises(error):
        load_notation(path)


def test_builtin_notations_still_validate_and_are_unstyled():
    for name in builtin_notations():
        assert load_notation(name).styled is False


# --- paleta ------------------------------------------------------------------------------------

def test_default_palette_is_accessible_and_distinguishable_without_colour():
    palette = load_palette()
    assert set(palette.kinds) == {"database", "queue", "storage", "gateway", "auth", "backend", "frontend", "client", "external"}
    pairs = {(k.shape, k.icon) for k in palette.kinds.values()}
    assert len(pairs) == len(palette.kinds)  # forma + icono distinguen sin el tono
    for kind in palette.kinds.values():
        for theme in ("light", "dark"):
            assert contrast(palette.color(kind.stroke)[theme], getattr(palette.backgrounds, theme)) >= 3.0
            assert contrast(getattr(palette.ink, theme), palette.color(kind.fill)[theme]) >= 4.5


@pytest.mark.parametrize("mutate, error, message", [
    (lambda p: p["colors"].update({"database-stroke": {"light": "#eeeeee", "dark": "#0072b2"}}), ValidationError, "WCAG 1.4.11"),
    (lambda p: p["colors"].update({"queue-fill": {"light": "#333333", "dark": "#4a3911"}}), ValidationError, "WCAG AA"),
    (lambda p: p["kinds"]["storage"].update(icon="database"), ValidationError, "only cue"),
    (lambda p: p["kinds"]["auth"].update(icon="rocket"), UnknownIconError, "icon set"),
    (lambda p: p["kinds"]["auth"].update(shape="hexagon"), UnknownShapeError, "shape"),
    (lambda p: p["kinds"]["auth"].update(fill="tomato"), InvalidColorError, "token"),
])
def test_palette_validation_is_typed(mutate, error, message):
    raw = yaml.safe_load(DEFAULT_PALETTE_YAML.read_text(encoding="utf-8"))
    mutate(raw)
    with pytest.raises(error, match=message):
        check_palette(PaletteSpec.model_validate(raw))


# --- precedencia -------------------------------------------------------------------------------

def test_precedence_glyph_over_spec_over_palette():
    palette = {"colors": {k: v.model_dump() for k, v in load_palette().colors.items()},
               "kinds": {k: v.model_dump() for k, v in load_palette().kinds.items()}}
    # solo paleta
    style = resolve_style({}, "database", None, palette)
    assert style["fill"]["light"] == "#dbebf4" and style["icon"] == "database" and set(style["source"].values()) == {"palette"}
    # el spec gana a la paleta, propiedad por propiedad
    style = resolve_style({}, "database", {"database": {"fill": "#ffeecc"}}, palette)
    assert style["fill"] == {"light": "#ffeecc", "dark": "#ffeecc"} and style["source"]["fill"] == "spec" and style["source"]["stroke"] == "palette"
    # el glifo gana a todo: explicito, y detras el kind de la paleta que nombra
    style = resolve_style({"fill": "#000000", "kind": "queue"}, "database", {"database": {"fill": "#ffeecc", "icon": "cpu"}}, palette)
    assert style["fill"]["light"] == "#000000" and style["stroke"]["light"] == "#b37c00" and style["icon"] == "list-ordered"
    assert style["source"] == {"fill": "glyph", "stroke": "glyph", "icon": "glyph"}
    # sin paleta en la notacion, la paleta no aplica; el spec si (sus tokens resuelven contra default)
    assert resolve_style({}, "database", None, None) == {}
    assert resolve_style({}, "backend", {"backend": {"stroke": "backend-stroke"}}, None)["stroke"]["dark"] == "#56b4e9"


# --- style.kinds del spec ----------------------------------------------------------------------

@pytest.mark.parametrize("entry, error", [({"fill": "blue"}, InvalidColorError), ({"icon": "rocket"}, UnknownIconError)])
def test_spec_style_kinds_are_validated_typed(entry, error):
    diagram = load_spec(FIXTURES / "component.kinds.yml")
    diagram.style.kinds["database"] = entry
    with pytest.raises(error):
        validate_spec(diagram)


# --- store: PaletteDoc, campos de estilo, resolve_view y resolve_documents ------------------------

def _store(tmp_path):
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    return tmp_path / ".sldb"


def test_styled_notation_syncs_its_palette_and_view_carries_resolved_style_and_legend(tmp_path):
    store = _store(tmp_path)
    notation = _write(tmp_path / "docs", STYLED)
    spec = shutil.copy(FIXTURES / "component.kinds.yml", tmp_path / "docs" / "kinds.yml")
    report = SpecSync(store).sync(Path(spec), notation=notation)
    assert "PaletteDoc:default" in report.created
    docs = {f"{d.model_name}:{d.name}": d.payload for d in sldb_api.load_runtime_documents(store, None, include_linked=False)}
    assert docs["NotationDoc:infra"]["palette"] == "PaletteDoc:default"
    assert docs["GlyphDoc:infra.db"]["kind"] == "database" and docs["LinkDoc:infra.any"]["color"] == "database-stroke"
    assert docs["SpecDoc:component.kinds"]["style"] == {"database": {"fill": "#ffeecc"}, "backend": {"stroke": "backend-stroke", "icon": "cpu"}}

    view = resolve_view(store, "component.kinds")
    nodes = {n["element"]: n for n in view["nodes"]}
    # db: glifo con kind database (gana al spec), api: fill del glifo, stroke e icono del spec
    assert nodes["db"]["style"]["fill"]["light"] == "#dbebf4" and nodes["db"]["style"]["source"]["fill"] == "glyph"
    assert nodes["api"]["style"]["fill"]["light"] == "#fafafa" and nodes["api"]["style"]["icon"] == "cpu"
    assert nodes["api"]["style"]["source"] == {"fill": "glyph", "stroke": "spec", "icon": "spec"}
    # web: solo la paleta de la notacion
    assert nodes["web"]["style"]["icon"] == "app-window" and set(nodes["web"]["style"]["source"].values()) == {"palette"}
    assert all(l["color"] == {"light": "#0072b2", "dark": "#0072b2"} for l in view["links"])
    assert view["palette"] == "PaletteDoc:default"
    legend = view["legend"]
    assert [g["glyph"] for g in legend["glyphs"]] == ["GlyphDoc:infra.db", "GlyphDoc:infra.api", "GlyphDoc:infra.any"]
    assert legend["glyphs"][0]["shape"] == "cylinder" and legend["glyphs"][0]["style"]["icon"] == "database"
    assert legend["links"][0]["color"]["light"] == "#0072b2"
    assert {k["kind"] for k in legend["kinds"]} == {"backend", "frontend"} and next(k for k in legend["kinds"] if k["kind"] == "frontend")["shape"] == "box"


def test_unstyled_notation_writes_no_palette_and_no_style(tmp_path):
    store = _store(tmp_path)
    spec = shutil.copy(FIXTURES / "deployment.runtime.yml", tmp_path / "docs" / "dep.yml")
    SpecSync(store).sync(Path(spec))
    assert not any(str(d.model_name) == "PaletteDoc" for d in sldb_api.load_runtime_documents(store, None, include_linked=False))
    text = (tmp_path / "sldb" / "notations" / "deployment" / "notation.md").read_text(encoding="utf-8")
    assert "palette:" not in text
    view = resolve_view(store, "deployment.runtime")
    assert all(n["style"] == {} for n in view["nodes"]) and all(l["color"] is None for l in view["links"])


def test_resolve_documents_is_public_and_filters_relations(tmp_path):
    store = _store(tmp_path)
    spec = shutil.copy(FIXTURES / "component.kinds.yml", tmp_path / "docs" / "kinds.yml")
    SpecSync(store).sync(Path(spec), notation=_write(tmp_path / "docs", STYLED))
    full = resolve_view(store, "component.kinds")
    refs = [n["doc"] for n in full["nodes"]]
    same = resolve_documents(store, "NotationDoc:infra", refs, spec_style={"database": {"fill": "#ffeecc"}, "backend": {"stroke": "backend-stroke", "icon": "cpu"}})
    assert [n["style"] for n in same["nodes"]] == [n["style"] for n in full["nodes"]] and same["links"] == full["links"]
    # api y db, y solo la arista api -> db aunque web -> api tambien exista
    keep = {r for r in refs if r.endswith((".api", ".db"))}
    edge = next(l["doc"] for l in full["links"] if l["source"] in keep and l["target"] in keep)
    one = resolve_documents(store, "infra", sorted(keep), relation_refs=[edge])
    assert len(one["nodes"]) == 2 and [l["doc"] for l in one["links"]] == [edge]
    assert resolve_documents(store, "infra", sorted(keep), relation_refs=[])["links"] == []


def test_palette_cli_sync_writes_the_store_document(tmp_path, capsys):
    store = _store(tmp_path)
    assert main(["notations", "sync", "--palette", "default", "--store", str(store)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert "PaletteDoc:default" in report["created"]
    doc = next(d.payload for d in sldb_api.load_runtime_documents(store, None, include_linked=False) if str(d.model_name) == "PaletteDoc")
    assert doc["kinds"]["queue"]["shape"] == "queue" and doc["icon_set"]["name"] == "lucide"


# --- un color propio para cada tema: el par {light, dark} --------------------------------------

PAIR = {"light": "#fff1c2", "dark": "#3d3200"}


@pytest.mark.parametrize("value, error", [
    ({"light": "#fff1c2"}, "exactly `light` and `dark`"),
    ({"light": "#fff1c2", "dark": "#3d3200", "hc": "#000000"}, "exactly `light` and `dark`"),
    ({"light": "#fff1c2", "dark": "dark-yellow"}, "dark"),
    ({"light": "fff1c2", "dark": "#3d3200"}, "light"),
])
def test_color_pair_is_validated_typed(tmp_path, value, error):
    notation = copy.deepcopy(STYLED)
    notation["glyphs"][1]["fill"] = value
    with pytest.raises(InvalidColorError, match=error):
        load_notation(_write(tmp_path, notation))


def test_single_hex_is_the_same_in_both_themes_and_a_pair_is_not():
    assert resolve_color("#FFF1C2", {}) == {"light": "#fff1c2", "dark": "#fff1c2"}
    tokens = {k: v.model_dump() for k, v in load_palette().colors.items()}
    assert resolve_color(PAIR, tokens) == PAIR
    # cada lado puede ser un token: se toma el valor de ese tema
    assert resolve_color({"light": "#fff1c2", "dark": "queue-fill"}, tokens) == {"light": "#fff1c2", "dark": "#4a3911"}


def test_pair_reaches_the_view_per_theme_for_glyph_link_and_spec(tmp_path):
    store = _store(tmp_path)
    notation = copy.deepcopy(STYLED)
    notation["glyphs"][1]["fill"] = PAIR
    notation["glyphs"][1]["stroke"] = {"light": "#7a5c00", "dark": "#e6c34a"}
    notation["links"][0]["color"] = {"light": "#0072b2", "dark": "#56b4e9"}
    spec = yaml.safe_load((FIXTURES / "component.kinds.yml").read_text(encoding="utf-8"))
    spec["style"]["kinds"]["frontend"] = {"fill": {"light": "#eef6ff", "dark": "#10233a"}}
    (tmp_path / "docs" / "kinds.yml").write_text(yaml.safe_dump(spec, allow_unicode=True), encoding="utf-8")
    SpecSync(store).sync(tmp_path / "docs" / "kinds.yml", notation=_write(tmp_path / "docs", notation))

    glyph = next(d.payload for d in sldb_api.load_runtime_documents(store, None, include_linked=False) if d.name == "infra.api")
    assert glyph["fill"] == PAIR  # el GlyphDoc guarda el par tal cual
    nodes = {n["element"]: n for n in resolve_view(store, "component.kinds")["nodes"]}
    assert nodes["api"]["style"]["fill"] == PAIR and nodes["api"]["style"]["stroke"] == {"light": "#7a5c00", "dark": "#e6c34a"}
    assert nodes["web"]["style"]["fill"] == {"light": "#eef6ff", "dark": "#10233a"} and nodes["web"]["style"]["source"]["fill"] == "spec"
    view = resolve_view(store, "component.kinds")
    assert {l["color"]["dark"] for l in view["links"]} == {"#56b4e9"}
