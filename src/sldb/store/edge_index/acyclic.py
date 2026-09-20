"""The relations sldb itself needs to be acyclic, and the check that they are.

`semantic_parent` is the semantic DAG: a cycle makes a tag its own ancestor, so the closure a
semantic query walks never terminates in a defined way. `extends` is model inheritance: a cycle
makes the load order undefined. Both are invariants sldb relies on and neither was ever checked
— per-edge validation cannot see a cycle, only the whole graph can.
"""

from __future__ import annotations

from sldb.store.graph.analysis import cycles

MUST_BE_ACYCLIC = ("semantic_parent", "extends")
"""Relations whose meaning depends on there being no cycle."""


def cycle_errors(index) -> list[str]:
    """One sentence per cyclic relation, naming the cycle; empty when every one is a DAG."""
    found = []
    for relation in MUST_BE_ACYCLIC:
        for cycle in cycles(index, [relation], limit=1):
            found.append(f"Relation '{relation}' has a cycle: {' -> '.join([*cycle, cycle[0]])}.")
    return found
