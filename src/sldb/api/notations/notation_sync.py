"""Synchronize visual palettes and notations to an SLDB store.

Writes PaletteDoc, NotationDoc, GlyphDoc, LinkDoc, and RelationTypeDoc to the store
using the public `sldb.api` functions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from sldb.notations.notation import (
    ANY_RELATION,
    glyph_ref,
    link_ref,
    load_notation,
    notation_palette,
    notation_ref,
    resolve_notation,
)
from sldb.notations.palette import load_palette, palette_ref

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


@dataclass
class SyncReport:
    spec_id: str
    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    relation_types_added: list[str] = field(default_factory=list)
    notation: str = ""
    unresolved: list[str] = field(default_factory=list)
    edge_errors: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_id": self.spec_id,
            "created": list(self.created),
            "updated": list(self.updated),
            "deleted": list(self.deleted),
            "relation_types_added": list(self.relation_types_added),
            "notation": self.notation,
            "unresolved": list(self.unresolved),
            "edge_errors": list(self.edge_errors),
            "problems": list(self.problems),
        }


class _StoreWriter:
    """Common logic for synchronizing notations and palettes to an sldb store."""

    def __init__(self, store_path: Path | str, pythonpath: str | None = None, actor: str = "sldb"):
        self.store_path = Path(store_path).resolve()
        self.pythonpath = pythonpath
        self.actor = actor
        self._prepared = False
        self._root: Path | None = None

    def prepare(self) -> None:
        """Register notation models and builtin relations; idempotent."""
        if self._prepared:
            return
        import sldb.api as api

        for name, ref in MODEL_REFS.items():
            try:
                api.load_registered_model(self.store_path, name, self.pythonpath)
            except Exception:
                api.add_model(self.store_path, ref, self.pythonpath, actor=self.actor)
        api.init_relations(self.store_path, self.pythonpath)
        self._prepared = True

    @property
    def root(self) -> Path:
        if self._root is None:
            import sldb.api as api

            self._root = Path(api.open_store(self.store_path).project_root).resolve()
        return self._root

    def existing_documents(self) -> dict[tuple[str, str], Any]:
        import sldb.api as api

        return {
            (str(doc.model_name), str(doc.name)): doc
            for doc in api.load_runtime_documents(self.store_path, self.pythonpath, include_linked=False)
            if str(doc.model_name) in _MANAGED_MODELS
        }

    def upsert(self, existing: dict, report: SyncReport, model: str, name: str, path: Path, payload: dict) -> None:
        import sldb.api as api

        if (model, name) in existing:
            api.save_document_payload(self.store_path, model, name, payload, self.pythonpath, actor=self.actor)
            report.updated.append(f"{model}:{name}")
        else:
            api.create_document(self.store_path, model, path, payload, name=name, pythonpath=self.pythonpath, actor=self.actor)
            report.created.append(f"{model}:{name}")

    def ensure_relation_type(self, existing: dict, report: SyncReport, relation: str, description: str) -> None:
        """Creates `RelationTypeDoc` for `relation` if not present in store."""
        import sldb.api as api

        type_name = f"reltype-{relation}"
        if ("RelationTypeDoc", type_name) in existing or api.doc_exists(self.store_path, f"RelationTypeDoc/{type_name}"):
            return
        payload = {
            "title": relation,
            "name": relation,
            "direction": "directed",
            "cardinality": "many_to_many",
            "axis": "",
            "source_types": [],
            "target_types": [],
            "condition": "",
            "description": description,
        }
        api.create_document(
            self.store_path,
            "RelationTypeDoc",
            self.root / RELATION_TYPES_DIR / f"{relation}.md",
            payload,
            name=type_name,
            pythonpath=self.pythonpath,
            actor=self.actor,
        )
        report.relation_types_added.append(relation)
        existing[("RelationTypeDoc", type_name)] = None

    def delete(self, existing: dict, report: SyncReport, model: str, name: str) -> None:
        import sldb.api as api

        api.delete_document(self.store_path, str(existing[(model, name)].path), self.pythonpath, actor=self.actor)
        report.deleted.append(f"{model}:{name}")

    def finish(self, report: SyncReport) -> SyncReport:
        import sldb.api as api

        api.rebuild_edges(self.store_path, self.pythonpath)
        report.edge_errors = list(api.check_edges(self.store_path).errors)
        return report


class PaletteSync(_StoreWriter):
    """Writes a palette (PaletteDoc) to a store."""

    def sync(self, name_or_path: str | Path = "default", *, base: Path | None = None, finish: bool = True) -> SyncReport:
        palette = load_palette(name_or_path, base)
        report = SyncReport(spec_id=palette.name)
        self.prepare()
        existing = self.existing_documents()
        payload = {
            "id": palette.name,
            "name": palette.name,
            "title": palette.title or palette.name,
            "backgrounds": palette.backgrounds.model_dump(),
            "ink": palette.ink.model_dump(),
            "icon_set": palette.icon_set.model_dump(),
            "colors": {k: v.model_dump() for k, v in palette.colors.items()},
            "kinds": {k: v.model_dump() for k, v in palette.kinds.items()},
            "description": palette.description,
        }
        self.upsert(existing, report, "PaletteDoc", palette.name, self.root / PALETTES_DIR / f"{palette.name}.md", payload)
        report.notation = palette_ref(palette.name)
        return self.finish(report) if finish else report


class NotationSync(_StoreWriter):
    """Writes a notation (NotationDoc, GlyphDoc, LinkDoc and its PaletteDoc) to a store."""

    def sync(self, name_or_path: str | Path, *, finish: bool = True) -> SyncReport:
        import sldb.api as api

        notation = load_notation(name_or_path)
        report = SyncReport(spec_id=notation.name, notation=notation_ref(notation.name))
        self.prepare()
        resolved_path = resolve_notation(name_or_path)
        palette = notation_palette(notation, resolved_path.parent if resolved_path else None)
        if palette is not None:
            sub = PaletteSync(self.store_path, self.pythonpath, self.actor).sync(
                notation.palette or palette.name,
                base=resolved_path.parent if resolved_path else None,
                finish=False,
            )
            for attr in ("created", "updated"):
                getattr(report, attr).extend(getattr(sub, attr))
        existing = self.existing_documents()
        out = self.root / NOTATIONS_DIR / notation.name

        # Verify model registrations
        for model in notation.models:
            try:
                api.load_registered_model(self.store_path, model, self.pythonpath)
            except Exception:
                report.unresolved.append(f"notation {notation.name}: model '{model}' is not registered in the store")

        # Ensure declared relations exist
        for relation in notation.relations:
            self.ensure_relation_type(
                existing,
                report,
                relation,
                f"Relacion `{relation}` declarada por la notacion `{notation.name}`.",
            )

        current: set[tuple[str, str]] = set()
        for glyph in notation.glyphs:
            name = f"{notation.name}.{glyph.id}"
            default_form = f'(where {glyph.model} "{glyph.where}")' if glyph.where else f"(model {glyph.model})"
            payload = {
                "id": name,
                "title": glyph.title or glyph.id,
                "notation": notation_ref(notation.name),
                "model": glyph.model,
                "where": glyph.where,
                "shape": glyph.shape,
                "label": glyph.label,
                "label_style": glyph.label_style,
                "keyword": glyph.keyword,
                "compartments": list(glyph.compartments),
                "function": glyph.function,
                "form": glyph.form or default_form,
                "description": glyph.description,
                "kind": glyph.kind or None,
                "fill": glyph.fill or None,
                "stroke": glyph.stroke or None,
                "icon": glyph.icon or None,
            }
            self.upsert(existing, report, "GlyphDoc", name, out / "glyphs" / f"{glyph.id}.md", payload)
            current.add(("GlyphDoc", name))

        for link in notation.links:
            name = f"{notation.name}.{link.id}"
            default_form = f"(model {link.model})" if link.model else f"(relation {link.relation})"
            payload = {
                "id": name,
                "title": link.title or link.id,
                "notation": notation_ref(notation.name),
                "relation": link.relation,
                "relation_type": "" if link.relation == ANY_RELATION else f"RelationTypeDoc:reltype-{link.relation}",
                "model": link.model,
                "draw": link.draw,
                "line": link.line,
                "source_end": link.source_end,
                "target_end": link.target_end,
                "label": link.label,
                "source_label": link.source_label,
                "target_label": link.target_label,
                "ends": {k: e.model_dump() for k, e in link.ends.items()},
                "form": link.form or default_form,
                "description": link.description,
                "color": link.color or None,
            }
            self.upsert(existing, report, "LinkDoc", name, out / "links" / f"{link.id}.md", payload)
            current.add(("LinkDoc", name))

        payload = {
            "id": notation.name,
            "title": notation.title or notation.name,
            "name": notation.name,
            "diagram_type": notation.diagram_type,
            "level": notation.level,
            "projection": notation.projection,
            "layout": dict(notation.layout),
            "markers": [m.model_dump() for m in notation.markers],
            "glyphs": [glyph_ref(notation.name, g.id) for g in notation.glyphs],
            "links": [link_ref(notation.name, l.id) for l in notation.links],
            "palette": palette_ref(palette.name) if palette is not None else None,
            "description": notation.description,
        }
        self.upsert(existing, report, "NotationDoc", notation.name, out / "notation.md", payload)

        prefix = f"{notation.name}."
        for (model, name) in list(existing):
            if model in ("GlyphDoc", "LinkDoc") and name.startswith(prefix) and (model, name) not in current:
                self.delete(existing, report, model, name)

        return self.finish(report) if finish else report


def sync_palette(
    store: Path | str,
    name_or_path: str | Path = "default",
    pythonpath: str | None = None,
    actor: str = "sldb",
) -> SyncReport:
    """Synchronize a palette into the store."""
    return PaletteSync(store, pythonpath, actor).sync(name_or_path)


def sync_notation(
    store: Path | str,
    name_or_path: str | Path,
    pythonpath: str | None = None,
    actor: str = "sldb",
) -> SyncReport:
    """Synchronize a notation and its palette into the store."""
    return NotationSync(store, pythonpath, actor).sync(name_or_path)


__all__ = [
    "SyncReport",
    "PaletteSync",
    "NotationSync",
    "sync_palette",
    "sync_notation",
]
