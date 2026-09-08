from __future__ import annotations

import json
from typing import Any
import yaml

from sldb.cli.store_context import get_store_context
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.query import (
    find_semantic,
    find_structural,
    get_global_semantic,
    get_semantic,
    get_structural,
    glob_semantic,
    glob_structural,
    list_global_semantic,
    list_semantic,
    list_structural,
)
from sldb.core.exceptions import SLDBStoreError


class QueryCLI:
    """Handles store-based queries and exploration."""

    def _resolve_store(self, args: Any) -> Any:
        return get_store_context(args.store)[0]

    def _route(self, args: Any, st_fn: Any, se_fn: Any, gse_fn: Any = None, **kwargs: Any) -> Any:
        store = self._resolve_store(args)
        ref = resolve_model_ref
        p = args.pythonpath
        if args.address.startswith("st"): return st_fn(store, args.address, ref, p, **kwargs)
        if args.address.startswith("gse") and gse_fn: return gse_fn(store, args.address, ref, p, **kwargs)
        if args.address.startswith("se"): return se_fn(store, args.address, ref, p, **kwargs)
        raise SLDBStoreError(f"Bad root: {args.address}")

    def ls(self, args: Any) -> int:
        res = self._route(args, list_structural, list_semantic, list_global_semantic)
        for item in res:
            print(item)
        return 0

    def get(self, args: Any) -> int:
        res = self._route(args, get_structural, get_semantic, get_global_semantic)
        if args.format == "text":
            print(res)
        else:
            payload = {"result": res}
            print(yaml.safe_dump(payload, sort_keys=False) if args.format == "yaml" else json.dumps(payload, indent=2))
        return 0 if res is not None else 1

    def glob(self, args: Any) -> int:
        res = self._route(args, glob_structural, glob_semantic)
        for item in res:
            print(item)
        return 0

    def find(self, args: Any) -> int:
        store, ref, p = self._resolve_store(args), resolve_model_ref, args.pythonpath
        if args.address.startswith("st"): res = find_structural(store, args.address, args.where, ref, p)
        elif args.address.startswith("se"): res = find_semantic(store, args.address, args.where, ref, p)
        else: raise SLDBStoreError(f"Bad root: {args.address}")
        for item in res:
            print(item)
        return 0
