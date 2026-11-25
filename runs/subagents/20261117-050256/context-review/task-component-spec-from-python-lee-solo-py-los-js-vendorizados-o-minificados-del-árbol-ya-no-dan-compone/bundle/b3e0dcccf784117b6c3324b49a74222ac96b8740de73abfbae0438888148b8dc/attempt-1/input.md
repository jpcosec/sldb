FILE:desk/tasks/task-component-spec-from-python-lee-solo-py-los-js-vendorizados-o-minificados-del-árbol-ya-no-dan-compone.md
---
sldb:
  by: agent
  at: '2026-11-17T01:33:28Z'
  authority: generated
  via: create_document
id: task-component-spec-from-python-lee-solo-py-los-js-vendorizados-o-minificados-del-árbol-ya-no-dan-compone
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-213452-suggestion-regresi-n-de-b2-600b51a9-component-spec-from-python-recorre-js-vendorizados-minificados-y-da-component-spec-syntax-error-rompe-2-pruebas-de-ir.md
depends_on: []
pills: []
files:
- src/sldb/api/notations/component_spec_python.py
- tests/notations/test_component_spec_python.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# component_spec_from_python lee solo .py: los .js vendorizados o minificados del árbol ya no dan component-spec/syntax-error (regresión de B2)

## Rationale

_Explain why this task exists or the business driver behind it._

Desde 600b51a9 (B2, sldb.code lee TS, TSX, JS y JSX), scan_tree recorre también .ts/.tsx/.js/.jsx, y component_spec_from_python (src/sldb/api/notations/component_spec_python.py) usa scan_tree. En IR, un .js vendorizado y minificado (bpmn-js production.min.js) produce un hallazgo component-spec/syntax-error y fallan, de forma determinista, dos pruebas de paridad de IR que exigen findings == []. Origen: desk/inbox/20261116-213452-suggestion-regresi-n-de-b2-600b51a9-component-spec-from-python-recorre-js-vendorizados-minificados-y-da-component-spec-syntax-error-rompe-2-pruebas-de-ir.md.

## Goal

_Describe the concrete result this task must produce._

component_spec_from_python construye el spec solo a partir de los archivos .py del árbol, como antes de B2; ningún archivo de otro lenguaje produce hallazgos en ese spec.

## Scope

_State what is in scope and what is out of scope._

Entra: que component_spec_from_python escanee solo .py (filtrar por extensión los archivos que recorre, o pedir a sldb.code un escaneo limitado a Python con la API que ya existe), sin cambiar scan_tree para los demás consumidores (code_facts, anclas). Test en tests/notations/test_component_spec_python.py: un árbol con un paquete Python y un .js minificado ilegible da el mismo spec y cero hallazgos que el árbol sin el .js. CHANGELOG. No entra: excluir vendor/ o *.min.js de scan_tree en general.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer component_spec_python.py y sldb.code.scan (scan_tree, scan_file) y files.py (find_files). 2) Limitar el recorrido a .py en el generador. 3) Test. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_graph.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con el test nuevo; el spec de src/sldb no cambia respecto de HEAD; CHANGELOG y commit; aviso a IR.

FILE:desk/rituals/execution.md
---
# ritual-xxx
id: ritual-execution
# Ordered prose steps; not document references
steps:
- 'Atomize: break the work into the smallest possible child tasks.'
- 'Dedupe: merge overlapping items.'
- 'Clean: delete legacy content that the work makes obsolete (with deskops retire,
  closeout or drawer remove, never by hand).'
- 'Audit existing work before claiming anything is done: check git history for relevant
  commits, verify artifacts exist where specified, and run tests to confirm the current
  state.'
