# SLDB Composition Modes

Verified against the working tree on 2026-09-28. Two composition mechanisms are implemented: model-driven summaries during rendering, and explicit document transclusions through the CLI.

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

The option is `template`, not `line_template`.

### Path anchoring

Relative child paths resolve against the document's project root — not the process working directory. The root is taken from, in order: the instance attribute `_composition_root` (set by renderers, set by `render_model_markdown(..., root=...)`), the class attribute `__composition_root__`, and finally the process cwd as a compatibility fallback when no root is available. Store-backed entry points (`sldb docs create/update`, the server's `/render`) always pass the store's project root, so composition output is independent of the server's cwd. Absolute child paths are used as-is.

### Broken children are reported, not silent

A missing child path, a child whose payload does not extract under the declared model, an empty payload, or a `template` formatting error leaves the rendered markdown unchanged — the summary line is skipped, exactly as before. The failure is not dropped: it is recorded on the instance and readable as `model.composition_issues`, a list of per-child diagnostics (`compose_field[<field>]: <reason> <ref> (<path>)`). An empty `composition_issues` is the only trustworthy sign of "no children compose".

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
