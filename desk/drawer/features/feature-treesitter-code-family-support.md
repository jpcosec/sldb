---
id: feature-treesitter-code-family-support
status: proposed
summary: Define Tree-sitter-backed code-family import, anchoring, selector, and canonicalization support as an authored surface beyond the first Markdown slice.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted to capture the discussed code-family surface explicitly."
references:
- interfaces.md
- libraries_core.md
- desk/atoms/canonical-ast.md
- desk/atoms/selector.md
- desk/atoms/anchor.md
- docs/architecture/spec2viz/target-anchoring.yml
depends_on:
- feature-anchoring-and-selector-stability
- feature-node-identity-and-reconciliation
- feature-multi-family-document-support
---

# Tree-sitter code family support

## Goal

Define the macrotask for Tree-sitter-backed code-family handling as an authored input surface that the kernel canonicalizes without changing authority placement.

## Includes

- code-family import boundary
- syntax/tree locators for anchors and selectors
- canonicalization path from parsed code structure into kernel state
- materialization expectations for code-family outputs where needed

## Excludes

- treating Tree-sitter trees as canonical authority
- unrestricted family sprawl across every parser up front

## Must stay true

- authored code is input, not canonical state
- Tree-sitter is parser/locator infrastructure, not the authority layer
- selector and anchor behavior must stay compatible with canonical identity rules

## Needs design or grounding before promotion

- exact first code families to support
- how Tree-sitter nodes map into canonical nodes and edges
- lossless vs lossy expectations per code family
- fixture corpus for locator and roundtrip stability
