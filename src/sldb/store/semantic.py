from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from sldb.runtime.validation import extract_model_data
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_semantic_dag,
    load_store_index,
    save_documents_index,
    save_semantic_dag,
    save_semantic_index,
)
from sldb.store.models import (
    SemanticDAG,
    SemanticDocumentRecord,
    SemanticIndex,
    SemanticNode,
)


def flatten_model_semantics(model_type: type) -> list[str]:
    semantics = getattr(model_type, "__semantics__", {}) or {}
    tags: list[str] = []
    for key, value in semantics.items():
        if isinstance(value, str):
            tags.append(f"{key}.{value}")
        elif isinstance(value, (list, tuple)):
            if value:
                tags.append(".".join([key, *[str(part) for part in value]]))
        elif isinstance(value, dict):
            for child_key, child_value in value.items():
                if isinstance(child_value, (list, tuple)):
                    tags.append(
                        ".".join([key, child_key, *[str(part) for part in child_value]])
                    )
                else:
                    tags.append(f"{key}.{child_key}.{child_value}")
    return sorted(set(tag for tag in tags if tag))


def collect_document_semantic_tags(model_type: type, payload: dict) -> list[str]:
    tags = set(flatten_model_semantics(model_type))
    payload_tags = payload.get("semantic_tags") or []
    if isinstance(payload_tags, list):
        for tag in payload_tags:
            if isinstance(tag, str) and tag.strip():
                tags.add(tag.strip())
    return sorted(tags)


def _prefix_edges(tag: str) -> list[tuple[str, str]]:
    parts = [part for part in tag.split(".") if part]
    edges: list[tuple[str, str]] = []
    for index in range(1, len(parts)):
        parent = ".".join(parts[:index])
        child = ".".join(parts[: index + 1])
        edges.append((parent, child))
    return edges


def rebuild_semantic_indexes(
    store_path: Path,
    project_root: Path,
    resolve_model_ref,
    pythonpath: str | None = None,
) -> None:
    store_index = load_store_index(store_path)
    existing_dag = load_semantic_dag(store_path)
    documents: dict[str, SemanticDocumentRecord] = {}
    tags_to_docs: dict[str, list[str]] = defaultdict(list)
    parents_by_node: dict[str, set[str]] = defaultdict(set)

    for model_entry in store_index.models:
        model_type = resolve_model_ref(model_entry.model_ref, pythonpath)
        models_idx = load_models_index(project_root / model_entry.models_index)
        docs_idx = load_documents_index(project_root / models_idx.documents_index)

        for doc in docs_idx.documents:
            doc_path = project_root / doc.path
            if not doc_path.exists():
                continue
            try:
                payload = extract_model_data(
                    model_type, doc_path.read_text(encoding="utf-8")
                )
            except Exception:
                payload = {}
            semantic_tags = collect_document_semantic_tags(model_type, payload)
            doc.semantic_tags = semantic_tags
            documents[doc.name] = SemanticDocumentRecord(
                model=model_entry.name,
                path=doc.path,
                tags=semantic_tags,
            )
            for tag in semantic_tags:
                tags_to_docs[tag].append(doc.name)
                for parent, child in _prefix_edges(tag):
                    parents_by_node[child].add(parent)
                    parents_by_node.setdefault(parent, set())

        save_documents_index(project_root / models_idx.documents_index, docs_idx)

    for child, parents in existing_dag.equivalences.items():
        parents_by_node.setdefault(child, set())
        for parent in parents:
            parents_by_node[child].add(parent)
            parents_by_node.setdefault(parent, set())

    dag = SemanticDAG(
        nodes=[
            SemanticNode(id=node_id, parents=sorted(parents))
            for node_id, parents in sorted(parents_by_node.items())
        ],
        equivalences=existing_dag.equivalences,
    )
    semantic_index = SemanticIndex(
        tags={
            tag: sorted(doc_names) for tag, doc_names in sorted(tags_to_docs.items())
        },
        documents=documents,
    )
    save_semantic_dag(store_path, dag)
    save_semantic_index(store_path, semantic_index)


def add_semantic_equivalence(store_path: Path, local_tag: str, global_tag: str) -> None:
    dag = load_semantic_dag(store_path)
    mapped = set(dag.equivalences.get(local_tag, []))
    mapped.add(global_tag)
    dag.equivalences[local_tag] = sorted(mapped)
    save_semantic_dag(store_path, dag)
