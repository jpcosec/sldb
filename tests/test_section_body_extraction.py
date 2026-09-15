from __future__ import annotations

from pydantic import Field
from sldb import StructuredNLDoc
from sldb.runtime.validation import extract_model_data


class SectionedDoc(StructuredNLDoc):
    """Three consecutive prose sections, each captured via section_body.

    This is the shape every deskops TaskDoc-style document has: a heading
    anchor, an italic instruction anchor, then a free-prose paragraph.
    """

    __template__ = """# ⸢rev•title⸥

## Alpha

_Describe alpha._

⸢rev•alpha⸥

## Beta

_Describe beta._

⸢rev•beta⸥

## Gamma

_Describe gamma._

⸢rev•gamma⸥"""

    title: str = Field(description="Doc title.")
    alpha: str = Field(default="", description="Alpha section body.")
    beta: str = Field(default="", description="Beta section body.")
    gamma: str = Field(default="", description="Gamma section body.")


def _doc(alpha: str, beta: str, gamma: str) -> str:
    def section(name: str, body: str) -> str:
        filled = f"\n{body}\n" if body else ""
        return f"## {name}\n\n_Describe {name.lower()}._\n{filled}"

    return f"# Doc\n\n{section('Alpha', alpha)}\n{section('Beta', beta)}\n{section('Gamma', gamma)}"


def test_all_sections_filled_extract_in_order():
    data = extract_model_data(SectionedDoc, _doc("A-BODY", "B-BODY", "G-BODY"))

    assert (data["alpha"], data["beta"], data["gamma"]) == ("A-BODY", "B-BODY", "G-BODY")


def test_empty_section_does_not_shift_later_sections():
    """Regression: an empty section used to consume its own boundary block.

    _handle_section_body set curr_block = max(search, boundary_idx - 1). With
    an empty body, boundary_idx == search, so it claimed the boundary block --
    the next section's heading -- as consumed. The next anchor then started
    searching past its own heading, matched the heading after it, and every
    later section shifted up by one, silently destroying the last one.
    """
    data = extract_model_data(SectionedDoc, _doc("", "B-BODY", "G-BODY"))

    assert data["alpha"] == ""
    assert data["beta"] == "B-BODY", "beta must not absorb the section after it"
    assert data["gamma"] == "G-BODY", "gamma must not be lost"


def test_multiple_empty_sections_do_not_shift():
    data = extract_model_data(SectionedDoc, _doc("", "", "G-BODY"))

    assert (data["alpha"], data["beta"], data["gamma"]) == ("", "", "G-BODY")


def test_trailing_empty_section_stays_empty():
    data = extract_model_data(SectionedDoc, _doc("A-BODY", "B-BODY", ""))

    assert (data["alpha"], data["beta"], data["gamma"]) == ("A-BODY", "B-BODY", "")


def test_repeated_extraction_is_stable_with_an_empty_section():
    """`deskops edit` re-reads, mutates, and writes back. With the old bug,
    each successive round trip corrupted one more neighbouring field, so
    stability across repeats is the property that actually matters."""
    markdown = _doc("", "B-BODY", "G-BODY")

    first = extract_model_data(SectionedDoc, markdown)
    second = extract_model_data(SectionedDoc, markdown)

    assert first == second
    assert first["beta"] == "B-BODY"
