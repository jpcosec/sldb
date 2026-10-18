---
name: use-sldb
description: Comprehensive Pi skill for SLDB. Use for StructuredNLDoc models, reversible Markdown markers, render/extract flows, tracked-document edits, field operations, and .sldb store workflows.
---

# Use SLDB

SLDB owns reusable structured Markdown document infrastructure.

Use this skill when the work involves:

- `StructuredNLDoc` models and their Markdown documents
- reversible render/extract markers such as `⸢rev•field⸥`
- tracked document creation, updates, composition, recovery, or validation
- field-level query, create, update, append, clean, or remove operations
- `.sldb` stores, model registration, and semantic/physical search
- model templates, field contracts, section ownership, and store-backed document workflows

## Core boundary

SLDB owns:

- model contracts
- reversible Markdown templates
- render and extract workflows
- document tracking and recovery
- field mutation and section-aware edits
- store indexing, integrity checks, and semantic queries

SLDB does **not** own deskops workflow logic such as tasks, boards, pills, rituals, or closeout policy.

## Core rules

- Every `StructuredNLDoc` field must use `Field(description="...")` with a non-empty description.
- The Markdown document is the source surface; the `.sldb/` store is the indexed query/edit layer over that source.
- Fields are already first-class through SLDB payloads, templates, sections, and field commands.
- Do not create desk-local field-instance docs just to make fields reusable, queryable, writable, or editable.
- Prefer `sldb` document and field commands over ad hoc manual edits when the document is tracked by a model.
- If an expected SLDB path fails, capture the gap in the sibling `sldb` repo instead of silently bypassing SLDB.
- Run validation before finishing a structured-document workflow.

## Common commands

```bash
python -m sldb --help
python -m sldb stores init --path .
python -m sldb stores check --store .sldb
python -m sldb stores update --store .sldb --pythonpath .
python -m sldb models add notes.models:MeetingNoteDoc --store .sldb --pythonpath .   # a model this repo declares
python -m sldb models inherit deskops:AtomDoc --store .sldb                         # a model the linked deskops store owns
python -m sldb models check AtomDoc MeetingNoteDoc --store .sldb
python -m sldb models show AtomDoc --store .sldb --pythonpath .
python -m sldb models template edit AtomDoc --input <template.md> --store .sldb --pythonpath .
python -m sldb models fields add AtomDoc <field> --type <type> --description "..." --store .sldb --pythonpath .
python -m sldb models fields remove AtomDoc <field> --store .sldb --pythonpath .
python -m sldb models validate AtomDoc --store .sldb --pythonpath .
python -m sldb models validate AtomDoc --promote --store .sldb --pythonpath .
python -m sldb docs create --model AtomDoc -o <path> <payload> --store .sldb --pythonpath .
python -m sldb docs track <path> --model AtomDoc --store .sldb --pythonpath .
python -m sldb docs update <doc> <payload> --store .sldb --pythonpath .
python -m sldb docs recover <doc> --store .sldb --pythonpath .
python -m sldb docs compose <doc> --store .sldb --pythonpath .
python -m sldb fields query <field> --store .sldb --pythonpath .
python -m sldb fields show docs/<doc>/<field> --store .sldb --pythonpath .
python -m sldb fields create docs/<doc>/<field> <value> --store .sldb --pythonpath .
python -m sldb fields update docs/<doc>/<field> <value> --store .sldb --pythonpath .
python -m sldb fields append docs/<doc>/<field> <value> --store .sldb --pythonpath .
python -m sldb fields remove docs/<doc>/<field> --store .sldb --pythonpath .
python -m sldb fields clean docs/<doc>/<field> --dedupe --drop-empty --store .sldb --pythonpath .
python -m sldb sections fields docs/<doc>/<section> --store .sldb --pythonpath .
python -m sldb ast show docs/<doc> --store .sldb --pythonpath .
python -m sldb extract deskops.models:AtomDoc <doc.md> <out.yaml> --pythonpath .
python -m sldb render deskops.models:AtomDoc <payload.yaml> <out.md> --pythonpath .
python -m sldb validate deskops.models:AtomDoc --input <doc.md> --pythonpath .
```

