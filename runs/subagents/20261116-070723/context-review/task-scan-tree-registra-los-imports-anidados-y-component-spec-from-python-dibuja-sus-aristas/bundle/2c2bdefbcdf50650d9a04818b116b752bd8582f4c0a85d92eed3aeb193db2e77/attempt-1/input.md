FILE:desk/tasks/task-scan-tree-registra-los-imports-anidados-y-component-spec-from-python-dibuja-sus-aristas.md
---
sldb:
  by: agent
  at: '2026-11-16T05:49:06Z'
  authority: generated
  via: save_document_payload
id: task-scan-tree-registra-los-imports-anidados-y-component-spec-from-python-dibuja-sus-aristas
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-203456-suggestion-code-scan-tree-nested-imports-component-spec-from-python-no-ve-los-from-imports-anidados.md
depends_on: []
pills: []
files:
- src/sldb/code/imports.py
- src/sldb/code/scan.py
- src/sldb/api/notations/component_spec_python.py
- tests/notations/test_component_spec_python.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-inventario-de-código-de-sldb-se-publica-como-hechos-de-fuente-y-cada-consumidor-los-proyecta
---

# scan_tree registra los imports anidados y component_spec_from_python dibuja sus aristas

## Rationale

_Explain why this task exists or the business driver behind it._

component_spec_from_python (src/sldb/api/notations/component_spec_python.py) arma las aristas imports del spec de componentes con attrs.imports de sldb.code.scan_tree, que solo trae las sentencias del nivel superior del módulo (py_imports en src/sldb/code/imports.py recorre root.named_children). spec2viz recorría todo el árbol y veía los imports dentro de funciones, if o try (imports perezosos, TYPE_CHECKING). En IR, specir/visual/commands.py importa compilers y lint_mermaid dentro de funciones y esas aristas faltan: el diagrama pierde dependencias reales. Origen: desk/inbox/20261115-203456-suggestion-code-scan-tree-nested-imports-component-spec-from-python-no-ve-los-from-imports-anidados.md.

## Goal

_Describe the concrete result this task must produce._

El spec de componentes generado desde Python incluye una arista imports por cada import anidado (dentro de def, class, if, try o with) además de los de nivel superior, sin cambiar los hechos de código (facts.rels) que ya consumen attrs.imports.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/code/imports.py una función que recorre el árbol completo y devuelve los imports anidados; en src/sldb/code/scan.py (líneas 58-61, donde se guarda attrs.imports) guardar esos imports en un attr aparte attrs.nested_imports, para no cambiar attrs.imports ni los facts que lo usan; en src/sldb/api/notations/component_spec_python.py (_module_elements línea 55, _imports línea 72) emitir aristas imports también desde nested_imports, deduplicadas contra las de nivel superior. Tests en tests/notations/test_component_spec_python.py (un módulo con import dentro de una función y otro bajo if TYPE_CHECKING producen la arista) y en tests/selfdoc/test_treesitter_symbols.py (attrs.imports no cambia; nested_imports aparece). CHANGELOG.md. No entra: marcar las aristas con estilo distinto en los renderers, cambiar facts.rels, ni el oráculo de paridad con spec2viz (tarea aparte del golden).

Precisiones (preflight-1): una sola arista imports por par (módulo fuente, módulo destino), aunque el destino se importe en varias funciones o también en el nivel superior; "anidado" es toda sentencia import o from-import que no es hijo directo del nodo module del árbol de tree-sitter, incluidas las que están dentro de if TYPE_CHECKING, try, def, class o with en el nivel del módulo. Test nuevo en tests/notations/test_component_spec_python.py: agregar al dict TREE un módulo "pkg/lazy.py" con "def f():\n    from pkg.sub import b\nif False:\n    import json\n" y comprobar que ("module_pkg_lazy", "module_pkg_sub_b") y ("module_pkg_lazy", "module_json") están en las aristas imports.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/code/imports.py (py_imports, línea 18) y src/sldb/code/scan.py 50-70. 2) Agregar py_nested_imports(root) que hace un recorrido completo y excluye los nodos hijos directos del módulo. 3) Guardar attrs["nested_imports"] en scan.py. 4) En component_spec_python.py unir imports y nested_imports al construir las aristas, sin duplicados. 5) Tests y CHANGELOG. Requiere el extra [code] (tree-sitter-python) instalado.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm pytest -q tests/selfdoc/test_treesitter_symbols.py

## Done When

_Name the observable condition that makes the task complete._

Los dos archivos de test pasan con los casos nuevos (import en función e import bajo TYPE_CHECKING generan arista imports; attrs.imports igual que antes); CHANGELOG con la entrada; commit con los archivos de Files.

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

