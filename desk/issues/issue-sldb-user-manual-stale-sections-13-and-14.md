---
id: issue-sldb-user-manual-stale-sections-13-and-14
status: closed
tags:
- system:sldb
- topic:documentation
- topic:bug
related_tasks:
- desk/tasks/task-build-code-self-documentation.md
---

# SLDB: user manual §13/§14 record three items that the code already resolved

## Problem

`docs/user-manual.md` claims in §16 that every statement was executed against a real store and audited by three reviewers. Three entries are now stale — the code moved and the manual did not.

Verified against this repo at the current commit:

**1. §13 — "`ast show` imprime warnings antes del JSON. Filtrá desde `^{`."**

```bash
python -m sldb ast show --store .sldb --format json 2>/dev/null | head -2
# {
#   "store": {

python -m sldb ast show --store .sldb --format json 2>&1 >/dev/null
# (empty)
```

stdout is clean JSON and stderr is empty. `src/sldb/cli/commands/ast.py` only prints the payload. The advice to filter from `^{` is now cargo-cult.

**2. §14 — "`__containment__` / `__references__` no generan aristas."**

`src/sldb/store/edge_index/declared_references.py` exists and emits `contains` / `references` edges with `origin: "schema"`. It is wired in: `doc_contribution.py:7` imports `declared_reference_edges`, and `edge_rebuild.py:15` imports `build_doc_edges`. The module docstring even states the past tense: *"Those two dunders **were** readable metadata only [...] the edge index ignored them."*

**3. §14 — "`Corpus.rank()` [...] ni se exporta en `sldb.api`."**

```bash
python -c "import sldb.api as a; print(hasattr(a,'Corpus'), hasattr(a.Corpus,'rank'))"
# True True
```

`src/sldb/api/__init__.py:74` exports `Corpus`, and line 86 lists it in `__all__`. §16 records this as an audit *correction* ("ademas no se exporta en `sldb.api`"), so the manual is confidently wrong on a point it went out of its way to sharpen.

## Why this matters

§16 is the manual's credibility claim. Stale entries in the two sections that exist to catalogue known problems are worse than no entries: they send readers to build workarounds for solved problems, and they undermine the audit table that asserts freshness.

## Relationship to tracked work

`task-build-code-self-documentation` (`status: active`) is the only task on the board still `active` without `current_node: completed`, and it owns exactly this problem class: keeping the repo's self-description true. The executable check this issue asks for belongs there, not as a standalone effort.

`docs/documentation-review.md` is referenced by three open tasks as the record of documentation defects. These three stale entries should land in it.

## What's needed

- Remove the `ast show` warning entry from §13.
- Remove or rewrite the `__containment__` / `__references__` entry in §14 to describe what the edges actually do (`origin: "schema"`, unresolved targets dropped rather than reported).
- Correct the `Corpus.rank()` entry: it is exported; state the real remaining gap if there is one (no CLI command).
- Correct the §16 audit table rows that assert the last two.
- Add a re-verification step so §13/§14 are checked against the code, not carried forward.

## Files to read first

- `docs/user-manual.md` §13, §14, §16
- `src/sldb/cli/commands/ast.py` — prints payload only
- `src/sldb/store/edge_index/declared_references.py` — docstring states the old behaviour in past tense
- `src/sldb/store/edge_index/doc_contribution.py:7`, `src/sldb/store/edge_rebuild.py:15` — the wiring
- `src/sldb/api/__init__.py:74,86` — the `Corpus` export

## Design considerations

- **Fix the process, not just the text.** These three drifted because nothing re-checks them. A test or lint pass that executes the manual's claims is the durable fix.
- **§16 is a verification record.** Edits there must state what changed and when, or it stops being evidence.
- The four other §13 entries were separately verified and remain accurate; do not sweep them into this cleanup.

## Task list

- [ ] Route the executable-check work into `task-build-code-self-documentation` rather than duplicating it
- [ ] Record the three stale entries in `docs/documentation-review.md`
- [ ] Re-verify all §13 and §14 entries against the current code; list which hold
- [ ] Remove the `ast show` warning entry from §13
- [ ] Rewrite the `__containment__` / `__references__` entry to describe actual edge behaviour
- [ ] Correct the `Corpus.rank()` entry to the real remaining gap
- [ ] Correct the affected §16 audit rows
- [ ] Add an executable check so manual claims fail loudly when the code moves
- [ ] Cross-link the issues opened for the entries that are still valid

## Pills

- `desk/pills/pill-015-self-documentation-boundaries.md` — what the repo is allowed to assert about itself
- `desk/pills/pill-002-onboarding-surface-before-depth.md` — the manual is the onboarding surface; stale known-limits text is a direct cost

## Resolution

Closed: 2026-10-18
Reason: Resuelto: §13 ya no lista fricciones resueltas (ast show con warnings, --format rechazado, edges show silencioso, los re-parseos, models template show) y §16 registra las correcciones; §14 ya estaba corregido.
Refs: f5541c04, 99e6cae93e, task-quitar-del-manual-las-fricciones-que-ya-no-existen
