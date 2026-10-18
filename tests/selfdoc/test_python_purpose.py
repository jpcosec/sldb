"""A symbol's purpose comes from its docstring's first paragraph, and what someone wrote stays."""

from __future__ import annotations

from sldb.selfdoc.python_purpose import PLACEHOLDER, first_paragraph, merged_purpose, purpose_conflict

DOC = "---\nid: m.f\n---\nLoad the store\n  and check it.\n\nDetails that are not the purpose."


def test_the_first_body_paragraph_without_metadata_and_whitespace():
    assert first_paragraph(DOC) == "Load the store and check it."
    assert first_paragraph(None) is None and first_paragraph(PLACEHOLDER) is None


def test_a_placeholder_or_a_previously_generated_purpose_follows_the_docstring():
    assert merged_purpose(PLACEHOLDER, None, DOC) == "Load the store and check it."
    assert merged_purpose("Old first paragraph.", "Old first paragraph.\n\nMore.", DOC) == "Load the store and check it."


def test_an_authored_purpose_is_kept_and_reported():
    assert merged_purpose("Written by hand.", "Old.", DOC) == "Written by hand."
    assert purpose_conflict("Written by hand.", DOC)
    assert not purpose_conflict("Load the store and check it.", DOC) and not purpose_conflict(PLACEHOLDER, DOC)


def test_no_docstring_leaves_the_purpose_alone():
    assert merged_purpose(PLACEHOLDER, None, None) == PLACEHOLDER
    assert merged_purpose("Written.", None, None) == "Written."
