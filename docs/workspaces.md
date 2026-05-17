# Workspace Pattern

SLDB can operate on a repo's own working surfaces, not only on end-user content.

## Three-Layer Architecture

This repo separates concerns across three explicit layers:

- **sldb** — structured document infrastructure (store, CLI, rendering, extraction, models framework, AST). Reusable across projects. Lives in `src/sldb/`.
- **specyaml** — canonical semantic contracts. The specYaml package is the shared semantic source-of-truth. Not owned by this repo.
- **opsys** — workflow-domain instance that lives in a sibling repo and owns `desk/` plus `desk/drawer/`. Includes tasks, pills, rituals, features, atoms, routines, edges, and materializers. Opsys-specific logic belongs there, not in sldb infra.

sldb and specyaml are upstream dependencies. opsys is a downstream consumer that uses sldb infrastructure to run specyaml-governed workflows.

Changes to opsys-owned surfaces should not leak into sldb's generic infrastructure. Conversely, sldb should not embed workflow-specific assumptions.

The pattern in this repo is:

- code explains the `how`
- documentation indexes the code and explains the `why`, `what`, and `when`
- tracked Markdown workspaces make temporary operational state queryable

In the local ecosystem checkout, that downstream layer currently lives in the sibling `../opsys` repo.

## Durable Project Docs: `docs/`

`docs/` is the durable explanatory layer.

- it indexes the codebase and user-facing workflows
- it explains intent, constraints, and operating guidance
- it should not become a duplicate implementation layer

Use `docs/` for stable guidance that should survive beyond one execution cycle.

## Store Discipline

When a workspace is tracked in `.sldb/`:

- use `docs track` or `docs create` to enter the active store
- use `stores update` to rebuild semantic and section indexes after bulk changes
- use `docs untrack` before deleting tracked workspace documents that are intentionally leaving the active surface

Git remains the durable historical record. The store is the current queryable routing layer.