- Resolve contradictory end states between the desk and the repo.
- Bind the pills the task depends on (the task's pills field or deskops bind).
- Keep the Board current; deskops maintains it, so use deskops verbs instead of editing
  it.
- 'Execute with explicit boundaries: scope, touched files and validation targets stated
  in the task.'
- 'After each step, run the context audit: is every aspect of the task covered by
  a pill, are the bound pills still accurate, update or retire the stale ones, and
  bind new ones as needed.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Execution ritual

## Purpose

_Explain why this ritual exists._

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for sldb.

## Trigger

_State when this ritual should start._

Before starting any task, and after each step while implementing it.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-execution gate: ask whether any aspect of the task is ambiguous or not covered by its task file, pills and atoms. If not, proceed. If so, create or request the missing context first; do not proceed until the task is unambiguous.
- The Board (desk/tasks/Board.md) is the single entry point for active work: read it before starting any task.

## Validation

_List the checks that prove the ritual was performed correctly._

- Scope, touched files and validation targets are explicit in the task.
- Every desk reference points at durable repo context: task files, pills, atoms, drawer notes, inbox messages, source files, tests, docs and commits.

## Failure Modes

_List common mistakes this ritual prevents._

- Proceeding with an ambiguous task without creating or requesting the missing context.
- Creating implementation artifacts instead of referencing existing pills.
- Referencing surfaces below the current layer.
- Desk documents pointing at chat memory or other non-durable context.
- Trusting the task file over the code: the task file describes intent; git history is truth.

## Completion

_Describe what completion looks like._

The task's change is implemented within its stated scope and the testing ritual can start.

FILE:desk/rituals/testing.md
---
# ritual-xxx
id: ritual-testing
# Ordered prose steps; not document references
steps:
- 'Invalidate: check whether existing tests are broken by the change; update or delete
  the ones that no longer describe the behavior.'
- 'Verify: add new tests where the change needs them.'
- 'Test: run the relevant test or validation suite, smallest first, then the full
  suite when shared behavior changed. All required checks must pass.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Testing ritual

## Purpose

_Explain why this ritual exists._

No task is complete without testing. Run the smallest relevant validation first, then broaden coverage when sldb changes shared behavior.

## Trigger

_State when this ritual should start._

When the implementation of a task is done, before closeout.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- All required checks pass: the test suite, plus stores check, tools/check.sh and tools/check_claims.py when the change touches the store, the gates or documented claims.

## Failure Modes

_List common mistakes this ritual prevents._

- Skipping tests to get it done.
- Declaring a check green from truncated output (a pipe through tail hides the exit status).

## Completion

_Describe what completion looks like._

Every required check passes on the final change.

FILE:desk/rituals/closeout.md
---
# ritual-xxx
id: ritual-closeout
# Ordered prose steps; not document references
steps:
- Update the CHANGELOG when the change is user-visible or release-relevant.
- 'Run the context audit: check the task''s pills, update stale ones, and retire the
  ones whose knowledge now lives in code or docs.'
- 'Close the task with deskops closeout (commit, or supersede/retire when it was already
  resolved): the task leaves the Board in the same atomic commit as its evidence.
  Completed tasks are not kept on the Board.'
- 'Commit atomically, only when the execution ritual is complete. Commit when a phase
  or slice objective is fully checked (a concise scoped message), for a critical bug
  fix mid-phase (fix(<scope>): <description>), or for chores such as dependencies
  or config (chore(<scope>): <description>). A slice that is not done is not a commit:
  work in progress is not committed.'
- 'Write commit messages as <type>(<scope>): <description>, with type one of feat,
  fix, docs, refactor, chore, test, perf, and scope the smallest accurate repo area,
  component, command or workflow surface.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Closeout ritual

## Purpose

_Explain why this ritual exists._

Close a sldb task only after validation passes, the board is updated, and the final change is ready to commit.

## Trigger

_State when this ritual should start._

When the testing ritual passes for a task.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-completion audit, git history: the commits match the completed work; on a mismatch, correct the commit history or update the task state to reflect reality.
- Pre-completion audit, artifacts: every specified output exists at the specified location; implement the missing ones.
- Pre-completion audit, tests: all pass; fix failing tests first.
- Pre-completion audit, clean tree: every untracked file is either gitignored or tracked; clean up a dirty tree before declaring done.
- Trust the code, not the task file: the task file describes intent, git history is truth.

## Validation

_List the checks that prove the ritual was performed correctly._

- deskops closeout verify reports the tests, commit and atom gates as passing, and the tree is clean.

## Failure Modes

_List common mistakes this ritual prevents._

