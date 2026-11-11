"""SEGURIDAD resto 2, model_registry: reindexing a model (`models update`) rehashes every tracked
document but never opens one whose path is a symlink out of the root: it warns with its finding
and goes on with the others."""

from __future__ import annotations

from tests.security.audited import escape, make_world


def test_models_update_does_not_open_the_symlink_and_names_it(tmp_path):
    world = make_world(tmp_path)
    escape(world, "b")
    ran = world.api("from sldb.api.model_registry.reindex_model import reindex_model\nreindex_model(sp, 'Memo', py)")
    assert not world.outside_opened(ran)
    assert "store/path-outside-root" in ran["output"] and "Traceback" not in ran["output"]
