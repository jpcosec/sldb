FILE:desk/tasks/task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam.md
---
sldb:
  by: agent
  at: '2026-11-17T00:25:41Z'
  authority: generated
  via: create_document
id: task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md
depends_on: []
pills: []
files:
- src/sldb/code/lang_ts.py
- src/sldb/code/ts_readers.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
---

# sldb.code publica facts genéricos de TS, TSX, JS y JSX: llamadas entre símbolos, llamadas HTTP como llamadas y handlers JSX (C3 de IR para IR09)

## Rationale

_Explain why this task exists or the business driver behind it._

IR09 (frontend) necesita los componentes, sus handlers y sus llamadas HTTP. Los componentes ya salen (B2); faltan las llamadas y los handlers. Misma decisión que la parte de Python: sldb publica hechos sintácticos genéricos y specIR los interpreta. Origen: desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md.

## Goal

_Describe the concrete result this task must produce._

Los facts de TS, TSX, JS y JSX llevan las llamadas que hace cada función, componente o hook (fetch(...), axios.get(...), api.posts.create(...) y llamadas a otros símbolos) con su primer argumento literal si lo hay, y los atributos JSX que ligan un evento a un handler (onClick={handleSave}), sin conocer ningún framework.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) relación calls desde cada función, componente o hook hacia cada nombre llamado (texto calificado tal cual); attrs.calls con {func, line, first_arg} donde first_arg es el texto de un primer argumento literal (string o template sin expresiones) o null. (2) attrs.handlers en componentes: lista de {element, attribute, handler} para atributos JSX que empiezan por on y cuyo valor es un identificador o una llamada; relación calls también hacia ese handler. (3) Mismas convenciones de forma que la tarea de Python (si esa ya cerró, seguir su forma exacta). Fixture con un componente que hace fetch y axios y tiene un botón con onClick; tests. CHANGELOG. No entra: interpretar REST ni frameworks, resolver imports, Python.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/code/lang_ts.py, ts_readers.py y ts_fingerprints.py, y la forma de calls de la tarea de Python si ya cerró. 2) Readers nuevos en módulos nuevos del paquete sldb.code. 3) Fixture en tests/fixtures/treesitter/frontend/src/ y tests en tests/selfdoc/test_treesitter_symbols.py. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; sobre el fixture salen las llamadas fetch y axios con su URL literal, la llamada del componente a su handler y el handler onClick en attrs.handlers; las anclas TS existentes no cambian de estado; CHANGELOG y commit; aviso a IR.

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

FILE:desk/atoms/atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos.md
---
sldb:
  by: agent
  at: '2026-11-16T21:25:37Z'
  authority: generated
  via: create_document
id: atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
title: sldb.code lee TS, TSX, JS y JSX con un mismo reader y ancla sus símbolos
five_wh_one_plus: what
tags:
- system:sldb
- topic:code
provenance: tarea B2 (IR08), ejecutor deskops-e-640c751d7c12, tester deskops-t-9d06b59a722f
  PASA
---

# sldb.code lee TS, TSX, JS y JSX con un mismo reader y ancla sus símbolos

## Answer

Con el extra code (tree-sitter-typescript), sldb.code escanea .ts con la gramática typescript y .tsx, .js y .jsx con la gramática tsx, en un mismo reader (lang_ts, ts_readers, ts_fingerprints). Publica hechos con la forma de los de Python: component (nombre en mayúscula con JSX en el cuerpo, incluidos memo y forwardRef), hook (use + mayúscula), type (type o interface, solo TS), function y module, con docstring JSDoc adyacente. Las anclas code:<ruta>.<ext>::<símbolo> pasan por intact, changed, lost y reconnected. Sin la gramática, el escaneo de .py sigue igual; find_files no recorre node_modules.

