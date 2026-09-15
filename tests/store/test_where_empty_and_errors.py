"""The empty literal and the loud failure of --where: `f = ""` is a field present and
empty, an absent field matches neither `=` nor `!=`, and a predicate no evaluator
parses is an error (WherePredicateError), never a silent empty result — on the engine
and on the CLI, which exits non-zero naming the predicate.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sldb.cli import main as cli_main
from sldb.store.query import find_structural
from sldb.store.query_engine.filter import DocumentFilter
from sldb.store.query_engine.models import RuntimeDocument
from sldb.store.query_engine.where_parse import WherePredicateError, compile_where


def _ref(model_ref, pythonpath=None):
    import where_models

    return where_models.MemoDoc


def _doc(payload: dict) -> RuntimeDocument:
    return RuntimeDocument("local", Path("."), "MemoDoc", object, "d", "d.md", payload, [])


@pytest.mark.parametrize(
    "predicate,payload,expected",
    [
        ('status = ""', {"status": ""}, True),
        ('status = ""', {"status": "open"}, False),
        ('status = ""', {}, False),
        ('status != ""', {"status": ""}, False),
        ('status != ""', {"status": "open"}, True),
        ('status != ""', {}, False),
        ("has(status)", {"status": ""}, False),
        ('status = "open"', {"status": "open"}, True),
    ],
)
def test_empty_literal_and_absent_field_semantics(predicate, payload, expected):
    assert DocumentFilter.where_matches(_doc(payload), predicate, _ref, None) is expected


def test_unparseable_predicate_raises_from_the_per_document_filter():
    with pytest.raises(WherePredicateError, match="status ==="):
        DocumentFilter.where_matches(_doc({"status": ""}), "status ===", _ref, None)


QUOTED = 'doesn\'t exist " here'
ESCAPED = 'title = "doesn\'t exist \\" here"'  # the predicate carries \" for the quote


@pytest.mark.parametrize(
    "predicate,payload,expected",
    [
        (ESCAPED, {"title": QUOTED}, True),  # the escaped literal matches exactly
        (ESCAPED, {"title": "doesn't exist here"}, False),  # without the quote: no
        (ESCAPED, {"title": QUOTED + " extra"}, False),  # not a prefix/partial match
        (ESCAPED, {"status": QUOTED}, False),  # an absent field matches neither
        ('"say \\"hi\\"" in title', {"title": 'say "hi" aloud'}, True),
        ('"say \\"hi\\"" in title', {"title": "say hi aloud"}, False),
        ('title ~ "exist \\" here"', {"title": QUOTED}, True),
        ('title ~ "exist \\" here"', {"title": "exist here"}, False),
    ],
)
def test_backslash_escapes_in_string_literals(predicate, payload, expected):
    assert DocumentFilter.where_matches(_doc(payload), predicate, _ref, None) is expected


@pytest.mark.parametrize(
    "predicate",
    [
        'title = "unterminated',
        'title = "escaped quote eats the closing \\"',  # \" is an escape, not the end
        '"unterminated in title',
        'title ~ "unterminated',
    ],
)
def test_an_unterminated_literal_is_still_an_error(predicate):
    with pytest.raises(WherePredicateError):
        compile_where(predicate)


@pytest.fixture
def setup(tmp_path):
    (tmp_path / "where_models.py").write_text(
        '''from pydantic import Field
from sldb import StructuredNLDoc


class MemoDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\nStatus: ⸢rev•status⸥"
    title: str = Field(description="Title.")
    status: str = Field(default="", description="Workflow status.")
''',
        encoding="utf-8",
    )
    root = tmp_path / "repo"
    root.mkdir()
    store = root / ".sldb"
    common = ["--store", str(store), "--pythonpath", str(tmp_path)]
    assert cli_main(["stores", "init", "--path", str(root)]) == 0
    assert cli_main(["models", "add", "where_models:MemoDoc", *common]) == 0
    assert cli_main(["docs", "create", "--model", "MemoDoc", "-o", str(root / "empty.md"), '{"title": "Empty"}', *common]) == 0
    payload = json.dumps({"title": "Open", "status": "open"})
    assert cli_main(["docs", "create", "--model", "MemoDoc", "-o", str(root / "open.md"), payload, *common]) == 0
    return store, common


def test_find_empty_literal_matches_only_the_present_empty_document(setup):
    store, common = setup
    found = find_structural(store, "st.{MemoDoc}", 'status = ""', _ref, common[3])
    assert found == ["st.{MemoDoc}.empty"]


def test_find_matches_the_escaped_title_and_only_it(setup):
    store, common = setup
    root = store.parent
    payload = json.dumps({"title": QUOTED, "status": "open"})
    assert (
        cli_main(
            ["docs", "create", "--model", "MemoDoc", "-o", str(root / "quoted.md"), payload, *common]
        )
        == 0
    )
    assert find_structural(store, "st.{MemoDoc}", ESCAPED, _ref, common[3]) == [
        "st.{MemoDoc}.quoted"
    ]


def test_unparseable_predicate_raises_from_the_engine(setup):
    store, common = setup
    with pytest.raises(WherePredicateError, match="bogus predicate"):
        find_structural(store, "st.{MemoDoc}", "bogus predicate", _ref, common[3])


def test_cli_find_prints_the_error_and_exits_non_zero(setup, capsys):
    store, common = setup
    with pytest.raises(SystemExit) as exc:
        cli_main(["find", "st.{MemoDoc}", "--where", "bogus predicate", *common])
    assert exc.value.code != 0
    assert "bogus predicate" in str(exc.value)
    assert capsys.readouterr().out == ""
