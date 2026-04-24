# Feature: Canonical Models And Global/Local Semantic Navigation

## Status

- Proposed
- Scope: model semantics, semantic federation, global/local navigation

## Goal

Define how canonical models, local specialized models, and federated semantic navigation work together.

This feature adds three ideas:

- central stores may register canonical models
- local stores may define specialized models that inherit from canonical ones
- federated semantic navigation must support jumping from global semantic nodes back into store-local semantic views

## Core Principle

Semantics exist at more than one layer.

### Model-Level Semantics

Models express the semantic kind of document they represent.

Examples:

- README
- ADR
- Concept
- Reference

Model semantics describe the intended family and role of a document type.

### Document-Level Semantics

Documents express the concrete contextual semantics of a specific instance.

Examples:

- this is a README
- this is a TypeScript README
- this is a project README
- this is part of a store
- this is onboarding documentation

Model semantics provide defaults and families. Document semantics provide local contextual placement.

## Canonical Models

A central or outer store may register canonical models.

These models act as semantic anchors for a family of documents.

Example:

```python
class ReadmeDoc(StructuredNLDoc):
    __description__ = "Canonical README document."
    __family__ = "readme"
    __semantics__ = {
        "type": ["documentation", "readme"],
    }
```

Canonical models should be:

- reusable across stores
- stable enough to act as shared references
- registered by the central/root store when appropriate

## Local Specialized Models

Local stores may define models that inherit from canonical ones.

Example:

```python
class TypeScriptReadmeDoc(ReadmeDoc):
    __description__ = "README for a TypeScript project."
    __semantics__ = {
        "ecosystem": ["typescript"],
        "scope": ["project"],
    }
```

This means:

- structural inheritance follows Python model inheritance
- semantic specialization follows model inheritance
- local stores can refine a shared family without replacing it

## Semantic Defaults And Overrides

The intended behavior is:

- canonical model defines baseline semantics
- local inherited model adds or narrows semantics
- concrete document adds document-specific semantic tags

So semantics flow downward:

```text
canonical model -> local specialized model -> local document
```

Documents should be able to:

- inherit model semantics by default
- add additional local tags
- override or narrow semantics where explicitly allowed

## Global And Local Semantic Views

There should be two semantic navigation contexts.

### Local Semantic View

`se` is the semantic index for the active/local store.

Examples:

```text
se.type.documentation.Readme
se.project.myproj.database
```

### Global/Federated Semantic View

`gse` is the semantic index materialized by the root or outer store.

Examples:

```text
gse.type.documentation.Readme
gse.project.sldb.database
```

The key requirement is that global semantic navigation must not erase local provenance.

## Jumping From Global To Local

It must be valid to navigate from a federated semantic node into a store-local semantic realization.

Example form:

```text
gse.sldb.se.{particular_store}
```

The precise final syntax may change, but the capability must exist.

Meaning:

- start from the federated semantic space
- identify a canonical/global semantic node
- descend into how a particular store realizes that node locally

This allows:

- canonical navigation at the root
- provenance-aware descent into local meaning
- inspection of store-specific specialization

## Why This Matters

Without global-to-local navigation:

- federation loses traceability
- local semantic specialization is hidden
- canonical semantics flatten local nuance

With global-to-local navigation:

- root store can expose canonical meaning
- local stores can preserve contextual specialization
- users can move between shared semantics and local realizations

## Semantic Federation Rule

For now, semantic federation should remain explicitly authored.

That means:

- root store declares the central semantic tree
- local stores declare explicit node equivalences into that tree
- no automatic semantic merge is attempted yet

This also applies to model semantics:

- canonical model semantics come from the root or central store
- local specialized model semantics are mapped explicitly into the federated tree

## Suggested Metadata Shape

Canonical model:

```python
class ReadmeDoc(StructuredNLDoc):
    __description__ = "Canonical README document."
    __family__ = "readme"
    __semantics__ = {
        "type": ["documentation", "readme"],
        "role": ["overview"],
    }
```

Local specialized model:

```python
class TypeScriptReadmeDoc(ReadmeDoc):
    __description__ = "README for a TypeScript project."
    __semantics__ = {
        "ecosystem": ["typescript"],
        "scope": ["project"],
        "part_of": ["store"],
    }
```

Concrete document tags:

```yaml
semantic_tags:
  - project.sldb.database
  - role.onboarding
```

## Query Implications

This model should support queries such as:

- all README-family documents in the federated root
- all TypeScript README specializations in one store
- all local realizations of the canonical README node
- all project/database documents across the root semantic tree

Examples:

```bash
sldb get gse.type.documentation.Readme
sldb ls gse.type.documentation.Readme
sldb ls 'gse.type.documentation.Readme.se.{my_store}'
sldb find se.type.documentation.Readme --where 'model <= ReadmeDoc'
```

## Responsibilities By Layer

### Central/Root Store

- declares canonical semantic tree
- registers canonical models
- defines explicit semantic equivalence mappings for federation
- materializes `gse`

### Local Store

- defines specialized models
- maps local semantic nodes into root semantic nodes
- indexes documents into local `se`
- exposes local semantic specialization to global navigation

### Document

- instantiates a model
- carries local semantic tags
- participates in both `se` and `gse`

## MVP

1. canonical model support at root store
2. local specialized models through Python inheritance
3. model-level semantic metadata
4. document-level semantic tags
5. `gse` to local `se` navigation bridge
6. explicit equivalence-based semantic federation only

## Deferred

- automatic semantic merging
- fuzzy equivalence detection
- ontology reasoning
- implicit model-family inference from prose

## Design Principle

Canonical semantics live at the root, local semantics specialize them through inherited models and document tags, and federated navigation must always be able to descend from global semantic nodes back into store-local semantic views.
