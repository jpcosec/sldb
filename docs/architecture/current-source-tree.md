# Current Source Tree

Verified against the working tree on 2026-09-13. This is a map of responsibilities, not an exhaustive file inventory.

## Repository Distribution

```text
src/sldb/
├── __init__.py             public library exports
├── __main__.py             module entry point
├── core/
│   ├── ast/                Markdown parser and node conversion
│   ├── contracts/          marker and render contracts
│   ├── ir/                 document, surface, meaning, graph models
│   ├── extractor/          template recipe matching
│   ├── handlers/           block value extraction
│   ├── renderer_engine/    rendering handlers
│   ├── ingest/             source ingestion utilities
│   └── exceptions/         domain errors
├── models/                 StructuredNLDoc and knowledge models
├── runtime/                configuration and roundtrip validation
├── links/                  explicit links, recovery, transclusion
├── store/
│   ├── io/                 index persistence and locks
│   ├── models/             index schemas
│   ├── ops.py              document tracking and hash cascade
│   ├── query_engine/       structural and semantic queries
│   └── export.py           semantic handoff
├── cli/
│   ├── main.py             entry point and error reporting
│   ├── dispatcher.py       command routing
│   ├── parsers/            argument definitions
│   ├── commands/           handlers
│   ├── graph_ops/          AST/IR construction and navigation
│   └── serve/              HTTP routes and serialization
├── assets/skills/          sldb init asset
└── examples/               reference bundle and Pandoc example
```

Store layout, hashing, diagnostics, migration, and caches also have modules directly under `store/`. Consult the source for the exhaustive inventory.

## Other Working Surfaces

- `docs/`: explanations, reference documents, and historical designs.
- `knowledge/`: command and surface records; coverage does not imply every record is complete.
- `desk/`: project operational records.
- `contracts/`: external integration contracts.
- `tests/`: library, CLI, markers, links, composition, addressability, HTTP, caching, and store tests.
- `.github/workflows/ci.yml`: tests and distribution build.

The old `src/nldb/` shim and top-level compatibility modules such as `sldb/structuredNLDoc.py` are absent. Public imports such as `from sldb import StructuredNLDoc` remain available through `src/sldb/__init__.py`.
