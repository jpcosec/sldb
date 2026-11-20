"""`sldb notations from-graph`: a component spec from a snapshot, a store's edge index or a Python tree.

Ported from `spec2viz diagram from-graph` and `spec2viz diagram generate` (python-ast). The YAML
goes to stdout unless `--output`; the findings (alerts) go to stderr, so stdout stays YAML.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

from sldb.api import load_edge_index, load_runtime_documents
from sldb.api.stores.open_store import open_store
from sldb.api.notations import component_spec_from_graph, document_ref, component_spec_from_python, index_graph, load_node_link_graph, write_component_spec
from sldb.api.notations.component_spec_findings import dangling_edges
from sldb.cli.alert_sink import report

_GRAPH_ONLY = ("node_types", "models", "relations", "exclude_relations", "drop_isolated", "label_field", "kind_field", "group_field")


def from_graph(args: Any) -> int:
    """Dispatch `--python` to the code scanner and `--snapshot`/`--store` to the graph compiler."""
    if args.python:
        return _from_python(args)
    try:
        nodes, edges, attrs, source, default_id = _read_graph(args)
        payloads = _read_payloads(args, nodes)
    except Exception as exc:
        print(f"Error reading graph: {exc}", file=sys.stderr)
        return 1
    _report(dangling_edges(nodes, edges))
    return _emit(_compile(args, nodes, edges, attrs, source, args.spec_id or default_id, payloads), args.output)


def _read_graph(args: Any) -> tuple:
    if args.store:
        nodes, edges = index_graph(load_edge_index(args.store))
        return nodes, edges, None, f"store {args.store}", "sldb-graph"
    nodes, edges, attrs = load_node_link_graph(args.snapshot)
    return nodes, edges, attrs, f"file {args.snapshot}", Path(args.snapshot).stem


def _read_payloads(args: Any, nodes: dict) -> dict:
    """Node id -> payload of the local documents, only when a field flag asks and `--store` is given."""
    if not (args.store and (args.label_field or args.kind_field or args.group_field)):
        return {}
    by_ref = {(d.model_name, d.name): d.payload for d in load_runtime_documents(open_store(args.store, mode="readonly").store_path)}
    return {nid: by_ref[ref] for nid, t in nodes.items() if (ref := document_ref(nid, t)) in by_ref}


def _compile(args: Any, nodes: dict, edges: list, attrs: dict | None, source: str, sid: str, payloads: dict) -> dict:
    return component_spec_from_graph(
        nodes, edges, node_types=args.node_types, models=args.models, relations=args.relations,
        exclude_relations=args.exclude_relations or None, drop_isolated=args.drop_isolated,
        spec_id=sid, title=args.title or f"{sid} graph", source=source, attrs=attrs, module_prefixes=args.module_prefixes,
        payloads=payloads, label_field=args.label_field, kind_field=args.kind_field, group_field=args.group_field,
    )


def _from_python(args: Any) -> int:
    if any(getattr(args, name) for name in _GRAPH_ONLY) or len(args.module_prefixes) > 1:
        raise SystemExit("--python takes only --module-prefix (one root package), --id, --title and --output")
    pid = args.spec_id or Path(args.python).resolve().parent.name
    root = args.module_prefixes[0] if args.module_prefixes else None
    spec, findings = component_spec_from_python(args.python, project_id=pid, title=args.title or f"{pid} AST Architecture", root_package=root)
    _report(findings)
    return 1 if spec is None else _emit(spec, args.output)


def _report(findings: list) -> None:
    """Kept for the envelope like any alert, and printed to stderr (stdout carries the YAML)."""
    report(findings, text=False)
    for finding in findings:
        print(finding.line() + (f"\n    fix     : {finding.fix}" if finding.fix else ""), file=sys.stderr)


def _emit(spec: dict, output: str | None) -> int:
    if not output:
        print(yaml.safe_dump(spec, sort_keys=False, allow_unicode=True), end="")
        return 0
    write_component_spec(spec, output)
    print(f"Generated {output} ({len(spec['data']['nodes'])} nodes, {len(spec['data']['edges'])} edges)")
    return 0
