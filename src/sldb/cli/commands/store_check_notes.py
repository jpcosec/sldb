"""Notes `stores check` prints even on PASS: findings that are not failures but are never hidden."""

from __future__ import annotations

from typing import Any


def print_notes(res: Any) -> None:
    """Every note, in a fixed order."""
    print_unresolved_models(res)
    print_legacy_contracts(res)


def print_unresolved_models(res: Any) -> None:
    """Models whose class cannot be imported here: their fields were not re-extracted, only their text."""
    unresolved = [m for m in res.models if not m.resolved]
    if unresolved:
        print(f"\nnote: {len(unresolved)} model(s) could not be imported, so only their documents' text was checked: {', '.join(m.name for m in unresolved)}")
        print("    fix     : make the model importable (install its package, or pass --pythonpath) to check fields too")
        _print_removable(unresolved)


def _print_removable(unresolved: list[Any]) -> None:
    """Unresolved models with no documents left: most likely deleted on purpose."""
    empty = [m.name for m in unresolved if not m.documents]
    if empty:
        print(f"    or      : `sldb models remove <name>` unregisters one with no documents: {', '.join(empty)}")


def print_legacy_contracts(res: Any) -> None:
    """Models signed under the contract formula sldb used before cecd97b (see `sldb.store.legacy_contract`)."""
    legacy = [m for m in res.models if m.legacy_contract and m.roster_ok]
    if legacy:
        print(f"\nnote: {len(legacy)} model(s) carry a legacy contract hash: {', '.join(m.name for m in legacy)}")
        print(f"    what    : {legacy[0].explain()}")
