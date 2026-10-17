# SLDB And Deskops Boundary Proposal

This note captures a useful next architectural step: keep SLDB as the structured Markdown/store infrastructure, and move richer operational workflow behavior into the downstream `deskops` layer.

Important clarification: much of the desk document layer already exists in the wider ecosystem. This proposal is not starting from zero. It is mainly about consolidating, naming, and drawing the boundary more clearly.

## Why Add The Diagrams Now

The repo now has a better onboarding CLI surface, a FAQ, an inbox command, and a clearer distinction between generic document infrastructure and workflow-specific desk behavior.

That is the right moment to make the boundary visible in diagrams instead of only in prose.

## Proposed Split

`sldb` should continue to own:

- `StructuredNLDoc` model contracts
- Markdown extract/render/validate flows
- stores and integrity hashing
- semantic and physical query primitives
- generic document navigation surfaces such as `find`, `sections`, `ast`, and `explore`

`deskops` should own:

- desk workspaces and inbox semantics
- atoms, tasks, pills, and future-work capture
- operator rituals and workflow transitions
- documentation linting and policy enforcement
- inter-repo messaging through tracked desk docs
- operational automations such as commit rituals after closed tasks

## What Already Exists

The ecosystem inventory already defines several desk-oriented document models and discovery surfaces, including:

- `TaskDoc`
- `DeskTaskDoc`
- `PillDoc`
- `DeskBoardDoc`
- `DeskSpecDoc`
- `DeskProfile`

These live under `docs/ecosystem_inventory/models/desk/` in the wider ecosystem checkout and show that the desk surface is already partially implemented as structured documents. <!-- gone -->

So the real gap is less about inventing desk structures and more about:

- consolidating them under a clearer `deskops` identity
- centralizing workflow behavior on top of those docs
- separating generic SLDB infrastructure from desk-specific orchestration
- making inter-repo messaging and ritual automation explicit first-class behavior

## New Diagrams

- `docs/architecture/spec2viz/current-onboarding-surface.yml`
- `docs/architecture/spec2viz/proposed-deskops-components.yml` <!-- gone -->

Rendered Mermaid outputs:

- `docs/architecture/spec2viz/rendered/current-onboarding-surface.mmd`
- `docs/architecture/spec2viz/rendered/proposed-deskops-components.mmd` <!-- gone -->

## Why This Boundary Helps

It keeps SLDB reusable across many repos while allowing `deskops` to be opinionated about operational workflows, desk state, rituals, and cross-repo coordination.

It also reduces the risk that desk-specific behavior slowly hardens into generic SLDB infrastructure.

It also acknowledges the current reality: the ecosystem already has desk documents and models, but the owning runtime and workflow semantics are still dispersed.

## Immediate Design Use

These diagrams should be used when deciding:

- whether `inbox` should remain a thin capture primitive in SLDB or move fully into `deskops`
- how desk docs should be modeled and tracked
- how atoms, tasks, and pills relate to generic SLDB stores
- how cross-repo messages should be materialized and queried
