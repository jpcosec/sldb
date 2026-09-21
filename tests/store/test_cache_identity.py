"""Process-wide caches identify a document by what it is derived from, not by a model's name.

Payloads and tags are what a model *class* makes of a text; a runtime document also belongs to
a store. The caches used to key on (relative path, hash_c, model name), so in one process two
stores holding a `d.md` of the same text under two different classes called `Spec` shared one
entry: the second store came back with the first one's tags, and `hash_d` — which is persisted
— could be computed from the other class's payload. Tests had been dodging it by giving their
documents distinct text.
"""

from __future__ import annotations

import sys
from pathlib import Path

from sldb import api
from sldb.store.hashing import hash_payload
from sldb.store.io import load_store_index
from sldb.store.query import load_runtime_documents
from sldb.store.runtime_cache import payload_of
from sldb.store.semantic_doc_tags import tags_of

SPEC = '''from pydantic import Field
from sldb import StructuredNLDoc


class Spec(StructuredNLDoc):
    __semantics__ = {semantics}
    __template__ = "# ⸢rev•{field}⸥"
    {field}: str = Field(description="The heading.")
'''


def world(base: Path, module: str, semantics: str, field: str = "title") -> tuple[Path, Path]:
    """A store with one `Spec` document at `d.md` whose text is `# D` — the same in every world."""
    sys.modules.pop(module, None)
    (base / f"{module}.py").write_text(SPEC.format(semantics=semantics, field=field), encoding="utf-8")
    root = base / "world"
    root.mkdir()
    store = api.init_store(root).store_path
    api.add_model(store, f"{module}:Spec", str(base))
    api.create_document(store, "Spec", root / "d.md", {field: "D"}, "d", str(base))
    return store, root


def tags(store: Path) -> list[str]:
    return sorted(e.target.rsplit("/", 1)[-1] for e in api.edges_from(store, "Spec:d", "tagged_as"))


def test_two_stores_same_path_same_text_same_class_name_keep_their_own_tags(tmp_path: Path):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    a, _ = world(tmp_path / "a", "cache_identity_alpha", '{"type": ["alpha"]}')
    b, _ = world(tmp_path / "b", "cache_identity_beta", '{"type": ["beta"]}')
    assert "type.alpha" in tags(a) and "type.beta" not in tags(a)
    assert "type.beta" in tags(b) and "type.alpha" not in tags(b)


def test_a_payload_is_what_this_class_extracted_and_hash_d_is_computed_from_it(tmp_path: Path):
    """Same text, two classes that read it into different fields: each gets its own payload."""
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    a, _ = world(tmp_path / "a", "cache_identity_title", '{"type": ["t"]}', field="title")
    b, _ = world(tmp_path / "b", "cache_identity_name", '{"type": ["n"]}', field="name")
    docs = {d.store_path: d for s in (a, b) for d in load_runtime_documents(s, api.resolve_model_ref, str(s.parent.parent))}
    title_cls, name_cls = docs[a].model_type, docs[b].model_type
    hash_c = _entry(b).hash_c
    assert hash_c == _entry(a).hash_c, "the premise: the two texts are identical"
    assert payload_of("d.md", hash_c, title_cls) == {"title": "D"}
    assert payload_of("d.md", hash_c, name_cls) == {"name": "D"}
    assert _entry(b).hash_d == hash_payload({"name": "D"})


def test_a_model_redefined_in_a_running_process_gets_its_new_tags(tmp_path: Path):
    """The long-running case: same document, a class object with new `__semantics__`."""
    (tmp_path / "a").mkdir()
    store, root = world(tmp_path / "a", "cache_identity_v1", '{"type": ["before"]}')
    before = load_runtime_documents(store, api.resolve_model_ref, str(tmp_path / "a"))[0]
    after_cls = type("Spec", (before.model_type,), {"__semantics__": {"type": ["after"]}})
    entry = _entry(store)
    first = tags_of(entry, root / "d.md", before.model_type, "Spec")
    second = tags_of(entry, root / "d.md", after_cls, "Spec")
    assert "type.before" in first and "type.after" in second and "type.before" not in second


def _entry(store: Path):
    from sldb.store import documents_hash

    model = next(m for m in load_store_index(store).models if m.name == "Spec")
    return next(iter(documents_hash.entries_of(store, model.name)))
