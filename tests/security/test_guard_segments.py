"""SEGURIDAD resto 2, segments: the segments of a tracked document whose path is a symlink out of
the root fail with its finding, never opening it; another document's segments do not touch it."""

from __future__ import annotations

import pytest

from tests.security.audited import escape, make_world

SEGMENTS = "from sldb.api.segments import build_document_segments\nresult = build_document_segments(sp, py, {name!r}).canonical"


@pytest.fixture
def world(tmp_path):
    made = make_world(tmp_path)
    escape(made, "b")
    return made


def test_the_segments_of_the_symlink_fail_with_its_finding(world):
    ran = world.api(SEGMENTS.format(name="b"))
    assert not world.outside_opened(ran)
    assert ran["error"].startswith("SLDBDocumentTargetError") and "store/path-outside-root" in ran["error"]


def test_the_segments_of_another_document_do_not_open_it(world):
    ran = world.api(SEGMENTS.format(name="a"))
    assert not world.outside_opened(ran) and not ran["error"]


def test_a_canonical_check_on_a_path_swapped_after_loading_is_refused(world):
    ran = world.api("from sldb.api.segments.build_document_segments import _read_stripped\nresult = _read_stripped(root, 'memos/b.md', '')")
    assert not world.outside_opened(ran) and "store/path-outside-root" in ran["error"]
