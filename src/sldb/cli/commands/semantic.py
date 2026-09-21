"""`sldb semantic` handlers: thin printing wrappers over `sldb.api.semantic`."""

from __future__ import annotations

import json
from typing import Any

from sldb.api.semantic import add_semantic_equivalence, add_semantic_parent, remove_semantic_parent, semantic_tag
from sldb.core.exceptions import SLDBStoreError


class SemanticCLI:
    """Write and read the semantic DAG."""

    def run(self, args: Any) -> int:
        handlers = {"parent": self._parent, "equivalent": self._equivalent, "show": self._show}
        try:
            return handlers[args.semantic_command](args)
        except SLDBStoreError as refused:
            print(str(refused))
            return 1

    def _parent(self, args: Any) -> int:
        write = add_semantic_parent if args.parent_command == "add" else remove_semantic_parent
        changed = write(args.store, args.tag, args.parent, args.actor)
        verb = "is now" if args.parent_command == "add" else "is no longer"
        print(f"{args.tag} {verb} a kind of {args.parent}." if changed else "Nothing to change.")
        return 0

    def _equivalent(self, args: Any) -> int:
        changed = add_semantic_equivalence(args.store, args.local, args.global_tag, args.actor)
        print(f"{args.local} now means {args.global_tag} across linked stores." if changed else "Nothing to change.")
        return 0

    def _show(self, args: Any) -> int:
        print(json.dumps(semantic_tag(args.store, args.tag), indent=2, ensure_ascii=False))
        return 0
