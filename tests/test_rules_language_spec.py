"""Spec tests for ``docs/architecture/rules-language.md`` (GO02).

Each test states the example documented for one construction and marks it ``xfail`` until
GO05 implements the language. ``EXPECTED_XFAIL`` is the number of documented constructions
fixed by this file (p9); it must stay >= 25.

The evaluator module does not exist yet, so the imports live inside the test bodies (via the
helpers below): collection must not break, and every test currently fails for the real
reason "module not found". The concrete module path, call signature and graph fixture are
recorded as hypotheses in the document (§8, H1-H4).
"""

from __future__ import annotations

import hashlib

import pytest

from sldb.store.query_engine.where_parse import WherePredicateError

EXPECTED_XFAIL = 52


# --- provisional spec adapter (see rules-language.md §8, H1-H4) -------------------------

def _parse(text: str):
    from sldb.store.query_engine.rules import parse_predicate

    return parse_predicate(text)


def _findings(text: str, graph: dict, subject: str | None = None) -> list:
    from sldb.store.query_engine.rules import eval_predicate, parse_predicate

    return eval_predicate(parse_predicate(text), graph, subject=subject)


def _value(finding, key: str):
    return finding[key] if isinstance(finding, dict) else getattr(finding, key)


def _norm(value) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value).lower()


def _one(text: str, graph: dict, subject: str | None = None):
    findings = _findings(text, graph, subject)
    assert len(findings) == 1, findings
    return findings[0]


def _holds(text: str, graph: dict, subject: str | None = None) -> str:
    return _norm(_value(_one(text, graph, subject), "holds"))


def _contract_hash(model_type, field_hashes: dict[str, str]) -> str:
    from sldb.store.query_engine.rules import contract_hash

    return contract_hash(model_type, field_hashes)


def _expected_contract(fields, field_hashes: dict[str, str]) -> str:
    lines = [
        f"{name}={field_hashes.get(name, '')}"
        for name in sorted(fields, key=lambda name: name.encode("utf-8"))
    ]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


# --- graph fixture builders (see rules-language.md §8, H2) -----------------------------

def _doc(model: str = "TaskDoc", **payload):
    return {"model": model, "payload": payload}


def _graph(nodes: dict, edges=()) -> dict:
    return {"nodes": dict(nodes), "edges": list(edges)}


def _edge(source: str, type_: str, target: str, field: str | None = None, **extra) -> dict:
    edge = {"source": source, "type": type_, "target": target, **extra}
    if field is not None:
        edge["field"] = field
    return edge


# --- (a) grammar ------------------------------------------------------------------------

