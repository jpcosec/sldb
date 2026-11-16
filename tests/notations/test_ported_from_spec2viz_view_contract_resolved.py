"""Portado de spec2viz tests/test_view_contract_resolved.py: el contrato de render que resuelve
`resolve_view` no lleva placeholders `{campo}` sin resolver; cada plantilla de la notacion
(rotulo, estereotipo, rotulos de extremo) llega interpolada.

Los specs de spec2viz/tests/fixtures ya existian identicos en tests/fixtures/specs/; los del repo
de spec2viz (docs/architecture/spec2viz/*.yml) estan copiados con su nombre en
tests/notations/fixtures/docs/architecture/spec2viz/.

Casos no portados: ninguno.
"""
import re
import shutil
from pathlib import Path

import pytest

import sldb.api as sldb_api
from sldb.api.notations import SpecSync, render_keyword, resolve_view

FIXTURES = Path(__file__).parent.parent / "fixtures" / "specs"
REPO_SPECS = Path(__file__).parent / "fixtures" / "docs" / "architecture" / "spec2viz"
PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_.]+\}")
SPECS = [
    FIXTURES / "deployment.nested.yml", FIXTURES / "deployment.runtime.yml", FIXTURES / "activity.lanes.yml",
    FIXTURES / "component.styled.yml", REPO_SPECS / "state-diagram-sync-lifecycle.yml",
    REPO_SPECS / "sequence-sync-pipeline.yml", REPO_SPECS / "class-sldb-models.yml",
]


def _strings(value, path="view"):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from _strings(v, f"{path}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _strings(v, f"{path}[{i}]")


def _unresolved(view):
    # `data` es el payload del documento tal cual; las plantillas resueltas son el resto
    return [(p, s) for p, s in _strings({k: v for k, v in view.items()}) if ".data." not in p and PLACEHOLDER.search(s)]


@pytest.mark.parametrize("spec", SPECS, ids=lambda p: p.stem)
def test_no_placeholder_reaches_the_render_contract(tmp_path, spec):
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    copy = shutil.copy(spec, tmp_path / "docs" / spec.name)
    report = SpecSync(tmp_path / ".sldb").sync(Path(copy))
    view = resolve_view(tmp_path / ".sldb", report.spec_id)
    assert _unresolved(view) == []


def test_deployment_keyword_interpolates_kind_and_drops_when_empty(tmp_path):
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    copy = shutil.copy(FIXTURES / "deployment.nested.yml", tmp_path / "docs" / "nested.yml")
    SpecSync(tmp_path / ".sldb").sync(Path(copy))
    nodes = {n["element"]: n for n in resolve_view(tmp_path / ".sldb", "deployment.nested")["nodes"]}
    assert nodes["db"]["keyword"] == "«database»" and nodes["api_image"]["keyword"] == "«image»"
    assert render_keyword("«{kind}»", {"kind": ""}) == "" and render_keyword("«{kind}»", {}) == ""
    assert render_keyword("«interface»", {}) == "«interface»" and render_keyword("", {"kind": "x"}) == ""
