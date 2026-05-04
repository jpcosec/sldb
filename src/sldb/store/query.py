from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sldb.runtime.validation import extract_model_data
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_semantic_dag,
    load_semantic_index,
    load_store_index,
)


@dataclass
class RuntimeDocument:
    store_name: str
    store_path: Path
    model_name: str
    model_type: type
    name: str
    path: str
    payload: dict[str, Any]
    semantic_tags: list[str]


def _resolve_path(base: Path, maybe_relative: str) -> Path:
    path = Path(maybe_relative)
    return path if path.is_absolute() else (base / path).resolve()


def _match_semantic_pattern(tag: str, pattern: str) -> bool:
    escaped = re.escape(pattern)
    escaped = escaped.replace(re.escape("**"), ".*")
    escaped = escaped.replace(re.escape("*"), "[^.]+")
    return re.fullmatch(escaped, tag) is not None


def load_runtime_documents(
    store_path: Path,
    resolve_model_ref,
    pythonpath: str | None = None,
    include_linked: bool = False,
) -> list[RuntimeDocument]:
    def _load_one(current_store_path: Path, store_name: str) -> list[RuntimeDocument]:
        project_root = current_store_path.parent
        store_index = load_store_index(current_store_path)
        runtime_docs: list[RuntimeDocument] = []
        for model_entry in store_index.models:
            model_type = resolve_model_ref(model_entry.model_ref, pythonpath)
            models_idx = load_models_index(project_root / model_entry.models_index)
            docs_idx = load_documents_index(project_root / models_idx.documents_index)
            for doc in docs_idx.documents:
                doc_path = project_root / doc.path
                if not doc_path.exists():
                    continue
                payload = extract_model_data(
                    model_type, doc_path.read_text(encoding="utf-8")
                )
                runtime_docs.append(
                    RuntimeDocument(
                        store_name=store_name,
                        store_path=current_store_path,
                        model_name=model_entry.name,
                        model_type=model_type,
                        name=doc.name,
                        path=doc.path,
                        payload=payload,
                        semantic_tags=list(doc.semantic_tags),
                    )
                )
        return runtime_docs

    docs = _load_one(store_path, "local")
    if include_linked:
        store_index = load_store_index(store_path)
        for linked in store_index.stores:
            linked_store = _resolve_path(store_path.parent, linked.path)
            if (linked_store / "store_index.yaml").exists():
                docs.extend(_load_one(linked_store, linked.name))
    return docs


def _model_scope_docs(
    store_path: Path,
    scope: str,
    recursive: bool,
    resolve_model_ref,
    pythonpath: str | None = None,
) -> list[RuntimeDocument]:
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    if scope == "*":
        return docs
    base_doc = next((doc for doc in docs if doc.model_name == scope), None)
    if base_doc is None:
        return []
    if not recursive:
        return [doc for doc in docs if doc.model_name == scope]
    base_type = base_doc.model_type
    return [doc for doc in docs if issubclass(doc.model_type, base_type)]


def list_structural(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None
) -> list[str]:
    if address == "st":
        store_index = load_store_index(store_path)
        return sorted(f"st.{{{entry.name}}}" for entry in store_index.models)

    match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}(?:\.([^.]+))?", address)
    if not match:
        return []
    model_name, recursive_flag, doc_name = match.groups()
    docs = _model_scope_docs(
        store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath
    )
    if doc_name is None:
        return sorted(doc.name for doc in docs)
    target = next((doc for doc in docs if doc.name == doc_name), None)
    if not target:
        return []
        
    results = []
    for key in sorted(target.payload.keys()):
        field = target.model_type.model_fields.get(key)
        description = field.description if field and field.description else ""
        if description:
            results.append(f"{key}: {description}")
        else:
            results.append(key)
    return results


