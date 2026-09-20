from __future__ import annotations

import re
from pathlib import Path

from sldb.store.io import load_semantic_dag
from sldb.store.semantic_dag_graph import reach
from sldb.store.query import load_runtime_documents


def get_global_semantic(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Gets documents across all linked stores for a global semantic tag."""
    return GlobalSemanticEngine.get_global_semantic(store_path, address, resolve_model_ref, pythonpath)

def list_global_semantic(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Lists nodes in the global semantic address space (gse)."""
    return GlobalSemanticEngine.list_global_semantic(store_path, address, resolve_model_ref, pythonpath)

class GlobalSemanticEngine:
    """Engine for processing global semantic queries."""

    @classmethod
    def get_global_semantic(
        cls, store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
    ) -> list[str]:
        """Gets documents across all linked stores for a global semantic tag."""
        docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=True)
        global_tag = address.removeprefix("gse.")
        results = []
        for doc in docs:
            if cls._has_global_tag(doc, global_tag):
                results.append(f"{doc.store_name}:st.{{{doc.model_name}}}.{doc.name}")
        return sorted(results)

    @classmethod
    def _has_global_tag(cls, doc, global_tag: str) -> bool:
        """A document is reachable by its own tags, by what they hang from, and by the global
        tags they are declared equivalent to."""
        dag = load_semantic_dag(doc.store_path)
        local = reach(dag, doc.semantic_tags)
        mapped = set(local if doc.store_name == "local" else [])
        for local_tag in local:
            mapped.update(dag.equivalences.get(local_tag, []))
        return global_tag in mapped

    @classmethod
    def list_global_semantic(
        cls, store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
    ) -> list[str]:
        """Lists nodes in the global semantic address space (gse)."""
        bridge_match = re.fullmatch(r"gse\.(.+)\.se\.\{([^{}]+)\}", address)
        if bridge_match:
            return cls._list_bridge(store_path, bridge_match, resolve_model_ref, pythonpath)
        matches = [
            entry.removeprefix("local:") 
            for entry in cls.get_global_semantic(store_path, address, resolve_model_ref, pythonpath)
        ]
        return matches if matches else []

    @classmethod
    def _list_bridge(cls, store_path: Path, bridge_match, resolve_model_ref, pythonpath: str | None) -> list[str]:
        global_tag, store_name = bridge_match.groups()
        linked_docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=True)
        store_docs = [doc for doc in linked_docs if doc.store_name == store_name]
        if not store_docs:
            return []
        dag = load_semantic_dag(store_docs[0].store_path)
        local_tags = sorted(tag for tag, globals in dag.equivalences.items() if global_tag in globals)
        return [f"se.{tag}" for tag in local_tags]
