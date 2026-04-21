from nldb import StructuredNLDoc


class NLDBGuide(StructuredNLDoc):
    __template__ = """
---
⸢rev,dict•frontmatter⸥
---

# ⸢rev•title⸥

> This is the canonical nlDB example. It demonstrates the supported reversible Markdown building blocks in one self-documenting guide.

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

Use scalar markers for single values, list markers for repeated list items, and dict markers for YAML-shaped blocks. The common forms are `rev•field`, `rev,list•items`, and `rev,dict•meta` wrapped in the nlDB marker brackets.

### Marker semantics

- `rev•field`: required reversible scalar. It is expected to extract from Markdown and render back symmetrically.
- `optrev•field`: optional reversible scalar. It may be absent in the document; if present, it should still extract and render symmetrically.
- `render•field`: non-reversible render-only marker. It renders from model data but is intentionally not extracted back.
- `py•expression`: non-reversible Python render marker. It evaluates a Python expression against the render context and writes the result into the document.
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
nldb validate myapp.docs:RecipeDoc --input recipe.md --pythonpath /path/to/project
```

## Closing note

⸢rev•closing_note⸥
""".strip()

    frontmatter: dict
    title: str
    intro: str
    why_it_exists: str
    benefits: list
    how_it_works: str
    model_ref_shape: str
    pythonpath_hint: str
    model_rules: list
    extension_steps: list
    metadata: dict
    commands: dict
    closing_note: str
