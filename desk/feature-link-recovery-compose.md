# Feature: Link-Aware Documents With Recover And Compose

## Status

- Proposed
- Scope: SLDB document layer

## Goal

Add explicit horizontal relationships to authored Markdown without requiring a full graph engine.

The feature introduces:

- `[[target]]` for explicit document-to-document links
- `![[target]]` for explicit transclusion/composition links
- `sldb recover` to resolve and return structured linked context
- `sldb compose` to materialize transcluded content deterministically

## Rationale

SLDB already treats documents as structured contracts. The natural place to express cross-document relationships is the document surface itself.

This gives us:

- human-visible links
- LLM-visible links
- roundtrippable relations
- a later path for `.sldb/` to index discovered links without owning them

## Syntax

### Standard Link

```md
See [[concept-auth-model]] for the domain model.
```

- expresses a horizontal relationship
- does not inline target content

### Transclusion Link

```md
Implementation constraints:
![[shared-auth-constraints]]
```

- requests inclusion/composition of linked content
- is resolved by `compose`

## Resolution Rules

Resolution order:

1. tracked document name in the active store
2. explicit relative file path
3. future typed store address support

Supported initial targets:

- `[[doc-name]]`
- `[[docs/path/to/file.md]]`

Deferred target forms:

- `[[doc#field]]`
- `[[st.{Model}.doc.field]]`

## Commands

### Recover

```bash
sldb recover <doc>
sldb recover <doc> --depth 1
sldb recover <doc> --format text|json|yaml
sldb recover <doc> --links-only
sldb recover <doc> --include transclusions
```

Behavior:

- parses the root document
- resolves `[[...]]`
- optionally resolves `![[...]]`
- returns a structured context bundle
- reports unresolved targets explicitly

Example output:

```yaml
root: adr-auth
links:
  - target: concept-auth-model
    kind: link
    resolved: true
  - target: shared-auth-constraints
    kind: transclusion
    resolved: true
```

### Compose

```bash
sldb compose <doc>
sldb compose <doc> -o composed.md
sldb compose <doc> --expand-transclusions
sldb compose <doc> --format markdown|json|yaml
```

Behavior:

- parses the root document
- resolves `![[...]]`
- produces composed Markdown or structured output
- keeps composition deterministic and inspectable

## Semantics

### `[[target]]`

- explicit semantic link
- recoverable
- not inlined by default

### `![[target]]`

- explicit composition/transclusion directive
- composeable
- may also be included in recovery output as a separate relation kind

## Store Relationship

Documents remain the source of truth.

The `.sldb/` store may later:

- index discovered links
- expose backlinks
- accelerate recovery/composition

But the store should not become the primary authored relationship system for this feature.

## MVP

- parse `[[doc]]` and `![[doc]]`
- resolve against tracked docs first
- add `recover`
- add `compose`
- preserve explicit unresolved-link diagnostics

## Deferred

- backlinks
- weighted relevance scoring
- richer relation taxonomies
- automatic graph materialization
- OWL or graph reasoning

## Example

```md
# Authentication ADR

See [[concept-auth-model]] for background.

Shared constraints:
![[shared-auth-constraints]]
```

```bash
sldb recover docs/adr/auth.md --format yaml
```

```bash
sldb compose docs/adr/auth.md -o build/auth.composed.md
```

## Design Principle

Keep explicit horizontal semantics in the Markdown layer, and let the store index them later.