- Marking a task complete without auditing git history.
- Committing with untracked files (gitignore or track them first).
- Force-pushing to hide failures.
- Committing work in progress.

## Completion

_Describe what completion looks like._

The closing commit exists, the task is off the Board, and the tree is clean.

FILE:desk/rituals/phase.md
---
# ritual-xxx
id: ritual-phase
# Ordered prose steps; not document references
steps:
- 'Compile: rebuild when applicable (bundles, dist).'
- 'Audit: run the relevant tests and quality checks.'
- 'Regress: fix any test failure.'
- 'Flow: move the pill knowledge that is still needed into code or docs, capture phase-level
  learning into an atom, and retire the redundant pills.'
- 'Advance: clear the Board for the next phase and move on.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Phase ritual

## Purpose

_Explain why this ritual exists._

Close the active phase only when every task on the sldb board is complete, capture any phase-level learning into an atom, and clear the board for the next phase.

## Trigger

_State when this ritual should start._

When every task in a phase or delivery slice is done.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- Tests and quality checks pass and no pill repeats what code or docs already say.

## Failure Modes

_List common mistakes this ritual prevents._

- 

## Completion

_Describe what completion looks like._

The Board holds only the next phase's tasks.

FILE:src/sldb/api/notations/component_spec_python.py
"""The component spec of a Python tree, from the facts of `sldb.code.scan_tree`.

Replaces spec2viz's `generate_python_ast_spec` without its own `ast` walk: the modules, their
top-level classes and their imports come from `sldb.code`, the only place that reads Python.
A node `module` per module (`__init__.py` skipped), `class` per top-level class, `defines`
from module to class, `imports` per resolved imported module (top-level and nested imports,
one edge per pair), and `external` for undeclared targets.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.notations.component_spec_findings import code_extra_missing, syntax_error
from sldb.api.notations.component_spec_python_build import _build_spec, _sanitize_id
from sldb.code.runtime import available
from sldb.code.scan import scan_tree
from sldb.core.finding import Finding


def component_spec_from_python(src_dir: str | Path, project_id: str = "project", title: str = "Python AST Architecture",
                               root_package: str | None = None) -> tuple[dict | None, list[Finding]]:
    """`(spec, findings)` for every `.py` under `src_dir`; `(None, [alert])` without the `[code]` extra."""
    if not available():
        return None, [code_extra_missing(src_dir)]
    elements: list[dict] = []
    relations: list[dict] = []
    findings: list[Finding] = []
    for module, classes in _modules(scan_tree(Path(src_dir)), root_package):
        findings += _module_elements(module, classes, elements, relations)
    return _build_spec(project_id, title, elements, relations), findings


def _modules(facts: list[dict], root_package: str | None) -> list[tuple[dict, list[dict]]]:
    """Each wanted module fact in path order, with its top-level class facts in source order."""
    classes: dict[str, list[dict]] = {}
    for fact in facts:
        if fact["kind"] == "class" and "." not in fact["qualified_name"]:
            classes.setdefault(fact["path"], []).append(fact)
    modules = sorted((f for f in facts if f["kind"] == "module" and _wanted(f["path"], root_package)), key=lambda f: tuple(f["path"].split("/")))
    return [(m, sorted(classes.get(m["path"], []), key=lambda c: c["span"]["start_line"])) for m in modules]


def _wanted(path: str, root_package: str | None) -> bool:
    return path.rsplit("/", 1)[-1] != "__init__.py" and (not root_package or path.startswith(root_package.replace(".", "/")))


def _module_elements(module: dict, classes: list[dict], elements: list[dict], relations: list[dict]) -> list[Finding]:
    """Elements and relations of one module; an unparsable file keeps only its module node."""
    name = module["qualified_name"]
    safe_id = f"module_{_sanitize_id(name)}"
    elements.append({"id": safe_id, "kind": "module", "label": name})
    if module["attrs"].get("has_error"):
        return [syntax_error(module["path"])]
    _class_elements(name, safe_id, classes, elements, relations)
    relations += [{"source": safe_id, "target": f"module_{_sanitize_id(t)}", "kind": "imports"} for t in _imports(name, module["attrs"]["imports"] + module["attrs"].get("nested_imports", []))]
    return []


def _class_elements(name: str, safe_id: str, classes: list[dict], elements: list[dict], relations: list[dict]) -> None:
    for cls in classes:
        cls_id = f"class_{_sanitize_id(name)}_{cls['name']}"
        elements.append({"id": cls_id, "kind": "class", "label": cls["name"]})
        relations.append({"source": safe_id, "target": cls_id, "kind": "defines"})


def _imports(module: str, imports: list[str]) -> list[str]:
    """Each imported module once, in first-seen order, relative ones resolved against `module`'s package."""
    targets = [_resolve(module, name) for entry in imports for name in entry.split(",")]
    return list(dict.fromkeys(t for t in targets if t))