def get_structural(
    store_path: Path, address: str, resolve_model_ref, pythonpath: str | None = None
) -> Any:
    match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}\.([^.]+)(?:\.(.+))?", address)
    if not match:
        return None
    model_name, recursive_flag, doc_name, field_name = match.groups()
    docs = _model_scope_docs(
        store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath
    )
    target = next((doc for doc in docs if doc.name == doc_name), None)
    if target is None:
        return None
    if field_name is None:
        return target.payload
    value: Any = target.payload
    for part in field_name.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return None
    return value


def glob_structural(
    store_path: Path, pattern: str, resolve_model_ref, pythonpath: str | None = None
) -> list[str]:
    match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}\.([^.]+)(?:\.(.+))?", pattern)
    if not match:
        return []
    model_name, recursive_flag, doc_pattern, field_pattern = match.groups()
    docs = _model_scope_docs(
        store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath
    )
    base_scope = f"st.{{{model_name}{'+' if recursive_flag else ''}}}"
    results: list[str] = []
    for doc in docs:
        if not fnmatch.fnmatch(doc.name, doc_pattern):
            continue
        if field_pattern is None:
            results.append(f"{base_scope}.{doc.name}")
            continue
        for field_name in sorted(doc.payload.keys()):
            if fnmatch.fnmatch(field_name, field_pattern):
                results.append(f"{base_scope}.{doc.name}.{field_name}")
    return sorted(results)


def _where_matches(
    doc: RuntimeDocument, expression: str, resolve_model_ref, pythonpath: str | None
) -> bool:
    expression = expression.strip()
    has_match = re.fullmatch(r"has\(([^)]+)\)", expression)
    if has_match:
        return has_match.group(1) in doc.payload and doc.payload[
            has_match.group(1)
        ] not in (None, "")

    contains_match = re.fullmatch(r'"([^"]+)"\s+in\s+([A-Za-z_][\w]*)', expression)
    if contains_match:
        needle, field = contains_match.groups()
        value = doc.payload.get(field)
        if isinstance(value, list):
            return needle in value
        if isinstance(value, str):
            return needle in value
        return False

    regex_match = re.fullmatch(r'([A-Za-z_][\w]*)\s*~\s*"([^"]+)"', expression)
    if regex_match:
        field, pattern = regex_match.groups()
        target = doc.name if field == "doc" else str(doc.payload.get(field, ""))
        return re.search(pattern, target) is not None

    model_match = re.fullmatch(r"model\s*<=\s*([A-Za-z_][\w]*)", expression)
    if model_match:
        base_name = model_match.group(1)
        base_type = resolve_model_ref(
            f"{doc.model_type.__module__}:{base_name}", pythonpath
        )
        return issubclass(doc.model_type, base_type)

    compare_match = re.fullmatch(
        r'([A-Za-z_][\w]*)\s*(=|!=|>=|<=)\s*("[^"]+"|\d+(?:\.\d+)?)', expression
    )
    if compare_match:
        field, op, raw_value = compare_match.groups()
        value = doc.payload.get(field)
        expected: Any = (
            raw_value[1:-1] if raw_value.startswith('"') else float(raw_value)
        )
        if isinstance(value, (int, float)) and isinstance(expected, float):
            pass
        elif op in {">=", "<="}:
            return False
        if op == "=":
            return value == expected
        if op == "!=":
            return value != expected
        if op == ">=":
            return value >= expected
        if op == "<=":
            return value <= expected
    return False


def find_structural(
    store_path: Path,
    address: str,
    where: str,
    resolve_model_ref,
    pythonpath: str | None = None,
) -> list[str]:
    match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}", address)
    if not match:
        return []
    model_name, recursive_flag = match.groups()
    docs = _model_scope_docs(
        store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath
    )
    base_scope = f"st.{{{model_name}{'+' if recursive_flag else ''}}}"
    return sorted(
        f"{base_scope}.{doc.name}"
        for doc in docs
        if _where_matches(doc, where, resolve_model_ref, pythonpath)
    )


def _semantic_children(tags: list[str], prefix: str) -> list[str]:
    children = set()
    prefix_dot = f"{prefix}." if prefix else ""
    for tag in tags:
        if not tag.startswith(prefix_dot):
            continue
        remainder = tag[len(prefix_dot) :]
        if not remainder or "." not in remainder:
            continue
        children.add(remainder.split(".", 1)[0])
    return sorted(children)