FILE:src/sldb/code/lang_ts.py
"""TypeScript and JavaScript (`.ts`, `.tsx`, `.js`, `.jsx`) into facts of the same form as Python's: the
module, then its top-level declarations in source order (components, hooks, types and functions; rules
in `ts_readers`). One reader for the four; the grammar comes from the extension (`runtime.grammar_of`).
The module's qualified name is its path without extension, like `py_module_name`; a symbol's id is
`module.name`, and a repeated id takes the `~2`, `~3` suffix from `Ids`.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from sldb.code.facts import fact, rels
from sldb.code.ids import Ids
from sldb.code.imports import py_module_name
from sldb.code.runtime import parse
from sldb.code.ts_fingerprints import ts_fingerprints
from sldb.code.ts_readers import declarations, jsdoc, kind_of, ts_imports, ts_signature


def scan_ts_file(rel: str, root: Path, idgen: Ids) -> list[dict[str, Any]]:
    src = (root / rel).read_bytes()
    rootn, module = parse(src, rel).root_node, py_module_name(rel)
    ctx = {"rel": rel, "module": module, "src": src, "digest": "sha256:" + hashlib.sha256(src).hexdigest(), "mid": idgen.take(module or "__init__")}
    facts, typed = [_module_fact(rootn, ctx)], rel.endswith((".ts", ".tsx"))
    for stmt in rootn.named_children:
        for name, node, fn in declarations(stmt, module.rsplit(".", 1)[-1], typed, src):
            facts.append(_definition_fact(name, node, fn, jsdoc(stmt, src), idgen, ctx))
    return facts


def _module_fact(rootn: Any, ctx: dict[str, Any]) -> dict[str, Any]:
    src, module = ctx["src"], ctx["module"]
    imports, nlines = ts_imports(rootn, src), len(src.decode("utf-8", "replace").splitlines())
    return fact(id=ctx["mid"], kind="module", name=module.rsplit(".", 1)[-1] if module else "__init__", qualified_name=module, path=ctx["rel"],
                span={"start_line": 1, "end_line": max(nlines, 1)}, source_hash=ctx["digest"], doc=None, relations=rels(None, imports),
                attrs={"native_kind": rootn.type, "module": module, "imports": imports, "nested_imports": [], "has_error": rootn.has_error},
                fingerprints=ts_fingerprints(None, rootn, None, None, src))


def _definition_fact(name: str, node: Any, fn: Any, doc: str | None, idgen: Ids, ctx: dict[str, Any]) -> dict[str, Any]:
    module, src = ctx["module"], ctx["src"]
    return fact(id=idgen.take(f"{module}.{name}" if module else name), kind=kind_of(name, node, fn), name=name, qualified_name=name, path=ctx["rel"],
                span={"start_line": node.start_point[0] + 1, "end_line": node.end_point[0] + 1}, source_hash=ctx["digest"],
                signature=ts_signature(name, fn, src), doc=doc, relations=rels(ctx["mid"]),
                attrs={"native_kind": (fn if fn is not None else node).type, "module": module}, fingerprints=ts_fingerprints(name, node, fn, doc, src))

FILE:src/sldb/code/ts_readers.py
"""Readers over tree-sitter TypeScript/JavaScript nodes: top-level declarations, their kind, JSDoc, signature, imports.

