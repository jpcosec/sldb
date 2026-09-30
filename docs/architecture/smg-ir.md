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

## Two Floors: Persisted And Derived

`S`, `M` and `G` are all derived. They are not stored: they are rebuilt from the store
every time something asks about a document. Only three floors are material.

```text
STORE  .sldb/                          <- identity: what exists
 |- core/store_index.yaml
 |- core/models/TaskDoc.yaml          MODEL     -> contract: template, fields, compositions
 |                                                (how a document of this type is read and written)
 \- core/documents/TaskDoc/
     \- task-x.yaml                   DOCUMENT  -> payload + content_hash + field_hashes
          |- payload: {title, steps, ...}   FIELD -> typed value + its own hash
          \- field_hashes: {title: a1b2...}
```

Everything above that is derived from those floors, per query:

```text
                        .yaml raw text
                              |  markdown-it-py
                              v
                       SLDBNode (AST)          <- blocks, with map=[line, line]
                              |  build_ir.py
                              v
   +------------------ DocumentIR ------------------+
   |  context    = store + model + path             |  <- the three floors, flattened
   |  structure  = MeaningNode (sections)           |  <- from the template
   |  nodes      = field -> section (heuristic!)    |  <- _map_fields_to_sections
   |  surface    = SurfaceNode (line/line)          |  <- the text, as a tree
   |  graph      = semantic edges                   |
   +-------------------------------------------------+
                              |
              +---------------+----------------+
              v               v                v
        /document/ir      graph_ui        edge_index/KGDB
```

The AST is never persisted; it is reconstructed on demand (only an in-memory runtime
cache, no on-disk projection). So `store > model > document > field` is the sole material
layer, and the IR is a view of it.

### The Open Seam

`structure`/`nodes` (meaning) and `surface` (text) are two trees born from the same
Markdown, and today they are joined by a heuristic: `_map_fields_to_sections` compares
template marker lines with rendered heading lines, and returns an empty mapping when the
counts differ. That is what makes `nodes -> section` wrong when rendering changes line
counts, and it is why line spans cannot support inline editing: to edit a field on line 2,
columns 4-42, a line range is not enough.

Character offsets close it. They are exact by construction when the render is instrumented
rather than re-parsed, because the render is the inverse of the extract. That work lands in
this layer, not as a fourth structure beside the IR.

## Layers

### Surface

The surface layer projects parsed Markdown into syntax nodes. The source file remains the text reference; the JSON projection is not a lossless serialization of every Markdown token and attribute.

It contains:

- block/node kind
- parser-provided node content (container nodes may have empty text)
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

Field nodes in `DocumentIR.nodes` carry an `owning_section` value derived from marker and heading positions. The current implementation compares template marker lines with rendered heading lines, which can assign the wrong section when rendering changes line counts. Section spans currently cover heading tokens, not whole bodies. See the [reproduced defects and contract gaps](../documentation-review.md#field-ownership-and-section-spans).

Section context indexes are now persisted in store artifacts during `stores update`, allowing queries to access section context without reparsing markdown.

The current `ast show docs/<doc>` output now includes an `ir` payload that exposes this shape.

## Why This Matters

- The original Markdown remains in the source file; inspect `surface` for its parsed projection.
- We do not stay trapped in plain text.
- Sections become first-class citizens.
- Query and mutation can target more than whole-document payload dumps.
- The graph can grow without forcing full OWL/RDF adoption up front.

## Non-Goals For This Slice

- full RDF export
- OWL reasoning inside SLDB
- recursive section-to-model resolution

Those can be added later on top of the same IR.
