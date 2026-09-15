---
name: imports
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

# imports

## Description

A Python lexical scope introduces a binding for the target through an import
statement. The edge preserves static import evidence and does not assert use.
