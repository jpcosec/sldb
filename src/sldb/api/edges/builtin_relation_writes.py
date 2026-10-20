"""Write the builtin relation types as tracked documents and register them as predicates."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.provenance_stamp import stamped_file
from sldb.api.edges.relations_init_report import RelationsInitReport
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.models.builtin_relation_types import BUILTIN_RELATION_TYPES, builtin_doc_name, builtin_payload
from sldb.runtime.validation import extract_model_data, render_model_markdown
from sldb.store import documents_hash
from sldb.store.io import load_store_index, save_store_index
from sldb.store.models import PredicateEntry
from sldb.store.ops import track_document

BUILTIN_DIR = Path("sldb") / "relation_types"


def write_builtin_relation_types(sp: Path, root: Path, pythonpath: str | None, report: RelationsInitReport) -> None:
    """One RelationTypeDoc per builtin relation that is not tracked yet, under `sldb/relation_types/`."""
    registered = load_registered_model(sp, "RelationTypeDoc", pythonpath)
    tracked = {e.name: e.path for e in documents_hash.entries_of(sp, "RelationTypeDoc")}
    for spec in (s for s in BUILTIN_RELATION_TYPES if _tracked_path(s, tracked) is None):
        path = root / BUILTIN_DIR / f"{spec['name']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(stamped_file(path, render_model_markdown(registered.model_type, builtin_payload(spec), root) + "\n", registered.model_type, "init_relations"), encoding="utf-8")
        track_document(sp, root, load_store_index(sp), registered.model_type, registered.entry, path, builtin_doc_name(spec), resolve_model_ref, pythonpath)
        report.types_written.append(spec["name"])
    _refresh_outdated(root, registered.model_type, tracked, report)


#: What a builtin's spec decides; a tracked builtin that disagrees on any of these is rewritten.
_SPEC_KEYS = ("cardinality", "axis", "description", "source_types", "target_types")


def _tracked_path(spec, tracked: dict[str, str]) -> str | None:
    """Where the relation type is tracked: as the builtin `reltype-<name>`, or as an authored
    type under its bare name (selfdoc's `contains`), which a builtin must not duplicate."""
    return tracked.get(builtin_doc_name(spec)) or tracked.get(spec["name"])


def _refresh_outdated(root: Path, model_type, tracked: dict[str, str], report: RelationsInitReport) -> None:
    """Rewrite a tracked builtin whose spec moved (`has_model` became many-to-many when stores
    began sharing models): the index produces those edges, so sldb owns their type. Compared
    on the payload, so a builtin that only reads differently is left alone."""
    for spec in BUILTIN_RELATION_TYPES:
        rel = tracked.get(builtin_doc_name(spec))  # only what sldb wrote: a bare name may be authored
        path = root / rel if rel else None
        if spec["name"] in report.types_written or path is None or not path.exists():
            continue
        current, wanted = extract_model_data(model_type, path.read_text(encoding="utf-8")), builtin_payload(spec)
        if any(current.get(k) != wanted[k] for k in _SPEC_KEYS):
            path.write_text(stamped_file(path, render_model_markdown(model_type, wanted, root) + "\n", model_type, "init_relations"), encoding="utf-8")
            report.types_updated.append(spec["name"])


def register_builtin_predicates(sp: Path, report: RelationsInitReport) -> None:
    """Each builtin relation name as an sldb predicate, so prose links share the vocabulary."""
    idx = load_store_index(sp)
    known = {p.name for p in idx.predicates}
    for spec in (s for s in BUILTIN_RELATION_TYPES if s["name"] not in known):
        idx.predicates.append(PredicateEntry(name=spec["name"], axis=spec["axis"], description=spec["description"]))
        report.predicates_added.append(spec["name"])
    if report.predicates_added:
        save_store_index(sp, idx)
