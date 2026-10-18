"""Orchestration helpers for the python-* selfdoc commands."""
from __future__ import annotations

import json
from contextlib import redirect_stdout
from pathlib import Path
import sys
from sldb.cli.selfdoc_context import documentation_store
from sldb.cli.selfdoc_inspect import inspect_documents
from sldb.cli.selfdoc_write import write_documents
from sldb.selfdoc.source_graph_file import graph_is_current, write_source_graph
from sldb.selfdoc.python_materialize import plan_python_documents
from sldb.selfdoc.python_relation_registry import (
    registered_source_relations,
    validate_source_snapshot,
)
from sldb.selfdoc.python_scanner import PythonScanner
from sldb.selfdoc.python_source_graph import source_snapshot
from sldb.selfdoc.python_source_scan import metadata_diagnostics, scan_source_facts


def print_python_records(source, root, records) -> None:
    print(json.dumps({"source_root": str(source.relative_to(root)), "symbols": [item.model_dump() for item in records]}, indent=2))


def python_report(plans, graph, graph_output, store, root, output, system):
    report = inspect_documents(plans, store, root, output, system)
    if not graph_is_current(graph, graph_output):
        report.graph_stale.append(str(graph_output.relative_to(root)))
    report.metadata_errors = list(graph["metadata"].get("diagnostics", []))
    return report


def python_graph(args, store, root):
    output = (root / args.graph_output).resolve()
    if not output.is_relative_to(root):
        raise ValueError("The source graph must stay within the store project")
    source = (root / args.source_root).resolve()
    files = scan_source_facts(source, args.package)
    graph = source_snapshot(files, args.system)
    graph["metadata"]["diagnostics"] = metadata_diagnostics(source, files)
    validate_source_snapshot(graph, registered_source_relations(store, root))
    return graph, output


def write_python_graph(graph, output) -> None:
    write_source_graph(graph, output)


def documentation_output(root, output_arg):
    output = (root / output_arg).resolve()
    if not output.is_relative_to(root):
        raise ValueError("Self-documentation output must stay within the store project")
    return output


def write_python_plans(plans, records, args, store, root, output, spec):
    with redirect_stdout(sys.stderr):
        written = write_documents(plans, store, root)
    report = inspect_documents(plan_python_documents(records, args.system, output, spec), store, root, output, args.system)
    report.written = written
    return report


def architecture_spec_path(root, value):
    return (root / value).resolve() if value else None