A declaration is a `function`, a `const`/`let`/`var` whose value is a function (directly or as the
first argument of a wrapping call, `memo(...)`, `forwardRef(...)`), or, in `.ts`/`.tsx`, a `type`
or an `interface`; exported or not. Reexports (`export { X } from ...`) declare nothing; an unnamed
`export default` takes the module's last segment as its name. Kinds: `hook` (`use` + capital),
`component` (capital and a JSX node anywhere in it), `type`, else `function`.
"""

from __future__ import annotations

import inspect
import re
from typing import Any

from sldb.code.readers import field_text, py_norm, text

_FUNCTIONS = {"arrow_function", "function_expression", "function", "function_declaration", "generator_function_declaration", "generator_function"}
_TYPES = {"type_alias_declaration", "interface_declaration"}
_VARIABLES = {"lexical_declaration", "variable_declaration"}
_JSX = {"jsx_element", "jsx_self_closing_element", "jsx_fragment"}
_HOOK = re.compile(r"use[A-Z]")


def function_of(value: Any) -> Any:
    """The function a value holds: itself, or the first argument of a wrapping call, recursively; None otherwise."""
    if value is None or value.type in _FUNCTIONS:
        return value
    args = value.child_by_field_name("arguments") if value.type == "call_expression" else None
    return function_of(args.named_children[0]) if args is not None and args.named_children else None


def declarations(stmt: Any, default_name: str, typed: bool, src: bytes) -> list[tuple[str, Any, Any]]:
    """`(name, node, function or None)` of each declaration a top-level statement makes."""
    inner = stmt.child_by_field_name("declaration") or stmt.child_by_field_name("value") if stmt.type == "export_statement" else stmt
    if inner is None:
        return []
    if inner.type in _VARIABLES:
        pairs = [(d, function_of(d.child_by_field_name("value"))) for d in inner.named_children if d.type == "variable_declarator"]
        return [(field_text(d, src, "name"), d, fn) for d, fn in pairs if fn is not None]
    if inner.type in _TYPES:
        return [(field_text(inner, src, "name"), inner, None)] if typed else []
    fn = function_of(inner)
    return [(field_text(inner, src, "name") or default_name, inner, fn)] if fn is not None else []


def kind_of(name: str, node: Any, fn: Any) -> str:
    if fn is None:
        return "type"
    if _HOOK.match(name):
        return "hook"
    return "component" if name[:1].isupper() and has_jsx(node) else "function"


def has_jsx(node: Any) -> bool:
    stack = [node]
    while stack:
        n = stack.pop()
        if n.type in _JSX:
            return True
        stack.extend(n.named_children)
    return False


def jsdoc(stmt: Any, src: bytes) -> str | None:
    """The `/** ... */` that ends on the line just before `stmt` (the last one, when several), without delimiters or `*`."""
    prev = stmt.prev_sibling
    if prev is None or prev.type != "comment" or not text(prev, src).startswith("/**") or prev.end_point[0] + 1 != stmt.start_point[0]:
        return None
    lines = [re.sub(r"^\s*\*? ?", "", line) for line in text(prev, src)[3:-2].splitlines()]
    return inspect.cleandoc("\n".join(lines)).strip() or None


def ts_signature(name: str, fn: Any, src: bytes) -> str | None:
    """`name(params)` like the Python reader's; None for a type."""
    if fn is None:
        return None
    params = fn.child_by_field_name("parameters")
    inner = [c for c in params.named_children if c.type != "comment"] if params is not None else [fn.child_by_field_name("parameter")]
    return f"{name}({', '.join(py_norm(text(p, src)) for p in inner if p is not None)})"


def ts_imports(root: Any, src: bytes) -> list[str]:
    """The source of each top-level `import`, sorted: `import R from "react"` is `react`."""
    sources = [s.child_by_field_name("source") for s in root.named_children if s.type == "import_statement"]
    return sorted({text(s, src)[1:-1] for s in sources if s is not None})

FILE:tests/selfdoc/test_treesitter_symbols.py
"""The tree-sitter symbols scanner (ported from kimun): ids, kinds, spans, docstrings, signatures.
Skipped without the `[code]` extra."""
from __future__ import annotations

import shutil
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


