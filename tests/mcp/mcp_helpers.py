"""What the MCP tests share: reading documents through the tools, and the world's own files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mcp_world import front_matter


def page_items(session, tool: str, limit: int = 500, **arguments: Any) -> list[Any]:
    """Every item of a paged answer, following `next_offset`."""
    items: list[Any] = []
    offset: int | None = 0
    while offset is not None:
        answer = session.call(tool, offset=offset, limit=limit, **arguments)
        items += answer["items"]
        offset = answer["next_offset"]
    return items


def one_document(session, path: str) -> dict[str, Any]:
    """The selected row of the document tracked at `path` (relative to the project root)."""
    rows = session.call("select_documents", path_glob=path)["items"]
    assert len(rows) == 1, f"{path}: {rows}"
    return rows[0]


def tracked(session, root: Path, path: Path) -> dict[str, Any]:
    """The document the store tracks at `path` (a file of the world), read in full."""
    return session.call("read_document", ref=one_document(session, str(path.relative_to(root)))["export_id"])


def files(root: Path, folder: str) -> list[Path]:
    """The Markdown documents of one folder of the world."""
    return sorted((root / folder).glob("*.md"))


def an_item(session, root: Path, with_dependency: bool = True) -> dict[str, Any]:
    """The first item (that depends on another, by default), read."""
    return tracked(session, root, next(p for p in files(root, "item") if bool(front_matter(p)["depends_on"]) == with_dependency))


def valid_edge(root: Path, name: str) -> dict[str, Any]:
    """A new edge the world's own `moves_to` type allows: from a stage to another it does not reach yet."""
    declared = front_matter(files(root, "relationtypedoc")[0])
    assert declared["cardinality"] == "many_to_many" and declared["source_types"] == ["Stage"], declared
    taken = {(e["source_id"], e["target_id"]) for e in map(front_matter, files(root, "relationdoc"))}
    source, target = next((s, t) for s in ("Stage:open", "Stage:review") for t in ("Stage:done", "Stage:review") if s != t and (s, t) not in taken)
    return {"action": "assert_edge", "name": name, "source": source, "target": target, "relation_type": declared["name"], "notes": "Asserted by the tests.", "path": f"relationdoc/{name}.md"}
