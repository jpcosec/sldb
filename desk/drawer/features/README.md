# Drawer Features

Deferred macrotask planning surfaces live here before they are grouped into tracks and later decomposed into promotable active tasks.

## Role in the drawer

- `features/` = large product or architecture work packages
- `tracks/` = grouped execution lanes made from related features
- `tasks/` = bounded planning tasks or later promotable execution units

## What belongs here

A feature file should describe one meaningful product/work package, not one tiny implementation step.

Use a feature when the work needs:

- multiple future tasks
- dependency planning
- scope boundaries
- explicit non-goals
- design gaps listed before promotion

## Expected shape

Each feature should normally include:

- `Goal`
- `Includes`
- `Excludes`
- `Must stay true` when architectural invariants matter
- `Needs design or grounding before promotion`
- `depends_on`
- references to governing docs/atoms/spec2viz

## Promotion rule

Do not promote a raw feature directly to active execution when it is still too large. Prefer:

`feature -> track -> bounded tasks -> board`
