"""Adding an optional optrev field to a model must be inert for documents
that do not use it:

- the rendered Markdown leaves no trace (the whole line is omitted), so the
  file on disk does not mutate either (hash_c stays stable too).
- the roundtrip render -> extract is exact: a document that does not use the
  field renders back byte-for-byte identical to the original, so any digest
  derived from it is unchanged by the model extension.
- optrev markers that SHARE a line with other content keep the line and are
  replaced with the empty string, never deleting the surrounding structure.
"""
from pydantic import Field

from sldb import StructuredNLDoc
from sldb.runtime.validation import extract_model_data, render_model_markdown


class Note(StructuredNLDoc):
    __template__ = """---
title: ⸢rev•title⸥
---

# ⸢render•title⸥

⸢rev•body⸥""".strip()

    title: str = Field(description="Title.")
    body: str = Field(description="Body text.")


class NoteWithOptional(StructuredNLDoc):
    __template__ = """---
title: ⸢rev•title⸥
summary_en: ⸢optrev•summary_en⸥
---

# ⸢render•title⸥

⸢rev•body⸥""".strip()

    title: str = Field(description="Title.")
    body: str = Field(description="Body text.")
    summary_en: str | None = Field(default=None, description="Optional summary.")


class SharedLineDoc(StructuredNLDoc):
    __template__ = """---
title: ⸢rev•title⸥
---

⸢rev•title⸥ — ⸢optrev•suffix⸥
""".strip()

    title: str = Field(description="Title.")
    suffix: str | None = Field(default=None, description="Optional suffix.")


class MixedCellTableDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

| a | b |
| --- | --- |
| ⸢rev•a⸥ | ⸢optrev•b⸥ |
""".strip()

    title: str = Field(description="Title.")
    a: str = Field(description="Required cell.")
    b: str | None = Field(default=None, description="Optional cell.")


DOC_WITHOUT_FIELD = """---
title: Hello
---

# Hello

World body
"""

DOC_USING_FIELD = """---
title: Hello
summary_en: Bonjour
---

# Hello

