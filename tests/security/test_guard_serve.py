"""SEGURIDAD resto 2, `serve`: `/document/ir` (and `/sections`) of a tracked document whose path is
a symlink out of the root answer with its finding, never opening it."""

from __future__ import annotations

import pytest

from tests.security.audited import escape, make_world

IR = "from sldb.cli.serve.document_routes import _respond_ir\nresult = _respond_ir('/document/ir', {name!r}, sp, py)"


@pytest.fixture
def world(tmp_path):
    made = make_world(tmp_path)
    escape(made, "b")
    return made


def test_the_ir_of_the_symlink_is_refused_with_its_finding(world):
    ran = world.api(IR.format(name="b"))
    assert not world.outside_opened(ran) and not ran["error"]
    body, status = ran["result"]
    assert status == 422 and "store/path-outside-root" in body["error"]


def test_the_ir_of_another_document_does_not_open_it(world):
    ran = world.api(IR.format(name="a"))
    assert not world.outside_opened(ran) and ran["result"][1] == 200


def test_the_sections_ir_of_the_symlink_is_not_read(world):
    ran = world.api("from sldb.cli.serve.sections_routes import _ir_json\nfrom types import SimpleNamespace\n"
                    "result = _ir_json(SimpleNamespace(path='memos/b.md', store_name='local', model_name='Memo', name='b', payload={}, semantic_tags=[], model_type=object), root)")
    assert not world.outside_opened(ran)
    assert "store/path-outside-root" in ran["result"][1]["error"]
