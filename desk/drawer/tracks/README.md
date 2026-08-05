# Drawer Tracks

Deferred execution-lane planning surfaces live here between `features/` and active `tasks/`.

## Role in the drawer

- `features/` = macrotasks
- `tracks/` = grouped promotion lanes that order related features
- `tasks/` = bounded work units suitable for active routing

## What belongs here

A track groups multiple related features when they should be promoted together or in a defined sequence.

Use a track when you need to capture:

- dependency order across features
- promotion sequencing
- grouping for one implementation wave
- shared design gates before task decomposition

## Expected shape

Each track should normally include:

- `Goal`
- `items` listing the participating features
- promotion order inside the track
- open design/decomposition questions before promotion
- references to governing docs/contracts

## Promotion rule

Tracks are not active work by themselves. They exist to turn large feature sets into a clean, staged task promotion plan.

Preferred flow:

`feature -> track -> bounded tasks -> board`
