# SMG Document IR

SLDB needs a first-class representation between raw Markdown surface and store/query indexes.

We name that representation `SMG`:

- `S` - Surface: reversible text and syntax
- `M` - Meaning: logical-operational structure
- `G` - Graph: relations, projections, indexes, and traversal

Formally:

```text
R(T) = (S, M, G)
```

Where `T` is the original document text and `R(T)` is the operable document representation.

## Layers

### Surface

The surface layer preserves the original document as a reversible syntax tree.

It contains:

- block/node kind
- original text content
- source span
- syntax metadata such as markdown tag/type

This layer should be stable enough to support roundtrip rendering and future grammar-aware edits.

### Meaning

The meaning layer represents the logical shape of the document.

It contains:

- document context
- section hierarchy
- recursive typed nodes
- field/value nodes
- section-local structure that can later map to nested models

This is the missing layer between `document -> payload -> render`.

### Graph

The graph layer organizes traversable relationships.

It contains:

- document -> section edges
- document -> field edges
- semantic tags and semantic equivalences
- physical anchors and paths
- future model inheritance and cross-document relationships

## Current Minimal Shape In SLDB

The initial implementation introduces `DocumentIR` with:

- `context`
- `structure`
- `nodes`
- `surface`
- `graph`
- `context_index`

`context_index` is the minimal "what is this section about" layer.
Each entry is section-oriented and carries:

- section path
- title
- breadcrumbs
- inferred `about` terms
- inherited semantic tags
- source span

This gives the AST a lightweight section/context index without requiring a separate reasoning library.

Field nodes in `DocumentIR.nodes` carry an `owning_section` field that identifies the section that owns each field via heading-based inference (the nearest preceding heading in the template).

Section context indexes are now persisted in store artifacts during `stores update`, allowing queries to access section context without reparsing markdown.

The current `ast show docs/<doc>` output now includes an `ir` payload that exposes this shape.

## Why This Matters

- We do not lose original Markdown text.
- We do not stay trapped in plain text.
- Sections become first-class citizens.
- Query and mutation can target more than whole-document payload dumps.
- The graph can grow without forcing full OWL/RDF adoption up front.

## Non-Goals For This Slice

- full RDF export
- OWL reasoning inside SLDB
- recursive section-to-model resolution

Those can be added later on top of the same IR.
