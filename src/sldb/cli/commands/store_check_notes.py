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


def print_shadowed(sp: Any) -> None:
    """Models this store owns under a name a linked store owns too: a note, never a failure."""
    from sldb.api.model_registry.model_reference import same_model_class
    from sldb.store.model_origin import shadowed_models

    for found in shadowed_models(sp, same_model_class):
        if found["copy"]:
            print(f"\nnote: {found['model']} is a copy of the model the store linked as '{found['store']}' owns")
            print(f"    fix     : sldb models inherit {found['store']}:{found['model']}   (keeps its documents; imports from the owner)")
        else:
            print(f"\nnote: {found['model']} is another class under the name of a model '{found['store']}' owns; the graph merges both in one node")
            print(f"    fix     : give the override a name of its own and extend {found['model']}")

