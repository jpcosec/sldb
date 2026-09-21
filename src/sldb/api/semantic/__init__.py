"""The semantic DAG as something you can write to: parents beyond the name, and equivalences."""

from sldb.api.semantic.dag_writes import add_semantic_equivalence, add_semantic_parent, remove_semantic_parent
from sldb.api.semantic.dag_reads import semantic_tag

__all__ = ["add_semantic_equivalence", "add_semantic_parent", "remove_semantic_parent", "semantic_tag"]