def _resolve(module: str, target: str) -> str | None:
    if not target.startswith("."):
        return target
    level = len(target) - len(target.lstrip("."))
    rest = target[level:]
    return ".".join(module.split(".")[:-level] + ([rest] if rest else [])) or None

FILE:tests/notations/test_component_spec_python.py
"""Component spec of a Python tree from `sldb.code.scan_tree` (`component_spec_from_python`).

Parity with spec2viz's `python_ast` generator is checked against a frozen golden
(`goldens/component_spec_python_spec2viz.json`: its modules, classes and `defines` on TREE, generated once
from the spec2viz commit in `_source`), so the test runs without spec2viz installed. Skipped without the
`[code]` extra (tree-sitter); the extra-missing alert is tested by simulating its absence.
"""
import json
from pathlib import Path

import pytest
import yaml

from sldb.api.notations import component_spec_from_python, validate_spec, write_component_spec
from sldb.cli import main
from sldb.code.runtime import available
from sldb.models.notation.diagram_specs.component import ComponentDiagram

needs_code = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")
SPEC2VIZ_GOLDEN = Path(__file__).parent / "goldens" / "component_spec_python_spec2viz.json"

TREE = {
    "pkg/__init__.py": "",
    "pkg/a.py": "import os\nimport json, sys as s\nfrom pkg.sub import b\nfrom . import c\nfrom .sub.b import Thing\n"
                "class A:\n    class Inner: pass\n    def m(self): pass\nif True:\n    class Hidden: pass\ndef f(): pass\nclass Z: pass\n",
    "pkg/sub/b.py": "from __future__ import annotations\nfrom pkg.a import A\nclass Thing(A): pass\n",
    "pkg/bad.py": "class Ok: pass\ndef broken(:\n",
    "pkg/lazy.py": "def f():\n    from pkg.sub import b\nif False:\n    import json\n",
    "pkg/typed.py": "import os\nfrom typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    from pkg.a import A\n    import os\n"
                    "def g():\n    import os\n    from .sub.b import Thing\n",
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
    golden = json.loads(SPEC2VIZ_GOLDEN.read_text(encoding="utf-8"))
    spec, findings = component_spec_from_python(tree)
    validate_spec(ComponentDiagram.model_validate(spec))
    modules, classes, defines = _defined(spec)
    assert {"modules": modules, "classes": classes, "defines": sorted(map(list, defines))} == {k: golden[k] for k in ("modules", "classes", "defines")}
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
def test_nested_imports_draw_one_edge_per_pair(tree):
    spec, _ = component_spec_from_python(tree, root_package="pkg")
    edges = [(e["from"], e["to"]) for e in spec["data"]["edges"] if e["relation"] == "imports"]
    # `from pkg.sub import b` names the module `pkg.sub`, like the same import at the top level of pkg/a.py
    assert ("module_pkg_lazy", "module_pkg_sub") in edges and ("module_pkg_lazy", "module_json") in edges  # en def y bajo if
    typed = [t for s, t in edges if s == "module_pkg_typed"]
    assert sorted(typed) == ["module_os", "module_pkg_a", "module_pkg_sub_b", "module_typing"]  # TYPE_CHECKING, def, relativo; os una vez
    assert len(edges) == len(set(edges))
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

FILE:instruccion
Cold-bundle de la tarea task-component-spec-from-python-lee-solo-py-los-js-vendorizados-o-minificados-del-árbol-ya-no-dan-compone: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_graph.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

