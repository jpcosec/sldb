# Workspace Pattern

SLDB can operate on a repo's own working surfaces, not only on end-user content.

The pattern in this repo is:

- code explains the `how`
- documentation indexes the code and explains the `why`, `what`, and `when`
- tracked Markdown workspaces make temporary operational state queryable

## Active Execution: `desk/`

`desk/` is the active execution workspace.

- task docs define the current unit of work
- pill docs capture temporary execution context
- ritual docs define execution, testing, and closeout policy
- the board routes the active set

Use `desk/` when implementation is happening now.

## Deferred Work: `drawer/`

`drawer/` is the deferred-work workspace.

- ideas live there before they become active execution
- future features and backlog plans stay out of the active board
- work is promoted into `desk/` before implementation starts

Use `drawer/` when the work should be kept but not executed yet.

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
