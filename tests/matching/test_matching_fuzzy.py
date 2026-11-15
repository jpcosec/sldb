"""Emparejamiento difuso de la etiqueta de un nodo con un atomo, por titulo y alias.

Prueba nueva de sldb (en spec2viz lo hacia el template en el navegador, `findAtomData`): no hay
matcher propio, el ranking es `DocumentIndex.rank` sobre `Matcher`/`DifflibMatcher`.
"""
from sldb.api.matching import DocumentIndex, Matcher, alias_candidates, atom_index_items, rank_atoms


def _entry(title, atom_id, tags=(), body="b"):
    return {"title": title, "aliases": alias_candidates(title, list(tags)), "atoms": {"what": {"id": atom_id, "body": body, "tags": list(tags)}}}


DB = {
    "evaluación de órdenes": _entry("Evaluación de órdenes", "a-eval"),
    "homologación de producto": _entry("Homologación de producto", "a-homo", ["proceso:alta-proveedor"]),
}


def test_node_label_ranks_its_atom_first_ignoring_accents_and_case(tmp_path):
    ranked = rank_atoms(DB, "EVALUACION DE ORDENES", tmp_path / "index.json")
    assert ranked[0][0] == "a-eval" and ranked[0][1] > ranked[1][1]
    assert [key for key, _ in rank_atoms(DB, "Homologacion producto", tmp_path / "index.json", k=1)] == ["a-homo"]


def test_tag_alias_matches_and_threshold_drops_unrelated(tmp_path):
    # "alta proveedor" solo esta en los alias por etiqueta del atomo de homologacion
    assert rank_atoms(DB, "alta proveedor", tmp_path / "index.json")[0][0] == "a-homo"
    assert rank_atoms(DB, "zzzz", tmp_path / "index.json", threshold=0.6) == []


def test_ranking_goes_through_document_index(tmp_path):
    cache = tmp_path / "index.json"
    rank_atoms(DB, "evaluacion", cache)
    index = DocumentIndex(Matcher(), cache)
    assert index.keys() == ["a-eval", "a-homo"]
    assert index.index(atom_index_items(DB)) == {"embedded": 0, "reused": 2, "dropped": 0}
