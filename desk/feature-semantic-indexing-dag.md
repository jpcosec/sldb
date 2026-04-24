# Feature: Semantic Indexing With Store-Local DAGs

## Status

- Proposed
- Scope: `.sldb/` semantic indexing layer

## Goal

Add a semantic indexing system parallel to the structural store tree.

This feature introduces:

- `st` as the structural/typed-position index
- `se` as the semantic index
- a per-store semantic DAG
- one or more semantic tags on each document
- tag-to-node mapping from documents into the semantic DAG

## Core Idea

SLDB should support more than one index tree over the same underlying documents.

### Structural Index

`st` indexes by typed position:

- model
- document
- field

Example:

```text
st.{ReadmeDoc}.project-readme.title
```

### Semantic Index

`se` indexes by meaning in context.

Examples:

```text
se.type.documentation.Readme
se.project.sldb.database
se.project.**.database
```

The semantic index is not derived only from model structure. It is built from:

1. a semantic DAG defined by the store
2. one or more tags on each document
3. tag-to-node mappings into that DAG

## Design Principle

Documents are stored once and indexed many ways.

- `st` is canonical structural navigation
- `se` is canonical semantic navigation

## Why A DAG

The semantic layer should be a DAG, not a strict tree.

This allows a semantic concept to have multiple parents.

Examples:

- `Readme` may belong under both documentation and onboarding
- `database` may belong under project scope and infrastructure scope

This means `se` can look tree-like for navigation while supporting shared semantic nodes internally.

## Semantics Are Store-Local

Semantic meaning is contextual.

For that reason:

- each store defines its own semantic DAG
- each store controls its own semantic vocabulary
- federation can later bridge semantic nodes across stores

The initial design should not require a global ontology.

## Document Tags

Documents provide one or more semantic tags.

Example frontmatter:

```yaml
semantic_tags:
  - type.documentation.Readme
  - project.sldb.database
  - role.onboarding
```

These tags are then mapped into the store semantic DAG.

## Semantic DAG Model

Conceptually:

```text
type
  -> documentation
     -> Readme

project
  -> sldb
     -> database

role
  -> onboarding
```

Because the structure is a DAG, a node may appear under multiple parents at the semantic level.

## Query Behavior

### Exact Node

```text
se.type.documentation.Readme
```

Returns all documents indexed at that semantic node.

### Descendant Query

```text
se.project.**.database
```

Returns all documents that map to `database` under any descendant branch of `project`.

### General Browsing

```bash
sldb ls se.type
sldb ls se.project.sldb
sldb glob 'se.project.**.database'
```

## Command Model

The semantic index should support the same explorer-style operations as the structural index where practical.

### List

```bash
sldb ls se.type.documentation
sldb ls se.project
```

Lists child semantic nodes or indexed documents depending on the level.

### Glob

```bash
sldb glob 'se.type.documentation.*'
sldb glob 'se.project.**.database'
```

Matches semantic paths over the DAG projection.

### Get

```bash
sldb get se.type.documentation.Readme
```

Returns the set of matching documents or document addresses.

### Find

```bash
sldb find se.type.documentation.Readme --where 'model = "ReadmeDoc"'
```

Applies typed filtering over the structurally resolved documents returned by the semantic node.

## Relationship To `st`

`st` and `se` are parallel indexes over the same tracked document set.

### `st`

- typed position
- model/document/field navigation
- deterministic structural lookup

### `se`

- semantic placement
- context-sensitive meaning
- DAG-based browsing and wildcard traversal

Examples:

```text
st.{ReadmeDoc}.project-readme.title
se.type.documentation.Readme
se.project.**.database
```

## Mapping Model

Each document may:

- declare multiple semantic tags
- map to multiple semantic nodes
- be reachable from multiple semantic parents through the DAG

This allows one document to be indexed simultaneously as:

- a README
- documentation
- onboarding material
- part of a project
- related to database concerns

## Suggested Store Artifacts

Possible store files:

```text
.sldb/semantic_dag.yaml
.sldb/semantic_index.yaml
```

Illustrative shapes:

```yaml
# .sldb/semantic_dag.yaml
nodes:
  - id: type
  - id: documentation
  - id: Readme
  - id: project
  - id: sldb
  - id: database
edges:
  - from: type
    to: documentation
  - from: documentation
    to: Readme
  - from: project
    to: sldb
  - from: sldb
    to: database
```

```yaml
# .sldb/semantic_index.yaml
tags:
  type.documentation.Readme:
    nodes: [Readme]
  project.sldb.database:
    nodes: [database]
documents:
  project-readme:
    tags:
      - type.documentation.Readme
      - role.onboarding
```

These exact files are illustrative, not final.

## Indexing Rules

- documents are indexed explicitly through declared tags
- tags map to one or more semantic nodes
- queries may expand through ancestor/descendant edges
- no semantic placement should depend only on loose prose inference

## Interaction With Families

Document families can be represented inside `se`.

For example:

```text
se.type.documentation.Readme
se.type.architecture.ADR
se.type.reference.API
```

This means family membership is part of semantic indexing, not a separate ad hoc mechanism.

## MVP

1. store-local semantic DAG definition
2. document semantic tags
3. tag-to-node mapping
4. `ls se...`
5. `glob 'se....'`
6. exact and descendant semantic queries

## Deferred

- federation bridges between semantic DAGs
- semantic ranking/relevance scores
- automatic tag inference from prose
- full ontology or OWL reasoning
- semantic mutation commands beyond basic indexing

## Example Session

```bash
sldb ls se.type.documentation
sldb get se.type.documentation.Readme
sldb glob 'se.project.**.database'
sldb find se.project.**.database --where 'model = "InfraDoc"'
```

## Design Principle

Semantic indexing is composed of a store-local DAG and one or more document tags that map documents into one or more nodes of that DAG.
