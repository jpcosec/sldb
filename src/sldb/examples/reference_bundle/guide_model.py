from pydantic import Field

from sldb import StructuredNLDoc


class SLDBGuide(StructuredNLDoc):
    __template__ = """
---
⸢rev,dict•frontmatter⸥
---

# ⸢rev•title⸥

> This is the canonical SLDB example. It demonstrates the supported reversible Markdown building blocks in one self-documenting guide.

⸢rev•intro⸥

---

## Why this repo exists

⸢rev•why_it_exists⸥

## Why structured reversible documents help

- ⸢rev,list•benefits⸥

## How it works

⸢rev•how_it_works⸥

Model reference shape: ⸢rev•model_ref_shape⸥

Python path hint: ⸢rev•pythonpath_hint⸥

## How to build a good StructuredNLDoc model

1. ⸢rev,list•model_rules⸥

## How to extend this library

- ⸢rev,list•extension_steps⸥

## Marker guide

Use scalar markers for single values, list markers for repeated list items, and dict markers for YAML-shaped blocks. The common forms are `rev•field`, `rev,list•items`, and `rev,dict•meta` wrapped in the SLDB marker brackets.

### Marker semantics

- `rev•field`: required reversible scalar. It is expected to extract from Markdown and render back symmetrically.
- `optrev•field`: optional reversible scalar. It may be absent in the document; if present, it should still extract and render symmetrically.
- `render•field`: non-reversible render-only marker. It renders from model data but is intentionally not extracted back.
- `py•expression`: non-reversible Python render marker. In safe mode it stays literal; in unsafe mode it evaluates against the render context.
- `rev,list•items`: reversible list item marker. Use it inside a Markdown list item template so repeated list entries map to one list field.
- `rev,dict•meta`: reversible dictionary marker. Use it for YAML/frontmatter or similar mapping-shaped blocks.
- `optrev,dict•meta`: optional reversible mapping marker. Use it when the YAML-shaped block may be empty or omitted.
- Table markers are still supported through reversible cell markers placed in the template row, for example `| ⸢rev•command⸥ | ⸢rev•purpose⸥ |`.
- `{{ title }}`: Jinja2 render-only expression. Use it for generated presentation text that should not participate in extraction.

## YAML metadata block

```yaml
⸢rev,dict•metadata⸥
```

## Command reference

| Command | Purpose | Example |
| --- | --- | --- |
| ⸢rev•commands⸥ | ⸢rev•purpose⸥ | ⸢rev•example⸥ |

## Literal CLI example

```bash
sldb validate myapp.docs:RecipeDoc --input recipe.md --pythonpath /path/to/project
```

## Closing note

⸢rev•closing_note⸥
""".strip()

    frontmatter: dict = Field(description="Top-level YAML frontmatter for the guide.")
    title: str = Field(description="Primary document title shown as the H1 heading.")
    intro: str = Field(description="Opening introduction after the quote block.")
    why_it_exists: str = Field(description="Explanation of the repo's purpose.")
    benefits: list = Field(
        description="Bullet list of benefits for structured documents."
    )
    how_it_works: str = Field(
        description="Overview of the SLDB extraction and rendering flow."
    )
    model_ref_shape: str = Field(
        description="Example shape for a StructuredNLDoc model reference."
    )
    pythonpath_hint: str = Field(
        description="Guidance on when to use the --pythonpath option."
    )
    model_rules: list = Field(description="Numbered rules for designing a good model.")
    extension_steps: list = Field(description="Action list for extending the library.")
    metadata: dict = Field(
        description="Example YAML metadata block embedded in the guide."
    )
    commands: dict = Field(description="Command reference rows keyed by command entry.")
    closing_note: str = Field(description="Final closing note at the end of the guide.")
