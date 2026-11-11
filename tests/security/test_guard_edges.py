"""SEGURIDAD resto 2, edges: `edges rebuild`, `rewrite_references` and the project graph never open a
document whose path is a symlink out of the root; the project graph and the rewrite warn with its
finding and go on with the other documents (the world of `tests/api/test_referrers.py`)."""

from __future__ import annotations

from pathlib import Path

import pytest

from sldb import api
from tests.api.test_referrers import World as ReferenceWorld, reference_world  # noqa: F401 - fixture
from tests.security.audited import World

SECRET_NOTE = "# Secret\n\nSECRET-BODY card:card-a.\n"
SECRET_CARD = "---\nid: card-b\nabout: card-a\nrelated: []\n---\n\n# SECRET-BODY\n\n"


def _escape(world: ReferenceWorld, relative: str, text: str) -> World:
    secret = world.root.parent / "outside" / Path(relative).name
    secret.parent.mkdir(exist_ok=True)
    secret.write_text(text, encoding="utf-8")
    (world.root / relative).unlink()
    (world.root / relative).symlink_to(secret)
    return World(world.root, secret)


def test_edges_rebuild_does_not_open_a_tracked_symlink(reference_world: ReferenceWorld) -> None:
    audited = _escape(reference_world, "cards/card-b.md", SECRET_CARD)
    ran = audited.cli("edges", "rebuild", "--store", ".sldb", "--pythonpath", audited.py)
    assert not audited.outside_opened(ran)
    assert "Traceback" not in ran["output"] and "SECRET-BODY" not in ran["output"]


def test_the_project_graph_does_not_open_a_symlinked_note_and_names_it(reference_world: ReferenceWorld) -> None:
    audited = _escape(reference_world, "notes/d.md", SECRET_NOTE)
    ran = audited.api("from sldb import api\nresult = [r.to_dict() for r in api.referrers(sp, 'card-a')]")
    assert not audited.outside_opened(ran) and not ran["error"]
    assert "store/path-outside-root" in ran["output"]
    assert "notes/d.md" not in [r["source"] for r in ran["result"]]


def test_rewrite_references_does_not_open_nor_write_a_symlinked_mention(reference_world: ReferenceWorld) -> None:
    api.referrers(reference_world.store, "card-a")  # the graph warm, with notes/d.md a mention
    audited = _escape(reference_world, "notes/d.md", SECRET_NOTE)
    ran = audited.api("from sldb import api\nresult = api.rewrite_references(sp, 'card-a', 'card-a2', pythonpath=py).to_dict()")
    assert not audited.outside_opened(ran) and not ran["error"]
    assert audited.secret.read_text(encoding="utf-8") == SECRET_NOTE
    assert "notes/d.md" not in [c["source"] for c in ran["result"]["changed"]]
    assert reference_world.payload("Card:card-b")["about"] == "card-a2"  # the others are rewritten
