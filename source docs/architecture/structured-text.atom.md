# Structured Text

## Related Concepts

- [AST View](ast-view.atom.md)
- [StructuredNLDoc Model](structurednldoc-model.atom.md)
- [Tracked Document](tracked-document.atom.md)

## What It Is

Structured text is human-readable text whose parts have stable boundaries, recognizable roles, and interpretable relationships. In SLDB that includes headings, sections, lists, tables, metadata blocks, links, transclusions, and stronger typed field structures when a document model defines them.

## Why It Matters

Without structure, documents collapse into opaque prose blobs and composition becomes string concatenation. With structure, the same document can stay readable for people while becoming queryable, addressable, and transformable for tools.

## How It Works

Markdown provides visible shape such as hierarchy and blocks. SLDB then treats that shape as machine-operable document structure: it can parse the document into nodes, map fields or sections to stable roles, and use that structure for extraction, validation, search, and composition.

## When It Shows Up

You encounter structured text whenever SLDB renders or extracts a document, shows sections, resolves field ownership, composes tracked docs, or exports graph-ready semantic material.

## Where It Lives

It lives in the authored Markdown documents themselves and in the AST-like structural representation SLDB derives from those documents at runtime.

## Who Uses It

Authors, agents, and downstream tooling use structured text when they need one document to remain readable, authoritative, and also operable as part of a larger knowledge system.
