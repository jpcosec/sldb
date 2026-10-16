"""Notes `stores check` prints even on PASS: findings that are not failures but are never hidden."""

from __future__ import annotations

from typing import Any


def print_legacy_contracts(res: Any) -> None:
    """Models signed under the contract formula sldb used before cecd97b (see `sldb.store.legacy_contract`)."""
    legacy = [m for m in res.models if m.legacy_contract and m.roster_ok]
    if legacy:
        print(f"\nnote: {len(legacy)} model(s) carry a legacy contract hash: {', '.join(m.name for m in legacy)}")
        print(f"    what    : {legacy[0].explain()}")
