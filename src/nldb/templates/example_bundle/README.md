# nlDB Example Bundle

This bundle is the reference example for nlDB.

Contents:
- `guide_model.py`: a `StructuredNLDoc` model with a self-documenting template
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

It is designed to be the bundle that a future `nldb example` command can unpack.
