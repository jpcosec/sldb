"""The facts of SQL objects: from a tree-sitter node (table, view, index, column), from a byte span
that pglast located (a key, or a column tree-sitter did not parse), and the `references` relations.

A `constraint` fact hangs from its table (`contained-in`): the table's fact for the keys of a `CREATE
TABLE`; for an `ALTER TABLE ... ADD`, the first table of that name read before it in the file, or the
module when there is none. Its qualified name is `<table>.<constraint name>` (`<table>.pk`, `.fk`,
`.unique` when unnamed), suffixed `~2`, `~3` per name within the table, in source order (`Ids`). A
span fact's signature is its text, whitespace collapsed; `shape` takes its name token out, `body` is
the text after it. The relation `references` goes from a key or a column with `attrs.references` to
the fact of the table whose qualified name is that `table`, before or after it in the same file.
"""

from __future__ import annotations

from typing import Any

from sldb.code.facts import fact, rels
from sldb.code.fingerprints import _sha
from sldb.code.sql_fingerprints import sql_fingerprints
from sldb.code.sql_readers import sql_norm


def sql_fact(node: Any, name: Any, kind: str, qualified: str, doc: str | None, owner: str, ctx: dict[str, Any]) -> dict[str, Any]:
    module, src = ctx["module"], ctx["src"]
    return fact(id=ctx["ids"].take(f"{module}.{qualified}" if module else qualified), kind=kind, name=ctx["name"](name, src).rsplit(".", 1)[-1], qualified_name=qualified,
                path=ctx["rel"], span={"start_line": node.start_point[0] + 1, "end_line": node.end_point[0] + 1}, source_hash=ctx["digest"],
                signature=sql_norm(node, src), doc=doc, relations=rels(owner), attrs={"native_kind": node.type, "module": module},
                fingerprints=sql_fingerprints(node, name, doc, src))


def span_fact(kind: str, name: str, qualified: str, owner: str, span: dict[str, int], native: str, ctx: dict[str, Any]) -> dict[str, Any]:
    module, src = ctx["module"], ctx["src"]
    sig, label, body = (" ".join(src[a:b].decode("utf-8", "replace").split()) for a, b in (
        (span["start"], span["end"]), (span["name_start"], span["name_end"]), (span["name_end"], span["end"])))
    lines = {"start_line": src.count(b"\n", 0, span["start"]) + 1, "end_line": src.count(b"\n", 0, max(span["end"] - 1, span["start"])) + 1}
    return fact(id=ctx["ids"].take(f"{module}.{qualified}" if module else qualified), kind=kind, name=name, qualified_name=qualified, path=ctx["rel"],
                span=lines, source_hash=ctx["digest"], signature=sig, doc=None, relations=rels(owner), attrs={"native_kind": native, "module": module},
                fingerprints={"signature": _sha(sig), "shape": _sha(sig.replace(label, "_", 1)), "docstring": None, "body": _sha(body)})


def link_references(facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Adds `references` from a key or a column to the referenced table's fact (the first of that qualified name in the file), if any."""
    tables = {f["qualified_name"]: f["id"] for f in reversed(facts) if f["kind"] == "table"}
    for f in (f for f in facts if f["kind"] in ("constraint", "column") and f["attrs"].get("references", {}).get("table") in tables):
        f["relations"] = sorted(f["relations"] + [{"type": "references", "target": tables[f["attrs"]["references"]["table"]]}], key=lambda r: (r["type"], r["target"]))
    return facts
