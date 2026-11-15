"""Component spec of a Python tree from `sldb.code.scan_tree` (`component_spec_from_python`).

spec2viz has no tests for its `python_ast` generator: the comparison test runs both on the same
small tree and asserts the same modules, classes and `defines` relations. Skipped without the
`[code]` extra (tree-sitter); the extra-missing alert is tested by simulating its absence.
"""
import pytest
import yaml

from sldb.api.notations import component_spec_from_python, validate_spec, write_component_spec
from sldb.cli import main
from sldb.code.runtime import available
from sldb.models.notation.diagram_specs.component import ComponentDiagram

needs_code = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")

TREE = {
    "pkg/__init__.py": "",
    "pkg/a.py": "import os\nimport json, sys as s\nfrom pkg.sub import b\nfrom . import c\nfrom .sub.b import Thing\n"
                "class A:\n    class Inner: pass\n    def m(self): pass\nif True:\n    class Hidden: pass\ndef f(): pass\nclass Z: pass\n",
    "pkg/sub/b.py": "from __future__ import annotations\nfrom pkg.a import A\nclass Thing(A): pass\n",
    "pkg/bad.py": "class Ok: pass\ndef broken(:\n",
    "other/x.py": "class X: pass\n",
}


@pytest.fixture
def tree(tmp_path):
    for rel, text in TREE.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text, encoding="utf-8")
    return tmp_path


def _defined(spec: dict) -> tuple[dict, dict, set]:
    nodes = spec["data"]["nodes"]
    pick = lambda kind: {k: v["label"] for k, v in nodes.items() if v["kind"] == kind}  # noqa: E731
    return pick("module"), pick("class"), {(e["from"], e["to"]) for e in spec["data"]["edges"] if e["relation"] == "defines"}


@needs_code
def test_matches_spec2viz_on_modules_classes_and_defines(tree):
    python_ast = pytest.importorskip("spec2viz.generators.python_ast")
    spec, findings = component_spec_from_python(tree)
    validate_spec(ComponentDiagram.model_validate(spec))
    assert _defined(spec) == _defined(python_ast.generate_python_ast_spec(tree))
    assert _defined(spec)[1] == {"class_pkg_a_A": "A", "class_pkg_a_Z": "Z", "class_pkg_sub_b_Thing": "Thing", "class_other_x_X": "X"}
    assert [(f.level, f.code, f.subject) for f in findings] == [("alert", "component-spec/syntax-error", "pkg/bad.py")]


@needs_code
def test_imports_are_resolved_and_undeclared_targets_are_external(tree):
    spec, _ = component_spec_from_python(tree, project_id="p", title="P", root_package="pkg")
    imports = {(e["from"], e["to"]) for e in spec["data"]["edges"] if e["relation"] == "imports"}
    assert ("module_pkg_a", "module_pkg_sub_b") in imports  # `from .sub.b import Thing`, relativo resuelto
    assert {("module_pkg_a", "module_os"), ("module_pkg_a", "module_json"), ("module_pkg_a", "module_sys")} <= imports
    assert spec["data"]["nodes"]["module_os"] == {"label": "os", "kind": "external"}
    assert "module_other_x" not in spec["data"]["nodes"] and spec["id"] == "p"
    validate_spec(ComponentDiagram.model_validate(spec))


@needs_code
def test_write_component_spec_and_cli_python(tree, tmp_path, capsys):
    out = tmp_path / "out" / "arch.yml"
    assert main(["notations", "from-graph", "--python", str(tree), "--id", "arch", "--output", str(out)]) == 0
    assert "Generated" in capsys.readouterr().out
    spec, _ = component_spec_from_python(tree, project_id="arch", title="arch AST Architecture")
    assert yaml.safe_load(out.read_text(encoding="utf-8")) == spec
    write_component_spec(spec, tmp_path / "again.yml")
    assert (tmp_path / "again.yml").read_text(encoding="utf-8") == out.read_text(encoding="utf-8")


def test_without_code_extra_returns_the_alert_and_writes_nothing(tree, tmp_path, monkeypatch, capsys):
    import sldb.api.notations.component_spec_python as gen

    monkeypatch.setattr(gen, "available", lambda: False)
    spec, findings = component_spec_from_python(tree)
    assert spec is None
    assert [f.as_dict() for f in findings] == [{"level": "alert", "code": "component-spec/code-extra-missing", "subject": str(tree),
                                                "what": "no hay tree-sitter", "fix": "pip install 'structuredLanguageDB[code]'", "document": None}]
    assert main(["notations", "from-graph", "--python", str(tree), "--output", str(tmp_path / "x.yml")]) == 1
    assert "component-spec/code-extra-missing" in capsys.readouterr().err and not (tmp_path / "x.yml").exists()
