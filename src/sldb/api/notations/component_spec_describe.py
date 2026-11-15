"""The envelope and the description of a component spec built from a graph (from `spec2viz.graph_import`)."""

from __future__ import annotations


def _describe(source: str, node_types, models, relations, exclude_relations, drop_isolated, module_prefixes=()) -> str:
    parts = [f"Generado desde {source}", f"node_types={','.join(node_types)}"]
    if models:
        parts.append(f"models={','.join(models)}")
    if module_prefixes:
        parts.append(f"module_prefix={','.join(module_prefixes)}")
    parts.append(f"relations={','.join(relations)}" if relations else f"exclude_relations={','.join(exclude_relations) or '-'}")
    if drop_isolated:
        parts.append("drop_isolated")
    return "; ".join(parts)


def _spec(spec_id: str, title: str, description: str, data: dict) -> dict:
    """El dict de spec `component`, con las claves en el orden de spec2viz."""
    return {
        "id": spec_id,
        "title": title,
        "type": "component",
        "version": "1.0",
        "metadata": {"description": description},
        "data": data,
    }
