from __future__ import annotations

from sldb.cli.graph_ops.extract import extract_sections
from sldb.cli.graph_ops.map_fields import _field_template_line_map, _map_fields_to_sections


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


def test_ownership_follows_template_heading_order_not_rendered_lines():
    template = "# ⸢rev•title⸥\n\n⸢rev,list•items⸥\n\n## Details\n\n⸢rev•detail⸥"
    rendered = "# A title\n\n- one\n- two\n- three\n\n## Details\n\nA value\n"
    assert _map_fields_to_sections(template, extract_sections(rendered)) == {
        "title": "a-title", "items": "a-title", "detail": "a-title/details",
    }


def test_section_span_covers_body_until_next_peer_or_parent():
    markdown = "# Parent\nbody\n## Child\nchild\n# Next\nnext\n"
    sections = extract_sections(markdown)
    assert [(section.path, section.line_start, section.line_end) for section in sections] == [
        ("parent", 1, 4), ("parent/child", 3, 4), ("next", 5, 6),
    ]


def test_repeated_sibling_titles_receive_distinct_deterministic_paths():
    sections = extract_sections("# Same\nfirst\n# Same\nsecond\n")
    assert [section.path for section in sections] == ["same", "same-2"]
