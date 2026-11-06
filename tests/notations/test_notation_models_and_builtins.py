"""Tests for notation & visualization models, legacy aliases, and builtin notations/palettes."""

import pytest
from sldb.api import (
    GlyphDoc,
    LinkDoc,
    NotationDoc,
    PaletteDoc,
    SpecDoc,
    SpecNodeDoc,
    ViewDoc,
    resolve_model_ref,
)
from sldb.api.model_registry.model_reference import same_model_class
from sldb.core.renderer import SLDBRenderer
from sldb.notations import (
    DEFAULT_NOTATIONS,
    builtin_notations,
    builtin_palettes,
    check_notation_style,
    check_palette,
    glyph_ref,
    link_ref,
    load_notation,
    load_palette,
    notation_palette,
    notation_ref,
    palette_ref,
    resolve_color,
    resolve_line_color,
    resolve_notation,
    resolve_palette,
    resolve_style,
)
from sldb.notations.exceptions import (
    InvalidColorError,
    UnknownShapeError,
    ValidationError,
)
from sldb.runtime.validation import extract_model_data


# --- 1. Model Instantiation and Validation ------------------------------------


def test_spec_doc_instantiation_and_roundtrip():
    doc = SpecDoc(
        id="test-spec",
        title="Test Spec",
        diagram_type="class",
        version="1.0",
        spec_path="specs/test.yml",
        sha256="abc123sha",
        nodes=["SpecNodeDoc:test-spec.nodeA", "SpecNodeDoc:test-spec.nodeB"],
        notation="NotationDoc:uml-class",
        category="core",
        nav="test",
        summary="A test specification",
        style={"kinds": {}},
        description="Detailed description of test spec.",
    )
    assert doc.id == "test-spec"
    assert doc.nodes == ["SpecNodeDoc:test-spec.nodeA", "SpecNodeDoc:test-spec.nodeB"]

    rendered = SLDBRenderer().render(doc)
    extracted = extract_model_data(SpecDoc, rendered)
    validated = SpecDoc.model_validate(extracted)
    assert validated.id == doc.id
    assert validated.diagram_type == doc.diagram_type
    assert validated.nodes == doc.nodes
    assert validated.notation == doc.notation


def test_spec_node_doc_instantiation_and_roundtrip():
    doc = SpecNodeDoc(
        id="test-spec.nodeA",
        title="Node A",
        spec="SpecDoc:test-spec",
        element="nodeA",
        kind="class",
        collection="classes",
        refs=["ClassDoc:MyClass"],
        atom_refs=["AtomDoc:atom-1"],
        contains=["SpecNodeDoc:test-spec.child"],
        data={"attributes": ["x: int", "y: str"]},
        description="Spec node description.",
    )
    assert doc.id == "test-spec.nodeA"
    assert doc.data == {"attributes": ["x: int", "y: str"]}

    rendered = SLDBRenderer().render(doc)
    extracted = extract_model_data(SpecNodeDoc, rendered)
    validated = SpecNodeDoc.model_validate(extracted)
    assert validated.id == doc.id
    assert validated.element == "nodeA"
    assert validated.data == doc.data
    assert validated.contains == doc.contains


def test_notation_doc_instantiation_and_roundtrip():
    doc = NotationDoc(
        id="custom-notation",
        title="Custom Notation",
        name="custom-notation",
        diagram_type="class",
        level="types",
        projection="all",
        layout={"kind": "graph", "direction": "TB"},
        markers=[{"id": "m1", "shape": "bullseye", "model": "SpecNodeDoc", "where": ""}],
        glyphs=["GlyphDoc:custom-notation.class_glyph"],
        links=["LinkDoc:custom-notation.inheritance"],
        palette="PaletteDoc:default",
        description="A custom notation for testing.",
    )
    assert doc.id == "custom-notation"
    assert len(doc.glyphs) == 1

    rendered = SLDBRenderer().render(doc)
    extracted = extract_model_data(NotationDoc, rendered)
    validated = NotationDoc.model_validate(extracted)
    assert validated.id == doc.id
    assert validated.name == doc.name
    assert validated.layout == doc.layout


def test_glyph_doc_instantiation_and_roundtrip():
    doc = GlyphDoc(
        id="custom-notation.class_glyph",
        title="Class Glyph",
        notation="NotationDoc:custom-notation",
        model="SpecNodeDoc",
        where='collection == "classes"',
        shape="class-box",
        label="{title}",
        label_style="bold",
        keyword="«class»",
        compartments=["data.attributes", "data.methods"],
        function="class",
        form="(node (class))",
        kind="class",
        fill="panel-fill",
        stroke="panel-stroke",
        icon="box",
        description="Glyph for class nodes.",
    )
    assert doc.id == "custom-notation.class_glyph"
    assert doc.shape == "class-box"

    rendered = SLDBRenderer().render(doc)
    extracted = extract_model_data(GlyphDoc, rendered)
    validated = GlyphDoc.model_validate(extracted)
    assert validated.id == doc.id
    assert validated.shape == doc.shape
    assert validated.compartments == doc.compartments


