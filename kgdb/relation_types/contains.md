---
name: contains
direction: directed
cardinality: many_to_many
axis: WHERE
source_types:
- python_module
- python_symbol
target_types:
- python_symbol
condition: ''
---

# contains

## Description

A Python module or declaration lexically contains the target declaration. This
is static AST evidence, not a runtime ownership or business relationship.
