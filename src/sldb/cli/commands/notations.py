"""`sldb notations` command handler: list, sync, view, and resolve notations/views."""

from __future__ import annotations

import json
from typing import Any

from sldb.api import (
    evaluate_projection_view,
    list_projection_views,
    resolve_documents,
    resolve_view,
    sync_notation,
    sync_palette,
)
from sldb.api.notations.notation_listing import list_notations


class NotationsCLI:
    """CLI surface for visual notations, palettes, views and diagram resolver."""

    def run(self, args: Any) -> int:
        """Dispatch to the handler of `args.notations_command`."""
        handler = {"list": self._list, "sync": self._sync, "view": self._view, "resolve": self._resolve}
        return handler[args.notations_command](args)

    def _dump(self, payload: Any) -> int:
        """Print the payload as JSON; returns the exit code."""
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    def _list(self, args: Any) -> int:
        store_path = args.store or "."
        if args.views:
            return self._dump(list_projection_views(store_path, args.pythonpath))
        return self._dump(list_notations(store_path, args.pythonpath))

    def _sync(self, args: Any) -> int:
        store_path = args.store or "."
        if not args.notation and not args.palette:
            raise SystemExit("Specify at least --notation <name|path> or --palette <name|path> to sync")
        reports = []
        if args.palette:
            reports.append(sync_palette(store_path, args.palette, pythonpath=args.pythonpath).to_dict())
        if args.notation:
            reports.append(sync_notation(store_path, args.notation, pythonpath=args.pythonpath).to_dict())
        return self._dump(reports[0] if len(reports) == 1 else {"reports": reports})

    def _view(self, args: Any) -> int:
        store_path = args.store or "."
        resolver = evaluate_projection_view if args.projection else resolve_view
        return self._dump(resolver(store_path, args.spec, pythonpath=args.pythonpath))

    def _resolve(self, args: Any) -> int:
        store_path = args.store or "."
        result = resolve_documents(store_path, args.notation, args.docs, relation_refs=args.relations, pythonpath=args.pythonpath)
        return self._dump(result)


__all__ = ["NotationsCLI"]