def test_link_doc_instantiation_and_roundtrip():
    doc = LinkDoc(
        id="custom-notation.inheritance",
        title="Inheritance Link",
        notation="NotationDoc:custom-notation",
        relation="inheritance",
        relation_type="RelationTypeDoc:reltype-inheritance",
        model="",
        draw="line",
        line="solid",
        source_end="none",
        target_end="hollow-triangle",
        label="",
        source_label="",
        target_label="",
        ends={},
        form="(relation inheritance)",
        color="panel-stroke",
        description="Inheritance arrow.",
    )
    assert doc.id == "custom-notation.inheritance"
    assert doc.target_end == "hollow-triangle"

    rendered = SLDBRenderer().render(doc)
    extracted = extract_model_data(LinkDoc, rendered)
    validated = LinkDoc.model_validate(extracted)
    assert validated.id == doc.id
    assert validated.relation == doc.relation
    assert validated.target_end == doc.target_end


def test_palette_doc_instantiation_and_roundtrip():
    doc = PaletteDoc(
        id="test-palette",
        name="test-palette",
        title="Test Palette",
        backgrounds={"light": "#ffffff", "dark": "#1a1a1a"},
        ink={"light": "#111111", "dark": "#eeeeee"},
        icon_set={"name": "lucide", "version": "1.0", "icons": ["box", "database"]},
        colors={"panel-fill": {"light": "#f5f5f5", "dark": "#252525"}},
        kinds={"service": {"shape": "rounded-box", "icon": "box", "fill": "panel-fill", "stroke": "panel-fill"}},
        description="Palette for testing.",
    )
    assert doc.id == "test-palette"
    assert doc.backgrounds["light"] == "#ffffff"

    rendered = SLDBRenderer().render(doc)
    extracted = extract_model_data(PaletteDoc, rendered)
    validated = PaletteDoc.model_validate(extracted)
    assert validated.id == doc.id
    assert validated.kinds == doc.kinds


def test_view_doc_instantiation_validation_and_gd25_fields():
    doc = ViewDoc(
        id="system-overview",
        name="system-overview",
        title="System Overview",
        nodes=[{"model": "SpecNodeDoc", "where": 'kind == "service"'}],
        relations=["contains", "dependency"],
        direction="both",
        notation="NotationDoc:component",
        layout={"kind": "graph", "style": "layered"},
        params=[{"name": "scope", "default": "backend"}, {"name": "depth", "required": True}],
        sections=[{"key": "architecture", "select": {"model": "SpecNodeDoc", "where": 'kind = {scope}'}}, {"key": "services", "select": {"prefix": "{depth}"}, "group_by": "kind"}],
        description="Overview of system services and dependencies.",
    )
    assert doc.id == "system-overview"
    assert [p.model_dump() for p in doc.params] == [{"name": "scope", "required": False, "default": "backend"}, {"name": "depth", "required": True, "default": None}]
    assert [s.key for s in doc.sections] == ["architecture", "services"]
    assert doc.sections[0].fields == ["*"] and doc.sections[1].group_by == "kind"

    rendered = SLDBRenderer().render(doc)
    extracted = extract_model_data(ViewDoc, rendered)
    validated = ViewDoc.model_validate(extracted)
    assert validated.id == doc.id
    assert validated.params == doc.params
    assert validated.sections == doc.sections

    # Default params and sections when omitted
    doc_defaults = ViewDoc(
        id="default-view",
        name="default-view",
        title="Default View",
        nodes=[{"model": "SpecNodeDoc"}],
    )
    assert doc_defaults.params == []
    assert doc_defaults.sections == []
    assert ViewDoc(id="v", name="v", title="V", params={}, sections=[]).params == []

    # Validation errors on invalid direction
    with pytest.raises(ValueError, match="direction.*must be both, outgoing or incoming"):
        ViewDoc(id="bad-dir", name="bad-dir", title="Bad", direction="diagonal")

    # Validation errors on invalid node structure
    with pytest.raises(ValueError, match="each view node entry needs a model"):
        ViewDoc(id="bad-node", name="bad-node", title="Bad", nodes=[{"where": "x == 1"}])


# --- 2. Model Reference Resolution & Aliasing ---------------------------------


def test_resolve_model_ref_legacy_spec2viz_aliases():
    for name, expected_cls in (
        ("SpecDoc", SpecDoc),
        ("SpecNodeDoc", SpecNodeDoc),
        ("NotationDoc", NotationDoc),
        ("GlyphDoc", GlyphDoc),
        ("LinkDoc", LinkDoc),
        ("PaletteDoc", PaletteDoc),
        ("ViewDoc", ViewDoc),
    ):
        legacy_ref = f"spec2viz.sldb_models:{name}"
        canonical_ref = f"sldb.models.notation_models:{name}"
        resolved_legacy = resolve_model_ref(legacy_ref)
        resolved_canonical = resolve_model_ref(canonical_ref)
        assert resolved_legacy is expected_cls
        assert resolved_canonical is expected_cls
        assert same_model_class(legacy_ref, canonical_ref) is True


