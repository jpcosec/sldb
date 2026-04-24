# Task 03: Semantic Indexing DAG

## Goal

Implement the first semantic indexing system under `se`, backed by a store-local DAG and document semantic tags.

## Scope

- semantic DAG definition per store
- document semantic tags
- tag-to-node mapping
- semantic browsing with `se`
- exact and descendant semantic queries

## Expected Changes

- semantic DAG store files
- tag extraction or loading strategy
- semantic index materialization logic
- CLI support for `ls/get/glob/find` over `se`
- tests for DAG traversal and tag mapping

## Suggested Milestones

1. define semantic DAG file format
2. define document semantic tag format
3. implement tag-to-node indexing
4. expose semantic namespace queries
5. add descendant traversal and tests

## Acceptance Criteria

- documents can map to multiple semantic nodes
- `se.type.documentation.Readme` style queries work
- descendant patterns like `se.project.**.database` work
- semantic indexing remains store-local by default
