# SLDB Composition Modes

Verified against the working tree on 2026-09-13. Two composition mechanisms are implemented: model-driven summaries during rendering, and explicit document transclusions through the CLI.

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

The option is `template`, not `line_template`. Relative child paths are currently resolved from the process working directory; this mechanism does not invoke the linked-store resolver. Missing paths and invalid child payloads can be skipped silently.

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
