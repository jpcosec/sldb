from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from sldb.cli.commands.store import StoreCLI
from sldb.cli.store_context import get_store_context
from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.utils import write_text
from sldb.store.export import export_kgdb_semantic_payload
from sldb.store.io import load_store_index
from sldb.store.catalog_reconcile import reconcile_catalog
from sldb.store.resolver import global_store_path


class StoresCLI:
    """Plural store surface for the redesigned CLI."""

    def __init__(self) -> None:
        self._store = StoreCLI()

    def run(self, args: Any) -> int:
        if args.stores_command == "list":
            return self.list(args)
        if args.stores_command == "semantic-export":
            return self.semantic_export(args)
        if args.stores_command == "reconcile":
            return self.reconcile(args)
        args.store_command = args.stores_command
        return self._store.run(args)

    def reconcile(self, args: Any) -> int:
        catalog = Path(args.catalog).resolve() if args.catalog else global_store_path().resolve()
        if not catalog.exists():
            raise ValueError(f"Catalog store does not exist at {catalog}")
        report = reconcile_catalog(catalog, Path(args.path).resolve(), args.apply)
        self._print_reconcile(report, args.format)
        return 0

    def _print_reconcile(self, report: dict, encoding: str) -> None:
        if encoding == "text":
            print(f"discovered={len(report['discovered'])} missing={len(report['missing'])} stale={len(report['stale'])}")
            return
        print(self._format_payload(report, encoding).strip())

    def semantic_export(self, args: Any) -> int:
        sp, root = get_store_context(args.store, mode="readonly")
        payload = export_kgdb_semantic_payload(
            sp, root, resolve_model_ref, args.pythonpath, rebuild=args.rebuild,
            command=["sldb", "stores", "semantic-export", "--format", args.format],
        )
        content = self._format_payload(payload, args.encoding)
        write_text(args.output, content)
        return 0

    def _format_payload(self, payload: Any, encoding: str) -> str:
        if encoding == "json":
            return json.dumps(payload, indent=2) + "\n"
        return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)

    def list(self, args: Any) -> int:
        sp, _root = get_store_context(args.store, mode="readonly")
        idx = load_store_index(sp)
        stores = [{"name": e.name, "path": e.path} for e in sorted(idx.stores, key=lambda i: i.name)]
        payload = {"store": str(sp), "stores": stores}
        
        if args.format in ("json", "yaml"):
            print(self._format_payload(payload, args.format).strip())
            return 0
        
        return self._print_text_list(sp, stores)

    def _print_text_list(self, sp: Any, stores: list[dict[str, str]]) -> int:
        if not stores:
            print(f"No federated stores linked in {sp}")
            return 0
        print(f"Federated stores in {sp}:")
        for item in stores:
            print(f"- {item['name']} -> {item['path']}")
        return 0