@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_precedence_not_over_and_over_or():
    graph = _graph({"Task:a": _doc(note="x")})
    assert _holds('has(status) and status = "open" or has(note)', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_not_binds_tighter_than_and():
    graph = _graph({"Task:a": _doc(note="x")})
    assert _holds("not has(status) and has(note)", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_parentheses_group_expression():
    graph = _graph({"Task:b": _doc()})
    assert _holds("not (has(a) or has(b))", graph, "Task:b") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_left_associativity_with_parentheses():
    graph = _graph({"Task:c": _doc(a=1, c=2), "Task:d": _doc(b=1)})
    assert _holds("(has(a) or has(b)) and has(c)", graph, "Task:c") == "true"
    assert _holds("(has(a) or has(b)) and has(c)", graph, "Task:d") == "false"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_equal():
    graph = _graph({"Task:a": _doc(status="open")})
    assert _holds('status = "open"', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_not_equal():
    graph = _graph({"Task:a": _doc(status="closed")})
    assert _holds('status != "open"', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_less_than():
    graph = _graph({"Task:a": _doc(priority=2)})
    assert _holds("priority < 3", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_less_or_equal():
    graph = _graph({"Task:a": _doc(priority=3)})
    assert _holds("priority <= 3", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_greater_than():
    graph = _graph({"Task:a": _doc(priority=4)})
    assert _holds("priority > 3", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_comparison_greater_or_equal():
    graph = _graph({"Task:a": _doc(priority=3)})
    assert _holds("priority >= 3", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_in_list_membership():
    graph = _graph({"Task:a": _doc(statuses=["draft", "open"])})
    assert _holds('"draft" in statuses', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_in_substring():
    graph = _graph({"Task:a": _doc(title="draft spec")})
    assert _holds('"raf" in title', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_in_other_type_is_false():
    graph = _graph({"Task:a": _doc(priority=5)})
    assert _holds('"x" in priority', graph, "Task:a") == "false"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_scalar_in_literal_list():
    graph = _graph({"Task:a": _doc(status="draft")})
    assert _holds('status in ["open", "draft"]', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_regex_search_semantics():
    graph = _graph({"Task:a": _doc(title="alpha beta")})
    assert _holds('title ~ "beta"', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_invalid_regex_raises_where_predicate_error():
    with pytest.raises(WherePredicateError):
        _parse('title ~ "("')


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_model_less_or_equal_family():
    graph = _graph({"Task:a": _doc("ChildDoc")})
    assert _holds("model <= BaseDoc", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_has_present_and_nonempty_value():
    graph = _graph({"Task:a": _doc(status="open"), "Task:b": _doc(status="")})
    assert _holds("has(status)", graph, "Task:a") == "true"
    assert _holds("has(status)", graph, "Task:b") == "false"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_nonempty_rejects_empty_collections():
    graph = _graph({"Task:a": _doc(tags=["x"]), "Task:b": _doc(tags=[])})
    assert _holds("nonempty(tags)", graph, "Task:a") == "true"
    assert _holds("nonempty(tags)", graph, "Task:b") == "false"


# --- (b) paths, quantifiers, count and substitution -------------------------------------

@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_any_quantifier():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="open"), "Task:c": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:a", "references", "Task:c", "depends_on")],
    )
    assert _holds('any(depends_on: status = "open")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_all_quantifier():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="closed"), "Task:c": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:a", "references", "Task:c", "depends_on")],
    )
    assert _holds('all(depends_on: status = "closed")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_none_quantifier():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="closed"), "Task:c": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:a", "references", "Task:c", "depends_on")],
    )
    assert _holds('none(depends_on: status = "open")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_count_in_comparison():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on")],
    )
    assert _holds('count(depends_on: status = "open") = 0', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_count_omits_missing_document_reference():
    graph = _graph(
        {"Task:a": _doc()},
        [_edge("Task:a", "references", "Doc:missing", "depends_on")],
    )
    assert _holds("count(depends_on: has(status)) = 0", graph, "Task:a") == "true"
    assert _holds("all(depends_on: status = \"closed\")", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_count_with_incomplete_element_is_incomplete():
    graph = _graph(
        {"Task:a": _doc()},
        [_edge("Task:a", "external_link", "Other:Doc:x", unavailable=True)],
    )
    assert _holds("count(rel:external_link: status = \"open\") = 0", graph, "Task:a") == "incomplete"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_substitution_from_subject_payload():
    graph = _graph({"Task:a": _doc(capacity=6, party_size=4)})
    assert _holds("capacity >= {party_size}", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_substitution_missing_field_makes_false():
    graph = _graph({"Task:a": _doc(capacity=6)})
    assert _holds("capacity >= {party_size}", graph, "Task:a") == "false"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_substitution_non_scalar_makes_false():
    graph = _graph({"Task:a": _doc(capacity=6, party_size=[4])})
    assert _holds("capacity >= {party_size}", graph, "Task:a") == "false"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_substitution_not_applied_inside_quoted_literal():
    graph = _graph({"Task:a": _doc(label="{party_size}", party_size=4)})
    assert _holds('label = "{party_size}"', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_field_step_follows_references():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="open")},
        [_edge("Task:a", "references", "Task:b", "depends_on")],
    )
    assert _holds('any(depends_on: status = "open")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_undeclared_reference_field_is_empty_set():
    graph = _graph({"Task:a": _doc(), "Task:b": _doc(status="open")})
    assert _holds('any(no_declarado: status = "open")', graph, "Task:a") == "false"
    assert _holds('all(no_declarado: status = "open")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_rel_type_step():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="active")},
        [_edge("Task:a", "task_activates", "Task:b")],
    )
    assert _holds('any(rel:task_activates: status = "active")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_inverse_field_step():
    graph = _graph(
        {"Task:a": _doc(), "Review:r": _doc(verdict="accepted")},
        [_edge("Review:r", "references", "Task:a", "subject")],
    )
    assert _holds('any(^subject: verdict = "accepted")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_transitive_closure_field():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="closed"), "Task:c": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:b", "references", "Task:c", "depends_on")],
    )
    assert _holds('all(depends_on+: status = "closed")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_transitive_closure_cycle_terminates():
    graph = _graph(
        {"Task:a": _doc(status="closed"), "Task:b": _doc(status="closed"), "Task:c": _doc(status="closed")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:b", "references", "Task:c", "depends_on"),
         _edge("Task:c", "references", "Task:a", "depends_on")],
    )
    assert _holds("count(depends_on+: has(status)) = 2", graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_transitive_closure_rel_type():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(), "Task:c": _doc(status="done")},
        [_edge("Task:a", "task_activates", "Task:b"),
         _edge("Task:b", "task_activates", "Task:c")],
    )
    assert _holds('any(rel:task_activates+: status = "done")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_transitive_closure_inverse():
    graph = _graph(
        {"Task:a": _doc(), "Review:r1": _doc(), "Review:r2": _doc(verdict="accepted")},
        [_edge("Review:r1", "references", "Task:a", "subject"),
         _edge("Review:r2", "references", "Review:r1", "subject")],
    )
    assert _holds('any(^subject+: verdict = "accepted")', graph, "Task:a") == "true"


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_linked_store_unavailable_is_incomplete():
    graph = _graph(
        {"Task:a": _doc()},
        [_edge("Task:a", "external_link", "Other:Doc:x", unavailable=True)],
    )
    assert _holds('any(rel:external_link: status = "open")', graph, "Task:a") == "incomplete"


# --- (d) explanation and (f) eval signature ---------------------------------------------

@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_finding_shape_and_seen_for_false_clause():
    graph = _graph({"Task:a": _doc(status="closed")})
    finding = _one('status = "open"', graph, "Task:a")
    assert _norm(_value(finding, "holds")) == "false"
    assert _value(finding, "node") == "Task:a"
    assert 'status = "open"' in _value(finding, "clause")
    assert _value(finding, "seen") == {"status": "closed"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_seen_and_first_false_branch():
    graph = _graph({"Task:a": _doc(status="closed", priority=5)})
    finding = _one('status = "open" and priority > 3', graph, "Task:a")
    assert _norm(_value(finding, "holds")) == "false"
    assert set(_value(finding, "seen")) == {"status"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_seen_or_first_true_branch():
    graph = _graph({"Task:a": _doc(status="open", priority=5)})
    finding = _one('status = "open" or priority > 3', graph, "Task:a")
    assert _norm(_value(finding, "holds")) == "true"
    assert set(_value(finding, "seen")) == {"status"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_seen_not_negated_leaf():
    graph = _graph({"Task:a": _doc(status="open")})
    finding = _one("not has(status)", graph, "Task:a")
    assert _norm(_value(finding, "holds")) == "false"
    assert set(_value(finding, "seen")) == {"status"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_seen_quantifier_witness():
    graph = _graph(
        {"Task:a": _doc(), "Task:b": _doc(status="closed"), "Task:c": _doc(status="open")},
        [_edge("Task:a", "references", "Task:b", "depends_on"),
         _edge("Task:a", "references", "Task:c", "depends_on")],
    )
    finding = _one('all(depends_on: status = "closed")', graph, "Task:a")
    assert _norm(_value(finding, "holds")) == "false"
    assert _value(finding, "seen") == {"status": "open"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_eval_with_subject_returns_one_finding():
    graph = _graph({"Task:a": _doc(status="open"), "Task:b": _doc(status="closed")})
    assert len(_findings("has(status)", graph, "Task:a")) == 1


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_eval_without_subject_returns_all_domain_documents():
    graph = _graph(
        {"Task:a": _doc(status="open"), "Task:b": _doc(status="closed"), "Task:c": _doc()}
    )
    findings = _findings("has(status)", graph)
    assert {_value(f, "node") for f in findings} == {"Task:a", "Task:b", "Task:c"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_top_level_model_conjunction_restricts_domain():
    graph = _graph(
        {"Task:a": _doc("ChildDoc", status="open"),
         "Task:b": _doc("ChildDoc", status="closed"),
         "Task:c": _doc("OtherDoc", status="open")}
    )
    findings = _findings('model <= BaseDoc and status = "open"', graph)
    assert {_value(f, "node") for f in findings} == {"Task:a", "Task:b"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_nested_model_does_not_restrict_domain():
    graph = _graph(
        {"Task:a": _doc("ChildDoc", status="open"),
         "Task:b": _doc("OtherDoc", status="closed"),
         "Task:c": _doc("OtherDoc")}
    )
    findings = _findings("has(status) or model <= BaseDoc", graph)
    assert {_value(f, "node") for f in findings} == {"Task:a", "Task:b", "Task:c"}


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_two_top_level_model_constraints_intersect_domain():
    graph = _graph(
        {"Task:a": _doc("OnlyOne", status="open"),
         "Task:b": _doc("OnlyTwo", status="open"),
         "Task:c": _doc("Both", status="open")}
    )
    findings = _findings("model <= BaseOne and model <= BaseTwo", graph)
    assert {_value(f, "node") for f in findings} == {"Task:c"}


# --- (e) contract hash ------------------------------------------------------------------

class _NoContract:
    pass


class _EmptyContract:
    __contract__: list[str] = []


class _TwoFieldContract:
    __contract__ = ["title", "goal"]


class _Utf8Contract:
    __contract__ = ["á", "z", "A"]


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_contract_absent_uses_all_payload_fields():
    field_hashes = {"title": "t", "goal": "g"}
    assert _contract_hash(_NoContract, field_hashes) == _expected_contract(
        ["title", "goal"], field_hashes
    )


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_contract_empty_list_is_load_error():
    with pytest.raises(ValueError):
        _contract_hash(_EmptyContract, {"title": "t"})


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_contract_absent_field_contributes_empty_hash():
    field_hashes = {"title": "t"}
    assert _contract_hash(_TwoFieldContract, field_hashes) == _expected_contract(
        ["title", "goal"], field_hashes
    )


@pytest.mark.xfail(strict=True, reason="GO05: lenguaje de reglas no implementado")
def test_contract_order_is_utf8_bytes():
    field_hashes = {"A": "a", "z": "z", "á": "aacute"}
    assert _contract_hash(_Utf8Contract, field_hashes) == _expected_contract(
        ["á", "z", "A"], field_hashes
    )