# --- 3. Builtin Palettes and Palette Validation -------------------------------


def test_load_default_palette_and_wcag_validation():
    palettes = builtin_palettes()
    assert "default" in palettes
    palette = load_palette("default")
    assert palette.name == "default"
    assert palette.backgrounds.light == "#ffffff"
    assert palette.backgrounds.dark == "#0d1117"
    assert len(palette.icon_set.icons) > 0
    assert len(palette.kinds) > 0
    # check_palette should pass with no errors
    check_palette(palette)


def test_palette_color_resolution():
    palette = load_palette("default")
    # Resolve token
    color_dict = palette.color("database-fill")
    assert "light" in color_dict and "dark" in color_dict
    assert color_dict["light"].startswith("#")

    # Resolve direct hex
    hex_color = palette.color("#abcdef")
    assert hex_color == {"light": "#abcdef", "dark": "#abcdef"}

    # Resolve dual-theme dict
    dual = palette.color({"light": "#112233", "dark": "#445566"})
    assert dual == {"light": "#112233", "dark": "#445566"}

    # Invalid color raises InvalidColorError
    with pytest.raises(InvalidColorError):
        palette.color("nonexistent-color-token")


# --- 4. Builtin Notations and Validation --------------------------------------


def test_all_8_builtin_notations_load_and_validate():
    expected_8 = {
        "activity",
        "component-view-matrix",
        "component",
        "deployment",
        "reflection",
        "statechart",
        "uml-class",
        "uml-sequence",
    }
    notations = builtin_notations()
    assert set(notations.keys()) == expected_8

    for name in expected_8:
        notation = load_notation(name)
        assert notation.name == name
        assert len(notation.glyphs) >= 1
        # Style check passes against default palette
        check_notation_style(notation)
        assert isinstance(notation.relations, list)
        assert isinstance(notation.models, list)
        assert len(notation.models) >= 1


def test_default_notations_map():
    assert DEFAULT_NOTATIONS["class"] == "uml-class"
    assert DEFAULT_NOTATIONS["state"] == "statechart"
    assert DEFAULT_NOTATIONS["sequence"] == "uml-sequence"
    assert DEFAULT_NOTATIONS["activity"] == "activity"
    assert DEFAULT_NOTATIONS["component"] == "component"
    assert DEFAULT_NOTATIONS["deployment"] == "deployment"
    assert DEFAULT_NOTATIONS["component_view_matrix"] == "component-view-matrix"
    assert DEFAULT_NOTATIONS["reflection"] == "reflection"


# --- 5. Styling Resolution and Precedence -------------------------------------


def test_resolve_style_precedence():
    palette = load_palette("default")
    palette_payload = {
        "name": palette.name,
        "colors": {k: v.model_dump() for k, v in palette.colors.items()},
        "kinds": {k: v.model_dump() for k, v in palette.kinds.items()},
        "icon_set": palette.icon_set.model_dump(),
        "ink": palette.ink.model_dump(),
    }

    # Layer 3: Palette only
    style_p = resolve_style(None, "database", None, palette_payload)
    assert style_p["source"]["fill"] == "palette"
    assert style_p["source"]["icon"] == "palette"

    # Layer 2: Spec overrides fill
    spec_kinds = {"database": {"fill": "#123456"}}
    style_s = resolve_style(None, "database", spec_kinds, palette_payload)
    assert style_s["source"]["fill"] == "spec"
    assert style_s["fill"] == {"light": "#123456", "dark": "#123456"}
    assert style_s["source"]["icon"] == "palette"

    # Layer 1: Glyph overrides spec and palette
    glyph_payload = {"fill": "#654321", "icon": "server"}
    style_g = resolve_style(glyph_payload, "database", spec_kinds, palette_payload)
    assert style_g["source"]["fill"] == "glyph"
    assert style_g["fill"] == {"light": "#654321", "dark": "#654321"}
    assert style_g["source"]["icon"] == "glyph"
    assert style_g["icon"] == "server"


def test_resolve_line_color():
    palette = load_palette("default")
    palette_payload = {
        "name": palette.name,
        "colors": {k: v.model_dump() for k, v in palette.colors.items()},
    }
    assert resolve_line_color(None, palette_payload) is None
    assert resolve_line_color({"color": ""}, palette_payload) is None

    res = resolve_line_color({"color": "#112233"}, palette_payload)
    assert res == {"light": "#112233", "dark": "#112233"}


def test_refs_helper_functions():
    assert palette_ref("default") == "PaletteDoc:default"
    assert notation_ref("uml-class") == "NotationDoc:uml-class"
    assert glyph_ref("uml-class", "class") == "GlyphDoc:uml-class.class"
    assert link_ref("uml-class", "inheritance") == "LinkDoc:uml-class.inheritance"
