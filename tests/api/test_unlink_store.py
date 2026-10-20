"""A link can be removed or pointed elsewhere, and a link to nothing is noted by the check.

deskops left the global store's `deskops` link on a deleted worktree: `link_store` refused the
name ("already linked"), nothing removed a link, and the only fix was editing
`store_index.yaml` by hand.
"""

from __future__ import annotations

import shutil

import pytest

from sldb.api import add_model, check_store, init_store, link_store, store_links, unlink_store
from sldb.cli import main
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index, save_store_index


@pytest.fixture
def linked(tmp_path):
    here, gone, owner = tmp_path / "here", tmp_path / "wt", tmp_path / "owner"
    for d in (here, gone, owner):
        d.mkdir()
        init_store(d)
    link_store(here / ".sldb", gone / ".sldb", "deskops")
    shutil.rmtree(gone)                                   # the worktree went away
    return here, owner


def test_the_check_notes_a_link_to_nothing(linked, capsys):
    here, _owner = linked
    assert [li["name"] for li in check_store(here / ".sldb", here)["broken_links"]] == ["deskops"]
    assert main(["stores", "check", "--store", str(here / ".sldb")]) == 1, "a link to no store is an error"
    assert "error: [store/link-broken] deskops: the linked store is missing" in capsys.readouterr().out


def test_replace_points_the_link_elsewhere(linked):
    here, owner = linked
    with pytest.raises(SLDBStoreError, match="already linked"):
        link_store(here / ".sldb", owner / ".sldb", "deskops")
    link_store(here / ".sldb", owner / ".sldb", "deskops", replace=True)
    assert [(li["name"], li["status"]) for li in store_links(here / ".sldb")] == [("deskops", "ok")]
    assert check_store(here / ".sldb", here)["broken_links"] == []


def test_remove_forgets_the_link(linked, capsys):
    here, _owner = linked
    assert main(["stores", "remove", "deskops", "--store", str(here / ".sldb")]) == 0
    assert store_links(here / ".sldb") == []
    with pytest.raises(SLDBStoreError, match="No store linked"):
        unlink_store(here / ".sldb", "deskops")


def test_a_link_models_inherit_from_is_replaced_not_removed(linked):
    here, owner = linked
    add_model(here / ".sldb", "sldb.models.relation_doc:RelationDoc")
    idx = load_store_index(here / ".sldb")
    idx.models = [m.model_copy(update={"origin": "deskops"}) for m in idx.models]   # as if inherited
    save_store_index(here / ".sldb", idx)
    with pytest.raises(SLDBStoreError, match="--replace"):
        unlink_store(here / ".sldb", "deskops")
    assert main(["stores", "add", str(owner / ".sldb"), "--name", "deskops", "--replace", "--store", str(here / ".sldb")]) == 0
    assert store_links(here / ".sldb")[0]["status"] == "ok"

