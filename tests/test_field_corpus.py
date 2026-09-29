"""Per-field indexing: the unit of indexing is the field, so the unit of invalidation is too.

A document's embedding is invalidated by an edit anywhere in it; a field's only by an edit
to that field. These tests pin the contracts that follow from it: the address space
(`docs/<Model>/<doc>/<field>`, the one `sldb fields` takes), the selective re-embedding
driven by `DocumentEntry.field_hashes`, the ranking that returns hits carrying the document
they belong to, and the audit that reports drift per field.
"""

from __future__ import annotations

import sys
from hashlib import md5
from pathlib import Path

from sldb import api
from sldb.api import Corpus, FieldProjection, field_id, split_field_id
from sldb.api.corpus.field_projection import default_field_text
from sldb.store.hashing import hash_field_map_of
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "field_index_models"


class BagOfWordsEmbedder:
    """A deterministic Embedder: real vectors computed from the text, no model download.

    One vector per word, summed into 64 slots; cosine similarity then ranks by shared
    vocabulary, which is what the ranking tests need to observe.
    """

    def __init__(self) -> None:
        self.embedded: list[str] = []

    def id(self) -> str:
        return "bag-of-words"

    def embed(self, texts) -> list[list[float]]:
        self.embedded.extend(texts)
        return [self._vector(t) for t in texts]

    def _vector(self, text: str) -> list[float]:
        v = [0.0] * 64
        for w in text.lower().split():
            v[int(md5(w.encode()).hexdigest(), 16) % 64] += 1.0
        return v


MODEL = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n⸢rev•body⸥"
    title: str = Field(description="The heading.")
    body: str = Field(description="The prose.")
'''

UNO = {"title": "Deploy del indice de campos", "body": "El cuerpo de la nota uno habla del deploy y del indice."}
DOS = {"title": "Cocina del pan artesanal", "body": "El cuerpo de la nota dos habla de cocina y de pan."}


def project(tmp_path: Path) -> tuple[Path, Path, BagOfWordsEmbedder]:
    """A store with two `Note`s of disjoint vocabularies, and a counting embedder for it."""
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODEL, encoding="utf-8")
    store = api.init_store(tmp_path).store_path
    api.add_model(store, f"{MODULE}:Note", str(tmp_path))
    api.create_document(store, "Note", tmp_path / "uno.md", UNO, "uno", str(tmp_path))
    api.create_document(store, "Note", tmp_path / "dos.md", DOS, "dos", str(tmp_path))
    return store, tmp_path, BagOfWordsEmbedder()


def corpus(store: Path, tmp_path: Path, embedder: BagOfWordsEmbedder) -> Corpus:
    invalidate_runtime_cache()
    return Corpus(store, str(tmp_path), tmp_path / "derived", embedder=embedder)


# --- the address space ---------------------------------------------------------------


def test_field_id_roundtrips_through_the_fields_address_space():
    plain = field_id("Note", "uno", "body")
    linked = field_id("Note", "uno", "steps/2/title", "other-store")
    assert plain == "docs/Note/uno/body"
    assert split_field_id(plain) == (None, "Note", "uno", "body")
    assert split_field_id(linked) == ("other-store", "Note", "uno", "steps/2/title")
    assert split_field_id("Note:uno") is None
    assert split_field_id("docs/uno") is None


def test_projection_excludes_identity_fields_and_short_text():
    projection = FieldProjection()
    assert projection.admits("body") and not projection.admits("name") and not projection.admits("tags")
    assert projection.text_of("corto") == ""
    assert default_field_text(["uno ", " dos"]) == "uno\ndos"


# --- entries: the field's own hash, the fields address -------------------------------


def test_entries_carry_the_fields_own_hash(tmp_path: Path):
    store, root, embedder = project(tmp_path)
    entries = corpus(store, root, embedder).field_entries()
    by_id = {e.id: e for e in entries}
    assert set(by_id) == {"docs/Note/uno/body", "docs/Note/uno/title",
                         "docs/Note/dos/body", "docs/Note/dos/title"}
    uno_body = by_id["docs/Note/uno/body"]
    assert uno_body.document_id == "Note:uno" and uno_body.payload == UNO
    assert uno_body.hash == hash_field_map_of(UNO)["body"]


def test_store_without_field_hashes_still_yields_hashes(tmp_path: Path):
    """An empty map means "could not compute" (a pre-migration store), not "nothing changed"."""
    import yaml
    store, root, embedder = project(tmp_path)
    doc = next(store.glob("core/documents/Note/uno.yaml"))
    record = yaml.safe_load(doc.read_text(encoding="utf-8"))
    del record["field_hashes"]
    doc.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")
    entries = corpus(store, root, embedder).field_entries()
    entry = next(e for e in entries if e.id == "docs/Note/uno/body")
    assert entry.hash == hash_field_map_of(UNO)["body"]


# --- invalidation: one field moved, one field re-embedded ---------------------------


def test_refresh_reembeds_only_the_field_that_moved(tmp_path: Path):
    store, root, embedder = project(tmp_path)
    first = corpus(store, root, embedder).refresh_fields()
    assert first["embedded"] == 4 and first["reused"] == 0

    same = corpus(store, root, embedder).refresh_fields()
    assert same == {"embedded": 0, "reused": 4, "dropped": 0}
    assert len(embedder.embedded) == 4

    api.save_document_payload(store, "Note", "uno", {**UNO, "body": "El cuerpo reescrito con otras palabras."}, str(root))
    moved = corpus(store, root, embedder).refresh_fields()
    assert moved["embedded"] == 1 and moved["reused"] == 3
    assert embedder.embedded[-1].startswith("El cuerpo reescrito")


def test_rank_fields_returns_the_document_a_hit_belongs_to(tmp_path: Path):
    store, root, embedder = project(tmp_path)
    corpus(store, root, embedder).refresh_fields()
    hits = corpus(store, root, embedder).rank_fields("receta de cocina y pan", k=4, refresh=False)
    assert hits and hits[0].document_id == "Note:dos"
    assert hits[0].payload == DOS and hits[0].id.startswith("docs/Note/dos/")
    assert hits == sorted(hits, key=lambda h: -h.score)

    among = corpus(store, root, embedder).rank_fields("deploy del indice", k=4, among=["Note:uno"], refresh=False)
    assert among and {h.document_id for h in among} == {"Note:uno"}


def test_audit_reports_drift_per_field_and_keeps_indexes_apart(tmp_path: Path):
    store, root, embedder = project(tmp_path)
    field_corpus = corpus(store, root, embedder)
    field_corpus.refresh()
    field_corpus.refresh_fields()
    assert field_corpus.audit_fields()["clean"]

    api.save_document_payload(store, "Note", "uno", {**UNO, "body": "Otro cuerpo distinto para nada."}, str(root))
    report = field_corpus.audit_fields()
    assert not report["clean"] and "docs/Note/uno/body" in report["stale"]
    assert field_corpus.field_index_path.name.startswith("fields.")
    assert field_corpus.index_path.name.startswith("docs.")
