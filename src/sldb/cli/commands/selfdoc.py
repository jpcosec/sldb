"""CLI orchestration for code-derived reference documents."""
from __future__ import annotations

import json
from contextlib import redirect_stdout
from pathlib import Path
import sys
from sldb.cli.selfdoc_context import documentation_store, load_parser
from sldb.cli.selfdoc_inspect import inspect_documents
from sldb.cli.selfdoc_write import write_documents
from sldb.selfdoc.materialize import plan_documents
from sldb.selfdoc.parser import ParserScanner
from sldb.store.resolver import find_local_store
from sldb.selfdoc.python_scanner import PythonScanner
from sldb.selfdoc.python_materialize import plan_python_documents
from sldb.selfdoc.kgdb_sync import graph_is_current, write_kgdb_snapshot
from sldb.selfdoc.python_source_graph import source_snapshot
from sldb.selfdoc.python_source_scan import scan_source_facts
from sldb.selfdoc.python_relation_registry import (
    registered_source_relations,
    validate_source_snapshot,
)


class SelfdocCLI:
    """Scan parser facts, synchronize tracked documents, or check freshness."""

    def run(self, args) -> int:
        """Use JSON stdout; existing lifecycle messages go to stderr."""
        if args.selfdoc_command.startswith("python-"):
            return self._python_operate(args)
        if args.selfdoc_command == "scan":
            return self._scan(args)
        store, root = documentation_store(args.store)
        output = (root / args.output).resolve()
        if not output.is_relative_to(root):
            raise ValueError("Self-documentation output must stay within the store project")
        records = self._records(args, root)
        return self._operate(args, records, store, root, output)

    def _python_operate(self, args) -> int:
        _store, root = documentation_store(args.store)
        source = (root / args.source_root).resolve()
        if not source.is_relative_to(root):
            raise ValueError("Python source root must stay within the store project")
        records = PythonScanner().scan(source, args.package)
        if args.selfdoc_command == "python-scan":
            self._print_python_records(source, root, records)
            return 0
        report = self._sync_python_documents(args, root, records)
        return 0 if report.ok else 1

    def _print_python_records(self, source, root, records) -> None:
        print(json.dumps({"source_root": str(source.relative_to(root)), "symbols": [item.model_dump() for item in records]}, indent=2))

    def _sync_python_documents(self, args, root, records) -> None:
        store, _root = documentation_store(args.store); output = self._documentation_output(root, args.output)
        spec = self._architecture_spec_path(root, args.architecture_spec)
        graph, graph_output = self._python_graph(args, store, root); plans = plan_python_documents(records, args.system, output, spec)
        report = self._python_report(plans, graph, graph_output, store, root, output, args.system)
        if args.selfdoc_command == "python-sync":
            written = self._write_python_plans(plans, records, args, store, root, output, spec)
            self._write_python_graph(graph, graph_output, args.kgdb_command)
            report = self._python_report(plans, graph, graph_output, store, root, output, args.system)
            report.written = written.written
        print(json.dumps({"ok": report.ok, **report.model_dump()}, indent=2)); return report

    def _python_report(self, plans, graph, graph_output, store, root, output, system):
        report = inspect_documents(plans, store, root, output, system)
        if not graph_is_current(graph, graph_output):
            report.kgdb_stale.append(str(graph_output.relative_to(root)))
        return report

    def _python_graph(self, args, store, root):
        output = (root / args.kgdb_output).resolve()
        if not output.is_relative_to(root):
            raise ValueError("KGDB output must stay within the store project")
        source = (root / args.source_root).resolve()
        graph = source_snapshot(scan_source_facts(source, args.package), args.system)
        validate_source_snapshot(graph, registered_source_relations(store, root))
        return graph, output

    def _write_python_graph(self, graph, output, command) -> None: write_kgdb_snapshot(graph, output, command)

    def _documentation_output(self, root, output_arg):
        output = (root / output_arg).resolve()
        if not output.is_relative_to(root): raise ValueError("Self-documentation output must stay within the store project")
        return output

    def _write_python_plans(self, plans, records, args, store, root, output, spec):
        with redirect_stdout(sys.stderr): written = write_documents(plans, store, root)
        report = inspect_documents(plan_python_documents(records, args.system, output, spec), store, root, output, args.system)
        report.written = written
        return report

    def _architecture_spec_path(self, root, value):
        return (root / value).resolve() if value else None

    def _records(self, args, root):
        return ParserScanner(args.include_hidden).scan(load_parser(args.factory, root, args.pythonpath))

    def _scan(self, args):
        local = find_local_store()
        root = documentation_store(args.store)[1] if args.store else (local.parent if local else Path.cwd())
        records = self._records(args, root)
        print(json.dumps({"factory": args.factory, "commands": [r.model_dump() for r in records]}, indent=2))
        return 0

    def _operate(self, args, records, store, root, output):
        plans = plan_documents(records, args.system, args.factory, output)
        report = inspect_documents(plans, store, root, output, args.system)
        if args.selfdoc_command == "sync":
            with redirect_stdout(sys.stderr):
                written = write_documents(plans, store, root)
            plans = plan_documents(records, args.system, args.factory, output)
            report = inspect_documents(plans, store, root, output, args.system)
            report.written = written
        print(json.dumps({"ok": report.ok, **report.model_dump()}, indent=2))
        return 0 if report.ok else 1
