# Docs Workspace

This directory can now be worked through SLDB models and the project-local store.

## Current Model Mapping

- `docs.models:ArchitectureNarrativeDoc` - `docs/architecture/*.md`
- `docs.models:PackagingDoc` - `docs/packaging instructions.md`
- `docs.models:RequestDoc` - `docs/requests/*.md`
- `docs.models:PlanDoc` - `docs/superpowers/plans/*.md`
- `docs.models:SpecDoc` - `docs/superpowers/specs/*.md`

## Why These Models Are Shallow

The documentation corpus is structurally heterogeneous.

For the current slice, the models are intentionally shallow:

- they validate and track the document families reliably
- they attach family-level semantic tags through model semantics
- they rely on `sections` and `find` for deeper navigation through headings

This keeps the docs workspace operable in SLDB without forcing every file into the same fine-grained field schema.

## Authoring Rule

If a document should use the generic `title + body` pattern, keep at least one short paragraph after the H1 before jumping into code fences or subsections.

That lead paragraph gives the current reversible extraction model a stable anchor while the section and semantic indexes continue to expose the deeper structure.

## Recommended Workflow

Register the models:

```bash
python -m sldb models add docs.models:ArchitectureNarrativeDoc --store .sldb --pythonpath .
python -m sldb models add docs.models:PackagingDoc --store .sldb --pythonpath .
python -m sldb models add docs.models:RequestDoc --store .sldb --pythonpath .
python -m sldb models add docs.models:PlanDoc --store .sldb --pythonpath .
python -m sldb models add docs.models:SpecDoc --store .sldb --pythonpath .
```

Track the documents, then rebuild indexes:

```bash
python -m sldb docs track docs/architecture/current-system-overview.md --model ArchitectureNarrativeDoc --name arch-current-system-overview --store .sldb --pythonpath .
python -m sldb stores update --store .sldb --pythonpath .
```

If a tracked docs document should leave the active store, remove it explicitly before deleting or moving it:

```bash
python -m sldb docs untrack arch-current-system-overview --store .sldb --pythonpath .
```

Query the tracked docs:

```bash
python -m sldb find type.documentation.architecture --in semantic --store .sldb --pythonpath .
python -m sldb sections show arch-current-system-overview --store .sldb --pythonpath . --format yaml
python -m sldb docs show req-ontology-feature-request --store .sldb --pythonpath . --format yaml
```

## Current Limits

- The current docs models are intentionally coarse and family-level.
- Deep heading navigation comes from `sections` and semantic indexes more than from many fine-grained document fields.
- Generic `title + body` models work best when the document starts with a short lead paragraph before jumping into dense fenced blocks.
