"""Write the builtin relation types as tracked documents and register them as predicates."""

from __future__ import annotations

from pathlib import Path

from sldb.api.edges.relations_init_report import RelationsInitReport
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.models.builtin_relation_types import BUILTIN_RELATION_TYPES, builtin_doc_name, builtin_payload
from sldb.runtime.validation import render_model_markdown
from sldb.store import documents_hash
from sldb.store.io import load_store_index, save_store_index
from sldb.store.models import PredicateEntry
from sldb.store.ops import track_document

BUILTIN_DIR = Path("sldb") / "relation_types"


def write_builtin_relation_types(sp: Path, root: Path, pythonpath: str | None, report: RelationsInitReport) -> None:
    """One RelationTypeDoc per builtin relation that is not tracked yet, under `sldb/relation_types/`."""
    registered = load_registered_model(sp, "RelationTypeDoc", pythonpath)
    tracked = {e.name for e in documents_hash.entries_of(sp, "RelationTypeDoc")}
    for spec in (s for s in BUILTIN_RELATION_TYPES if builtin_doc_name(s) not in tracked):
        path = root / BUILTIN_DIR / f"{spec['name']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_model_markdown(registered.model_type, builtin_payload(spec)) + "\n", encoding="utf-8")
        track_document(sp, root, load_store_index(sp), registered.model_type, registered.entry, path, builtin_doc_name(spec), resolve_model_ref, pythonpath)
        report.types_written.append(spec["name"])


def register_builtin_predicates(sp: Path, report: RelationsInitReport) -> None:
    """Each builtin relation name as an sldb predicate, so prose links share the vocabulary."""
    idx = load_store_index(sp)
    known = {p.name for p in idx.predicates}
    for spec in (s for s in BUILTIN_RELATION_TYPES if s["name"] not in known):
        idx.predicates.append(PredicateEntry(name=spec["name"], axis=spec["axis"], description=spec["description"]))
        report.predicates_added.append(spec["name"])
    if report.predicates_added:
        save_store_index(sp, idx)
