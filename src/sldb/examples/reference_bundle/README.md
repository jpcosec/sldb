# SLDB Example Bundle

This bundle is the reference example for SLDB.

Contents:
- `guide_model.py`: a `StructuredNLDoc` model with a self-documenting template and required `Field(description=...)` metadata
- `guide.input.md`: a rendered Markdown document that the model can extract
- `guide.data.yaml`: model-shaped data that the model can render

What it demonstrates:
- frontmatter dictionary extraction
- heading and paragraph scalar markers
- static anchor sections
- blockquote and thematic break anchors
- bullet lists and ordered lists
- YAML fenced metadata
- table extraction/rendering
- field descriptions as part of the document contract

It is the bundle that `sldb example` unpacks into a local `sldb_example` directory.
