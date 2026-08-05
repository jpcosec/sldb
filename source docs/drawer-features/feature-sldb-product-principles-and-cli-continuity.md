# Feature: Product principles and CLI continuity for the SLDB refactor

## Kind

feature

## Status

open

## Core principle

The refactor should preserve the original product principle of SLDB.

This should still be the same kind of tool at heart.

It should remain a system for structured documents, typed models, extraction, rendering, validation, and document-oriented workflows.

The goal is not to replace SLDB with a different product.

The goal is to rebuild its internals on a cleaner and more extensible architecture.

## CLI continuity principle

The CLI should remain functionally equivalent to the current SLDB CLI at the user level.

We should remove accumulated garbage, accidental complexity, duplicated surfaces, and legacy confusion.

But the working mental model of the CLI should remain recognizable.

That means the refactor should aim for:

- continuity of the main command surface
- continuity of the main document/model/store workflows where they still make sense
- removal of unnecessary compatibility clutter
- simplification of internal implementation without changing the core user promise

In short:

- the architecture changes deeply
- the product promise should stay legible
- the CLI should feel like the same tool, only clearer and cleaner

## Materialization must become optional

One important architectural change is that document materialization should no longer be mandatory.

The system should support working against canonical internal structure even when a concrete rendered Markdown document is not materialized yet.

Materialized documents become one projection among others.

This means:

- a document may exist canonically in AST form without being rendered to Markdown yet
- Markdown files remain important, but they are not the only operational existence of a document
- render/materialize becomes an explicit projection step
- internal workflows should be able to act over AST-level documents and nodes directly

## The system must be designed for a future visual UX from the start

The refactor should be designed immediately with a visual editor and visual runtime in mind.

This should not be treated as a future afterthought.

The architecture should assume from the beginning that the system will need its own visual UX.

That UX should eventually support at least:

- structured document editing
- syntax and semantic highlighting
- rich field-aware editing
- link creation and inspection
- transclusion-aware editing
- graph visualization
- model browsing
- template browsing
- node/field inspection
- anchor inspection
- provenance inspection
- hook visibility
- query and graph exploration

## Why this matters

If the architecture is only designed around terminal commands and Markdown files, we will repeat the same trap as the current system.

The new architecture must support both:

- CLI workflows
- visual workflows

without forcing the visual layer to reverse-engineer the runtime from ad hoc textual artifacts.

## Architectural implication

This reinforces several already-discussed decisions.

### 1. Canonical AST is mandatory

A visual system cannot rely on Markdown text as the only source of truth.

It needs a structured canonical model with explicit nodes, fields, links, anchors, and metadata.

### 2. Materialization is a projection, not existence itself

If the future UX must browse and manipulate documents before or beyond Markdown rendering, then Markdown cannot define whether the document exists.

### 3. CLI and UX should sit over the same canonical substrate

The terminal surface and future visual editor should not be separate products with separate truths.

They should be different operating surfaces over the same canonical AST-centered runtime.

### 4. Models and templates must be inspectable first-class entities

The future UX must be able to show:

- models
- field contracts
- templates
- AST nodes
- graph relations
- links
- anchors
- projections

That means those things must be represented explicitly in the architecture, not hidden inside ad hoc Python behavior.

## Product continuity constraints

The refactor must preserve these product-level expectations:

- SLDB still works with structured documents
- typed models still matter
- extraction still matters
- rendering still matters
- validation still matters
- links and composition still matter
- store-like infrastructure may still exist where useful
- CLI workflows remain first-class

But the implementation should evolve so those things rest on a cleaner foundation.

## What should be removed

The refactor should remove or reduce:

- duplicated CLI surfaces
- legacy compatibility clutter kept only for historical reasons
- internal architectural dependence on Markdown as sovereign truth
- accidental coupling between CLI, store, rendering, query, and semantic logic
- hidden logic that cannot be surfaced cleanly in either CLI or future visual tools

## Practical product target

At the product level, the target is this:

- same fundamental SLDB promise
- same recognizable CLI family
- cleaner internal model
- optional materialization
- architecture ready for a dedicated visual editor/runtime

## Open design questions

- Which current CLI commands remain unchanged at the surface, and which are simplified?
- What is the minimum AST/runtime capability needed so a future visual UX can inspect nodes, fields, models, templates, links, and graphs?
- Which parts of the current store should remain user-visible versus becoming purely infrastructural?
- What is the first migration slice that preserves CLI continuity while introducing optional materialization?
