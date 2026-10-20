"""The fact one definition or module becomes (kimun's protocol-1 symbols schema, plus `fingerprints`)."""

from __future__ import annotations

from typing import Any


def fact(**kw: Any) -> dict[str, Any]:
    base: dict[str, Any] = {"id": None, "kind": None, "name": None, "qualified_name": None, "path": None, "span": None,
                            "source_hash": None, "signature": None, "synopsis": None, "doc": None, "relations": [], "attrs": {}, "fingerprints": {}}
    base.update(kw)
    return base


def rels(owner: str | None, imports: Any = ()) -> list[dict[str, str]]:
    r = [{"type": "imports", "target": t} for t in sorted(imports)]
    if owner is not None:
        r.append({"type": "contained-in", "target": owner})
    return sorted(r, key=lambda x: (x["type"], x["target"]))


def key_of(node: Any) -> tuple[int, int, str]:
    """A node's identity within one file: its byte span and type."""
    return (node.start_byte, node.end_byte, node.type)
