from __future__ import annotations

from pathlib import Path

from sldb.links import compose_document, recover_links
from sldb.links.sections import extract_section, strip_frontmatter

ATOM = """---
id: atom-x
kind: atom
---
# Atom X

## Answer

Body with [[other.md]].

### Detail

deep text

## Other

other text
"""


def _tree(tmp_path: Path) -> Path:
    (tmp_path / "other.md").write_text("# Other\n", "utf-8")
    (tmp_path / "atom-x.md").write_text(ATOM, "utf-8")
    view = tmp_path / "view.md"
    view.write_text("---\ntitle: vista\n---\n# Vista\n\n![[atom-x.md]]\n\n![[atom-x.md#answer]]\n", "utf-8")
    return view


def test_transclusion_drops_frontmatter_but_root_keeps_its_own(tmp_path):
    out = compose_document(_tree(tmp_path), None)["markdown"]
    assert out.startswith("---\ntitle: vista\n---")
    assert "id: atom-x" not in out and "kind: atom" not in out
    assert "# Atom X" in out


def test_section_transclusion_takes_heading_down_to_next_peer(tmp_path):
    res = compose_document(_tree(tmp_path), None)
    tail = res["markdown"].split("# Atom X")[-1].split("## Other")[-1]
    assert "## Answer" in tail and "### Detail" in tail and "deep text" in tail
    assert tail.count("other text") == 1  # the 2nd inclusion stops before "## Other"
    assert res["unresolved"] == []


def test_same_document_can_be_included_twice(tmp_path):
    res = compose_document(_tree(tmp_path), None)
    assert res["markdown"].count("Body with") == 2


def test_missing_section_is_unresolved_and_left_raw(tmp_path):
    view = tmp_path / "v2.md"
    _tree(tmp_path)
    view.write_text("![[atom-x.md#Nope]]\n", "utf-8")
    res = compose_document(view, None)
    assert res["unresolved"] == ["atom-x.md#Nope"]
    assert "![[atom-x.md#Nope]]" in res["markdown"]


def test_recover_checks_the_section(tmp_path):
    view = _tree(tmp_path)
    ok = recover_links(view, None)
    assert ok["unresolved"] == []
    view.write_text("![[atom-x.md#Nope]]\n![[atom-x.md#Answer]]\n", "utf-8")
    assert recover_links(view, None)["unresolved"] == ["atom-x.md#Nope"]


def test_helpers():
    assert strip_frontmatter("---\na: 1\n---\n\n# T\n") == "# T\n"
    assert strip_frontmatter("# T\n---\nx\n---\n") == "# T\n---\nx\n---\n"
    assert extract_section("```\n## Answer\n```\n", "Answer") is None


def test_tracked_document_whose_file_is_gone_does_not_resolve(tmp_path, monkeypatch):
    from sldb.links import resolver

    ghost = tmp_path / "ghost.md"  # tracked in the store, absent on disk
    monkeypatch.setattr(resolver, "_tracked_documents", lambda _store: {"ghost": str(ghost)})
    view = tmp_path / "v.md"
    view.write_text("[[ghost]] ![[ghost]]\n", "utf-8")
    res = recover_links(view, tmp_path, predicate_types={})
    assert [l["resolved"] for l in res["links"]] == [False, False]
    assert compose_document(view, tmp_path)["unresolved"] == ["ghost"]
