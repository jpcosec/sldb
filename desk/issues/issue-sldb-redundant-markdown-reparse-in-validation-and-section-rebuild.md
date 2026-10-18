---
id: issue-sldb-redundant-markdown-reparse-in-validation-and-section-rebuild
status: closed
tags:
- system:sldb
- topic:performance
- topic:runtime
- topic:debt
related_tasks:
- desk/drawer/tasks/task-ast-parse-hotspots-re-parseo-duplicado-y-markdownit-no-reusado.md
---

# SLDB: redundant markdown re-parsing dominates the validation pipeline

## Problem

Two avoidable re-parses account for most of the wall time on a corpus-sized run. Measured over 200 documents: **~483 ms of 561 ms** is markdown parsing (`docs/user-manual.md` §13).

1. `runtime/validation.py` parses the document markdown *and* the template separately on **every** validation. The template is stable per model — it only changes through the `models template edit → validate → promote` flow — so re-parsing it per document is pure waste.
2. `store/section_rebuild.py` constructs a fresh `MarkdownIt` instance on every call instead of reusing one.

## Why this is debt, not a bug

Output is correct. The cost is structural: it scales with corpus size and silently taxes `stores update`, `models validate`, and any `sldb.api` integration doing bulk work.

## Relationship to tracked work

**A drawer task already covers this with better data.** `desk/drawer/tasks/task-ast-parse-hotspots-re-parseo-duplicado-y-markdownit-no-reusado.md` (`Status: deferred`) has the full measurement and names the same two hotspots with line numbers:

- `runtime/validation.py:56` calls `ast.split_nodes()` twice per validation
- `store/section_rebuild.py:18` builds a fresh `MarkdownIt("gfm-like")` on every `_parse_md_nodes` call

It also carries the benchmark this issue asks for, so **do not re-measure** — the baseline exists:

```
parse only       : 483.2 ms
SyntaxTreeNode   :  56.5 ms  (12% of parsing)
full split_nodes : 561.3 ms
convert overhead :  21.6 ms  (4%)
```

Two things that task establishes and this issue should inherit rather than relitigate:

1. **Parser migration is settled as not worth it.** mistune v3 on the same corpus: 437 ms vs 561 ms — ~10% at the cost of CommonMark compliance. 86% of the time is pure markdown-it-py parsing, payable with any parser.
2. **There is a secondary finding unrelated to performance.** `core/ast/markdown_ast_handler.py::_convert` discards `info` (fence lang), `markup`, and `attrs` that the token already carries. Propagating them yields ~90% of "mdast parity" with no parser change. That is a separate AST-richness issue, not part of this one.

The correct move is to promote that drawer task out of `deferred`, not to run this issue beside it. This issue's value is that it is reachable from the manual's §13; the drawer task has the engineering.

## What's needed

- Cache the parsed template per model, keyed so the cache invalidates when the template literal changes (the promote flow is the natural invalidation point).
- Reuse a single `MarkdownIt` instance in `section_rebuild.py` instead of per-call construction.
- Add a repeatable benchmark so the 483/561 ms figure stops being a one-off observation.

## Files to read first

- `src/sldb/runtime/validation.py` — the per-document validation loop and where the template is parsed
- `src/sldb/store/section_rebuild.py` — per-call `MarkdownIt` construction
- `src/sldb/core/template_extractor.py` — what a parsed template actually yields, and whether it is safe to share
- `src/sldb/api/` — bulk entry points that would benefit

## Design considerations

- **Invalidation key**: prefer the template literal's hash over model name alone, so an in-process template edit cannot serve a stale parse.
- **Mutable shared state**: confirm the parsed template structure is not mutated downstream before sharing it across documents. If it is, cache an immutable form or a cheap clone.
- **`MarkdownIt` reuse**: verify the instance is stateless across `parse()` calls with the plugin set in use before hoisting it.
- **Scope**: this is an internal optimization. No CLI surface, no output, and no store format should change.

## Task list

- [ ] **First**: promote `task-ast-parse-hotspots-...` out of `deferred` and fold this issue into it
- [ ] Reuse the existing 200-doc baseline from that task instead of re-measuring
- [ ] Confirm parsed-template structures are safe to share (no downstream mutation)
- [ ] Cache parsed templates per model, keyed by template literal hash
- [ ] Hoist and reuse the `MarkdownIt` instance in `section_rebuild.py`
- [ ] Re-run the benchmark; record the delta
- [ ] Assert unchanged behaviour: full roundtrip and `stores check` suites stay green
- [ ] Update `docs/user-manual.md` §13 with the resolved numbers

## Pills

- `desk/pills/pill-003-template-marker-roundtrip-contract.md` — roundtrip fidelity is the invariant any caching must preserve
- `desk/pills/pill-005-store-health-is-sldb-owned.md` — `runtime/` is derived cache; rebuild cost is SLDB's concern

## Resolution

Closed: 2026-10-18
Reason: Resuelto: las recetas del template se calculan una vez por template, validate renderiza una vez y section_rebuild reusa un MarkdownIt; en el store de sldb la extracción bajó de ~420 a ~275 ms.
Refs: 9e8ec426, tests/test_parse_once.py, task-quitar-los-re-parseos-evitables-del-pipeline-de-markdown
