"""Orchestration helpers for the python-* selfdoc commands."""
from __future__ import annotations

import json
from contextlib import redirect_stdout
from pathlib import Path
import sys
from sldb.cli.selfdoc_context import documentation_store
from sldb.cli.selfdoc_inspect import inspect_documents
from sldb.cli.selfdoc_write import write_documents
from sldb.selfdoc.kgdb_sync import graph_is_current, write_kgdb_snapshot
from sldb.selfdoc.python_materialize import plan_python_documents
from sldb.selfdoc.python_relation_registry import (
    registered_source_relations,
    validate_source_snapshot,
)
from sldb.selfdoc.python_scanner import PythonScanner
from sldb.selfdoc.python_source_graph import source_snapshot
from sldb.selfdoc.python_source_scan import scan_source_facts


def print_python_records(source, root, records) -> None:
    print(json.dumps({"source_root": str(source.relative_to(root)), "symbols": [item.model_dump() for item in records]}, indent=2))


def python_report(plans, graph, graph_output, store, root, output, system):
    report = inspect_documents(plans, store, root, output, system)
    if not graph_is_current(graph, graph_output):
        report.kgdb_stale.append(str(graph_output.relative_to(root)))
    return report


def python_graph(args, store, root):
    output = (root / args.kgdb_output).resolve()
    if not output.is_relative_to(root):
        raise ValueError("KGDB output must stay within the store project")
    source = (root / args.source_root).resolve()
    graph = source_snapshot(scan_source_facts(source, args.package), args.system)
    validate_source_snapshot(graph, registered_source_relations(store, root))
    return graph, output


def write_python_graph(graph, output, command) -> None:
    write_kgdb_snapshot(graph, output, command)


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