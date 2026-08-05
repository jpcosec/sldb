# ADR: Keep SLDB As The Structured Text Layer And KGDB As The Graph Layer

- Status: Proposed
- Date: 2026-06-19
- Decision Makers: Local architecture discussion in the SLDB repo
- Related Repos: `sldb`, `kgdb`, `deskops`
- Related Topics: structured text, document ASTs, composition, semantic export, knowledge codebases

## Context

The current ecosystem contains at least two conceptually adjacent systems:

- **SLDB**, which operates on structured Markdown/text documents, typed document models, extraction/rendering, local store indexes, and semantic export;
- **KGDB**, which is intended to operate as a higher-level graph-native knowledge system.

As both systems evolve, there is a risk of boundary drift. SLDB could gradually absorb graph-native concerns such as global traversal and inference, or KGDB could start to absorb text-native concerns such as source authorship, document rendering, and structural text validation.

At the same time, a clear user need has emerged:

1. write a unit of knowledge once;
2. keep it in a human-readable document;
3. treat the document as a structured machine-operable artifact;
4. query the document structure;
5. recompose source knowledge into new documents;
6. project the result into a higher-level graph for global reasoning.

That need requires both systems, but with a strict and durable separation of roles.

## Problem

Without an explicit architecture decision, the ecosystem risks several kinds of confusion:

- duplicated functionality between the text layer and graph layer;
- unclear ownership of composition and query features;
- accidental duplication of authored knowledge across documents and graph artifacts;
- over-modeling prose as graph data too early;
- under-modeling graph relationships by leaving too much responsibility inside the text layer;
- difficulty explaining to contributors where a capability belongs.

More specifically, the project needs a principled answer to these questions:

- What is a structured text system supposed to own?
- What is a graph-native system supposed to own?
- What does it mean to treat documents as AST-like objects?
- Where should recomposition of documents happen?
- Where should graph traversal and inference happen?

## Decision

We will treat **SLDB as the structured text substrate** and **KGDB as the graph-native semantic substrate**.

### SLDB owns

SLDB owns the human-authored document layer and its machine-operable structural forms. This includes:

- readable source documents as canonical authored artifacts;
- parsing documents into AST-like structural forms;
- typed document contracts where appropriate;
- extraction and rendering between text and structured payloads;
- structural validation, roundtrip checks, and idempotency concerns;
- field, block, list, section, and template-level textual structure;
- structural and document-local semantic query;
- textual composition and materialized textual outputs;
- store-local indexes and graph-ready semantic export.

### KGDB owns

KGDB owns graph-native persistence and graph-level reasoning over exported knowledge. This includes:

- entity and relation persistence in graph form;
- cross-document and cross-repository links as graph edges;
- graph traversal;
- equivalence and identity resolution beyond local document structure;
- ontology/taxonomy-aware reasoning where applicable;
- inferred and derived relationships that are not explicit textual truth;
- systemic graph analytics and higher-order query.

### Short boundary statement

- **SLDB answers:** “What does this document say, structurally and textually?”
- **KGDB answers:** “What does the ecosystem imply, relationally and globally?”

## Rationale

### 1. Human-readable authorship must remain canonical

The source of truth for many knowledge artifacts should remain a readable document rather than a graph record. This is especially important for specs, notes, decisions, procedures, explanations, and similar artifacts where narrative form matters.

If the graph becomes the authoring center, the system risks losing readability, local editability, and stable textual intent. Therefore authorship should remain rooted in SLDB-managed documents.

### 2. Structured text is not the same as a graph

A structured document has hierarchy, sections, lists, tables, metadata, and typed local roles. That is enough to support AST-like parsing and query, but it does not automatically imply graph-native traversal or inference.

Text structure is tree-biased and presentation-aware. Graph structure is relation-biased and topology-aware. They are complementary forms, not interchangeable ones.

### 3. Query should exist at more than one layer

The ecosystem needs both:

- local structural query over textual units;
- global graph query over relational structures.

If those two layers are conflated, either text queries become needlessly graph-centric or graph queries become constrained by document shape. Keeping the systems separate allows each query style to remain clear and useful.

### 4. Composition belongs primarily to the text layer

The need to recompose knowledge into new documents is fundamentally a textual need. Summaries, reports, packets, checklists, stitched narratives, and materialized handbooks are textual outputs.

KGDB may help discover what should be included, but the responsibility for rendering and composing readable textual artifacts should stay with SLDB.

### 5. Export should be a projection, not a replacement

Graph export should project document structure, semantics, references, and provenance into graph-ready form. It should not erase the distinction between authored text and graph-native interpretation.

This preserves a clean source-to-projection discipline.

## Detailed Consequences

### Consequence A: SLDB should deepen AST-like document operations

Treating documents like ASTs implies that SLDB should continue to invest in:

- stable structural parsing;
- document/section/field/block addressability;
- structural query APIs and CLI surfaces;
- typed and untyped document inspection modes;
- composition over sections, fields, and transclusions;
- provenance-preserving transforms.

This does not require every document to be rigidly typed. It does require a reliable internal representation of document structure.

### Consequence B: Composition should be text-first

SLDB should support composition modes such as:

