"""What an anchor's `ref` names (ported from kgdb's typed ingest): both spellings of a ref —
the `kind:rest` scheme and the pron form (spec 13) — name the same nodes."""

from __future__ import annotations

import pytest

from sldb.store.edge_index.anchor_targets import anchor_targets

TABLE, CAPACITY, ASSIGNED = "sldb://model/Table", "sldb://field/Table.capacity", "sldb://relation_type/assigned_to"


@pytest.mark.parametrize(
    ("ref", "targets"),
    [
        ("model:Table", [TABLE]),
        ("field:Table.capacity", [CAPACITY]),
        ("field:Table", []),
        ("predicate:Table:capacity >= 6", [TABLE]),
        ("relation:assigned_to", [ASSIGNED]),
        ("doc:Table:table-12", ["sldb://document/Table:table-12"]),
        ("action:Table.capacity=8 Table.title=x", [CAPACITY, "sldb://field/Table.title"]),
        ("nothing:known", []),
        ("(model Table)", [TABLE]),
        ('(where Table "capacity >= 6")', [TABLE]),
        ("(field Table capacity)", [CAPACITY]),
        ("(relation assigned_to)", [ASSIGNED]),
        ('(doc "Table:table-12")', ["sldb://document/Table:table-12"]),
        ("(change (it of Table) capacity 8)", [CAPACITY]),
        ("(change capacity 8)", []),
        ("(move (create Reservation) (assert assigned_to (created) (a Table)))", ["sldb://model/Reservation", ASSIGNED]),
        ('("not a symbol" Table)', []),
        ("(", []),
    ],
)
def test_anchor_targets(ref: str, targets: list[str]):
    assert anchor_targets({"ref": ref}) == targets


def test_compose_refs_name_their_steps():
    payload = {"ref": "compose:book", "steps": [{"model": "Reservation"}, {"relation": "assigned_to"}, "free text", {"model": ""}]}
    assert anchor_targets(payload) == ["sldb://model/Reservation", ASSIGNED]