def test_nested_imports_are_a_separate_attr(facts, tmp_path):
    from sldb.code.scan import scan_tree

    assert facts["pkg.mod"]["attrs"]["imports"] == [".", "..a", "__future__", "os,sys"] and facts["pkg.mod"]["attrs"]["nested_imports"] == []
    (tmp_path / "lazy.py").write_text("import os\nif TYPE_CHECKING:\n    from a.b import C\ntry:\n    import json, sys as s\nexcept ImportError: pass\n"
                                      "class K:\n    def m(self):\n        from . import x\n        with ctx():\n            import os\n", encoding="utf-8")
    lazy = next(f for f in scan_tree(tmp_path) if f["id"] == "lazy")
    assert lazy["attrs"]["imports"] == ["os"] and [r["target"] for r in lazy["relations"]] == ["os"], "attrs.imports y facts.rels sin cambios"
    assert lazy["attrs"]["nested_imports"] == [".", "a.b", "json,sys", "os"]


def test_docstring_forms_and_duplicate_ids(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "docs.py").write_text('def a():\n    r"""raw \\d"""\ndef b():\n    "x\\ty" \'z\'\ndef c():\n    f"{1}"\ndef d():\n    b"bytes"\ndef e():\n    pass\n    "late"\n', encoding="utf-8")
    (tmp_path / "dup.py").write_text("def f(): pass\ndef f(): pass\n", encoding="utf-8")
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert [facts[f"docs.{n}"]["doc"] for n in "abcde"] == ["raw \\d", "x       yz", None, None, None]
    assert "dup.f" in facts and "dup.f~2" in facts


def test_without_the_runtime_the_error_names_the_extra(monkeypatch):
    import sldb.code.runtime as rt

    monkeypatch.setattr(rt, "_RUNTIME", {})
    monkeypatch.setattr(rt.importlib, "import_module", lambda name: (_ for _ in ()).throw(ImportError(name, name=name)))
    with pytest.raises(rt.TreeSitterUnavailable, match=r"\[code\]"):
        rt.runtime()
    assert not rt.available()


FRONTEND = Path(__file__).parent.parent / "fixtures" / "treesitter" / "frontend"
needs_ts = pytest.mark.skipif(not available(".ts"), reason="tree-sitter-typescript not installed (extra [code])")


@pytest.fixture
def ts_facts():
    from sldb.code.scan import scan_tree

    return {f["id"]: f for f in scan_tree(FRONTEND)}


@needs_ts
def test_ts_kinds_names_and_top_level_only(ts_facts):
    app = {i.removeprefix("src.App."): f["kind"] for i, f in ts_facts.items() if i.startswith("src.App.")}
    assert app == {"App": "component", "Button": "component", "ButtonProps": "type", "Card": "component", "Mode": "type",
                   "NotComponent": "function", "helper": "function", "useCounter": "hook"}, "no reexport, no nested `inner`"
    assert (ts_facts["src.useToggle.useToggle"]["kind"], ts_facts["src.useToggle.Pair"]["kind"]) == ("hook", "type")
    assert (ts_facts["src.util.double"]["kind"], ts_facts["src.Panel.Panel"]["kind"]) == ("function", "component")
    assert ts_facts["src.App"]["kind"] == "module" and ts_facts["src.App"]["qualified_name"] == "src.App" and ts_facts["src.App.Button"]["qualified_name"] == "Button"
    assert ts_facts["src.App.Button"]["relations"] == [{"type": "contained-in", "target": "src.App"}]


@needs_ts
def test_ts_jsdoc_signature_span_and_imports(ts_facts):
    assert ts_facts["src.App.Button"]["doc"] == "A button.\n\n  Indented.", "the last of two JSDoc blocks"
    assert (ts_facts["src.App.ButtonProps"]["doc"], ts_facts["src.App.Card"]["doc"], ts_facts["src.util.double"]["doc"]) == ("Props of a button.", None, "Doubles a number.")
    assert ts_facts["src.App.Button"]["signature"] == "Button({ label }: ButtonProps)" and ts_facts["src.App.helper"]["signature"] == "helper(x)"
    assert ts_facts["src.App.Mode"]["signature"] is None and ts_facts["src.App.Button"]["span"] == {"start_line": 16, "end_line": 21}
    assert ts_facts["src.App"]["attrs"]["imports"] == ["./app.css", "react"] and [r["target"] for r in ts_facts["src.Panel"]["relations"]] == ["./util"]
    assert all(set(f["fingerprints"]) == {"signature", "shape", "docstring", "body"} for f in ts_facts.values())


