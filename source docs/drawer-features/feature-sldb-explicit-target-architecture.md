# Feature: Explicit target architecture for the SLDB refactor

## Kind

feature

## Status

open

## Why this exists

The current SLDB codebase grew around Markdown templates, Pydantic document models, store metadata, CLI surfaces, links, semantic projections, and desk/workflow usage without a stable architectural center.

We now have enough clarity to state the target explicitly before starting the deep refactor.

This document captures that target as directly as possible.

## Main decision

SLDB should move toward a **canonical AST-centered architecture**.

Markdown should no longer be the sovereign representation.

Pydantic-style field contracts should not disappear, but they should stop being the structural center of the system.

The new center should be a **general, extensible, typed AST** that can represent:

- documents
- sections
- fields
- links
- transclusions
- anchors
- hooks
- provenance
- temporal history
- derived projections

## What we think the system needs

### 1. A complete and extensible canonical IR/AST

The system needs a general AST of its own.

That AST must be able to represent the real document structure and not just the current Markdown-template marker logic.

The AST is the main source of truth.

Everything else becomes an importer, adapter, projection, cache, or derived view over that AST.

### 2. A translator from Markdown into the canonical AST

Markdown remains important, but only as one input surface.

We still need a strong Markdown importer because the current ecosystem and authoring flow depend on it.

But Markdown should be treated as:

- a source format
- a projection target
- a human editing surface

not as the canonical semantic representation.

### 3. A compiler from the canonical AST to Markdown

The system needs to compile AST back to Markdown.

Later it may also compile to:

- code
- text-only views
- config surfaces
- graph-friendly exports
- other structured formats

### 4. Infrastructure for cache, hashing, Merkle behavior, and recomputation

The system needs structural hashing and subtree-level recomputation.

Store-like behavior should become infrastructure over AST, not the core architecture itself.

### 5. Durable graph-friendly and semantic projections

Links, anchoring, semantic navigation, and graph export should be derived projections from the AST and related metadata.

## Why Markdown is no longer enough

Markdown is useful as a human-facing textual surface.

But it becomes too weak as the canonical representation once we need all of the following at the same time:

- stable addressability
- external anchoring
- executable hooks
- transclusions
- rich links
- graph projection
- field-aware extraction
- durable temporal tracking
- future code generation or code projection

If we keep layering all of that directly on top of Markdown, we are effectively inventing a new language anyway.

That is why the architecture should stop treating Markdown as the core.

## Relationship with the old Pydantic model idea

The refactor does **not** mean abandoning typed models.

Instead, it means generalizing them.

The current Pydantic contract captured one important dimension of the system: fields and validation.

The new AST must preserve that dimension and make it explicit.

That means the AST must carry **field binding** information.

## The AST must be field-aware

The AST cannot be only a document tree.

It must also know how document structure binds to typed fields.

That includes at least:

- field identity
- field path
- field type
- cardinality
- extraction strategy
- render strategy
- reversibility
- derived vs authored status
- nested composition
- provenance of field values

This is important because SLDB is not just a Markdown parser.

It is an extension over typed document models.

## What the canonical AST must carry

### Structural layer

- node ids
- document ids
- parent/child relationships
- sibling order
- node kinds
- subtypes
- slots / named regions
- textual or typed content
- attributes / properties
- source spans

### Field/schema layer

- field bindings
- field paths
- schema bindings
- type contracts
- cardinality
- defaults
- validation constraints
- render/extract strategy metadata
- reversibility markers

### Link/reference layer

- links
- transclusions
- typed references
- internal targets
- external targets
- resolution state
- link provenance

### Addressability layer

- structural paths
- local anchors
- stable selectors
- aliases
- fragment ids

### External anchoring layer

This is important because of the work around external document anchoring.

The AST must support anchoring data that can point beyond the local document.

That includes:

- external resource references
- location selectors
- sampled text
- surrounding context
- content hashes
- reattachment policies
- confidence/evidence data

This is the point where local AST structure is not enough on its own.

A node may need to anchor against an external file or external text fragment.

### Hook layer

The AST must support declarative hooks.

Not every hook needs to execute inside the AST runtime directly, but the AST must be able to describe them.

That includes:

- hook type
- executable target
- expected inputs
- expected outputs
- execution policy
- verification/result contract

### Provenance and history layer

The AST or the surrounding canonical model must support durable provenance.

We want more than git-only history.

We want system-level knowledge of:

