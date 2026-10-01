from __future__ import annotations

from sldb.api.records.extract import extract_sections
from sldb.api.records.map_fields import _field_template_line_map, _map_fields_to_sections


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


def test_single_section_template_keeps_ownership_when_a_field_value_has_headings():
    """Un field con markdown adentro aporta headings que no son secciones del template.

    Un template de una sola seccion tiene un unico dueno posible, asi que los headings
    extra no pueden desplazarlo. Antes se descartaba el mapeo entero y el documento
    perdia el owning_section de todos sus fields: 16 de los 1550 de este repo, 60 fields.
    """
    template = "# ⸢rev•title⸥\n\n⸢rev•body⸥"
    rendered = "# A title\n\n## Section inside the body\n\nText.\n\n## Another one\n\nMore.\n"
    owners = _map_fields_to_sections(template, extract_sections(rendered))
    assert set(owners) == {"title", "body"}
    assert set(owners.values()) == {"a-title"}


def test_multiple_section_template_still_refuses_when_counts_differ():
    """Con mas de una seccion un heading inyectado puede ocupar el lugar de uno del template.

    Ahi el mapeo seria incorrecto en silencio, que es justo el defecto que el guard evita:
    se prefiere no mapear antes que atribuir mal.
    """
    template = "# ⸢rev•title⸥\n\n## Goal\n\n⸢rev•goal⸥"
    rendered = "# A title\n\n## Goal\n\nText.\n\n## Injected by a value\n\nMore.\n"
    assert _map_fields_to_sections(template, extract_sections(rendered)) == {}