If the installed CLI is available as `sldb`, that shorter form is also fine.

## Models that live in your repo

A model is declared in the repo that owns the content it describes, not in the tool's repo:
any repo can write `class MeetingNoteDoc(StructuredNLDoc)` in, say, `notes/models.py` and
register it as `notes.models:MeetingNoteDoc`.

- `--pythonpath .` is how sldb imports it. The repo does not need a `pyproject.toml` or to be
  pip-installable; the store keeps the reference and the source path, never the code.
- A model another repo owns (deskops' `AtomDoc`, `TaskDoc`...) is not copied: link that
  repo's store (`sldb stores add ../deskops/.sldb --name deskops`) and `models inherit` it.

## Model editing workflow

When changing a `StructuredNLDoc` contract:

1. register the model if needed
2. inspect the current contract
3. edit the template through the SLDB draft flow
4. add or remove fields with model commands
5. validate the draft
6. promote only after validation passes
7. update the store so indexes match the new contract

Typical commands:

```bash
sldb models add <model-ref> --store .sldb --pythonpath .
sldb models show <ModelName> --store .sldb --pythonpath .
sldb ast show models/<ModelName> --store .sldb --pythonpath .
sldb models template edit <ModelName> --input <template.md> --store .sldb --pythonpath .
sldb models fields add <ModelName> <field> --type <type> --description "..." --store .sldb --pythonpath .
sldb models validate <ModelName> --store .sldb --pythonpath .
sldb models validate <ModelName> --promote --store .sldb --pythonpath .
sldb stores update --store .sldb --pythonpath .
```

Do not manually rewrite a model contract and call it done if the same change should travel through SLDB's draft/validate/promote workflow.

## Search modes

Use physical search for literal names or paths:

- file paths
- document names
- model names
- section titles
- field paths such as `title`, `goal`, or `tags`

Examples:

```bash
sldb find desk/atoms --in physical --store .sldb --pythonpath .
sldb find title --in physical --store .sldb --pythonpath .
```

Use semantic search for meaning-oriented discovery:

- model semantics such as `type.knowledge.atom`
- semantic tags such as `system:deskops`
- topic-oriented discovery such as `topic:atoms`

Examples:

```bash
sldb find topic:atoms --in semantic --store .sldb --pythonpath .
sldb find type.knowledge.atom --in semantic --store .sldb --pythonpath .
sldb find <term> --in both --store .sldb --pythonpath .
sldb find <term> --in semantic --global --store .sldb --pythonpath .
```

## Store guidance

The `.sldb/` store tracks:

- registered model contracts
- tracked document identities and paths
- extracted field payloads
- semantic indexes
- section ownership and section context
- integrity hashes
- linked-store discovery metadata

Use:

```bash
sldb stores check --store .sldb
sldb stores update --store .sldb --pythonpath .
```

Run `stores update` after model changes, tracked-doc changes, document moves, or when results look stale.

## Deskops boundary

If the work is about reading, rendering, validating, creating, tracking, updating, querying, composing, or mutating fields in a structured Markdown document, use SLDB.

If the work is about deciding workflow state, routing tasks, binding pills, closeout, or project execution logic, use deskops.

## Validation

For SLDB-heavy work, use the smallest relevant proof first, then downstream tests when needed:

```bash
pytest
sldb stores check --store .sldb
```

When changing extraction or rendering used by deskops, run SLDB tests and the affected downstream deskops tests.

## Anti-patterns

Do not:

- build desk-local workarounds for missing SLDB behavior before recording the gap
- treat the store as the source of truth instead of the Markdown doc
- create duplicate field-instance documents for behavior SLDB already owns
- bypass tracked-document commands with ad hoc edits when a safe SLDB operation exists
