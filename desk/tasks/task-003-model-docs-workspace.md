# Model the docs workspace with SLDB

ID: task-003
Status: active

## Goal

Create the models needed to use SLDB over the full `docs/` tree and adapt the documentation so the workflow is practical and testable.

## Scope

In scope: all of `docs/`, model selection or creation, document tracking, and documentation updates needed to make the workflow operable. Out of scope: final skill packaging.

## References

- `docs/`
- `README.md`
- `desk/models/`

## Dependencies

- none

## Pills

- pill-001
- pill-002
- pill-003

## Files

- `docs/`
- `README.md`
- `desk/tasks/`
- `desk/contexts/`

## Implementation Path

Partition the `docs/` corpus into workable document families, create the required SLDB models, use the CLI to create or track documents against those models, and capture every ambiguity that should become better project guidance.

## Validation

- validate representative documents against their models
- track or create documents through the CLI
- exercise structural and semantic retrieval over the tracked docs

## Done When

The full `docs/` area can be worked with through SLDB models and CLI operations, and the confusing parts discovered during execution have been written back into the project guidance.

## Tags

- system:sldb
- workspace:docs
- topic:modeling
- topic:documentation
