"""GD22: `sldb.api.rewrite_references` and `sldb edges rewrite` (docs/architecture/references.md).

On the world of `test_referrers`: rewriting A to A2 leaves B and C pointing at A2 (C keeps its
order and its other values), the anchor of R unpinned so the save pins it again, and the
mentions of C and D rewritten as whole tokens; removing empties B, drops the element of C and
keeps the prose (skipped); a failure injected while C is written reverts B; a dry run changes
no byte and runs no `on_write` rule; nothing walks the project once the index and the graph
are warm; the same transaction can be joined.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sldb import api
from sldb.api.documents import payload_save, transaction_ops
from sldb.cli import main
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBValidationError
from tests.api.test_referrers import EXPECTED, World, count_walks, reference_world  # noqa: F401 - fixture

A2_CHANGES = [
    {"source": "Card:card-b", "field": "about", "index": None, "location": None, "before": "card-a", "after": "card-a2"},
    {"source": "Card:card-c", "field": "related", "index": 1, "location": None, "before": "card-a", "after": "card-a2"},
    {"source": "Review:r1", "field": "subject", "index": None, "location": None, "before": "doc:Card:card-a", "after": "doc:Card:card-a2"},
    {"source": "cards/card-c.md", "field": None, "index": None, "location": "cards/card-c.md:16", "before": "card:card-a", "after": "card:card-a2"},
    {"source": "notes/d.md", "field": None, "index": None, "location": "notes/d.md:3", "before": "card:card-a", "after": "card:card-a2"},
]


def test_rewriting_to_another_document_moves_every_field_and_mention_keeping_their_forms(reference_world: World) -> None:
    report = api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py)
    assert report.to_dict() == {"changed": A2_CHANGES, "skipped": []}
    assert reference_world.payload("Card:card-b")["about"] == "card-a2"
    assert reference_world.payload("Card:card-c")["related"] == ["card-x", "card-a2", "card-z"]
    assert reference_world.payload("Card:card-c")["body"] == "Also card:card-a2."
    assert reference_world.text("notes/d.md") == "# D\n\nSee card:card-a2 and card:card-ab, not card:card-a2.\n"
    subject = reference_world.payload("Review:r1")["subject"]
    assert subject.startswith("doc:Card:card-a2@sha256:") and len(subject) == len("doc:Card:card-a2@sha256:") + 64
    assert api.referrers(reference_world.store, "card-a") == []
    assert _without_lines(api.referrers(reference_world.store, "card-a2")) == _without_lines(EXPECTED)  # C was rendered again: its line may move


def _without_lines(found: list) -> list[dict]:
    rows = [r.to_dict() if hasattr(r, "to_dict") else dict(r) for r in found]
    return [{**row, "location": row["location"] and row["location"].rsplit(":", 1)[0]} for row in rows]


def test_removing_empties_the_scalar_drops_the_element_and_keeps_the_prose(reference_world: World) -> None:
    before_d = reference_world.text("notes/d.md")
    report = api.rewrite_references(reference_world.store, "card-a", None, pythonpath=reference_world.py)
    assert report.changed == [{**change, "after": None} for change in A2_CHANGES[:3]]
    assert [s["location"] for s in report.skipped] == ["cards/card-c.md:16", "notes/d.md:3"]
    assert all("never deleted" in s["reason"] for s in report.skipped)
    assert "about" not in reference_world.payload("Card:card-b") and "about:" not in reference_world.text("cards/card-b.md")
    assert reference_world.payload("Card:card-c")["related"] == ["card-x", "card-z"]
    assert "subject" not in reference_world.payload("Review:r1")
    assert reference_world.text("notes/d.md") == before_d and reference_world.payload("Card:card-c")["body"] == "Also card:card-a."
    assert _without_lines(api.referrers(reference_world.store, "card-a")) == _without_lines(EXPECTED[3:])


def test_a_scalar_the_model_does_not_let_be_null_refuses_the_removal_and_nothing_is_written(reference_world: World) -> None:
    api.create_document(reference_world.store, "Strict", reference_world.root / "strict" / "s1.md", {"title": "S1", "about": "card-a"}, "s1", reference_world.py)
    before = reference_world.digests()
    with pytest.raises(SLDBValidationError, match="Strict:s1: the rewritten document does not validate under Strict") as refused:
        api.rewrite_references(reference_world.store, "card-a", None, pythonpath=reference_world.py)
    assert "about" in str(refused.value)
    assert reference_world.digests() == before
    with pytest.raises(SLDBValidationError, match="Strict:s1"):
        api.rewrite_references(reference_world.store, "card-a", None, dry_run=True, pythonpath=reference_world.py)
    assert reference_world.digests() == before


def test_a_failure_injected_while_c_is_written_puts_b_back_bytes_entry_and_index(reference_world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    before, entry = reference_world.digests(), api.edge_node(reference_world.store, "Card:card-b").source_hash
    update = transaction_ops.update

    def failing_update(state, ref, payload, expected_source_hash, expected):
        if str(ref).endswith("card-c.md"):
            raise RuntimeError("disk full while writing C")
        return update(state, ref, payload, expected_source_hash, expected)

    monkeypatch.setattr(transaction_ops, "update", failing_update)
    with pytest.raises(RuntimeError, match="disk full"):
        api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py)
    assert reference_world.digests() == before
    assert reference_world.payload("Card:card-b")["about"] == "card-a" and api.edge_node(reference_world.store, "Card:card-b").source_hash == entry
    assert [r.to_dict() for r in api.referrers(reference_world.store, "card-a")] == EXPECTED


def test_a_dry_run_reports_the_same_changes_writes_no_byte_and_runs_no_on_write_rule(reference_world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []
    check = payload_save.check_rules_on_write
    monkeypatch.setattr(payload_save, "check_rules_on_write", lambda *args: calls.append(args[2]) or check(*args))
    before = reference_world.digests()
    report = api.rewrite_references(reference_world.store, "card-a", "card-a2", dry_run=True, pythonpath=reference_world.py)
    assert report.to_dict() == {"changed": A2_CHANGES, "skipped": []}
    assert reference_world.digests() == before and calls == []
    assert api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py).to_dict() == report.to_dict()
    assert reference_world.digests() != before and sorted(calls) == ["Card:card-b", "Card:card-c", "Review:r1"]


def test_with_the_index_and_the_graph_warm_a_dry_run_walks_nothing(reference_world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    api.rewrite_references(reference_world.store, "card-a", "card-a2", dry_run=True, pythonpath=reference_world.py)
    counts = count_walks(monkeypatch, reference_world.root)
    assert api.rewrite_references(reference_world.store, "card-a", "card-a2", dry_run=True, pythonpath=reference_world.py).changed == A2_CHANGES
    assert counts == {"walk": 0, "rglob": 0, "scandir": 0}


@pytest.mark.parametrize("before, after", [("Card:card-a", "Card:card-a2"), ("cards/card-a.md", "cards/card-a2.md"), ("`card-a`", "card-a2")])
def test_a_value_keeps_the_form_it_named_the_target_in(reference_world: World, before: str, after: str) -> None:
    reference_world.card("card-f", "Card F", about=before)
    api.rewrite_references(reference_world.store, "card-a", "Card/card-a2", pythonpath=reference_world.py)
    assert reference_world.payload("Card:card-f")["about"] == after


def test_a_replacement_that_is_no_document_is_written_as_given_and_an_ambiguous_one_is_refused(reference_world: World) -> None:
    with pytest.raises(SLDBValidationError, match="Review:r1: the rewritten document does not validate") as refused:
        api.rewrite_references(reference_world.store, "card-a", "card-elsewhere", pythonpath=reference_world.py)
    assert "is not a document anchor" in str(refused.value)  # an anchor field only takes `doc:Model:name`
    api.delete_document(reference_world.store, "r1", reference_world.py)
    api.rewrite_references(reference_world.store, "card-a", "card-elsewhere", pythonpath=reference_world.py)
    assert reference_world.payload("Card:card-b")["about"] == "card-elsewhere" and reference_world.payload("Card:card-c")["body"] == "Also card-elsewhere."
    assert reference_world.text("notes/d.md") == "# D\n\nSee card-elsewhere and card:card-ab, not card:card-a2.\n"
    api.create_document(reference_world.store, "Review", reference_world.root / "reviews" / "card-a2.md", {"title": "Same name"}, "card-a2", reference_world.py)
    with pytest.raises(SLDBDocumentTargetError, match="Ambiguous document target: card-a2"):
        api.rewrite_references(reference_world.store, "card-b", "card-a2", pythonpath=reference_world.py)


def test_a_list_never_duplicates_the_replacement(reference_world: World) -> None:
    reference_world.card("card-g", "Card G", related=["card-a2", "card-a", "card-a"])
    report = api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py)
    assert reference_world.payload("Card:card-g")["related"] == ["card-a2"]
    assert [c["index"] for c in report.changed if c["source"] == "Card:card-g"] == [1, 1]


def test_a_mention_whose_token_is_gone_from_its_line_is_skipped(reference_world: World) -> None:
    (reference_world.root / "notes" / "d.md").write_text("# D\n\nSee card:card-ab only.\n", encoding="utf-8")
    api.project_graph(reference_world.store)  # the graph notices the file moved; the index did not change
    report = api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py)
    assert [c["source"] for c in report.changed] == ["Card:card-b", "Card:card-c", "Review:r1", "cards/card-c.md"]
    assert report.skipped == [] and reference_world.text("notes/d.md") == "# D\n\nSee card:card-ab only.\n"


def test_sentence_dots_after_a_token_are_punctuation_but_a_dot_inside_one_is_not(reference_world: World) -> None:
    """q16 and q18: `card:card-a.` and `card:card-a...` are the token plus punctuation; `card:card-a.b` and `card:card-ab` are other tokens."""
    (reference_world.root / "notes" / "e.md").write_text("Ver card:card-a. Luego card:card-a... y card:card-a.b o card:card-ab, nunca.\n", encoding="utf-8")
    report = api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py)
    assert reference_world.text("notes/e.md") == "Ver card:card-a2. Luego card:card-a2... y card:card-a.b o card:card-ab, nunca.\n"
    assert [c for c in report.changed if c["source"] == "notes/e.md"] == [{"source": "notes/e.md", "field": None, "index": None, "location": "notes/e.md:1", "before": "card:card-a", "after": "card:card-a2"}]
    assert report.skipped == []


def test_the_call_joins_the_transaction_it_receives_and_the_outermost_one_rolls_back(reference_world: World) -> None:
    before = reference_world.digests()
    with pytest.raises(RuntimeError, match="later"):
        with api.transaction(reference_world.store, reference_world.py) as tx:
            api.rewrite_references(reference_world.store, "card-a", "card-a2", transaction=tx, pythonpath=reference_world.py)
            assert reference_world.payload("Card:card-b")["about"] == "card-a2"
            raise RuntimeError("something later fails")
    assert reference_world.digests() == before and reference_world.payload("Card:card-b")["about"] == "card-a"


def test_the_cli_rewrites_removes_and_dry_runs_with_the_envelope(reference_world: World, capsys) -> None:
    before = reference_world.digests()
    code, envelope = reference_world.cli(capsys, "rewrite", "card-a", "--to", "card-a2", "--dry-run")
    assert (code, envelope["ok"], envelope["data"]) == (0, True, {"changed": A2_CHANGES, "skipped": []}) and reference_world.digests() == before
    assert main(["edges", "rewrite", "card-a", "--remove", "--store", str(reference_world.store), "--pythonpath", reference_world.py, "--format", "json"]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert [c["after"] for c in printed["changed"]] == [None, None, None] and len(printed["skipped"]) == 2
    assert reference_world.payload("Card:card-c")["related"] == ["card-x", "card-z"]
    code, envelope = reference_world.cli(capsys, "rewrite", "nope", "--to", "x")
    assert (code, envelope["error"]["type"]) == (1, "docs/missing")


@pytest.mark.parametrize("argv", [["card-a"], ["card-a", "--to", "x", "--remove"]])
def test_to_and_remove_exclude_each_other_and_one_is_required(reference_world: World, argv: list[str], capsys) -> None:
    assert main(["edges", "rewrite", *argv, "--store", str(reference_world.store)]) == 2
    err = capsys.readouterr().err
    assert "one of the arguments --to --remove is required" in err or "not allowed with argument" in err
    code, envelope = reference_world.cli(capsys, "rewrite", *argv)
    assert (code, envelope["error"]["type"]) == (6, "cli/usage")


def test_the_text_output_names_each_change(reference_world: World, capsys) -> None:
    assert main(["edges", "rewrite", "card-a", "--to", "card-a2", "--dry-run", "--store", str(reference_world.store), "--pythonpath", reference_world.py]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "Card:card-b .about: 'card-a' -> 'card-a2'" and lines[-1] == "would change 5 reference(s), skipped 0"
    assert Path(reference_world.root / "cards" / "card-b.md").read_text(encoding="utf-8").count("card-a2") == 0
