---
name: nldb
description: Use for StructuredNLDoc models that embed a Markdown contract in `__template__`. Extract, render, validate idempotency, and document structured Markdown workflows.
---

# nldb

Use `nldb` for StructuredNLDoc models and their Markdown documents.

When to use
- Any StructuredNLDoc-backed document that should roundtrip as structured data
- Any structured document change that needs model-level idempotency validation

What it does
- Extracts data from Markdown with a model
- Renders Markdown from data with a model
- Validates model roundtrip behavior

Commands
- `nldb extract <model-ref> <input-markdown> <output-json-or-yaml>`
- `nldb render <model-ref> <input-data> <output-markdown>`
- `nldb validate <model-ref> --input <markdown>`
- `nldb validate <model-ref> --data <json-or-yaml>`
- `nldb validate <model-ref> --input <markdown> --pythonpath <project-path>`
- `nldb init [path]`

Rule
- For every StructuredNLDoc workflow, run `nldb validate` before finishing.
