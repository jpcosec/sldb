from __future__ import annotations

import json
from typing import Any

import yaml

from sldb.cli.graph import ast_for_target


SCHEMA = {
    "nodes": [
        "store",
        "linked_store",
        "model",
        "field",
        "document",
        "section",
        "collection_item",
    ],
    "edges": [
        "store->model",
        "model->field",
        "model->document",
        "document->section",
        "section->field",
        "model->semantic_tag",
        "document->semantic_tag",
        "document->physical_anchor",
    ],
    "views": {
        "physical": "documents, tracked paths, sections, nested paths",
        "semantic": "model and document semantic tags",
    },
}


class ASTCLI:
    """Expose the normalized SLDB graph."""

    def run(self, args: Any) -> int:
        if args.ast_command == "schema":
            payload = {"ast": SCHEMA}
        else:
            payload = ast_for_target(
                args.store, args.pythonpath, args.target or "store"
            )
        self._print(payload, args.format)
        return 0

    def _print(self, payload: dict[str, Any], fmt: str) -> None:
        if fmt == "yaml":
            print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
            return
        if fmt == "text":
            print(json.dumps(payload, indent=2))
            return
        print(json.dumps(payload, indent=2))
