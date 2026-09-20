"""Which relations an analysis walks.

The edge index mixes two very different things. `has_document`, `has_section`, `has_field` and
the rest of the builtins are **derived**: sldb writes them from the store's own structure, and
they make every document of a model a neighbour of every other one. The rest are **authored**:
somebody wrote a `RelationDoc` saying this implements that.

Running a path search or a centrality over the derived spine answers nothing — every pair of
documents is two hops apart through their model node. So an analysis that is not told which
relations to walk defaults to the authored ones.
"""

from __future__ import annotations

from sldb.models.builtin_relation_types import BUILTIN_RELATION_TYPES

DERIVED: frozenset[str] = frozenset(str(r["name"]) for r in BUILTIN_RELATION_TYPES)
"""The relations sldb derives from the store: the structural spine and the semantic DAG."""

ALL = "*"
"""Ask for this instead of a relation list to walk everything, derived spine included."""


def present(index) -> set[str]:
    """Every relation that actually has an edge in this index."""
    return {e.relation for e in index.edges}


def authored(index) -> set[str]:
    """The relations somebody asserted: what is present, minus what sldb derives."""
    return present(index) - DERIVED


def resolve(index, relations: object = None) -> set[str]:
    """The relations to walk: the ones asked for, else the authored ones, else everything.

    A store with no authored relations yet falls back to all of them, so the analyses say
    something instead of nothing on a store that has only its structure.
    """
    if relations == ALL:
        return present(index)
    if relations is not None:
        return set(relations)
    return authored(index) or present(index)
