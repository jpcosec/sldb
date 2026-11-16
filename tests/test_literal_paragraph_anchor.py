"""A template's literal paragraph anchors only a paragraph with that text.

deskops' InboxNoteDoc and TaskDoc templates carry a placeholder paragraph
(`_Describe the incoming message..._`). A document written without it had its first real
paragraph taken as the placeholder and dropped, so every rewrite of the document deleted it
(the first paragraph of several sldb inbox notes; `why`, `goal` and `done_when` of a task).
"""

from __future__ import annotations

import pytest
from pydantic import Field

from sldb import StructuredNLDoc
from sldb.runtime.validation import extract_model_data, render_model_markdown


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n_Describe the message._\n\n⸢rev,markdown•body⸥\n"
    title: str = Field(description="Title.")
    body: str = Field(description="Body.")


@pytest.mark.parametrize("md", [
    "# T\n\nFirst paragraph.\n\n## Scope\n\nmore\n",                       # without the placeholder
    "# T\n\n_Describe the message._\n\nFirst paragraph.\n\n## Scope\n\nmore\n",  # with it
])
def test_the_first_paragraph_is_the_bodys_with_or_without_the_placeholder(md):
    assert extract_model_data(Note, md)["body"] == "First paragraph.\n\n## Scope\n\nmore"


def test_a_rewrite_keeps_it():
    payload = extract_model_data(Note, "# T\n\nFirst paragraph.\n")
    again = extract_model_data(Note, render_model_markdown(Note, payload))
    assert again["body"] == "First paragraph."


class Anchored(StructuredNLDoc):
    __template__ = (
        "# ⸢rev•title⸥\n\n"
        "## Goal\n\n_Describe the goal._\n\n⸢rev,markdown•goal⸥\n\n"
        "## Implementation Path\n\n_Outline the expected implementation route or affected surface._\n\n"
        "⸢rev,markdown•implementation_path⸥\n\n"
        "## Notes\n\n⸢rev,markdown•notes⸥\n"
    )
    title: str = Field(description="Title.")
    goal: str = Field(description="Goal.")
    implementation_path: str = Field(description="Path.")
    notes: str = Field(description="Notes.")


def test_template_anchors_gives_each_anchored_field_its_literal_paragraph():
    from sldb.api import template_anchors

    assert template_anchors(Anchored) == {
        "goal": "_Describe the goal._",
        "implementation_path": "_Outline the expected implementation route or affected surface._",
    }
    assert template_anchors(Note) == {"body": "_Describe the message._"}


def test_the_anchor_is_what_render_writes_and_extract_consumes():
    from sldb.api import template_anchors

    data = {"title": "T", "goal": "G", "implementation_path": "P", "notes": "N"}
    rendered = render_model_markdown(Anchored, data)
    for text in template_anchors(Anchored).values():
        assert f"\n{text}\n" in rendered
    assert extract_model_data(Anchored, rendered) == data


@pytest.mark.parametrize("bad", [Anchored(title="T", goal="G", implementation_path="P", notes="N"), dict, "Anchored"])
def test_template_anchors_rejects_anything_but_a_model_class(bad):
    from sldb.api import template_anchors

    with pytest.raises(TypeError):
        template_anchors(bad)
