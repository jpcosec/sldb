"""The steps of a notation sync: palette, model checks, relations, glyphs, links, pruning."""

from __future__ import annotations

from typing import Any

from sldb.api.notations.glyph_payload import glyph_payload
from sldb.api.notations.link_payload import link_payload
from sldb.api.notations.notation_payloads import notation_payload
from sldb.api.notations.palette_sync import PaletteSync
from sldb.api.notations.sync_constants import NOTATIONS_DIR
from sldb.notations.notation import notation_palette, resolve_notation


def sync_palette_of(writer: Any, notation: Any, name_or_path: Any, report: Any) -> Any:
    """Sync the notation's palette (if any) into `report`; returns the palette."""
    resolved_path = resolve_notation(name_or_path)
    base = resolved_path.parent if resolved_path else None
    palette = notation_palette(notation, base)
    if palette is not None:
        sub = PaletteSync(writer.store_path, writer.pythonpath, writer.actor)
        sub_report = sub.sync(notation.palette or palette.name, base=base, finish=False)
        report.created.extend(sub_report.created)
        report.updated.extend(sub_report.updated)
    return palette


def check_models(writer: Any, notation: Any, report: Any) -> None:
    """Record each model of the notation that is not registered in the store."""
    import sldb.api as api

    for model in notation.models:
        try:
            api.load_registered_model(writer.store_path, model, writer.pythonpath)
        except Exception:
            report.unresolved.append(f"notation {notation.name}: model '{model}' is not registered in the store")


def ensure_relations(writer: Any, existing: dict, report: Any, notation: Any) -> None:
    """Ensure a `RelationTypeDoc` exists for every relation the notation declares."""
    for relation in notation.relations:
        description = f"Relacion `{relation}` declarada por la notacion `{notation.name}`."
        writer.ensure_relation_type(existing, report, relation, description)


def upsert_glyphs(writer: Any, existing: dict, report: Any, notation: Any) -> set[tuple[str, str]]:
    """Upsert every glyph; returns their `(model, name)` keys."""
    out = writer.root / NOTATIONS_DIR / notation.name
    for glyph in notation.glyphs:
        payload = glyph_payload(notation, glyph)
        writer.upsert(existing, report, "GlyphDoc", payload["id"], out / "glyphs" / f"{glyph.id}.md", payload)
    return {("GlyphDoc", f"{notation.name}.{g.id}") for g in notation.glyphs}


def upsert_links(writer: Any, existing: dict, report: Any, notation: Any) -> set[tuple[str, str]]:
    """Upsert every link; returns their `(model, name)` keys."""
    out = writer.root / NOTATIONS_DIR / notation.name
    for link in notation.links:
        payload = link_payload(notation, link)
        writer.upsert(existing, report, "LinkDoc", payload["id"], out / "links" / f"{link.id}.md", payload)
    return {("LinkDoc", f"{notation.name}.{l.id}") for l in notation.links}


def write_notation(writer: Any, existing: dict, report: Any, notation: Any, palette: Any) -> set[tuple[str, str]]:
    """Upsert glyphs, links and the notation itself; returns the glyph and link keys."""
    check_models(writer, notation, report)
    ensure_relations(writer, existing, report, notation)
    current = upsert_glyphs(writer, existing, report, notation) | upsert_links(writer, existing, report, notation)
    path = writer.root / NOTATIONS_DIR / notation.name / "notation.md"
    writer.upsert(existing, report, "NotationDoc", notation.name, path, notation_payload(notation, palette))
    return current


def prune(writer: Any, existing: dict, report: Any, notation: Any, current: set[tuple[str, str]]) -> None:
    """Delete glyphs and links of this notation that the sync no longer declares."""
    prefix = f"{notation.name}."
    for model, name in list(existing):
        if model in ("GlyphDoc", "LinkDoc") and name.startswith(prefix) and (model, name) not in current:
            writer.delete(existing, report, model, name)
