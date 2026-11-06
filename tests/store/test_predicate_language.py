"""GO05: the unified predicate language against the two old ones (rules-language.md §7).

`PAYLOADS` is the fixed set of payloads (p5): null, lists, an absent field, numbers and
strings. `tests/fixtures/where_goldens/` holds, for each row of the equivalence table, the old
expression (a `where_parse` string, or a `FieldCondition` as its JSON dict, p13) and the
sorted names of the payloads it matched, captured with the code of main before GO05 touched
`src/` (commit 4d090ee2). The old evaluators are gone (GO10): the old expression is data, and
each row evaluates its new construction of §7 against the golden. The goldens are never
regenerated. An old evaluator that raised on a payload (where_parse ordering `None` or mixed
types raises TypeError) counted as "does not match".
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

GOLDENS = Path(__file__).resolve().parents[1] / "fixtures" / "where_goldens"

PAYLOADS: dict[str, dict] = {
    "absent": {},
    "closed": {"status": "closed", "priority": 5, "tags": [], "title": "alpha beta", "note": ""},
    "float": {"status": "draft", "priority": 2.5, "tags": ["y"], "title": "Draft", "note": "b"},
    "list_valued": {"status": ["open"], "priority": [2], "tags": "x-y", "title": ["draft"], "note": ["n"]},
    "null": {"status": None, "priority": None, "tags": None, "title": None, "note": None},
    "numeric_text": {"status": "3", "priority": 3, "tags": ["3"], "title": "3", "note": "x"},
    "open": {"status": "open", "priority": 2, "tags": ["x", "y"], "title": "draft spec", "note": "a"},
}

# (table row, old where_parse expression); the new construction is the same text (§7 rows 1-11)
WHERE_ROWS: list[tuple[str, str]] = [
    ("1", "has(status)"),
    ("2", "nonempty(tags)"),
    ("3", '"x" in tags'),
    ("4", 'title ~ "dra"'),
    ("5", "model <= BaseDoc"),
    ("6", 'status = "open"'),
    ("6", "priority = 2"),
    ("7", 'status != "open"'),
    ("7", "priority != 2"),
    ("9", "priority <= 3"),
    ("11", "priority >= 3"),
]

# (table row, old FieldCondition dict, new construction of §7)
FIELD_CONDITION_ROWS: list[tuple[str, dict, str]] = [
    ("12", {"field": "status", "op": "eq", "value": "open"}, 'status = "open"'),
    ("13", {"field": "status", "op": "ne", "value": "open"}, 'status != "open"'),
    ("14", {"field": "priority", "op": "gt", "value": 2}, "priority > 2"),
    ("15", {"field": "priority", "op": "lt", "value": 3}, "priority < 3"),
    ("16", {"field": "tags", "op": "contains", "value": "x"}, '"x" in tags'),
    ("17", {"field": "title", "op": "starts_with", "value": "dra"}, 'title ~ "^dra"'),
    ("18", {"field": "note", "op": "is_null", "value": None}, "not has(note)"),
    ("19", {"field": "note", "op": "is_not_null", "value": None}, "has(note)"),
]


def _golden(name: str) -> list[dict]:
    return json.loads((GOLDENS / f"{name}.json").read_text(encoding="utf-8"))


def _matching(check) -> list[str]:
    names = []
    for name, payload in sorted(PAYLOADS.items()):
        try:
            if check(payload):
                names.append(name)
        except TypeError:
            pass
    return names


def test_the_goldens_cover_every_row_in_order():
    assert [g["old"] for g in _golden("where_parse")] == [old for _, old in WHERE_ROWS]
    assert [g["old"] for g in _golden("field_condition")] == [old for _, old, _ in FIELD_CONDITION_ROWS]


# Where the new language answers otherwise than the golden, and why (rules-language.md §7).
WHERE_DIFFERENCES = {
    # an absent field holds no comparison; where_parse let `!=` with a number literal hold on it
    "priority != 2": {"absent"},
}
FIELD_CONDITION_DIFFERENCES = {
    "16": {"list_valued"},  # contains: also a substring in the new language ("x" in "x-y")
    "18": {"closed"},  # is_null ~ not has(f): has also rejects ""
    "19": {"closed"},  # is_not_null ~ has(f): has also rejects ""
}


def _changed(new: list[str], golden: list[str]) -> set[str]:
    return set(new) ^ set(golden)


def test_where_parse_rows_answer_their_goldens_in_the_new_language():
    from sldb.api.where import where_matches

    for (row, old), golden in zip(WHERE_ROWS, _golden("where_parse")):
        assert golden["old"] == old, row
        new = _matching(lambda payload: where_matches(old, payload))
        assert _changed(new, golden["matches"]) == WHERE_DIFFERENCES.get(old, set()), (row, old)


def test_field_condition_rows_answer_their_goldens_with_the_construction_of_the_table():
    from sldb.store.graph.language.predicate_documents import payload_holds

    for (row, old, construction), golden in zip(FIELD_CONDITION_ROWS, _golden("field_condition")):
        assert golden["old"] == old, row
        through_the_language = _matching(lambda p: payload_holds(construction, {k: v for k, v in p.items() if v is not None}))
        assert _changed(through_the_language, golden["matches"]) == FIELD_CONDITION_DIFFERENCES.get(row, set()), row


def test_the_new_api_does_not_warn():
    import warnings

    from sldb.api.where import where_matches
    from sldb.store.graph.language.predicate_parser import parse_predicate

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        assert where_matches('status = "open" and not has(note)', {"status": "open"})
        assert parse_predicate('any(depends_on: status = "open")').text


# --- GraphBackend.eval over a composed index (GO05 step 3; h1, p8, p10) ------------------

def _index(payloads: dict[str, dict], edges: list[tuple], bases: dict[str, list[str]] | None = None):
    from sldb.store.edge_index.edge_index import EdgeIndex
    from sldb.store.models import EdgeNodeRecord, EdgeRecord

    docs = [EdgeNodeRecord(id=f"sldb://document/{i}", node_type=i.split(":")[0], payload=p) for i, p in payloads.items()]
    models = [EdgeNodeRecord(id=f"sldb://model/{m}", node_type="sldb_model", semantics={"base_models": b}) for m, b in (bases or {}).items()]
    records = [EdgeRecord(source=f"sldb://document/{s}", target=f"sldb://document/{t}", relation=r, metadata=m) for s, r, t, m in edges]
    return EdgeIndex(nodes={n.id: n for n in docs + models}, edges=records)


def _backend(index, projection=None):
    from sldb.store.graph.backend import NetworkXBackend

    backend = NetworkXBackend()
    backend.load(index, projection)
    return backend


_TASKS = {"Task:a": {"depends_on": ["Task:b", "Task:c"], "subject": "Task:b"}, "Task:b": {"status": "closed"}, "Task:c": {"status": "open"}, "Sub:d": {"status": "open"}}
_EDGES = [
    ("Task:a", "references", "Task:b", {"field": "depends_on", "declared": "Task:b"}),
    ("Task:a", "references", "Task:c", {"field": "depends_on", "declared": "Task:c"}),
    ("Task:a", "references", "Task:b", {"field": "subject", "declared": "Task:b"}),
    ("Task:c", "task_activates", "Sub:d", {}),
]


def test_backend_eval_follows_paths_over_the_index():
    backend = _backend(_index(_TASKS, _EDGES))
    holds = lambda text: backend.eval(text, {"id": "Task:a", **_TASKS["Task:a"]})[0]["holds"]  # noqa: E731
    assert holds('any(depends_on: status = "open")') == "true"
    assert holds('all(depends_on: status = "closed")') == "false"
    assert holds('any(depends_on.rel:task_activates: status = "open")') == "true"
    assert backend.eval('any(^depends_on: has(subject))', {"id": "Task:b"})[0]["holds"] == "true"


def test_backend_eval_without_subject_covers_every_document_of_the_index():
    backend = _backend(_index(_TASKS, _EDGES, {"Sub": ["Task"]}))
    assert [f["node"] for f in backend.eval("has(status)")] == ["Sub:d", "Task:a", "Task:b", "Task:c"]
    assert [f["node"] for f in backend.eval('model <= Task and status = "open"')] == ["Sub:d", "Task:a", "Task:b", "Task:c"]
    assert [f["node"] for f in backend.eval('model <= Sub and status = "open"')] == ["Sub:d"]


def test_backend_eval_by_export_id_reads_the_projection():
    projection = {i: dict(p) for i, p in _TASKS.items()}
    backend = _backend(_index(_TASKS, _EDGES), projection)
    assert backend.eval('any(depends_on: status = "open")', "Task:a")[0]["holds"] == "true"


def test_anchor_state_is_exposed_when_the_origin_carries_the_entry():
    projection = {**{i: dict(p) for i, p in _TASKS.items()}}
    projection["Task:a"] = {**_TASKS["Task:a"], "depends_on__anchor_state": ["fresh", "stale"], "subject__anchor_state": "fresh"}
    backend = _backend(_index(_TASKS, _EDGES), projection)
    finding = backend.eval('any(depends_on: anchor_state = "stale")', "Task:a")[0]
    assert (finding["holds"], finding["seen"]) == ("true", {"anchor_state": "stale"})
    assert backend.eval('all(depends_on: has(anchor_state))', "Task:a")[0]["holds"] == "true"
    assert backend.eval('any(subject: anchor_state = "fresh")', "Task:a")[0]["holds"] == "true"


def test_anchor_state_is_undefined_without_the_entry():
    backend = _backend(_index(_TASKS, _EDGES), {i: dict(p) for i, p in _TASKS.items()})
    assert backend.eval("any(depends_on: has(anchor_state))", "Task:a")[0]["holds"] == "false"


def test_backend_eval_and_eval_predicate_give_the_same_findings():
    from sldb.store.query_engine.rules import eval_predicate, parse_predicate

    nodes = {i: {"model": i.split(":")[0], "payload": p, "base_models": ["Task"] if i.startswith("Sub") else []} for i, p in _TASKS.items()}
    graph = {"nodes": nodes, "edges": [{"source": s, "type": r, "target": t, **m} for s, r, t, m in _EDGES]}
    backend = _backend(_index(_TASKS, _EDGES, {"Sub": ["Task"]}))
    for text in ('any(depends_on: status = "open")', "count(depends_on+: has(status)) = 2", "model <= Task and not has(status)", 'none(rel:task_activates: status = "open")'):
        assert backend.eval(parse_predicate(text)) == eval_predicate(parse_predicate(text), graph), text


# --- the CLI: find --where (paths, --explain), graph query's where, zero extractions -----

_TASK_MODULE = "sldb_go05_predicate_models"
_TASK_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Task(StructuredNLDoc):
    __references__ = ["depends_on"]
    __template__ = """---
