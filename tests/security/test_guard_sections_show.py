"""SEGURIDAD resto 2, `sections show` (and `sections fields`): the one document the command names,
when its tracked path is a symlink out of the root, fails with its finding (exit 1) and is never
opened; another document is shown without touching it."""

from __future__ import annotations

import pytest

from tests.security.audited import escape, make_world


@pytest.fixture
def world(tmp_path):
    made = make_world(tmp_path)
    escape(made, "b")
    return made


@pytest.mark.parametrize("command", [["sections", "show", "b"], ["sections", "fields", "docs/b/status"]])
def test_the_symlink_named_by_the_command_fails_with_its_finding(world, command):
    ran = world.cli(*command, "--store", ".sldb", "--pythonpath", world.py)
    assert not world.outside_opened(ran)
    assert ran["code"] == 1 and "store/path-outside-root" in ran["output"]
    assert "Traceback" not in ran["output"]


def test_another_document_is_shown_without_opening_it(world):
    ran = world.cli("sections", "show", "a", "--store", ".sldb", "--pythonpath", world.py)
    assert not world.outside_opened(ran) and ran["code"] == 0
