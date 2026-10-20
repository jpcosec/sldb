"""`stores check` names the documents a rewrite would lose content from (inbox 20260924-011411).

A model that cannot read its own document extracts empty fields over a consistent hash, so the
store passed and any rewrite wrote the empties. A block the model does not read is reported;
a section the template regenerates (`render` markers, like deskops' Board task summaries) is
not, since a stale copy there is not data.
"""

from __future__ import annotations

import sys

import pytest
from pydantic import Field

from sldb import StructuredNLDoc, api
from sldb.api.documents.rewrite_loss import rewrite_loss
from sldb.cli import main


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n## What\n\n⸢rev•what⸥\n\n## Derived\n\n⸢render•summary⸥\n"
    title: str = Field(description="Title.")
    what: str = Field(description="What.")

    @property
    def summary(self) -> str:
        return "- regenerated"


def test_a_block_the_model_does_not_read_is_what_a_rewrite_loses():
    assert rewrite_loss(Note, "# T\n\nAn intro nobody declares.\n\n## What\n\nW.\n") == ["An intro nobody declares."]


def test_a_readable_document_and_a_stale_derived_section_lose_nothing():
    assert rewrite_loss(Note, "# T\n\n## What\n\nW.\n\n## Derived\n\n- an old summary\n") == []


MODULE = "sldb_rewrite_loss_models"


@pytest.fixture
def store(tmp_path):
    (tmp_path / f"{MODULE}.py").write_text('''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n## What\\n\\n⸢rev•what⸥\\n"
    title: str = Field(description="Title.")
    what: str = Field(description="What.")
''', encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    root = tmp_path / "world"
    root.mkdir()
    sp = api.init_store(root).store_path
    api.add_model(sp, f"{MODULE}:Note", str(tmp_path))
    api.create_document(sp, "Note", root / "n.md", {"title": "n", "what": "W."}, "n", str(tmp_path))
    yield sp, root, str(tmp_path)
    sys.path.remove(str(tmp_path))
    sys.modules.pop(MODULE, None)


def test_stores_check_names_the_document_and_the_block(store, capsys):
    sp, root, py = store
    (root / "n.md").write_text("# n\n\nAdded by hand.\n\n## What\n\nW.\n", encoding="utf-8")
    assert api.check_store(sp, root, py)["rewrite_loss"] == [{"document": "n", "model": "Note", "path": "n.md", "lost": ["Added by hand."]}]
    main(["stores", "check", "--store", str(sp), "--pythonpath", py])
    assert "would be lost on a rewrite" in capsys.readouterr().out
