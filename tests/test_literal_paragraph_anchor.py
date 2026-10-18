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
