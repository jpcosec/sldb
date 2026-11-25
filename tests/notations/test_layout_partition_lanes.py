"""Layout partition-lanes con `by` en NotationDoc y en la vista resuelta."""

from __future__ import annotations

from pathlib import Path

import pytest

import sldb.api as api
from sldb.api import resolve_view, sync_notation, sync_palette
from sldb.notations.notation_spec import NotationSpec

_GLYPH = {"id": "box", "title": "Box", "model": "SpecNodeDoc", "shape": "class-box", "label": "{title}"}


def _spec(layout: dict) -> NotationSpec:
    return NotationSpec(name="lanes-n", diagram_type="class", layout=layout, glyphs=[_GLYPH])


def test_partition_lanes_with_valid_by():
    assert _spec({"kind": "partition-lanes", "by": " lane "}).layout == {"kind": "partition-lanes", "by": "lane"}


def test_partition_lanes_without_by():
    assert _spec({"kind": "partition-lanes"}).layout == {"kind": "partition-lanes"}


def test_by_with_other_kind_rejected():
    with pytest.raises(ValueError, match="layout.by only applies to kind partition-lanes"):
        _spec({"kind": "graph", "by": "lane"})


@pytest.mark.parametrize("by", ["   ", "", 3])
def test_by_empty_or_not_str_rejected(by):
    with pytest.raises(ValueError, match="layout.by must be a non-empty field name"):
        _spec({"kind": "partition-lanes", "by": by})


def test_resolved_view_keeps_kind_and_by(tmp_path: Path):
    root = tmp_path / "project"
    root.mkdir()
    store = root / ".sldb"
    api.init_store(root)
    sync_palette(store, "default")
    notation = tmp_path / "lanes-n.yml"
    notation.write_text(
        "name: lanes-n\ntitle: Lanes\ndiagram_type: class\n"
        "layout: {kind: partition-lanes, by: lane}\n"
        "glyphs:\n  - id: box\n    title: Box\n    model: SpecNodeDoc\n    shape: class-box\n    label: \"{title}\"\n",
        encoding="utf-8",
    )
    sync_notation(store, notation)
    api.create_document(
        store, "SpecDoc", root / "sldb" / "specs" / "s.md",
        {"id": "s", "title": "S", "diagram_type": "class", "version": "1", "spec_path": "s.yml",
         "sha256": "x", "notation": "NotationDoc:lanes-n", "nodes": [], "category": "diagram",
         "nav": "", "summary": "", "style": {}, "description": ""},
        name="s",
    )
    view = resolve_view(store, "SpecDoc:s")
    assert view["layout"]["kind"] == "partition-lanes"
    assert view["layout"]["by"] == "lane"
