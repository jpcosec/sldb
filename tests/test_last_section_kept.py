"""A document that ends before the template does keeps its last section.

deskops' hand-written pill ended at `## Why` + a paragraph; the template goes on with `## When`
and its field. That later field matched the `Why` paragraph, so `why` came out empty and any
rewrite erased it (also the `purpose` of three of sldb's rituals).
"""

from __future__ import annotations

from pydantic import Field

from sldb import StructuredNLDoc
from sldb.runtime.validation import extract_model_data, render_model_markdown


class Pill(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n## What\n\n⸢rev•what⸥\n\n## Why\n\n⸢rev•why⸥\n\n## When\n\n⸢rev•when⸥\n"
    title: str = Field(description="Title.")
    what: str = Field(description="What.")
    why: str = Field(description="Why.")
    when: str = Field(description="When.")


def test_the_last_section_of_a_shorter_document_is_its_own():
    got = extract_model_data(Pill, "# P\n\n## What\n\nW.\n\n## Why\n\nY.\n")
    assert (got["what"], got["why"], got["when"]) == ("W.", "Y.", "")


def test_a_complete_document_is_unchanged():
    payload = {"title": "P", "what": "W.", "why": "Y.", "when": "N."}
    assert extract_model_data(Pill, render_model_markdown(Pill, payload)) == payload
