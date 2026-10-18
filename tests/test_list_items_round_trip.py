"""A scalar list item reads back as written, whatever markdown its text looks like.

graph-ui found it through deskops: `validation=["```bash", "pytest", "```"]` rendered as three
items and came back as `["pytest"]`, so any rewrite of the document, even one that edited
another field, deleted the fence lines. A heading, a quote, a nested list marker or a leading
space lost its syntax the same way.
"""

from __future__ import annotations

import pytest
from pydantic import Field

from sldb import StructuredNLDoc
from sldb.runtime.validation import extract_model_data, render_model_markdown


class Steps(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n## Validation\n\n- ⸢rev,list•validation⸥\n"
    title: str = Field(description="Title.")
    validation: list[str] = Field(default_factory=list, description="Commands, one per item.")


class Labelled(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n## Validation\n\n- run: ⸢rev,list•validation⸥\n"
    title: str = Field(description="Title.")
    validation: list[str] = Field(default_factory=list, description="Commands after a label.")


CASES = [
    ["```bash", "pytest", "```"], ["~~~", "x"], ["# not a heading"], ["> not a quote"],
    ["- not nested", "1. not ordered", "+ plus"], ["***", "---", "_ _ _"], ["<b>html</b>"],
    ["    indented", " lead"], ["", "after an empty one"],
    ["\\# escaped by hand", "\\\\# twice", "\\path", "a\\b"], ["plain", "**bold** `code` [l](u)"],
]


@pytest.mark.parametrize("items", CASES)
def test_an_item_reads_back_as_written(items):
    md = render_model_markdown(Steps, {"title": "t", "validation": items})
    assert extract_model_data(Steps, md)["validation"] == items, md


def test_an_empty_list_is_still_empty():
    assert extract_model_data(Steps, render_model_markdown(Steps, {"title": "t", "validation": []}))["validation"] == []


def test_a_value_after_a_label_is_not_escaped():
    """`- run: ```bash` is no fence: only a value that opens its item is escaped."""
    md = render_model_markdown(Labelled, {"title": "t", "validation": ["```bash"]})
    assert "- run: ```bash" in md
