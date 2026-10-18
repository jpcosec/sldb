# Semantic Export Boundary

> Note (2026-10-18): KGDB was merged into sldb and is now its graph layer (`sldb.store.graph`, CLI `sldb graph ...`). Where this document says KGDB it means that layer; no external `kgdb` package or executable exists any more. The `sldb_semantic_export` contract name is kept as a data contract.

SLDB owns the semantic truth for tracked Markdown documents. KGDB should ingest that truth through the versioned semantic export contract instead of scraping `.sldb/runtime` files directly.

The export is a graph-ready payload for downstream graph persistence and traversal. It preserves SLDB's model, document, section, semantic tag, semantic DAG, equivalence, and hash provenance, while leaving source-file and workflow-specific graph edges to downstream adapters such as deskops.

## Command

Generate the KGDB payload from a store with `sldb stores semantic-export`:

```bash
sldb stores semantic-export --store .sldb --pythonpath . --format sldb --encoding json --rebuild -o semantic.json
```

Use `-o -` or omit `-o` to write the payload to stdout. Use `--encoding yaml` when a YAML handoff is easier to inspect. `--rebuild` refreshes semantic and section indexes before export.

The current contract name is `sldb_semantic_export` with version `1`.

## What The Export Includes

- Contract metadata: payload name, version, and generation timestamp.
- Producer metadata: SLDB version and the command surface that produced the export.
- Store provenance: project root, store path, store hash, and diagnostic runtime source paths.
- Model entries: model name, import ref, source path, index paths, version, canonical flag, family, model semantics, base models, and model hash.
- Document entries: stable export id, tracked doc name, model name, Markdown path, document index hash, document content hash, and semantic tags.
- Section entries: stable section id, owning document id, section path, title, breadcrumbs, derived `about` terms, semantic tags, slug, heading level, and source line range when available.
- Semantic DAG: semantic nodes, parent relationships, and equivalence mappings.

These fields give KGDB enough normalized identity, semantics, hierarchy, and provenance to create nodes and semantic edges without depending on SLDB's private runtime layout.

## What The Export Excludes

- Source-code relation extraction, such as Python imports, call graphs, class references, or file-to-file dependency edges.
- Workflow-specific edges, such as `task blocks source file`, `inbox note raised by command`, `desk task depends on implementation file`, or repository-specific ownership rules.
- KGDB persistence details, NetworkX storage, traversal policies, graph projections, or query APIs.
- Raw Markdown document bodies and rendered document text beyond the paths, section titles, breadcrumbs, derived context, semantic tags, and hashes needed for graph identity.
- Ad hoc access to `.sldb/runtime` as an ingestion mechanism. Runtime source paths in the payload are provenance hints, not a scraping contract.

Downstream systems may add these excluded edges after ingestion. For example, deskops can connect `TaskDoc:003-document-semantic-export-boundary` to files it edited, but that edge is a deskops workflow fact, not SLDB semantic truth.

## Example SLDB To KGDB Flow

1. A project registers `StructuredNLDoc` models and tracks Markdown documents in `.sldb`.
2. The project runs `sldb stores update --store .sldb --pythonpath .` or exports with `--rebuild` so semantic and section indexes are current.
3. The project emits the semantic payload with `sldb stores semantic-export --store .sldb --pythonpath . --format sldb --encoding json -o semantic.json`.
4. The graph layer (`sldb.store.graph`, formerly kgdb) validates the payload against `sldb_semantic_export` version `1`.
5. KGDB creates or updates graph nodes for exported models, documents, sections, semantic tags, DAG relationships, and equivalences.
6. Downstream adapters add non-SLDB graph edges, such as source-file relations or workflow provenance, using the SLDB export ids as stable anchors.

This keeps the semantic layer and graph layer separate: SLDB publishes document meaning, while KGDB persists and traverses graph relationships.

## Difference From SLDB Semantic Search

Semantic search is an interactive retrieval surface inside SLDB. Commands such as `sldb find type.documentation.architecture --in semantic --store .sldb --pythonpath .` return matching documents, sections, or fields for a query.

Semantic export is a bulk handoff contract. `sldb stores semantic-export` emits the normalized semantic payload for another system to ingest. It is not a query result, and it is not meant to decide which graph edges KGDB should store beyond the SLDB-owned semantic relationships in the payload.

Use semantic search when a human or tool needs to find matching SLDB content. Use semantic export when KGDB or another graph consumer needs the whole SLDB semantic state as graph-ready input.
