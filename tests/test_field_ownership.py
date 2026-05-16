from __future__ import annotations

from sldb.cli.graph import _field_template_line_map


def test_normal_marker():
    result = _field_template_line_map("# ⸢rev•title⸥")
    assert result == {"title": 1}


def test_list_marker():
    result = _field_template_line_map("- ⸢rev,list•tasks⸥")
    assert result == {"tasks": 1}


def test_unknown_extra_modifier():
    result = _field_template_line_map("⸢rev,list,opt•status⸥")
    assert result == {"status": 1}


def test_malformed_no_name():
    result = _field_template_line_map("⸢rev•⸥")
    assert result == {}


def test_multiple_markers_one_line():
    result = _field_template_line_map("⸢rev•a⸥ ⸢rev•b⸥ ⸢rev•c⸥")
    assert result == {"a": 1, "b": 1, "c": 1}


def test_multiple_lines():
    template = "# ⸢rev•title⸥\n\nStatus: ⸢rev•status⸥\n\n## Tasks\n\n- ⸢rev,list•tasks⸥"
    result = _field_template_line_map(template)
    assert result == {"title": 1, "status": 3, "tasks": 7}


def test_optrev_marker_also_captured():
    result = _field_template_line_map("⸢optrev•title⸥")
    assert result == {"title": 1}


def test_render_marker_ignored():
    result = _field_template_line_map("⸢render•title⸥")
    assert result == {}


def test_unknown_field_logs_warning(caplog):
    import logging

    caplog.set_level(logging.WARNING)
    result = _field_template_line_map("⸢rev•bogus⸥", known_fields={"title", "status"})
    assert result == {"bogus": 1}
    assert "bogus" in caplog.text
