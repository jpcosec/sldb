"""`atoms: [id]` por elemento del spec -> vinculacion explicita, alias y filtro por tags.

Portado de spec2viz (`tests/test_explicit_atoms.py`, `tests/test_atoms_matching.py` y los de
`parse_atoms` de `tests/test_deskops.py`) contra las funciones puras de `sldb.api.matching`: la
vista es un `SpecView` con el spec ya cargado y los atomos salen de `--atoms-dir` (sin store), en
vez de construir el HTML del catalogo.
"""
import json
from pathlib import Path

import pytest
import yaml

from sldb.api.matching import (
    SpecView, UnknownAtomError, alias_candidates, build_explicit_atoms, filter_atoms_payload, label_key, parse_atoms, raw_atoms_by_view,
)


def _atom(d: Path, atom_id: str, title: str, q="what"):
    (d / f"{atom_id}.md").write_text(
        f"---\ntitle: {title}\nfive_wh_one_plus: {q}\nid: {atom_id}\n---\nCuerpo de {atom_id}.\n", encoding="utf-8"
    )


def _project(tmp_path, state_atoms_a, state_atoms_b):
    atoms = tmp_path / "atoms"
    atoms.mkdir()
    _atom(atoms, "atom-uno", "Uno")
    _atom(atoms, "atom-dos", "Dos", "why")
    _atom(atoms, "atom-ruido", "Otro tema")
    spec = {
        "id": "ciclo", "title": "Ciclo", "type": "state", "version": "1.0",
        "data": {
            "entity": "OC", "initial": "nueva",
            "states": [
                {"id": "nueva", "label": "4 Nueva", **({"atoms": state_atoms_a} if state_atoms_a is not None else {})},
                {"id": "cerrada", "label": "Cerrada", **({"atoms": state_atoms_b} if state_atoms_b is not None else {})},
            ],
            "transitions": [{"from": "nueva", "to": "cerrada", "on": "cierra"}],
        },
    }
    (tmp_path / "ciclo.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
    return atoms


def _build(tmp_path, atoms, strict=False):
    """Lo que `catalog build --atoms-dir` resolvia: atomos de la vista y su resolucion explicita."""
    spec = yaml.safe_load((tmp_path / "ciclo.yml").read_text(encoding="utf-8"))
    views = [SpecView(key="v1", id="v1", specs=[spec], source=str(tmp_path / "f.mmd"), base_dir=str(tmp_path))]
    raw, _ = raw_atoms_by_view(views, atoms)
    return build_explicit_atoms(views, raw, strict=strict)


def test_build_exposes_explicit_map_by_label_and_id(tmp_path):
    atoms = _project(tmp_path, ["atom-uno", "atom-dos"], None)
    explicit, _complete, findings, _linked = _build(tmp_path, atoms)
    assert findings == []
    view = explicit["v1"]
    assert [a["id"] for a in view["4 nueva"]["list"]] == ["atom-uno", "atom-dos"]
    assert [a["id"] for a in view["nueva"]["list"]] == ["atom-uno", "atom-dos"]
    assert "cerrada" not in view


def test_unknown_atom_is_warning_unless_strict(tmp_path):
    atoms = _project(tmp_path, ["atom-uno", "no-existe"], None)
    explicit, _complete, findings, _linked = _build(tmp_path, atoms)
    assert [(f.level, f.code) for f in findings] == [("warning", "matching/unknown-atom"), ("warning", "matching/unknown-atom")]
    assert all("no-existe" in f.what for f in findings) and findings[0].fix == "crear el átomo o corregir el id"
    assert {f.subject for f in findings} == {"v1#4 nueva", "v1#nueva"}
    assert [a["id"] for a in explicit["v1"]["4 nueva"]["list"]] == ["atom-uno"]
    with pytest.raises(UnknownAtomError) as raised:
        _build(tmp_path, atoms, strict=True)
    assert "no-existe" in str(raised.value)
    assert {f.level for f in raised.value.findings} == {"error"}


def test_fully_explicit_view_embeds_no_fuzzy_payload(tmp_path):
    atoms = _project(tmp_path, ["atom-uno"], ["atom-dos"])
    explicit, complete, _findings, _linked = _build(tmp_path, atoms)
    # la vista queda entre las completas: el catalogo no embebe payload difuso para ella
    assert complete == {"v1"}
    bodies = {a["body"] for entry in explicit["v1"].values() for a in entry["list"]}
    assert bodies == {"Cuerpo de atom-uno.", "Cuerpo de atom-dos."}


def test_partially_explicit_view_keeps_fuzzy_payload(tmp_path):
    atoms = _project(tmp_path, ["atom-uno"], None)
    _explicit, complete, _findings, _linked = _build(tmp_path, atoms)
    assert "v1" not in complete


def test_atoms_linked_from_explicit_are_embedded_one_level(tmp_path):
    atoms = _project(tmp_path, ["atom-uno"], ["atom-dos"])
    (atoms / "atom-uno.md").write_text(
        "---\ntitle: Uno\nfive_wh_one_plus: what\nid: atom-uno\n---\nVer [depende:: [[atom-ruido]]] y [[atom-lejano]].\n", encoding="utf-8")
    _atom(atoms, "atom-lejano", "Lejano")
    (atoms / "atom-ruido.md").write_text(
        "---\ntitle: Otro tema\nfive_wh_one_plus: what\nid: atom-ruido\n---\nSigue [[atom-lejano2]].\n", encoding="utf-8")
    _atom(atoms, "atom-lejano2", "Nivel dos")
    _explicit, _complete, findings, linked = _build(tmp_path, atoms)
    assert findings == []
    assert set(linked) == {"atom-ruido", "atom-lejano"}  # un nivel: no atom-lejano2


def _two_atoms(tmp_path):
    d = tmp_path / "atoms"
    d.mkdir()
    for i, (title, tags) in enumerate([("Uno", ["dominio:oc"]), ("Dos", ["dominio:stock"])]):
        (d / f"a{i}.md").write_text(
            f"---\ntitle: {title}\nfive_wh_one_plus: what\nid: a{i}\ntags: {json.dumps(tags)}\n---\nCuerpo {i}.\n",
            encoding="utf-8",
        )
    return d


def test_filter_atoms_payload_by_full_tag_or_value(tmp_path):
    payload = json.loads(parse_atoms(_two_atoms(tmp_path)))
    assert set(filter_atoms_payload(payload, ["dominio:oc"])) == {"uno"}
    assert set(filter_atoms_payload(payload, ["stock"])) == {"dos"}
    assert set(filter_atoms_payload(payload, None)) == {"uno", "dos"}
    assert filter_atoms_payload(payload, ["nada"]) == {}


def test_parse_atoms_handles_missing_dir(tmp_path):
    assert parse_atoms(tmp_path / "missing") == "{}"


def test_parse_atoms_builds_index_and_skips_bad_files(tmp_path):
    atoms_dir = tmp_path / "atoms"
    atoms_dir.mkdir()
    (atoms_dir / "good.md").write_text("---\ntitle: Architecture\nfive_wh_one_plus: what\nid: atom-1\n---\nBody text.\n", encoding="utf-8")
    (atoms_dir / "bad.md").write_text("---\n: bad yaml\n---\nBroken.\n", encoding="utf-8")
    findings = []
    payload = json.loads(parse_atoms(atoms_dir, findings))
    assert payload["architecture"]["title"] == "Architecture"
    assert "architecture" in payload["architecture"]["aliases"]
    assert payload["architecture"]["atoms"]["what"]["id"] == "atom-1"
    assert payload["architecture"]["atoms"]["what"]["body"] == "Body text."
    assert [f.code for f in findings] == ["matching/atom-parse-failed"]
    assert "Failed to parse atom" in findings[0].what


def test_aliases_by_title_and_tags():
    aliases = alias_candidates("Evaluación de órdenes", ["dominio:orden-compra", "sin-namespace"])
    assert aliases == [
        "evaluación de órdenes", "evaluación", "órdenes", "evaluación órdenes", "orden compra", "orden", "compra",
    ]


def test_label_key_matches_template_normkey():
    # normKey: minusculas, puntuacion a espacio, espacios colapsados; los acentos se conservan
    assert label_key("  HOMOLOGACIÓN de producto (R1) ") == "homologación de producto r1"
    assert label_key("4 Nueva") == "4 nueva"
