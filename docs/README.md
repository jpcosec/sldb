# Docs Workspace

The [CLI self-documentation workflow](self-documentation.md) now regenerates tracked command references from the parser and checks freshness. The [task board](../desk/tasks/Board.md) separates self-documentation, store federation, and AST correctness work.

The [Python docstring indexing spec](architecture/code-docstring-indexing.spec.md) defines the next slice: source metadata, AST-derived structure, selective tag inheritance, and KGDB/spec2viz integration. Two source examples are annotated; consuming this convention is still pending. The [continuation handoff](architecture/code-docstring-indexing-handoff.md) bounds the next annotation batch and lists implementation gaps.

This directory can now be worked through SLDB models and the project-local store.

For behavior verified on 2026-09-13, start with the [CLI tree](architecture/current-cli-tree.md), [source map](architecture/current-source-tree.md), [AST queries](ast_query_primitives.md), and [composition modes](composition_modes.md). The [review findings](documentation-review.md) collect remaining defects, missing contracts, and incomplete coverage. Target architecture and migration plans are historical proposals for this frozen v1 repository.

## Current Model Mapping

- `docs.models:ArchitectureNarrativeDoc` - `docs/architecture/*.md`
- `docs.models:AtomicDocumentDoc` - `docs/atoms/*.atom.md`
- `docs.models:FAQDoc` - `docs/faq.md`
- `docs.models:PackagingDoc` - `docs/packaging instructions.md`
- `docs.models:RequestDoc` - `docs/requests/*.md`
- `docs.models:StoreReadmeDoc` - `.sldb/README.md`

## Atom And Document Split

The docs surface now has two layers:

- `docs/atoms/*.atom.md` holds short SSOT concept definitions such as store, tracked doc, semantic versus physical search, and compose versus recover.
- `docs/faq.md` and the other higher-level docs explain workflows and point back to those atoms instead of redefining everything inline.

The architecture docs also define integration boundaries, including the [SLDB semantic export boundary for KGDB](architecture/semantic-export-boundary.md).

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
python -m sldb models add docs.models:AtomicDocumentDoc --store .sldb --pythonpath .
python -m sldb models add docs.models:FAQDoc --store .sldb --pythonpath .
python -m sldb models add docs.models:PackagingDoc --store .sldb --pythonpath .
python -m sldb models add docs.models:RequestDoc --store .sldb --pythonpath .
python -m sldb models add docs.models:StoreReadmeDoc --store .sldb --pythonpath .
```

Track the documents, then rebuild indexes:

```bash
python -m sldb docs track docs/architecture/current-system-overview.md --model ArchitectureNarrativeDoc --name arch-current-system-overview --store .sldb --pythonpath .
python -m sldb docs track docs/atoms/store.atom.md --model AtomicDocumentDoc --name atom-store --store .sldb --pythonpath .
python -m sldb docs track docs/faq.md --model FAQDoc --name faq --store .sldb --pythonpath .
python -m sldb docs track .sldb/README.md --model StoreReadmeDoc --name sldb-readme --store .sldb --pythonpath .
python -m sldb stores update --store .sldb --pythonpath .
```

If a tracked docs document should leave the active store, remove it explicitly before deleting or moving it:

```bash
python -m sldb docs untrack arch-current-system-overview --store .sldb --pythonpath .
```

Query the tracked docs:

```bash
python -m sldb find type.documentation.architecture --in semantic --store .sldb --pythonpath .
python -m sldb find type.documentation.atom --in semantic --store .sldb --pythonpath .
python -m sldb docs show faq --store .sldb --pythonpath . --format yaml
python -m sldb docs show sldb-readme --store .sldb --pythonpath . --format yaml
python -m sldb sections show arch-current-system-overview --store .sldb --pythonpath . --format yaml
python -m sldb docs show req-ontology-feature-request --store .sldb --pythonpath . --format yaml
```

## Current Limits

- The current docs models are intentionally coarse and family-level.
- Deep heading navigation comes from `sections` and semantic indexes more than from many fine-grained document fields.
- Generic `title + body` models work best when the document starts with a short lead paragraph before jumping into dense fenced blocks.
- That same shallow pattern is the current recommended path for Pandoc fenced div documents such as CVs: preserve the blocks in `body` first, then add custom handlers only if you need typed access to div attributes.
- Atom docs are intentionally smaller and more repetitive than the narrative docs because they are meant to act as canonical concept definitions.
