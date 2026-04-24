# Task 02: Store Tree Indexing

## Goal

Implement the first structural store tree under `st` for typed-position navigation.

## Scope

- structural address syntax rooted at `st`
- exact model scope and recursive model scope
- `ls`
- `get`
- `glob`
- minimal typed `find --where`

## Expected Changes

- query/address parser module
- store traversal/resolution logic
- CLI commands for exploration
- tests for address resolution and filtering

## Suggested Milestones

1. define canonical address grammar
2. implement model -> doc -> field resolution
3. implement `ls` and `get`
4. implement `glob`
5. implement minimal typed filtering

## Acceptance Criteria

- model/document/field addresses resolve deterministically
- recursive model expansion works
- exploration commands are scriptable
- filtering works for basic predicates like equality and field existence
