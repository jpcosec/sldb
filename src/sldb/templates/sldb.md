---
name: sldb
description: Use for StructuredNLDoc models that embed a Markdown contract in `__template__`. Extract, render, validate idempotency, and document structured Markdown workflows.
---

# SLDB

Use `sldb` for StructuredNLDoc models and their Markdown documents.

When to use
- Any StructuredNLDoc-backed document that should roundtrip as structured data
- Any structured document change that needs model-level idempotency validation

What it does
- Extracts data from Markdown with a model
- Renders Markdown from data with a model
- Validates model roundtrip behavior

Commands
- `sldb extract <model-ref> <input-markdown> <output-json-or-yaml>`
- `sldb render <model-ref> <input-data> <output-markdown>`
- `sldb validate <model-ref> --input <markdown>`
- `sldb validate <model-ref> --data <json-or-yaml>`
- `sldb validate <model-ref> --input <markdown> --pythonpath <project-path>`
- `sldb init [path]`

Python marker modes
- Safe mode is the default; `py` markers stay literal and are not evaluated
- Unsafe mode enables `py` marker evaluation for trusted templates only

Rule
- For every StructuredNLDoc workflow, run `sldb validate` before finishing.
