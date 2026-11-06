"""`sldb notations` command handler: list, sync, view, and resolve notations/views."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sldb.api import (
    evaluate_projection_view,
    list_projection_views,
    open_store,
    resolve_documents,
    resolve_view,
    sync_notation,
    sync_palette,
)
from sldb.notations.notation import builtin_notations
from sldb.notations.palette import builtin_palettes


class NotationsCLI:
    """CLI surface for visual notations, palettes, views and diagram resolver."""

    def run(self, args: Any) -> int:
        handler = {
            "list": self._list,
            "sync": self._sync,
            "view": self._view,
            "resolve": self._resolve,
        }[args.notations_command]
        return handler(args)

    def _list(self, args: Any) -> int:
        store_path = args.store or "."
        if args.views:
            views = list_projection_views(store_path, args.pythonpath)
            print(json.dumps(views, indent=2, ensure_ascii=False))
            return 0

        # List notations: builtins + store NotationDocs
        builtins = sorted(builtin_notations())
        store_notations: list[str] = []
        try:
            import sldb.api as api

            docs = api.load_runtime_documents(Path(store_path), args.pythonpath, include_linked=False)
            store_notations = [f"NotationDoc:{d.name}" for d in docs if d.model_name == "NotationDoc"]
        except Exception:
            pass

        result = {
            "builtin_notations": builtins,
            "builtin_palettes": sorted(builtin_palettes()),
            "store_notations": store_notations,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    def _sync(self, args: Any) -> int:
        store_path = args.store or "."
        if not args.notation and not args.palette:
            raise SystemExit("Specify at least --notation <name|path> or --palette <name|path> to sync")

        reports = []
        if args.palette:
            rep = sync_palette(store_path, args.palette, pythonpath=args.pythonpath)
            reports.append(rep.to_dict())
        if args.notation:
            rep = sync_notation(store_path, args.notation, pythonpath=args.pythonpath)
            reports.append(rep.to_dict())

        payload = reports[0] if len(reports) == 1 else {"reports": reports}
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    def _view(self, args: Any) -> int:
        store_path = args.store or "."
        spec = args.spec
        if args.projection:
            result = evaluate_projection_view(store_path, spec, pythonpath=args.pythonpath)
        else:
            result = resolve_view(store_path, spec, pythonpath=args.pythonpath)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    def _resolve(self, args: Any) -> int:
        store_path = args.store or "."
        result = resolve_documents(
            store_path,
            args.notation,
            args.docs,
            relation_refs=args.relations,
            pythonpath=args.pythonpath,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0


__all__ = ["NotationsCLI"]