@needs_ts
def test_ts_types_only_in_ts_and_same_module_names_take_a_suffix(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "a.ts").write_text("export const f = () => 1;\n", encoding="utf-8")
    (tmp_path / "a.js").write_text("type T = number;\nfunction g() {}\n", encoding="utf-8")
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert sorted(facts) == ["a", "a.f", "a.g", "a~2"] and (facts["a"]["path"], facts["a~2"]["path"]) == ("a.js", "a.ts")


def test_without_the_ts_grammar_python_still_scans(monkeypatch, tmp_path):
    import sldb.code.runtime as rt
    from sldb.code.scan import scan_tree

    real = rt.importlib.import_module
    monkeypatch.setattr(rt, "_RUNTIME", {})
    monkeypatch.setattr(rt.importlib, "import_module", lambda name: (_ for _ in ()).throw(ImportError(name, name=name)) if name == "tree_sitter_typescript" else real(name))
    shutil.copytree(FRONTEND, tmp_path / "front")
    (tmp_path / "front" / "m.py").write_text("def f(): pass\n", encoding="utf-8")
    assert not rt.available(".tsx") and sorted(f["id"] for f in scan_tree(tmp_path / "front")) == ["m", "m.f"]


SQL = Path(__file__).parent.parent / "fixtures" / "treesitter" / "sql"
needs_sql = pytest.mark.skipif(not available(".sql"), reason="tree-sitter-sql not installed (extra [code])")


@pytest.fixture
def sql_facts():
    from sldb.code.scan import scan_tree

    return {f["id"].removeprefix("migrations.0001_initial."): f for f in scan_tree(SQL) if f["path"].startswith("migrations/")}


@needs_sql
def test_sql_tables_columns_views_and_index_of_a_postgres_migration(sql_facts):
    kinds = {i: f["kind"] for i, f in sql_facts.items()}
    assert kinds == {"migrations.0001_initial": "module", "public.users": "table", "public.users.id": "column", "public.users.email": "column",
                     "public.users.profile": "column", "public.users.created_at": "column", "orders": "table", "orders.id": "column",
                     "orders.user_id": "column", "orders.total": "column", "active_users": "view", "order_totals": "view", "orders_user_idx": "index"}, "constraints are not columns"
    users, email = sql_facts["public.users"], sql_facts["public.users.email"]
    assert (users["name"], users["qualified_name"], email["name"], email["qualified_name"]) == ("users", "public.users", "email", "public.users.email")
    assert sql_facts["orders"]["qualified_name"] == "orders" and sql_facts["migrations.0001_initial"]["qualified_name"] == "migrations.0001_initial"
    assert email["relations"] == [{"type": "contained-in", "target": "migrations.0001_initial.public.users"}]
    assert (sql_facts["order_totals"]["attrs"]["native_kind"], sql_facts["active_users"]["attrs"]["native_kind"]) == ("create_materialized_view", "create_view")


@needs_sql
def test_sql_comments_signatures_spans_and_imports(sql_facts):
    assert sql_facts["public.users"]["doc"] == "Accounts of the app.\nOne row per person.", "contiguous -- lines, not the one after a blank line"
    assert (sql_facts["orders"]["doc"], sql_facts["public.users.email"]["doc"], sql_facts["order_totals"]["doc"]) == (None, None, "Totals per user, refreshed nightly.")
    assert sql_facts["public.users.email"]["signature"] == "email text NOT NULL UNIQUE" and sql_facts["public.users"]["span"] == {"start_line": 5, "end_line": 10}
    assert sql_facts["orders_user_idx"]["signature"] == "CREATE INDEX CONCURRENTLY orders_user_idx ON orders (user_id)"
    assert sql_facts["migrations.0001_initial"]["attrs"]["imports"] == [] and sql_facts["migrations.0001_initial"]["relations"] == []
    assert all(set(f["fingerprints"]) == {"signature", "shape", "docstring", "body"} for f in sql_facts.values())


