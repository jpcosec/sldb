"""A model's template is parsed once, validate renders once, and the AST keeps a fence's language.

The template was re-split on every extract and validate, validate rendered twice, and the
sections index built a markdown-it parser per document; the AST dropped `info`/`markup`/`attrs`.
"""

from __future__ import annotations

from pydantic import Field

from sldb import StructuredNLDoc
from sldb.core.ast import AST_Handler
from sldb.runtime import validation
from sldb.store import section_rebuild


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n- ⸢rev,list•items⸥\n"
    title: str = Field(description="Title.")
    items: list[str] = Field(default_factory=list, description="Items.")


def test_the_template_is_split_once_per_template():
    validation._recipes.cache_clear()
    for text in ("# a\n\n- x\n", "# b\n\n- y\n"):
        validation.extract_model_data(Note, text)
    assert validation._recipes.cache_info().misses == 1


def test_validate_renders_once(monkeypatch):
    calls = []
    real = validation.Validator.render
    monkeypatch.setattr(validation.Validator, "render", lambda self, data, ref_root=None: calls.append(1) or real(self, data, ref_root))
    assert validation.validate_model_data_roundtrip(Note, {"title": "t", "items": ["a"]})[0]
    assert len(calls) == 1


def test_the_sections_index_reuses_one_parser():
    section_rebuild._parse_md_nodes("# a\n")
    first = section_rebuild._parser()
    section_rebuild._parse_md_nodes("# b\n")
    assert section_rebuild._parser() is first


def test_a_fence_keeps_its_language_and_markup():
    fence = next(n for n in AST_Handler().split_nodes("```python\nx = 1\n```\n") if n.type == "fence")
    assert fence.metadata == {"info": "python", "markup": "```"}
