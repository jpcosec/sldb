"""Assemble and write the component spec of a Python tree (migrated from `spec2viz.generators.python_ast`)."""

from __future__ import annotations

from pathlib import Path

import yaml


def _sanitize_id(module_path: str) -> str:
    """Convert a dotted module path to a safe node identifier."""
    return module_path.replace(".", "_").replace("-", "_")


def _build_spec(project_id: str, title: str, elements: list[dict], relations: list[dict]) -> dict:
    """Assemble the final spec2viz YAML structure."""
    seen_ids = {el["id"] for el in elements}
    _register_missing_nodes(elements, relations, seen_ids)
    nodes = {}
    for el in elements:
        nodes[el["id"]] = {"label": el["label"], "kind": el["kind"]}
    edges = [{"from": r["source"], "to": r["target"], "relation": r["kind"]} for r in relations]
    return {"id": project_id, "title": title, "type": "component", "version": "1.0", "data": {"nodes": nodes, "edges": edges}}


def _register_missing_nodes(elements: list[dict], relations: list[dict], seen_ids: set[str]) -> None:
    """Auto-register nodes referenced in edges but not yet declared."""
    for rel in relations:
        target = rel["target"]
        if target not in seen_ids:
            label = target.split("_")[-1]
            elements.append({"id": target, "kind": "external", "label": label})
            seen_ids.add(target)


def write_component_spec(spec: dict, output_path: str | Path) -> None:
    """Write a component spec dict to a YAML file (spec2viz's `write_spec`)."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(spec, f, sort_keys=False, allow_unicode=True)
