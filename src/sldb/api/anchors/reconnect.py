"""Where a symbol went when its name is gone (code-anchoring.md §5): selfdoc's rename heuristic
over per-node fingerprints. Candidates of the same kind, the same file first, then the whole
project; a candidate matches when its body is the same, or its shape and docstring are.
One candidate: reconnected. None or several: lost, with the candidates listed.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.models.code_ref import code_ref


def candidates(root: Path, path: str, kind: str, seen: dict[str, Any], same_file: list[dict] | None) -> list[str]:
    """The refs of the symbols that look like what the anchor saw; the same file's first."""
    here = [_ref(f) for f in (same_file or []) if _matches(f, kind, seen)]
    if here:
        return here
    return [_ref(f) for f in _project_facts(root) if f["path"] != path and _matches(f, kind, seen)]


def _matches(fact: dict, kind: str, seen: dict[str, Any]) -> bool:
    if fact["kind"] != kind or fact["kind"] == "module":
        return False
    now = fact["fingerprints"]
    return now["body"] == seen.get("body") or (now["shape"] == seen.get("shape") and now["docstring"] == seen.get("docstring"))


def _ref(fact: dict) -> str:
    module = fact["id"].split(".")[0] if fact["kind"] == "module" else None
    return code_ref(fact["path"], _qualified(fact)) if module is None else code_ref(fact["path"], "")


def _qualified(fact: dict) -> str:
    """The qualified name with the scanner's `~n` suffix, as the reference form wants it."""
    suffix = fact["id"][len(fact["id"].split("~")[0]):]
    return fact["qualified_name"] + suffix


def _project_facts(root: Path) -> list[dict]:
    from sldb.code.scan import scan_tree

    try:
        return scan_tree(root)
    except (OSError, UnicodeDecodeError):
        return []
