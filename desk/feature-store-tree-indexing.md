# Feature: Store Tree Indexing With Typed Addresses

## Status

- Proposed
- Scope: `.sldb/` store layer

## Goal

Add a typed, navigable address space over the store so users and tools can explore models, tracked documents, and extracted fields without introducing a full graph query system.

This feature introduces:

- typed addresses rooted at `st`
- explorer commands like `ls` and `glob`
- direct value resolution with `get`
- typed filtering with `find --where`

## Rationale

The store already knows about:

- registered models
- tracked documents
- extracted typed structure

What is missing is a first-class way to navigate that structure.

The desired UX is closer to filesystem traversal than to a graph DSL.

## Address Model

The original idea used `R{Model}` to mark recursive model expansion. That recursion marker can be dropped from the base syntax and expressed separately.

Canonical forms:

```text
st.{Model}
st.{Model+}
st.{Model}.document
st.{Model}.document.field
```

Address parts:

- `st` = active store root
- `{Model}` = exact model scope
- `{Model+}` = include submodels/subclasses recursively
- `.document` = tracked document name
- `.field` = extracted structured field

Examples:

```text
st.{ConceptDoc}
st.{ConceptDoc+}
st.{ConceptDoc}.readme
st.{ConceptDoc}.readme.abstract
st.{ADRDoc+}.adr-auth.status
```

## Why `+` Instead Of `R`

- keeps the base address simpler
- makes exact vs recursive scope visible at the model token itself
- avoids implying a special top-level namespace just for recursion

If desired, `R{Model}` could still be accepted as a compatibility alias, but it is not necessary for the primary syntax.

## Commands

### List

```bash
sldb ls st
sldb ls 'st.{ConceptDoc}'
sldb ls 'st.{ConceptDoc}.readme'
```

Behavior:

- `sldb ls st` lists available model scopes
- `sldb ls 'st.{Model}'` lists tracked docs for that model
- `sldb ls 'st.{Model}.doc'` lists fields for that doc

Example:

```text
$ sldb ls 'st.{ConceptDoc+}'
readme
auth-overview
query-model
```

### Get

```bash
sldb get 'st.{ConceptDoc}.readme.abstract'
sldb get 'st.{ADRDoc}.adr-auth'
```

Behavior:

- resolves a single address
- returns either a scalar field value or a structured document payload

### Glob

```bash
sldb glob 'st.{ConceptDoc+}.*.title'
sldb glob 'st.{ADRDoc}.*'
```

Behavior:

- matches typed addresses
- returns concrete resolved address paths

Example:

```text
st.{ConceptDoc}.readme.title
st.{ConceptDoc}.auth-overview.title
```

### Find With Typed Filter

```bash
sldb find 'st.{ADRDoc+}' --where 'status = "accepted"'
sldb find 'st.{ConceptDoc+}' --where 'has(abstract)'
```

Behavior:

- evaluates typed predicates over resolved nodes
- returns matching documents or addresses

## Typed Filter Language

Initial predicates:

- `has(field)`
- `field = value`
- `field != value`
- `field >= number`
- `field <= number`
- `"value" in field`
- `doc ~ "pattern"`
- `model <= ConceptDoc` for subclass-aware filtering

Examples:

```bash
sldb find 'st.{ConceptDoc+}' --where 'has(abstract)'
sldb find 'st.{ADRDoc+}' --where 'status = "accepted"'
sldb find 'st.{TestDoc}' --where 'coverage >= 85'
```

## Resolution Rules

- active store is local `.sldb/` if present, otherwise global `~/.sldb/`
- exact model scope uses registered model identity only
- recursive model scope expands through Python subclass hierarchy at query time
- document names come from tracked documents in the store
- field access resolves extracted structured payload, not raw Markdown text

## Command Semantics

### `ls`

- explorer-style traversal
- no mutation
- cheap view of the next node layer

### `get`

- deterministic address resolution
- suitable for scripting and tool use

### `glob`

- wildcard expansion over typed addresses
- useful for discovery and batch operations

### `find`

- typed filter over resolved structures
- intended as the smallest useful query surface

## Relationship To Links

This feature does not replace `[[...]]` or `![[...]]`.

Instead:

- links represent authored horizontal semantics
- typed addresses represent indexed structural navigation

Later, discovered links may be exposed through the store as indexed metadata or sibling namespaces.

## MVP

1. exact model addresses: `st.{Model}`
2. recursive model addresses: `st.{Model+}`
3. `ls`
4. `get`
5. `glob`
6. minimal `find --where`

## Deferred

- graph traversal syntax
- inferred relationships
- OWL reasoning
- ranking/relevance engine
- complex query language

## Example Session

```bash
sldb ls st
sldb ls 'st.{ConceptDoc+}'
sldb get 'st.{ConceptDoc}.readme.abstract'
sldb glob 'st.{ConceptDoc+}.*.title'
sldb find 'st.{ADRDoc+}' --where 'status = "accepted"'
```

## Design Principle

Make the store feel like a typed tree that can be explored, globbed, and filtered, without turning SLDB into a general-purpose graph database.
