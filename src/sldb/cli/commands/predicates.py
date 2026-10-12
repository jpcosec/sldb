from __future__ import annotations

import json
from typing import Any

import yaml

from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index, save_store_index
from sldb.cli.commands.predicates_file import export_command, sync_command
from sldb.store.models import PredicateEntry
from sldb.store.predicates import validate_predicate, validate_predicates

class PredicatesCLI:
    """Manage store-backed predicate definitions used by document links."""

    def run(self, args: Any) -> int:
        cmds = {"add": self.add, "list": self.list, "show": self.show, "validate": self.validate, "remove": self.remove, "sync": sync_command, "export": export_command}
        if args.predicates_command not in cmds:
            raise SLDBStoreError(f"Unknown command: {args.predicates_command}")
        return cmds[args.predicates_command](args)

    def _ctx(self, args: Any, readonly: bool = False) -> tuple[Any, Any]:
        sp, _ = get_store_context(args.store, mode="readonly" if readonly else "")
        return sp, load_store_index(sp)

    def _fmt(self, data: Any, fmt: str) -> bool:
        if fmt not in ("json", "yaml"): return False
        print(json.dumps(data, indent=2) if fmt == "json" else yaml.safe_dump(data, sort_keys=False))
        return True

    def add(self, args: Any) -> int:
        sp, idx = self._ctx(args)
        if any(e.name == args.name for e in idx.predicates):
            raise SLDBStoreError(f"Predicate '{args.name}' already exists.")
        entry = PredicateEntry(name=args.name, axis=args.axis.upper(), description=args.description or "")
        errs = validate_predicate(entry)
        if errs: raise SLDBStoreError(" ".join(errs))
        idx.predicates.append(entry)
        save_store_index(sp, idx)
        print(f"Registered predicate '{entry.name}'")
        return 0

    def list(self, args: Any) -> int:
        sp, idx = self._ctx(args, True)
        entries = [e.model_dump() for e in sorted(idx.predicates, key=lambda i: i.name)]
        if self._fmt({"store": str(sp), "predicates": entries}, args.format): return 0
        if not entries:
            print(f"No predicates registered in {sp}")
            return 0
        print(f"Predicates in {sp}:")
        for e in entries: print(f"- {e['name']} | {e['axis']} | {e['description']}")
        return 0

    def show(self, args: Any) -> int:
        _, idx = self._ctx(args, True)
        entry = next((e for e in idx.predicates if e.name == args.name), None)
        if not entry: raise SLDBStoreError(f"Predicate '{args.name}' is not registered.")
        if self._fmt(entry.model_dump(), args.format): return 0
        print(f"{entry.name} | {entry.axis} | {entry.description}")
        return 0

    def validate(self, args: Any) -> int:
        _, idx = self._ctx(args, True)
        entries = [e for e in idx.predicates if e.name == args.name] if args.name else idx.predicates
        if args.name and not entries: raise SLDBStoreError(f"Predicate '{args.name}' is not registered.")
        errs = validate_predicates(entries)
        if self._fmt({"valid": not errs, "errors": errs}, args.format): return 0 if not errs else 1
        print("PASS: predicates valid" if not errs else "FAIL: predicates invalid")
        for err in errs: print(f"- {err}")
        return 0 if not errs else 1

    def remove(self, args: Any) -> int:
        sp, idx = self._ctx(args)
        rem = [e for e in idx.predicates if e.name != args.name]
        if len(rem) == len(idx.predicates): raise SLDBStoreError(f"Predicate '{args.name}' is not registered.")
        idx.predicates = rem
        save_store_index(sp, idx)
        print(f"Removed predicate '{args.name}'")
        return 0
