# Section Context Index

**Type:** `pattern`
**Scope:** `component`
**Language:** `en`
**Nature:** `context`
**Bound Tasks:** `task-13`, `task-14`, `task-15`, `task-16`

## Why

The missing capability is not only seeing section headings, but being able to answer what a section is about in a lightweight, operable way.

## What

- Section context must be indexable from the AST.
- The minimum payload is: `path`, `title`, `breadcrumbs`, `about`, `semantic_tags`, `span`.
- `about` is a compact derived vocabulary for search and context; it is not a full ontology.

## Where

- `src/sldb/core/ir.py`
- `src/sldb/cli/graph.py`
- `src/sldb/cli/commands/find.py`

## How

Derive section context from heading hierarchy plus inherited document semantic tags first. Expand only when code/tests show a concrete need.

## Language

- Use `context_index` for the persisted/runtime list.
- Use `about terms` for the search-oriented vocabulary.
- Use `breadcrumbs` for hierarchical section context.

## Scope

This pill is about section discoverability. It does not define section mutation or cross-document reasoning.
