---
id: pill-015-self-documentation-boundaries
tags: [system:sldb, topic:selfdoc, topic:execution]
---

# Self-documentation execution boundaries

## What

_Define the context or guardrail this pill carries._

The user authorized continuing work in this checkout despite its historical v1 freeze. The first delivery is CLI self-documentation; store federation and AST correctness are separate tasks. Existing unrelated local changes must be preserved.

## Why

_Explain why this context matters for safe execution._

Code owns extracted parser facts. Authored purpose, operating explanations, examples, and tags belong to the documentation author and must survive regeneration. A parser-contract hash detects changes to the executable interface; it must not be described as a hash of every handler's implementation.

## When

_Describe when an agent should apply this pill._

Apply during parser extraction, document synchronization, and the future Python/architecture slices. Re-audit after each delivered slice.

## Where

_Name the files, surfaces, or scope this pill applies to._

The three follow-up task documents, src/sldb/selfdoc, the selfdoc CLI, knowledge/commands, knowledge/surfaces, and the selected project store.

## How

_Describe the correct way to apply this guidance._

Use store-relative destinations and the nearest enclosing store for the new workflow. Do not silently enroll external stores or modify the global registry while implementing self-documentation.

For Python declarations, follow `docs/architecture/code-docstring-indexing.spec.md`: leading docstring metadata owns local identity/classification; selected context tags inherit lexically; the AST supplies structural facts; KGDB owns persisted edges. Do not copy `contains` or `edges` into frontmatter or duplicate source explanations across generated documents. Pilot annotations do not imply that the current scanner implements the convention. Continue through `docs/architecture/code-docstring-indexing-handoff.md` in small batches.

Removed commands are reported for review; their documents are retained. Registration and document writes must validate their payloads and preserve identity. Check is read-only. A repeated sync of unchanged inputs should not rewrite documents.

## How Not

_Describe the shortcut or failure mode to avoid._

Python AST facts and semantic architecture interpretation have separate provenance. Spec2viz is the view generator; clean code improves extraction but cannot substitute for explicit semantic declarations.

Bound to the three tasks created from the September 2026 documentation review. Re-audit after each delivered slice; retire only when the decisions are fully captured by implementation contracts.
