"""SEGURIDAD resto 2, links: `docs compose --render-links` (the coordinator's reproduction) and the
transclusion of `docs compose` never open a link target whose tracked path is a symlink out of
the root; the link stays as written and no path outside is emitted. Composing that document
itself fails with its finding (exit 1)."""

from __future__ import annotations

import pytest

from tests.security.audited import escape, make_world


@pytest.fixture
def world(tmp_path):
    made = make_world(tmp_path)
    escape(made, "b")
    return made


def test_render_links_does_not_open_the_target_and_leaves_the_link_as_written(world):
    ran = world.cli("docs", "compose", "a", "--render-links", "--store", ".sldb")
    assert not world.outside_opened(ran)
    assert "[[b]]" in ran["output"] and "outside" not in ran["output"] and "SECRET-BODY" not in ran["output"]
    assert "[c](c.md)" in ran["output"]  # a readable target is still rendered
    assert "Traceback" not in ran["output"]


def test_a_transclusion_of_the_symlink_is_not_opened(world):
    ran = world.cli("docs", "compose", "a", "--store", ".sldb")
    assert not world.outside_opened(ran)
    assert "![[b]]" in ran["output"] and "SECRET-BODY" not in ran["output"]


def test_composing_the_symlink_itself_fails_with_its_finding(world):
    ran = world.cli("docs", "compose", "b", "--store", ".sldb")
    assert not world.outside_opened(ran)
    assert ran["code"] == 1 and "store/path-outside-root" in ran["output"]


def test_links_recovery_does_not_open_the_target(world):
    ran = world.cli("docs", "links", "a", "--store", ".sldb", "--format", "json")
    assert not world.outside_opened(ran)
    assert "outside" not in ran["output"]
