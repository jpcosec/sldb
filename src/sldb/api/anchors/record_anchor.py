"""What a symbol looks like now: the `code` block an anchor keeps (code-anchoring.md §2)."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from sldb.models.code_ref import code_ref, parse_code_ref
from sldb.code.fingerprints import NORMALIZATION

SCANNER = "treesitter-symbols/1"


def record_anchor(root: Path, ref: str) -> dict[str, Any]:
    """`{ref, kind, seen, normalization, recorded_with}` of the symbol `ref` names under `root`.

    Raises:
        ValueError: The reference is malformed, the file is missing or does not parse, or the
            symbol is not in it (the message names which).
        TreeSitterUnavailable: The `[code]` extra is not installed.
    """
    parsed = parse_code_ref(ref)
    if parsed is None:
        raise ValueError(f"invalid code reference: {ref!r} (expected code:<path>::<qualified_name>)")
    path, name = parsed
    found = symbol_of(root, path, name)
    if found is None:
        raise ValueError(f"no symbol {name!r} in {path} (or the file is missing)")
    return {"ref": code_ref(path, name), "kind": found["kind"], "seen": dict(found["fingerprints"]), "normalization": NORMALIZATION, "recorded_with": recorded_with()}


def symbols_of(root: Path, path: str) -> list[dict[str, Any]] | None:
    """The facts of one file, or None when it is missing; `attrs.has_error` on the module fact says it did not parse clean."""
    from sldb.code.scan import scan_file

    return scan_file(path, root) if (root / path).is_file() else None


def symbol_of(root: Path, path: str, name: str) -> dict[str, Any] | None:
    """The fact whose qualified name (with its `~n` suffix, if any) is `name`; the module for an empty name."""
    facts = symbols_of(root, path)
    if facts is None:
        return None
    wanted = name or facts[0]["qualified_name"]
    module = facts[0]["id"]
    return next((f for f in facts if (f["id"] if f["kind"] == "module" else f["id"].removeprefix(module + ".")) == wanted or (f["kind"] == "module" and not name)), None)


def recorded_with() -> str:
    try:
        grammar = version("tree-sitter-python")
    except PackageNotFoundError:
        grammar = "?"
    return f"{SCANNER} (tree-sitter-python {grammar})"