FILE:desk/atoms/atom-el-inventario-de-código-de-sldb-se-publica-como-hechos-de-fuente-y-cada-consumidor-los-proyecta.md
---
id: atom-el-inventario-de-código-de-sldb-se-publica-como-hechos-de-fuente-y-cada-consumidor-los-proyecta
title: El inventario de código de sldb se publica como hechos de fuente, y cada consumidor
  los proyecta
five_wh_one_plus: how
tags:
- system:sldb
- topic:selfdoc
provenance: docs/architecture/code-docstring-indexing.spec.md
---

# El inventario de código de sldb se publica como hechos de fuente, y cada consumidor los proyecta

## Answer

sldb selfdoc escanea su propio código sin importarlo. Hay dos salidas: documentos PythonSymbolDoc y CliCommandDoc trackeados en el store (knowledge/), y un grafo de fuente regenerable (.sldb/runtime/graphs/python-source.graph.json) con contains, imports (siguiendo re-exports, con via) y references, con su evidencia. La metadata de un docstring (id, kind, tags) se lee estricta y sus errores frenan la escritura; los tags se heredan por la cadena léxica con su origen. python-check dice si todo está al día. Un consumidor proyecta esos hechos sin reinterpretarlos: spec2viz diagram from-graph --module-prefix … arma un diagrama válido. Spec: docs/architecture/code-docstring-indexing.spec.md.

FILE:src/sldb/code/imports.py
"""A module's name from its path, and the imports its top level declares (from kimun's adapter)."""

from __future__ import annotations

import os
from typing import Any

from sldb.code.readers import field_text, text


def py_module_name(rel: str) -> str:
    parts = rel[:-len(os.path.splitext(rel)[1])].split("/")
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def py_imports(root: Any, src: bytes) -> set[str]:
    out: set[str] = set()
    for stmt in root.named_children:
        if stmt.type == "import_statement":
            out.add(_import_names(stmt, src))
        elif stmt.type == "future_import_statement":
            out.add("__future__")
        elif stmt.type == "import_from_statement":
            out.add("".join(field_text(stmt, src, "module_name").split()))
    return out


def _import_names(stmt: Any, src: bytes) -> str:
    names = [field_text(c, src, "name") if c.type == "aliased_import" else text(c, src) for c in stmt.children_by_field_name("name")]
    return ",".join("".join(n.split()) for n in names)

