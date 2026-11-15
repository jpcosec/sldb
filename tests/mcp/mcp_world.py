"""A real store built with the public API: items that depend on each other, a lifecycle of stages
joined by `moves_to` edges, a rule, and a composed view. The MCP tests copy it, serve the copy
and compare what the tools answer with the files of the copy; no expected value is a literal that
restates an answer."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Any

import yaml

from sldb import api

MODULE = "world_models"
ITEM_COUNT = 24
RULE = {"title": "owned", "subject": "model <= Item", "condition": "nonempty(owner)", "severity": "alert", "moment": "on_write", "message": "an item has an owner"}
BOARD = {
    "id": "board", "name": "board", "title": "Board", "params": [{"name": "owner", "default": "ana"}],
    "sections": [{"key": "items", "select": {"model": "Item"}, "fields": ["title", "status", "owner"], "group_by": "status", "group_order": ["open", "review", "done"]}],
}


def front_matter(path: Path) -> dict[str, Any]:
    """The YAML front matter of a Markdown document."""
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} has no front matter"
    return yaml.safe_load(text.split("\n---", 1)[0][4:]) or {}


class World:
    """The store at `root/.sldb`, models importable from `root`."""

    def __init__(self, root: Path) -> None:
        self.root = root
        root.mkdir(parents=True)
        shutil.copy(Path(__file__).with_name(f"{MODULE}.py"), root / f"{MODULE}.py")
        sys.path.insert(0, str(root))
        self.store = api.init_store(root).store_path
        for ref in (f"{MODULE}:Stage", f"{MODULE}:Item", "sldb.models.rule_doc:RuleDoc", "sldb.models.notation_models:ViewDoc"):
            api.add_model(self.store, ref, str(root))
        api.init_relations(self.store, str(root))

    def doc(self, model: str, name: str, payload: dict[str, Any]) -> None:
        api.create_document(self.store, model, self.root / model.lower() / f"{name}.md", payload, name, str(self.root))

    def populate(self) -> None:
        """Three stages and two edges between them, items depending on the one before, a rule and a view."""
        for stage in ("open", "review", "done"):
            self.doc("Stage", stage, {"title": stage})
        self.doc("RelationTypeDoc", "type-moves", {"title": "moves", "name": "moves_to", "source_types": ["Stage"], "target_types": ["Stage"], "cardinality": "many_to_many", "description": "A transition."})
        self.edge("e-review", "Stage:open", "Stage:review")
        self.edge("e-done", "Stage:review", "Stage:done")
        for n in range(ITEM_COUNT):
            status = ("open", "review", "done")[n % 3]
            self.doc("Item", f"i{n}", {"title": f"Item {n}", "status": status, "owner": "" if n % 4 == 1 else "ana", "stage": f"Stage:{status}", "depends_on": [f"Item:i{n - 1}"] if n else []})
        self.doc("RuleDoc", "rule-owned", RULE)
        self.doc("ViewDoc", "board", BOARD)

    def edge(self, name: str, source: str, target: str) -> None:
        self.doc("RelationDoc", name, {"title": name, "source_id": source, "target_id": target, "relation_type": "moves_to", "notes": f"{name} moves an item along its lifecycle."})


def build(root: Path) -> Path:
    """A populated world at `root`; the path of its project root."""
    World(root).populate()
    return root