World body
"""


# --- model extension is byte-neutral (option A, the render) --------------


def test_model_extension_is_neutral_for_document_that_does_not_use_field():
    """The invariant promised by the contract: extending a model with an
    optional field does NOT touch a document that does not use it. The render
    of that document under the extended model is byte-for-byte the original,
    so everything derived from the document (its extraction payload, its
    content hash, its future re-firm) is unchanged.

    Why both layers: the render omits the line (hash_c stable) AND the
    extractor drops absent-optional None keys (exclude_none), so the payload
    is identical to a model that never declared the field (hash_d stable for
    docs that never used it). Known, accepted one-time cost: documents whose
    stored payload already carried None from OTHER optional fields re-hash on
    re-firm (measured: 78/168 in the real knowledge_psp store) -- that is the
    price of real hash-neutrality, paid once."""
    extracted = extract_model_data(NoteWithOptional, DOC_WITHOUT_FIELD)
    base_render = render_model_markdown(Note, {"title": "Hello", "body": "World body"})
    assert render_model_markdown(NoteWithOptional, extracted) == base_render


def test_document_using_the_field_extracts_the_value():
    """A document that actually uses the field keeps a present value in the
    extract (never collapsed with the absent case)."""
    assert extract_model_data(NoteWithOptional, DOC_USING_FIELD) == {
        "title": "Hello",
        "body": "World body",
        "summary_en": "Bonjour",
    }


# --- option A: the render leaves no trace ---------------------------------


def test_rendered_markdown_omits_absent_optional_line():
    data = {"title": "Hello", "body": "World body", "summary_en": None}
    rendered = render_model_markdown(NoteWithOptional, data)
    assert "summary_en" not in rendered


def test_render_is_byte_identical_to_model_without_the_field():
    """Adding the field changes zero bytes of a document that does not use it
    (hash_c stays stable too, not just hash_d)."""
    with_optional = render_model_markdown(
        NoteWithOptional, {"title": "Hello", "body": "World body", "summary_en": None}
    )
    without_field = render_model_markdown(Note, {"title": "Hello", "body": "World body"})
    assert with_optional == without_field


def test_roundtrip_exact_with_optional_field_model():
    """The extractor drops absent optional fields (exclude_none), so the
    extract of a render whose optional field is None carries NO key for it.
    This is the hash-neutral invariant: an absent field is indistinguishable
    from a field that was never declared."""
    data = {"title": "Hello", "body": "World body", "summary_en": None}
    rendered = render_model_markdown(NoteWithOptional, data)
    assert extract_model_data(NoteWithOptional, rendered) == {
        "title": "Hello",
        "body": "World body",
    }


def test_extract_omits_absent_optional_field():
    """The explicit hash-neutral invariant: extracting a document that does
    not use an optional field yields a payload WITHOUT the absent key, so the
    payload (and its hash_d) is identical to a model that never declared it."""
    assert extract_model_data(NoteWithOptional, DOC_WITHOUT_FIELD) == {
        "title": "Hello",
        "body": "World body",
    }


def test_roundtrip_exact_with_optional_field_absent_from_disk():
    """Extraction of the omitted render equals extraction of the original
    document: the field is absent from both files."""
    extracted = extract_model_data(NoteWithOptional, DOC_WITHOUT_FIELD)
    rendered = render_model_markdown(NoteWithOptional, extracted)
    assert extract_model_data(NoteWithOptional, rendered) == extracted


# --- shared-line behavior (pinned decision) -------------------------------


def test_shared_line_optrev_replaced_with_empty_string_keeps_line():
    """A line whose optrev marker shares content (text / another marker) is
    kept; only the marker becomes ''. Dropping the whole line there would
    destroy the line structure (e.g. a table column or a text sentence)."""
    rendered = render_model_markdown(SharedLineDoc, {"title": "Hello", "suffix": None})
    assert "Hello —" in rendered  # line kept; trailing space trimmed by the pipeline
    assert "suffix" not in rendered


def test_table_row_with_optrev_cell_keeps_all_cells():
    """In a table row every cell must survive: the optrev cell renders as an
    empty cell, never as a deleted line (which would cost a column)."""
    rendered = render_model_markdown(
        MixedCellTableDoc, {"title": "Hello", "a": "A1", "b": None}
    )
    assert "| A1 |  |" in rendered
    assert "| ⸢" not in rendered

def test_render_absent_optrev_leaves_no_trace_in_frontmatter():
    """The reproduction case: a payload whose optional field is None must
    render a document that reads byte-for-byte as if the field were never
    declared — the optrev contract ('It MAY BE ABSENT in the document').
    Before the fix this rendered `summary_en: null` and the extract picked the
    key back up, so the ported model changed hash_d of every document that
    does not use the field."""
    rendered = render_model_markdown(
        NoteWithOptional, {"title": "Hello", "body": "World body", "summary_en": None}
    )
    assert "summary_en" not in rendered
    assert extract_model_data(NoteWithOptional, rendered) == extract_model_data(
        NoteWithOptional, DOC_WITHOUT_FIELD
    )


def test_render_absent_optrev_leaves_no_trace_on_plain_line():
    """Same invariant for a `key: ⸢optrev•key⸥` line outside a YAML block:
    the whole line is omitted instead of surviving as an empty `key:` line."""
    class PlainLineDoc(StructuredNLDoc):
        __template__ = """# ⸢rev•title⸥

summary_en: ⸢optrev•summary_en⸥

⸢rev•body⸥""".strip()

        title: str = Field(description="Title.")
        body: str = Field(description="Body text.")
        summary_en: str | None = Field(default=None, description="Optional summary.")

    rendered = render_model_markdown(
        PlainLineDoc, {"title": "Hello", "body": "World body", "summary_en": None}
    )
    assert "summary_en" not in rendered
    assert "Hello" in rendered and "World body" in rendered


def test_render_optrev_with_value_is_unchanged():
    """A present optional value must still render and extract symmetrically —
    the fix only changes the absent case."""
    rendered = render_model_markdown(
        NoteWithOptional, {"title": "Hello", "body": "World body", "summary_en": "Bonjour"}
    )
    assert "summary_en: Bonjour" in rendered
    assert extract_model_data(NoteWithOptional, rendered) == {
        "title": "Hello", "body": "World body", "summary_en": "Bonjour"
    }
