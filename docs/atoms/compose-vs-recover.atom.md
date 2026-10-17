# Compose vs Recover

## Related Concepts

- [Tracked Document](tracked-document.atom.md)
- [Store](store.atom.md)
- [AST View](ast-view.atom.md)

## What It Is

`recover` and `compose` are link-oriented commands, not payload extraction commands. `recover` resolves `[[links]]` and reports what they point to. `compose` expands `![[transclusions]]` into a composed Markdown output.

## Why It Matters

The names sound intuitive, but users can easily misread them as data roundtrip commands. They are really about explicit Markdown link and transclusion behavior.

## How It Works

`recover` scans the document for Obsidian-style links, resolves each target through tracked docs or physical paths, and reports unresolved targets. `compose` recursively replaces transclusions with the referenced Markdown body.

## When It Shows Up

You encounter these commands when a tracked or local Markdown document references other documents and you want either a dependency report or a fully materialized composed view.

## Where It Lives

The links live in Markdown content. The resolution logic lives in `src/sldb/links/` and the CLI surfaces it through `docs recover` and `docs compose`.

## Who Uses It

Writers and automation use `recover` to inspect references and `compose` to produce an expanded document for export or review.
