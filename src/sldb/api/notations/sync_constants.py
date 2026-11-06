"""Models and store directories managed by notation and palette sync."""

from __future__ import annotations

from pathlib import Path

MODEL_REFS = {
    "SpecDoc": "sldb.models.notation_models:SpecDoc",
    "SpecNodeDoc": "sldb.models.notation_models:SpecNodeDoc",
    "NotationDoc": "sldb.models.notation_models:NotationDoc",
    "GlyphDoc": "sldb.models.notation_models:GlyphDoc",
    "LinkDoc": "sldb.models.notation_models:LinkDoc",
    "ViewDoc": "sldb.models.notation_models:ViewDoc",
    "PaletteDoc": "sldb.models.notation_models:PaletteDoc",
}

_MANAGED_MODELS = ("SpecDoc", "SpecNodeDoc", "RelationDoc", "RelationTypeDoc", "NotationDoc", "GlyphDoc", "LinkDoc", "PaletteDoc")

RELATION_TYPES_DIR = Path("sldb") / "relation_types"
NOTATIONS_DIR = Path("sldb") / "notations"
PALETTES_DIR = Path("sldb") / "palettes"
