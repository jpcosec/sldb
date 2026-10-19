# SLDB Desk Surface Spec

## Product Goal

Provide a minimal but credible local desk surface for the SLDB repo so current work, decisions, local drawer notes, and future workflow boundaries can be represented as structured Markdown and queried through the store.

## Real Use Case

When the repo evolves through multiple documentation, CLI, and architecture slices, contributors need a local operational layer that records what was done, why it was done, what remains open, and which parts should eventually move into `deskops`.

## Minimal Feature Slice To Deliver

- un board (desk/tasks/Board.md)
- tasks del desk local
- pills de contexto (desk/contexts/)
- átomos de conocimiento (desk/atoms/)
- rituales y grafo del ciclo de vida (desk/rituals/, desk/lifecycle/)
- issues del repo (desk/issues/)
- un doc de standards y un doc de spec
- el drawer para trabajo diferido
- el inbox para mensajes entre repos, ruteados por deskops
- el registry de repos de la suite

## What Is Currently Missing

El ciclo de vida de las tasks, el closeout con sus evidencias, el cierre de issues, el ruteo de mensajes entre repos y el retiro de documentos del desk los opera deskops (desk/lifecycle/, desk/rituals/). Lo que sigue manual en este desk: editar issues (deskops no tiene verbo para eso) y las tasks del drawer en formato viejo, sin frontmatter.

## Non-Goals For This Delivery

- implementar deskops dentro de sldb
- implementar en sldb la semántica de ruteo entre repos
- rituales de commit automáticos dentro de sldb (los commits de cierre los hace deskops)

## Acceptance Criteria

The local desk surfaces exist as structured documents, validate against local models, and are tracked in the store so they can be queried as part of the repo's normal documentation workspace.