def _local_semantic_docs(
    store_path: Path, resolve_model_ref, pythonpath: str | None = None
) -> tuple[list[RuntimeDocument], Any]:
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    semantic_index = load_semantic_index(store_path)
    if not semantic_index.documents:
        from sldb.store.semantic import rebuild_semantic_indexes

        rebuild_semantic_indexes(
            store_path, store_path.parent, resolve_model_ref, pythonpath
        )
        semantic_index = load_semantic_index(store_path)
    return docs, semantic_index


def list_semantic(
    store_path: Path,
    address: str,
    resolve_model_ref,
    pythonpath: str | None = None,
) -> list[str]:
    docs, semantic_index = _local_semantic_docs(
        store_path, resolve_model_ref, pythonpath
    )
    tags = sorted(semantic_index.tags.keys())
    if address == "se":
        return _semantic_children(tags, "")
    prefix = address.removeprefix("se.")
    children = _semantic_children(tags, prefix)
    if children:
        return children
    return sorted(doc.name for doc in docs if prefix in doc.semantic_tags)


def get_semantic(
    store_path: Path,
    address: str,
    resolve_model_ref,
    pythonpath: str | None = None,
) -> list[str]:
    docs, _ = _local_semantic_docs(store_path, resolve_model_ref, pythonpath)
    tag = address.removeprefix("se.")
    return sorted(
        f"st.{{{doc.model_name}}}.{doc.name}"
        for doc in docs
        if tag in doc.semantic_tags
    )


def glob_semantic(
    store_path: Path,
    pattern: str,
    resolve_model_ref,
    pythonpath: str | None = None,
) -> list[str]:
    _, semantic_index = _local_semantic_docs(store_path, resolve_model_ref, pythonpath)
    semantic_pattern = pattern.removeprefix("se.")
    return sorted(
        f"se.{tag}"
        for tag in semantic_index.tags.keys()
        if _match_semantic_pattern(tag, semantic_pattern)
    )


def find_semantic(
    store_path: Path,
    address: str,
    where: str,
    resolve_model_ref,
    pythonpath: str | None = None,
) -> list[str]:
    docs, _ = _local_semantic_docs(store_path, resolve_model_ref, pythonpath)
    semantic_pattern = address.removeprefix("se.")
    matching = [
        doc
        for doc in docs
        if any(
            _match_semantic_pattern(tag, semantic_pattern) for tag in doc.semantic_tags
        )
    ]
    return sorted(
        f"st.{{{doc.model_name}}}.{doc.name}"
        for doc in matching
        if _where_matches(doc, where, resolve_model_ref, pythonpath)
    )


def get_global_semantic(
    store_path: Path,
    address: str,
    resolve_model_ref,
    pythonpath: str | None = None,
) -> list[str]:
    docs = load_runtime_documents(
        store_path, resolve_model_ref, pythonpath, include_linked=True
    )
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
    store_path: Path,
    address: str,
    resolve_model_ref,
    pythonpath: str | None = None,
) -> list[str]:
    bridge_match = re.fullmatch(r"gse\.(.+)\.se\.\{([^{}]+)\}", address)
    if bridge_match:
        global_tag, store_name = bridge_match.groups()
        linked_docs = load_runtime_documents(
            store_path, resolve_model_ref, pythonpath, include_linked=True
        )
        store_docs = [doc for doc in linked_docs if doc.store_name == store_name]
        if not store_docs:
            return []
        dag = load_semantic_dag(store_docs[0].store_path)
        local_tags = sorted(
            local_tag
            for local_tag, global_tags in dag.equivalences.items()
            if global_tag in global_tags
        )
        return [f"se.{tag}" for tag in local_tags]

    matches = [
        entry.removeprefix("local:")
        for entry in get_global_semantic(
            store_path, address, resolve_model_ref, pythonpath
        )
    ]
    if matches:
        return matches
    return []