status: ⸢rev•status⸥
depends_on: ⸢rev•depends_on⸥
---

# ⸢rev•title⸥
"""
    title: str = Field(description="Title.")
    status: str = Field(description="Status.")
    depends_on: list[str] = Field(default_factory=list, description="Tasks this one waits for.")
'''


@pytest.fixture
def tasks(tmp_path):
    import sys

    from sldb import api

    (tmp_path / f"{_TASK_MODULE}.py").write_text(_TASK_MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        root = tmp_path / "world"
        root.mkdir()
        sp, py = api.init_store(root).store_path, str(tmp_path)
        api.add_model(sp, f"{_TASK_MODULE}:Task", py)
        for name, status, depends in (("b", "closed", []), ("c", "open", []), ("a", "open", ["Task:b", "Task:c"]), ("d", "open", ["Task:b"])):
            api.create_document(sp, "Task", root / f"{name}.md", {"title": name, "status": status, "depends_on": depends}, name, py)
        yield sp, py
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(_TASK_MODULE, None)


def _cli(*argv: str) -> tuple[int, str]:
    import contextlib
    import io

    from sldb.cli import main as cli_main

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = cli_main(list(argv))
    return code, out.getvalue()


def _find(sp, py, where: str, *extra: str) -> dict:
    code, printed = _cli("--envelope", "find", "Task", "--type", "doc", "--where", where, "--format", "json", "--store", str(sp), "--pythonpath", py, *extra)
    return json.loads(printed)


def test_find_where_any_over_a_relation_answers_through_the_envelope(tasks):
    envelope = _find(*tasks, 'any(depends_on: status = "open")')
    assert envelope["ok"] and envelope["warnings"] == []
    assert [r["doc"] for r in envelope["data"]["results"]] == ["a"]
    assert "findings" not in envelope["data"]


def test_find_where_all_with_explain_names_the_failing_clause_per_document(tasks):
    envelope = _find(*tasks, 'all(depends_on: status = "closed")', "--explain")
    assert sorted(r["doc"] for r in envelope["data"]["results"]) == ["b", "c", "d"]
    findings = {f["node"]: f for f in envelope["data"]["findings"]}
    assert sorted(findings) == ["Task:a", "Task:b", "Task:c", "Task:d"]
    assert findings["Task:a"] == {"node": "Task:a", "holds": "false", "clause": 'all(depends_on: status = "closed")', "seen": {"status": "open"}}
    assert {f["holds"] for n, f in findings.items() if n != "Task:a"} == {"true"}


def test_find_where_with_the_same_expression_does_not_warn(tasks):
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        envelope = _find(*tasks, 'status = "closed"')
    assert envelope["warnings"] == [] and [r["doc"] for r in envelope["data"]["results"]] == ["b"]


def test_graph_query_with_a_where_filter_answers_without_warnings(tasks, tmp_path):
    sp, py = tasks
    query = tmp_path / "query.json"
    query.write_text(json.dumps({"filters": [{"facet": "payload", "where": 'status = "closed"'}]}), encoding="utf-8")
    plain_code, plain = _cli("graph", "query", "--query-file", str(query), "--store", str(sp), "--local")
    code, printed = _cli("--envelope", "graph", "query", "--query-file", str(query), "--store", str(sp), "--local")
    envelope = json.loads(printed)
    assert plain_code == code == 0 and envelope["data"] == json.loads(plain)
    assert [n["id"] for n in envelope["data"]] == ["sldb://document/Task:b"]
    assert envelope["warnings"] == []


def test_a_path_in_a_facet_where_is_rejected_naming_it():
    from sldb.store.edge_index.edge_index import EdgeIndex
    from sldb.store.exceptions import SLDBGraphArgumentError
    from sldb.store.graph import StructuredQuery, execute_query

    query = StructuredQuery.model_validate({"filters": [{"facet": "payload", "where": 'any(depends_on: status = "open")'}]})
    with pytest.raises(SLDBGraphArgumentError, match="any\\(depends_on"):
        execute_query(EdgeIndex(nodes={}), query)


def test_where_over_every_document_of_a_repo_model_extracts_nothing(tmp_path, monkeypatch):
    from sldb import api
    from sldb.api.where import where_findings
    from sldb.runtime.validation import Validator
    from sldb.store.edge_index.compose import invalidate_composed_edge_indexes
    from sldb.store.io.shards import invalidate_shard_cache
    from sldb.store.runtime_cache import invalidate_runtime_cache

    repo = str(Path(__file__).resolve().parents[2])
    root = tmp_path / "world"
    root.mkdir()
    sp = api.init_store(root).store_path
    api.add_model(sp, "docs.models:SpecDoc", repo)
    for name in ("alpha", "beta", "gamma"):
        api.create_document(sp, "SpecDoc", root / f"{name}.md", {"title": name, "body": f"About {name}."}, name, repo)
    calls = []
    original = Validator.extract
    monkeypatch.setattr(Validator, "extract", lambda self, md: calls.append(1) or original(self, md))
    invalidate_composed_edge_indexes(), invalidate_shard_cache(), invalidate_runtime_cache()
    findings = where_findings(sp, 'model <= SpecDoc and title ~ "a"')
    assert [(f["node"], f["holds"]) for f in findings] == [("SpecDoc:alpha", "true"), ("SpecDoc:beta", "true"), ("SpecDoc:gamma", "true")]
    assert calls == []
