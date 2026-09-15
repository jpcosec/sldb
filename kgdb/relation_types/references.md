---
name: references
direction: directed
cardinality: many_to_many
axis: WHAT
source_types:
- python_module
- python_symbol
target_types:
- python_module
- python_symbol
- python_external
condition: ''
---

# references

## Description

A Python declaration statically references the target at an annotation site.
This is neither a runtime call nor a general business dependency.