- what changed
- when it changed
- which node changed
- which field changed
- what source produced it
- whether it was authored or derived

### Hashing/cache layer

The system must support:

- node hashes
- subtree hashes
- dependency hashes
- structural fingerprints
- dirty-state invalidation
- projection cache keys

## How ProseMirror fits

ProseMirror should **not** be the canonical AST.

It is still useful, but as a downstream projection or editing model.

It can help with:

- editable structured document views
- positional transforms
- local anchoring within document edits
- rendering/document interaction

But it should not be treated as:

- the main store
- the append-only history system
- the Merkle implementation
- the complete anchoring layer

## How tree-sitter fits

tree-sitter should also **not** be the canonical AST.

It is useful as a parser/projection technology for programming-language surfaces.

That makes it suitable for:

- code-oriented importers
- code-oriented projections
- syntax-aware code generation paths

But it is not the sovereign model for the whole system.

## What this implies about architecture

We should separate the system into the following broad layers.

### A. Canonical AST core

This is the center.

It defines the node model, field bindings, addressability model, provenance model, and transformation rules.

### B. Importers / translators

These bring external representations into the AST.

Examples:

- Markdown -> AST
- YAML/JSON -> AST
- external anchor references -> AST records
- future code/document formats -> AST

### C. Adapters / projection models

These are specialized representations built from the AST.

Examples:

- AST -> ProseMirror model
- AST -> tree-sitter-oriented code model

### D. Emitters / compilers

These render the AST outward.

Examples:

- AST -> Markdown
- AST -> code
- AST -> text
- AST -> config
- AST -> graph payloads

### E. Infrastructure layers

These support the AST but are not the AST itself.

Examples:

- Merkle / hashing
- cache
- dependency index
- append-only event log
- snapshots
- temporal storage

### F. Derived projections

Examples:

- graph projection
- semantic views
- search views
- structural query views
- store indexes

## Store should stop being the conceptual center

The current `store` area may still survive in some form, but its role should change.

Instead of being treated as a domain center, it should mostly become infrastructure over the canonical AST.

That means things like:

- tracked document indexes
- hashes
- cache artifacts
- semantic projections
- federated references
- diagnostics

should be reconsidered as infrastructure, projections, or runtime services built around AST.

Also, some parts of current store behavior may be large enough to split into a separate module or even a separate project.

## Links and graph projection become much easier under this model

Once the AST owns:

- node identity
- addressability
- references
- provenance
- anchoring

then links and graph projection stop being special hacks.

They become ordinary derived structures over canonical nodes and typed relations.

## Legacy policy

Legacy runtime surfaces should not be preserved as first-class architecture in the target system.

They stay recoverable through git history.

The target architecture should be designed cleanly, not around permanent compatibility baggage.

## Runtime and language direction

The current direction discussed is:

- **Rust** for the canonical AST core and low-level structural infrastructure
- **Python** for the CLI and orchestration layer

This would allow:

- a stronger canonical data model
- better hashing / Merkle support
- clearer invariants
- continued use of the current Python CLI ecosystem during migration

## High-level target flow

The intended flow looks like this:

1. External input arrives.
   - Markdown
   - YAML/JSON
   - code-oriented inputs where possible
   - external anchoring references

2. Importers translate that input into the canonical AST.

3. The AST is enriched with:
   - field bindings
   - links
   - anchors
   - hooks
   - provenance
   - hashes

4. Infrastructure layers compute:
   - subtree hashes
   - dependency relationships
   - cache materializations
   - append-only events / snapshots

5. Derived projections are produced:
   - Markdown
   - code
   - graph exports
   - semantic/search/query views
   - store-like runtime artifacts

## What this means for the refactor starting now

We should start by writing explicitly toward this target.

The refactor should not begin as a file-shuffle inside the current Python package layout.

It should begin from:

- the target architecture
- the canonical AST model
- the boundaries between AST core, infrastructure, adapters, projections, and CLI

## Open design questions

- What is the minimum canonical node schema for the first AST version?
- Which current SLDB concepts become true AST nodes, and which remain metadata or projections?
- Which field semantics from the current Pydantic workflow must be preserved in the first migration slice?
- What is the first safe end-to-end slice?
  - likely Markdown -> AST -> Markdown
- At what point do links and anchoring move from ad hoc logic into the AST core contract?
- Which current store subsystems survive as infrastructure, and which should disappear entirely?