@needs_sql
def test_sql_repeated_objects_take_a_suffix_and_a_statement_with_errors_keeps_what_reads(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "m.sql").write_text('CREATE TABLE t (a int);\nCREATE TABLE "t" (a int, b int);\n'
                                    "CREATE TABLE bad (a int GENERATED BY DEFAULT AS IDENTITY, b int, CONSTRAINT k UNIQUE (a));\n"
                                    'CREATE TABLE (z int);\nCREATE INDEX i ON t (a);\nCREATE INDEX "i" ON t (b);\n', encoding="utf-8")
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert sorted(facts) == ["m", "m.bad", "m.bad.b", "m.i", "m.i~2", "m.t", "m.t.a", "m.t~2", "m.t~2.a", "m.t~2.b"], "no column with an error, nothing of a nameless table"
    assert (facts["m.t~2"]["qualified_name"], facts["m.t~2.b"]["qualified_name"], facts["m.i~2"]["qualified_name"]) == ("t~2", "t~2.b", "i~2"), '"t" is t'
    (tmp_path / "n.sql").write_text("CREATE TABLE (z int);\n", encoding="utf-8")
    modules = {f["id"]: f["attrs"] for f in scan_tree(tmp_path) if f["kind"] == "module"}
    assert [(modules[m]["has_error"], modules[m]["parse_errors"]) for m in ("m", "n")] == [(False, True), (True, True)], "unparseable only when nothing reads"


DJANGO = {"app_author": "table", "app_author.name": "column", "app_author.profile": "column", "app_author.created_at": "column",
          "app_book": "table", "app_book.title": "column", "app_book.pages": "column", "app_book.slug": "column", "app_book.author_id": "column",
          "app_book_slug_780ddf03_like": "index", "app_book_author_id_980d3e25": "index", "app_book_title_idx": "index"}


@needs_sql
def test_a_django_sqlmigrate_migration_gives_its_tables_columns_and_indexes():
    from sldb.code.scan import scan_file

    facts = {f["qualified_name"]: f for f in scan_file("django/0001_initial.sql", SQL)[1:]}
    assert {q: f["kind"] for q, f in facts.items()} == DJANGO, "inside BEGIN/COMMIT, unquoted; the IDENTITY id columns are left out"
    assert (facts["app_book"]["doc"], facts["app_book"]["name"], facts["app_book.slug"]["name"]) == ("Create model Book", "app_book", "slug")
    assert facts["app_book.author_id"]["relations"] == [{"type": "contained-in", "target": "django.0001_initial.app_book"}]
    assert facts["app_book_author_id_980d3e25"]["signature"] == 'CREATE INDEX "app_book_author_id_980d3e25" ON "app_book" ("author_id")'


def test_without_the_sql_grammar_sql_files_are_not_scanned(monkeypatch, tmp_path):
    import sldb.code.runtime as rt
    from sldb.code.scan import scan_tree

    real = rt.importlib.import_module
    monkeypatch.setattr(rt, "_RUNTIME", {})
    monkeypatch.setattr(rt.importlib, "import_module", lambda name: (_ for _ in ()).throw(ImportError(name, name=name)) if name == "tree_sitter_sql" else real(name))
    shutil.copytree(SQL, tmp_path / "db")
    (tmp_path / "db" / "m.py").write_text("def f(): pass\n", encoding="utf-8")
    assert not rt.available(".sql") and sorted(f["id"] for f in scan_tree(tmp_path / "db")) == ["m", "m.f"]

FILE:instruccion
Cold-bundle de la tarea task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