FILE:src/sldb/code/scan.py
"""Scan Python files into symbol facts: module, classes, functions and methods, each with its
qualified name, span, docstring, signature and fingerprints (from kimun's adapter).

A definition under `if`, `try` or any statement other than a class or function body is not
a symbol (its owner chain is not a chain of definitions), exactly like `ast`-based scanners.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from sldb.code.facts import fact, key_of, rels
from sldb.code.fingerprints import fingerprints
from sldb.code.ids import Ids
from sldb.code.imports import py_imports, py_module_name
from sldb.code.readers import field_text, py_doc, py_end_line, py_native_kind, py_signature
from sldb.code.runtime import parse, runtime

QUERY = "(class_definition) @class (function_definition) @function"
_TRANSPARENT = {"block", "decorated_definition"}


def scan_tree(root: Path) -> list[dict[str, Any]]:
    """Every `.py` under `root`, facts sorted by id; one id space for the whole tree."""
    idgen, facts = Ids(), []
    for rel in find_files(root):
        facts.extend(scan_file(rel, root, idgen))
    return sorted(facts, key=lambda f: f["id"])


def find_files(root: Path) -> list[str]:
    out = []
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        out += [os.path.relpath(os.path.join(base, f), root).replace(os.sep, "/") for f in files if f.endswith(".py")]
    return sorted(out, key=lambda r: tuple(r.split("/")))


def scan_file(rel: str, root: Path, idgen: Ids | None = None) -> list[dict[str, Any]]:
    """The facts of one file: the module first, then its definitions in source order."""
    src, idgen = (root / rel).read_bytes(), idgen or Ids()
    rootn, module = parse(src).root_node, py_module_name(rel)
    digest = "sha256:" + hashlib.sha256(src).hexdigest()
    mid = idgen.take(module or "__init__")
    facts = [_module_fact(mid, module, rel, rootn, src, digest)]
    captured = _captures(rootn)
    items = sorted(captured.values(), key=lambda cn: (cn[1].start_byte, -cn[1].end_byte))
    owners = {key_of(n): _owner_of(n, captured) for _, n in items}
    names = _qualified_names(items, owners, captured, src)
    return facts + _definition_facts(items, owners, names, captured, src, module, mid, rel, digest, idgen)


def _module_fact(mid: str, module: str, rel: str, rootn: Any, src: bytes, digest: str) -> dict[str, Any]:
    nlines = len(src.decode("utf-8", "replace").splitlines())
    imports = sorted(py_imports(rootn, src))
    return fact(id=mid, kind="module", name=module.rsplit(".", 1)[-1] if module else "__init__", qualified_name=module, path=rel,
                span={"start_line": 1, "end_line": max(nlines, 1)}, source_hash=digest, doc=py_doc(rootn, src), relations=rels(None, imports),
                attrs={"native_kind": rootn.type, "module": module, "imports": imports, "has_error": rootn.has_error}, fingerprints=fingerprints(rootn, src))


def _captures(rootn: Any) -> dict[tuple, tuple[str, Any]]:
    ts, language = runtime()
    captured = {}
    for cap, nodes in ts.QueryCursor(ts.Query(language, QUERY)).captures(rootn).items():
        for n in nodes:
            captured[key_of(n)] = (cap, n)
    return captured


def _owner_of(n: Any, captured: dict) -> Any:
    """`"root"`, the key of the owning definition, or None when something else sits between."""
    p = n.parent
    while p is not None and p.type in _TRANSPARENT:
        p = p.parent
    if p is None:
        return None
    return "root" if p.type == "module" else (key_of(p) if key_of(p) in captured else None)


def _qualified_names(items: list, owners: dict, captured: dict, src: bytes) -> dict[tuple, str | None]:
    qual: dict[tuple, str | None] = {}
    for _cap, n in items:
        _resolve(key_of(n), owners, captured, src, qual)
    return qual


def _resolve(k: tuple, owners: dict, captured: dict, src: bytes, qual: dict) -> str | None:
    if k in qual:
        return qual[k]
    o, name = owners.get(k), field_text(captured[k][1], src, "name")
    parent = None if o in (None, "root") else _resolve(o, owners, captured, src, qual)
    qual[k] = None if o is None or name is None or (o != "root" and parent is None) else (name if o == "root" else f"{parent}.{name}")
    return qual[k]


def _definition_facts(items, owners, names, captured, src, module, mid, rel, digest, idgen) -> list[dict[str, Any]]:
    ids, facts = {}, []
    for cap, n in items:
        k, q = key_of(n), names.get(key_of(n))
        if q is None:
            continue
        kind = "method" if cap == "function" and owners[k] != "root" and captured[owners[k]][0] == "class" else cap
        ids[k] = idgen.take(f"{module}.{q}" if module else q)
        facts.append(_definition_fact(n, ids[k], kind, q, mid if owners[k] == "root" else ids.get(owners[k]), src, module, rel, digest))
    return facts


def _definition_fact(n, fid, kind, q, owner_id, src, module, rel, digest) -> dict[str, Any]:
    return fact(id=fid, kind=kind, name=field_text(n, src, "name"), qualified_name=q, path=rel, span={"start_line": n.start_point[0] + 1, "end_line": py_end_line(n)},
                source_hash=digest, signature=py_signature(n, src), doc=py_doc(n, src), relations=rels(owner_id),
                attrs={"native_kind": py_native_kind(n, src), "module": module}, fingerprints=fingerprints(n, src))

FILE:src/sldb/api/notations/component_spec_python.py
"""The component spec of a Python tree, from the facts of `sldb.code.scan_tree`.

Replaces spec2viz's `generate_python_ast_spec` without its own `ast` walk: the modules, their
top-level classes and their imports come from `sldb.code`, the only place that reads Python.
A node `module` per module (`__init__.py` skipped), `class` per top-level class, `defines`
from module to class, `imports` per resolved import, and `external` for undeclared targets.
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
    relations += [{"source": safe_id, "target": f"module_{_sanitize_id(t)}", "kind": "imports"} for t in _imports(name, module["attrs"]["imports"])]
    return []


def _class_elements(name: str, safe_id: str, classes: list[dict], elements: list[dict], relations: list[dict]) -> None:
    for cls in classes:
        cls_id = f"class_{_sanitize_id(name)}_{cls['name']}"
        elements.append({"id": cls_id, "kind": "class", "label": cls["name"]})
        relations.append({"source": safe_id, "target": cls_id, "kind": "defines"})


def _imports(module: str, imports: list[str]) -> list[str]:
    """Each imported module, relative ones resolved against `module`'s package."""
    targets = [_resolve(module, name) for entry in imports for name in entry.split(",")]
    return [t for t in targets if t]