- direct transclusion;
- render-time composition from referenced child docs;
- summary composition over selected fields;
- sectional composition across multiple docs;
- query-driven composition where selected source fragments become a new textual output.

These are textual materialization capabilities, not graph reasoning capabilities.

### Consequence C: KGDB should not own document authoring behavior

KGDB should not become responsible for:

- Markdown contract design;
- text template rendering;
- roundtrip extraction/render validation;
- deciding how a human-readable section should be written;
- local textual composition semantics.

Those concerns belong to the source-document layer.

### Consequence D: SLDB should not own graph-native reasoning

SLDB should avoid growing into:

- graph-wide ontology inference;
- full multi-hop graph traversal as a first-class truth model;
- graph-native ranking/centrality/analytics as core ownership;
- workflow- or project-specific graph edge semantics beyond its explicit export contract.

Those capabilities belong downstream.

### Consequence E: Provenance must survive the handoff

The export boundary should preserve enough structure that KGDB can trace graph nodes and edges back to:

- source document identity,
- source section or field identity where relevant,
- semantic tags,
- model contract identity,
- and extraction/hash provenance.

That allows KGDB to reason globally without severing the chain back to authored textual truth.

## Alternatives Considered

### Alternative 1: Put both text and graph behavior into SLDB

Rejected.

This would blur the line between document operations and graph operations. It would likely make SLDB too broad, too opinionated, and harder to explain. It would also risk mixing local authored truth with inferred semantic truth.

### Alternative 2: Treat KGDB as the primary source of truth and use SLDB only as a renderer

Rejected.

This would invert the human workflow in the wrong direction. It would undermine the principle that documents should remain canonical authored artifacts and that text should be writable and maintainable on its own terms.

### Alternative 3: Keep both systems loosely defined and decide case by case

Rejected.

That approach invites drift, duplication, and repeated boundary debates. A doctrine-level split is needed so contributors can evaluate new features against a stable frame.

## What This Means For Structured Text

This decision assumes a specific understanding of structured text:

Structured text is human-readable text whose parts have stable boundaries, recognizable roles, and interpretable relationships. Its shape is meaningful enough that the document can be parsed into a machine-usable structural representation without discarding the reasons humans find it readable.

Examples include:

- spec documents with stable semantic sections;
- decision records;
- concept/reference pages;
- operational procedures;
- heterogeneous but still structured pages such as Wikipedia-like entries.

This definition justifies the idea that documents can be AST-like without ceasing to be documents.

## What This Means For Knowledge Codebases

A “knowledge codebase” in this doctrine is a repository where documents behave analogously to source code:

- they are canonical source artifacts;
- they have parseable structure;
- their subunits are addressable;
- they support validation and transformation;
- they can be queried and recomposed;
- they generate derived outputs;
- and they can be projected into graph form for higher-order analysis.

The document layer remains primary for authored truth. The graph layer remains primary for relational truth.

## Interaction With Deskops

`deskops` remains a third, distinct concern.

- SLDB should own generic structured text infrastructure.
- `deskops` should own workflow-domain desk semantics.
- KGDB should own graph-native semantics and analysis.

This ADR therefore reinforces, rather than replaces, the existing effort to keep workflow-specific behavior out of SLDB.

## Implementation Guidance

Future design and implementation work should evaluate proposed features using the following test:

### A feature belongs in SLDB if it primarily concerns:

- document shape;
- textual structure;
- extraction/rendering;
- section/field/block identity;
- textual validation;
- structural query;
- document composition;
- store-local structural semantics;
- graph-ready export.

### A feature belongs in KGDB if it primarily concerns:

- graph persistence;
- entity unification;
- edge modeling beyond explicit textual structure;
- transitive or inferred relations;
- graph-wide query and traversal;
- ontology-aware reasoning;
- systemic graph analysis.

### A feature belongs in deskops if it primarily concerns:

- workflow tasks and rituals;
- inbox and drawer routing;
- cross-project operational coordination;
- active operational surfaces built on top of text infrastructure.

## Risks

Even with this decision, several risks remain:

- contributors may continue to add graph-like semantics to SLDB because the graph need is real and nearby;
- contributors may under-specify the export boundary and make KGDB ingestion brittle;
- addressability and provenance may remain too shallow for useful downstream graph projection;
- composition may stay too narrow if it remains only transclusion-oriented.

These are acceptable risks, but they should be managed consciously.

## Follow-Up Work

Likely follow-up work includes:

1. define a more formal AST/addressability model for SLDB documents;
2. define public query primitives over the document layer;
3. expand composition beyond current transclusion/render-only mechanisms;
4. tighten the semantic export contract with explicit provenance guarantees;
5. document the boundary clearly in architecture docs for contributors.

## Decision Summary

We will preserve a strict architectural separation:

- **SLDB** is the structured textual substrate of the knowledge codebase.
- **KGDB** is the graph-native semantic substrate over exported knowledge.

The text layer owns canonical readable authorship, AST-like structure, structural query, and textual recomposition.
The graph layer owns traversal, equivalence, inference, and system-wide relational reasoning.

This boundary is not merely descriptive. It is the intended operating doctrine for future feature placement.
