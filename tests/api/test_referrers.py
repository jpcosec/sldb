"""GD22: `sldb.api.referrers` and `sldb edges referrers` (docs/architecture/references.md).

A card A is referenced by B (scalar field `about`), by C (list field `related`, among two other
values, and a mention in its body), by a review R (a `__doc_anchors__` field) and by an
untracked note D (a mention in prose the project graph's `MentionPattern` captures). The
references come from the edge index (fields) and from the project graph (mentions); nothing
walks the project once both are warm.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api.edges.project_graph import DocumentSurface, LineMentions, MentionPattern, ProjectGraphConfig
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import save_declaration
from sldb.cli import main
from sldb.core.exceptions import SLDBDocumentTargetError

MODULE = "sldb_gd22_reference_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Card(StructuredNLDoc):
    __references__ = ["about", "related"]
    __reference_models__ = {"about": ["Card"], "related": ["Card"]}
    __template__ = "---\\nid: ⸢rev•id⸥\\nabout: ⸢optrev•about⸥\\nrelated: ⸢rev,list•related⸥\\n---\\n\\n# ⸢rev•title⸥\\n\\n⸢rev•body⸥"
    id: str = Field(description="Card id.")
    title: str = Field(description="Title.")
    about: str | None = Field(default=None, description="The card this one is about.")
    related: list[str] = Field(default_factory=list, description="Related cards.")
    body: str = Field(default="", description="Body.")


class Review(StructuredNLDoc):
    __doc_anchors__ = ["subject"]
    __template__ = "---\\nsubject: ⸢optrev•subject⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    subject: str | None = Field(default=None, description="The reviewed card.")


class Strict(StructuredNLDoc):
    __references__ = ["about"]
    __reference_models__ = {"about": ["Card"]}
    __template__ = "---\\nabout: ⸢rev•about⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    about: str = Field(description="A card; never null.")
'''

CONFIG = ProjectGraphConfig(
    document_extractor="docs_v1", file_extractor="files_v1", edge_extractor="edges_v1",
    surfaces=(DocumentSurface(kind="card", directory="cards", pattern="*.md", identity="document_id"), DocumentSurface(kind="note", directory="notes", pattern="*.md")),
    fields_by_model={"Card": ("about", "related")},
    kind_by_model={"Card": "card"},
    line_mentions=(LineMentions(kinds=("card", "note"), patterns=(MentionPattern(regex=r"card:[a-z0-9-]+", target="{0}"),), role="mentions", locator="prose"),),
)
D_TEXT = "# D\n\nSee card:card-a and card:card-ab, not card:card-a2.\n"


class World:
    """The store of the module docstring, with `project_graph` declared in its `store.yaml`."""

    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Card", "Review", "Strict"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        self.card("card-a", "Card A")
        self.card("card-a2", "Card A2")
        self.card("card-b", "Card B", about="card-a")
        self.card("card-c", "Card C", related=["card-x", "card-a", "card-z"], body="Also card:card-a.")
        api.create_document(self.store, "Review", self.root / "reviews" / "r1.md", {"title": "R1", "subject": "doc:Card:card-a"}, "r1", self.py)
        (self.root / "notes").mkdir()
        (self.root / "notes" / "d.md").write_text(D_TEXT, encoding="utf-8")
        save_declaration(self.store, declare_store(self.store, self.root).model_copy(update={"project_graph": CONFIG.to_mapping()}))

    def card(self, name: str, title: str, **fields) -> None:
        api.create_document(self.store, "Card", self.root / "cards" / f"{name}.md", {"id": name, "title": title, **fields}, name, self.py)

    def payload(self, export_id: str) -> dict:
        return api.edge_node(self.store, export_id).payload

    def text(self, relative: str) -> str:
        return (self.root / relative).read_text(encoding="utf-8")

    def digests(self) -> dict[str, str]:
        files = sorted(p for p in self.root.rglob("*") if p.is_file() and ".sldb" in p.parts or p.suffix == ".md")
        return {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

    def cli(self, capsys, *argv: str) -> tuple[int, object]:
        code = main(["--envelope", "edges", *argv, "--store", str(self.store), "--pythonpath", self.py, "--format", "json"])
        return code, json.loads(capsys.readouterr().out)


@pytest.fixture
def reference_world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


EXPECTED = [
    {"source": "Card:card-b", "field": "about", "index": None, "location": None, "origin": "schema"},
    {"source": "Card:card-c", "field": "related", "index": 1, "location": None, "origin": "schema"},
    {"source": "Review:r1", "field": "subject", "index": None, "location": None, "origin": "schema"},
    {"source": "cards/card-c.md", "field": None, "index": None, "location": "cards/card-c.md:16", "origin": "mention"},
    {"source": "notes/d.md", "field": None, "index": None, "location": "notes/d.md:3", "origin": "mention"},
]


def test_referrers_gives_the_fields_with_their_positions_and_the_mentions_with_their_lines(reference_world: World) -> None:
    found = [referrer.to_dict() for referrer in api.referrers(reference_world.store, "card-a")]
    assert found == EXPECTED
    assert [r.to_dict() for r in api.referrers(reference_world.store, "card-a2")] == [{**EXPECTED[4]}]  # D also says `card:card-a2`


@pytest.mark.parametrize("target", ["Card/card-a", "Card:card-a", "cards/card-a.md"])
def test_a_tracked_document_is_named_by_name_export_id_model_name_or_path(reference_world: World, target: str) -> None:
    assert [r.to_dict() for r in api.referrers(reference_world.store, target)] == EXPECTED


def test_a_project_node_id_resolves_after_the_documents_and_has_only_mentions(reference_world: World) -> None:
    assert [r.to_dict() for r in api.referrers(reference_world.store, "card:card-a")] == EXPECTED[3:]
    with pytest.raises(SLDBDocumentTargetError, match="Unknown document target: nope"):
        api.referrers(reference_world.store, "nope")


def test_an_ambiguous_target_names_its_candidates(reference_world: World) -> None:
    api.create_document(reference_world.store, "Review", reference_world.root / "reviews" / "card-a.md", {"title": "Same name"}, "card-a", reference_world.py)
    with pytest.raises(SLDBDocumentTargetError, match=r"Ambiguous document target: card-a \(candidates: Card:card-a, Review:card-a\)"):
        api.referrers(reference_world.store, "card-a")
    assert [r.source for r in api.referrers(reference_world.store, "Card:card-a")] == [r["source"] for r in EXPECTED]


def test_a_store_without_a_project_graph_has_only_the_fields(reference_world: World) -> None:
    declared = declare_store(reference_world.store, reference_world.root)  # keeps the authored project_graph (H5): the test removes it
    save_declaration(reference_world.store, declared.model_copy(update={"project_graph": None}))
    assert [r.to_dict() for r in api.referrers(reference_world.store, "card-a")] == EXPECTED[:3]


def test_an_anchor_pinned_on_save_is_still_a_field_reference(reference_world: World) -> None:
    api.save_document_payload(reference_world.store, "Review", "r1", {"title": "R1", "subject": "doc:Card:card-a"}, reference_world.py)
    subject = reference_world.payload("Review:r1")["subject"]
    assert subject.startswith("doc:Card:card-a@sha256:") and len(subject) == len("doc:Card:card-a@sha256:") + 64
    assert [r.field for r in api.referrers(reference_world.store, "card-a") if r.source == "Review:r1"] == ["subject"]


def count_walks(monkeypatch: pytest.MonkeyPatch, root: Path) -> dict[str, int]:
    """Count `os.walk`, `Path.rglob` and `os.scandir` outside the store (q17: the shards signature stat-scans `.sldb_cache/edges`)."""
    counts = {"walk": 0, "rglob": 0, "scandir": 0}
    walk, rglob, scandir = os.walk, Path.rglob, os.scandir

    def counted_walk(*args, **kwargs):
        counts["walk"] += 1
        return walk(*args, **kwargs)

    def counted_rglob(self, *args, **kwargs):
        counts["rglob"] += 1
        return rglob(self, *args, **kwargs)

    def counted_scandir(path=".", *args, **kwargs):
        counts["scandir"] += not any(part.startswith(".sldb") for part in Path(str(path)).parts)
        return scandir(path, *args, **kwargs)

    monkeypatch.setattr(os, "walk", counted_walk)
    monkeypatch.setattr(Path, "rglob", counted_rglob)
    monkeypatch.setattr(os, "scandir", counted_scandir)
    return counts


def test_with_the_index_and_the_graph_warm_referrers_walks_nothing(reference_world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    api.referrers(reference_world.store, "card-a")
    counts = count_walks(monkeypatch, reference_world.root)
    assert [r.to_dict() for r in api.referrers(reference_world.store, "card-a")] == EXPECTED
    assert counts == {"walk": 0, "rglob": 0, "scandir": 0}


def test_the_cli_prints_the_list_and_the_envelope_wraps_it(reference_world: World, capsys) -> None:
    assert main(["edges", "referrers", "card-a", "--store", str(reference_world.store), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out) == EXPECTED
    code, envelope = reference_world.cli(capsys, "referrers", "card:card-a")
    assert (code, envelope["ok"], envelope["data"]) == (0, True, EXPECTED[3:])
    code, envelope = reference_world.cli(capsys, "referrers", "nope")
    assert (code, envelope["error"]["type"]) == (1, "docs/missing")
    assert main(["edges", "referrers", "card-a", "--store", str(reference_world.store)]) == 0
    assert capsys.readouterr().out.splitlines() == ["schema: Card:card-b .about", "schema: Card:card-c .related[1]", "schema: Review:r1 .subject", "mention: cards/card-c.md:16", "mention: notes/d.md:3"]
