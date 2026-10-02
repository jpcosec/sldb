# SLDB Composition Modes

Verified against the working tree on 2026-10-01. Two composition mechanisms are implemented: model-driven summaries during rendering, and explicit document transclusions through the CLI.

## Render-Time Summaries

A `StructuredNLDoc` declares `__compositions__` and places a `render` marker in its Markdown template:

```python
__compositions__ = {
    "task_summaries": {
        "source_field": "tasks",
        "model": "myapp.models:TaskDoc",
        "template": "- {title} [{status}]",
        "separator": "\n",
    }
}
# In __template__: ⸢render•task_summaries⸥
```

The `tasks` field supplies a list of file paths. The model is an import reference or a model class. Each child is extracted with that model; `template` formats its payload with Python string formatting, and `separator` joins the results. The defaults are `"- {title}"` and a newline.

The option is `template`, not `line_template`. Missing paths and invalid child payloads can be skipped silently.

### Where a relative child path resolves

A child ref is a path in the project (`docs/tasks/task-a.md`), not a path relative to the directory the process happens to run in. Every store-aware path passes the project root: `create_document`, `save_document_payload`, `docs update`, model backfill, `sldb render` on a tracked document, and the segment views (`/document/segments`, `/extract/segments`). The renderer takes it as `ref_root`.

Two cases have no store to take a root from, so they still resolve against the working directory: `render_model_markdown` called directly as a library function with no `ref_root`, and the store-less `sldb render MODEL INPUT OUTPUT` — which accepts `--ref-root DIR` to say so explicitly.

This mechanism does not invoke the linked-store resolver: a ref is resolved as a filesystem path under the root, never as a `alias:` address or a linked store's document.

### The composition does not reach the graph

A composed field is a `render` marker, which is display-only and never extracted, so the child does not become an edge of the parent and graph traversal (impact radius) does not follow the composition. To get that edge, declare the source field in `__references__` and store export ids (`Model:name`) rather than paths.

Use `sldb render` or a document render/create/update workflow to produce the summaries. Render-only markers are not extracted back into the parent payload. There is no implemented edit-through operation from a summary to its child document.

The executable examples are in `tests/test_composition.py`.

## Explicit Transclusions

```bash
sldb docs recover guide --store /absolute/project/.sldb --format json
sldb docs compose guide --store /absolute/project/.sldb --format markdown -o -
```

`recover` reports explicit `[[links]]` and predicate links. `compose` recursively expands `![[child.md]]` into Markdown and reports unresolved targets in its structured output. Ordinary links are not expanded.

This is separate from `__compositions__`: it operates on document text and the link resolver, rather than formatting a child model's extracted payload.

## Historical Proposals

Section-only transclusion, query-driven composition, and edits propagated from composed output to source documents were proposals. They are not advertised as supported operations in this checkout. Remaining contract and documentation gaps are listed in [the review findings](documentation-review.md).