def _resolve(module: str, target: str) -> str | None:
    if not target.startswith("."):
        return target
    level = len(target) - len(target.lstrip("."))
    rest = target[level:]
    return ".".join(module.split(".")[:-level] + ([rest] if rest else [])) or None

FILE:tests/notations/test_component_spec_python.py
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

FILE:tests/selfdoc/test_treesitter_symbols.py
"""The tree-sitter symbols scanner (ported from kimun): ids, kinds, spans, docstrings, signatures.
Skipped without the `[code]` extra."""
from __future__ import annotations

from pathlib import Path

import pytest

from sldb.code.runtime import available

pytestmark = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")

SOURCE = '''"""Mod doc."""
import os, sys as s
from . import x
from ..a import b
from __future__ import annotations


@deco
async def top(a, b: int = 1, *rest, c="q"):
    """Top.

        Indented.
    """
    def inner(): pass


class K:
    "k doc"

    def m(self): pass

    class N:
        def d(self):
            # trailing comment
            return 1

# trailing comment after class
if True:
    def hidden(): pass
'''


@pytest.fixture
def facts(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "pkg" / "mod.py").write_text(SOURCE, encoding="utf-8")
    return {f["id"]: f for f in scan_tree(tmp_path)}


def test_ids_kinds_and_spans(facts):
    assert sorted(facts) == ["pkg", "pkg.mod", "pkg.mod.K", "pkg.mod.K.N", "pkg.mod.K.N.d", "pkg.mod.K.m", "pkg.mod.top", "pkg.mod.top.inner"]
    assert [facts[i]["kind"] for i in ("pkg.mod", "pkg.mod.top", "pkg.mod.top.inner", "pkg.mod.K", "pkg.mod.K.m")] == ["module", "function", "function", "class", "method"]
    assert facts["pkg.mod.top"]["span"] == {"start_line": 9, "end_line": 14}, "starts at `async def`, not at the decorator"
    assert facts["pkg.mod.top"]["attrs"]["native_kind"] == "AsyncFunctionDef"
    assert facts["pkg.mod.K.N.d"]["span"] == {"start_line": 23, "end_line": 25}, "a trailing comment is not part of the body"
    assert facts["pkg.mod.K"]["span"] == {"start_line": 17, "end_line": 25} and facts["pkg.mod"]["span"] == {"start_line": 1, "end_line": 29}
    assert "pkg.mod.hidden" not in facts, "a definition under `if` is not a symbol"


def test_docstrings_signatures_and_relations(facts):
    assert (facts["pkg.mod"]["doc"], facts["pkg.mod.top"]["doc"], facts["pkg.mod.K"]["doc"], facts["pkg.mod.K.m"]["doc"]) == ("Mod doc.", "Top.\n\nIndented.", "k doc", None)
    assert facts["pkg.mod.top"]["signature"] == "top(a, b: int=1, *rest, c='q')" and facts["pkg.mod.K"]["signature"] is None
    assert facts["pkg.mod.K.N.d"]["relations"] == [{"type": "contained-in", "target": "pkg.mod.K.N"}]
    assert [r["target"] for r in facts["pkg.mod"]["relations"]] == [".", "..a", "__future__", "os,sys"]
    assert facts["pkg.mod"]["source_hash"].startswith("sha256:") and facts["pkg"]["name"] == "pkg"


def test_docstring_forms_and_duplicate_ids(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "docs.py").write_text('def a():\n    r"""raw \\d"""\ndef b():\n    "x\\ty" \'z\'\ndef c():\n    f"{1}"\ndef d():\n    b"bytes"\ndef e():\n    pass\n    "late"\n', encoding="utf-8")
    (tmp_path / "dup.py").write_text("def f(): pass\ndef f(): pass\n", encoding="utf-8")
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert [facts[f"docs.{n}"]["doc"] for n in "abcde"] == ["raw \\d", "x       yz", None, None, None]
    assert "dup.f" in facts and "dup.f~2" in facts


def test_without_the_runtime_the_error_names_the_extra(monkeypatch):
    import sldb.code.runtime as rt

    monkeypatch.setattr(rt, "_RUNTIME", [])
    monkeypatch.setattr(rt.importlib, "import_module", lambda name: (_ for _ in ()).throw(ImportError(name, name=name)))
    with pytest.raises(rt.TreeSitterUnavailable, match=r"\[code\]"):
        rt.runtime()
    assert not rt.available()

FILE:instruccion
Cold-bundle de la tarea task-scan-tree-registra-los-imports-anidados-y-component-spec-from-python-dibuja-sus-aristas: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm pytest -q tests/selfdoc/test_treesitter_symbols.py

