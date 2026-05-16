from __future__ import annotations

import re
from pathlib import Path

from sldb.store.io import load_semantic_dag
from sldb.store.query import load_runtime_documents


def get_global_semantic(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Gets documents across all linked stores for a global semantic tag."""
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=True)
    global_tag = address.removeprefix("gse.")
    results = []
    for doc in docs:
        dag = load_semantic_dag(doc.store_path)
        mapped_tags = set(doc.semantic_tags if doc.store_name == "local" else [])
        for local_tag in doc.semantic_tags:
            mapped_tags.update(dag.equivalences.get(local_tag, []))
        if global_tag in mapped_tags:
            results.append(f"{doc.store_name}:st.{{{doc.model_name}}}.{doc.name}")
    return sorted(results)


def list_global_semantic(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Lists nodes in the global semantic address space (gse)."""
    bridge_match = re.fullmatch(r"gse\.(.+)\.se\.\{([^{}]+)\}", address)
    if bridge_match:
        global_tag, store_name = bridge_match.groups()
        linked_docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=True)
        store_docs = [doc for doc in linked_docs if doc.store_name == store_name]
        if not store_docs:
            return []
        dag = load_semantic_dag(store_docs[0].store_path)
        local_tags = sorted(tag for tag, globals in dag.equivalences.items() if global_tag in globals)
        return [f"se.{tag}" for tag in local_tags]

    matches = [entry.removeprefix("local:") for entry in get_global_semantic(store_path, address, resolve_model_ref, pythonpath)]
    return matches if matches else []
