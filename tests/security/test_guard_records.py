"""SEGURIDAD resto 2, records: `ast show docs/<doc>` (one document) fails with the finding of a
tracked symlink out of the root, without opening it; `find` and the field records (every
document) never open it and go on with the others."""

from __future__ import annotations

import pytest

from tests.security.audited import escape, make_world


@pytest.fixture
def world(tmp_path):
    made = make_world(tmp_path)
    escape(made, "b")
    return made


def test_the_ast_of_the_symlink_fails_with_its_finding(world):
    ran = world.cli("ast", "show", "docs/b", "--store", ".sldb", "--pythonpath", world.py)
    assert not world.outside_opened(ran)
    assert ran["code"] == 1 and "store/path-outside-root" in ran["output"]


def test_find_rebuilding_the_records_does_not_open_it(world):
    ran = world.cli("find", "open", "--rebuild", "--store", ".sldb", "--pythonpath", world.py, "--format", "json")
    assert not world.outside_opened(ran)
    assert "SECRET-BODY" not in ran["output"] and "Traceback" not in ran["output"]


def test_the_field_records_skip_it(world):
    ran = world.api("from sldb.api.records import query_field_records\nresult = query_field_records(str(sp), py, 'status')")
    assert not world.outside_opened(ran) and not ran["error"]
    assert sorted(r["doc"] if "doc" in r else r.get("name") for r in ran["result"]) == ["a", "c"]
