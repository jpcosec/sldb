---
example: true
audience: maintainers
validated: true
---

# SLDB Example Guide

> This is the canonical SLDB example. It demonstrates the supported reversible Markdown building blocks in one self-documenting guide.

SLDB lets one Markdown document act as both a human-friendly source of truth and a machine-readable contract.

---

## Why this repo exists

It exists to parse Markdown into a StructuredNLDoc model and render the same model back into stable Markdown without losing document intent.

## Why structured reversible documents help

- Human-readable source of truth.
- Machine-extractable typed data.
- One artifact for authoring and parsing.
- Easier validation, automation, and diffing.
- Safer roundtrips for evolving document workflows.

## How it works

A StructuredNLDoc model owns a Markdown contract in __template__. Stable prose stays literal, variable spans become markers, SLDB parses the Markdown structurally, fills model fields, and can render the model back to Markdown.

Field descriptions should explain each model field in plain language so both humans and LLMs can infer document intent from the schema.

Model reference shape: package.module:ModelName

Python path hint: Use --pythonpath when the model lives in another local project.

## How to build a good StructuredNLDoc model

1. Start from a real document shape, not an abstract schema.
2. Keep stable prose literal and mark only changing spans.
3. Use clear field names that reflect document meaning.
4. Let headings and sections anchor the structure.
5. Choose field types that match the Markdown block shape.
6. Add a meaningful Field(description="...") to every model field.
7. Validate roundtrips whenever the model or template changes.

## How to extend this library

- Add or refine a node handler in the extraction/rendering pipeline when a Markdown structure is not covered yet.
- Start from a real example document and write a failing roundtrip test for the new artifact.
- Teach the handler how to compile template recipes and extract values from parsed nodes.
- Update rendering so the same structure can be emitted back into stable Markdown.
- Add the new artifact to the bundled guide example so the feature stays documented and tested.

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
install: pip install sldb
supports:
  - headings
  - paragraphs
  - lists
  - tables
  - yaml
note: Use validate to confirm idempotent roundtrips.
```

## Command reference

| Command | Purpose | Example |
| --- | --- | --- |
| sldb extract | Parse Markdown into model-shaped data. | sldb extract myapp.docs:RecipeDoc recipe.md recipe.json |
| sldb render | Render Markdown from JSON or YAML input. | sldb render myapp.docs:RecipeDoc recipe.yaml recipe.md |
| sldb validate | Check document and model roundtrip idempotency. | sldb validate myapp.docs:RecipeDoc --input recipe.md |

## Literal CLI example

```bash
sldb validate myapp.docs:RecipeDoc --input recipe.md --pythonpath /path/to/project
```

```python
from pydantic import Field

class RecipeDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Recipe title shown in the H1 heading.")
```

## Closing note

Use this bundle as the baseline example, then adapt the model to the real document you want to make reversible.
