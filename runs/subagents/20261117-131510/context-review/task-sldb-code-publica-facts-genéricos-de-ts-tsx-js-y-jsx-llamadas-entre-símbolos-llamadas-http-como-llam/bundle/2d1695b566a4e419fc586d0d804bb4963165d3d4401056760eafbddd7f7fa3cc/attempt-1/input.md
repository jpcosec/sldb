FILE:desk/tasks/task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam.md
---
sldb:
  by: agent
  at: '2026-11-17T13:12:27Z'
  authority: generated
  via: save_document_payload
id: task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam
status: draft
summary: 'BLOQUEADA 2026-11-17 tras 2 ciclos de corrección (tester FALLA en intento
  1, c1 y c2). Resuelto: await, type args, espacios, cadenas en varias líneas, ''()'',
  ''(fn)'', ''[]'', first_arg y handlers; facts existentes idénticos a HEAD. Pendiente:
  cuando el objeto de la cadena es un array, binario, new o literal, el nombre sale
  como texto sin espacios y puede ser erróneo (new Set(xs) -> newSet(xs); (a ?? []).map
  -> a??[].map; ''a b''.split -> ''ab''.split): 123 de unos 2000 nombres en tres frontends
  reales. Propuesta: un ciclo más con marcadores fijos para esas expresiones ([...],
  (expr), (lit)) en ts_callee.py; necesita OK del supervisor. Diff guardado en runs/subagents/20261116-exec-k4-c2/executor-diff-c3ts-c2.patch
  (reaplicable); informes en runs/subagents/20261116-test-k4*/.'
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md
depends_on:
- task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre
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

Precisiones (intento 2): esta tarea depende de la de facts genéricos de Python y sigue su forma exacta para calls, attrs.calls y kwargs cuando aplique. El destino de una relación calls es el texto completo de la expresión llamada como un solo nombre (api.posts.create, axios.get, fetch), sin partirlo. first_arg es el valor del literal sin comillas ni backticks (/api/posts, no '/api/posts'); un template con expresiones da null. element es el nombre del tag JSX tal como está escrito (button, Button, Form.Item). Los readers nuevos van en módulos nuevos del paquete sldb.code; están autorizados aunque no figuren en files.

Precisiones (corrección 2, tras dos testers): forma canónica del nombre de una llamada (name en attrs.calls y destino de la relación calls). Se arma desde el árbol, no desde el texto: identificadores y nombres de propiedad unidos por '.' (con '?.' y '!' si están escritos), sin espacios ni saltos de línea, sin await y sin argumentos de tipo. Si un tramo de la cadena es a su vez una llamada, se escribe con '()' sin sus argumentos (fetch(url).then(cb).then -> fetch().then().then; (await listDocuments(m)).slice -> listDocuments().slice). Una función anónima o una IIFE como objeto se escribe '(fn)'. Un acceso por índice se escribe '[]'. Los handlers JSX son atributos 'on' seguidos de mayúscula. El diff de los intentos anteriores está en el árbol o en runs/subagents/20261116-exec-k4-c1/ y es el punto de partida.

Decisión del supervisor (2026-11-17, prevalece): no se busca la forma canónica de los nombres cuya cadena empieza en un array, una expresión binaria, un new, un literal u otra expresión que no sea identificador, this, super, llamada, miembro, índice, non-null o función. Esas llamadas se emiten igual en attrs.calls con canonical: false y name igual al texto de la expresión llamada con cada tramo de espacios en blanco colapsado a un solo espacio (no borrado), sin await ni type args; las canónicas llevan canonical: true. La relación calls solo se emite para nombres canónicos, para no poner en el grafo destinos que no son símbolos. Nada se omite en silencio. Canonizarlos queda para una tarea aparte de baja prioridad. El punto de partida es el diff guardado en runs/subagents/20261116-exec-k4-c2/executor-diff-c3ts-c2.patch.

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

Los comandos de Validation pasan; sobre el fixture salen las llamadas fetch y axios con su URL literal, la llamada del componente a su handler y el handler onClick en attrs.handlers; en los tres frontends reales del workspace (solo lectura) todo name canónico cumple la forma canónica y todo name no canónico lleva canonical: false, sin espacios dobles, sin await y sin type args; ningún destino de la relación calls es no canónico; las anclas TS existentes no cambian de estado; CHANGELOG y commit; aviso a IR.

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

import importlib.util
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


needs_pg = pytest.mark.skipif(not available(".sql") or importlib.util.find_spec("pglast") is None, reason="pglast not installed (extra [postgres])")


@pytest.fixture
def no_pg(monkeypatch):
    """The reading without the extra [postgres], whether pglast is installed or not."""
    import sldb.code.sql_pg as sql_pg

    monkeypatch.setattr(sql_pg, "_pg", None)


@pytest.fixture
def sql_facts():
    from sldb.code.scan import scan_tree

    return {f["id"].removeprefix("migrations.0001_initial."): f for f in scan_tree(SQL) if f["path"].startswith("migrations/")}


def _scan(tmp_path, sql, name="k"):
    from sldb.code.scan import scan_tree

    (tmp_path / f"{name}.sql").write_text(sql, encoding="utf-8")
    return {f["id"]: f for f in scan_tree(tmp_path)}


def _keys(facts):
    return {i: (f["attrs"]["constraint_type"], f["attrs"]["columns"], f["attrs"].get("references")) for i, f in facts.items() if f["kind"] == "constraint"}


MIGRATION = {"migrations.0001_initial": "module", "public.users": "table", "public.users.id": "column", "public.users.email": "column",
             "public.users.profile": "column", "public.users.created_at": "column", "orders": "table", "orders.id": "column",
             "orders.user_id": "column", "orders.total": "column", "active_users": "view", "order_totals": "view", "orders_user_idx": "index"}


@needs_sql
def test_sql_tables_columns_views_and_index_of_a_postgres_migration(no_pg, sql_facts):
    assert {i: f["kind"] for i, f in sql_facts.items()} == MIGRATION, "without the extra: constraints are not columns, and no keys"
    users, email = sql_facts["public.users"], sql_facts["public.users.email"]
    assert (users["name"], users["qualified_name"], email["name"], email["qualified_name"]) == ("users", "public.users", "email", "public.users.email")
    assert sql_facts["orders"]["qualified_name"] == "orders" and sql_facts["migrations.0001_initial"]["qualified_name"] == "migrations.0001_initial"
    assert email["relations"] == [{"type": "contained-in", "target": "migrations.0001_initial.public.users"}]
    assert (sql_facts["order_totals"]["attrs"]["native_kind"], sql_facts["active_users"]["attrs"]["native_kind"]) == ("create_materialized_view", "create_view")
    assert all(set(f["attrs"]) <= {"native_kind", "module", "imports", "nested_imports", "has_error", "parse_errors"} for f in sql_facts.values()), "no keys_partial: no ERROR"


@needs_pg
def test_with_pglast_a_postgres_migration_also_gives_its_keys(sql_facts):
    keys = {"orders.pk": "constraint", "orders.fk": "constraint", "orders.unique": "constraint"}
    assert {i: f["kind"] for i, f in sql_facts.items()} == MIGRATION | keys, "table constraints are keys, not columns"
    assert not any("keys_partial" in f["attrs"] for f in sql_facts.values())


@needs_pg
def test_sql_unnamed_table_keys_and_the_keys_written_in_a_column(sql_facts):
    fk, pk, uniq = sql_facts["orders.fk"], sql_facts["orders.pk"], sql_facts["orders.unique"]
    assert [(k["name"], k["qualified_name"], k["attrs"]["constraint_type"], k["attrs"]["columns"]) for k in (pk, fk, uniq)] == [
        ("pk", "orders.pk", "primary_key", ["id"]), ("fk", "orders.fk", "foreign_key", ["user_id"]), ("unique", "orders.unique", "unique", ["user_id", "id"])]
    assert fk["attrs"]["references"] == {"table": "public.users", "columns": ["id"]} and "references" not in pk["attrs"]
    assert fk["relations"] == [{"type": "contained-in", "target": "migrations.0001_initial.orders"}, {"type": "references", "target": "migrations.0001_initial.public.users"}]
    assert (fk["signature"], fk["span"], fk["attrs"]["native_kind"]) == ("FOREIGN KEY (user_id) REFERENCES public.users (id)", {"start_line": 17, "end_line": 17}, "Constraint")
    users_id, email, user_id = (sql_facts[c]["attrs"] for c in ("public.users.id", "public.users.email", "orders.user_id"))
    assert (users_id["type"], users_id.get("primary_key"), email.get("unique"), email.get("primary_key"), user_id["type"]) == ("bigserial", True, True, None, "bigint")
    assert not any("parse_partial" in a or "identity" in a or "primary_key" in a for a in (email, user_id)), "a REFERENCES in a column is no key mark"
    assert user_id["references"] == {"table": "public.users", "columns": ["id"]} and "orders.user_id" not in {f["qualified_name"] for f in sql_facts.values() if f["kind"] == "constraint"}


@needs_sql
def test_sql_comments_signatures_spans_and_imports(sql_facts):
    assert sql_facts["public.users"]["doc"] == "Accounts of the app.\nOne row per person.", "contiguous -- lines, not the one after a blank line"
    assert (sql_facts["orders"]["doc"], sql_facts["public.users.email"]["doc"], sql_facts["order_totals"]["doc"]) == (None, None, "Totals per user, refreshed nightly.")
    assert sql_facts["public.users.email"]["signature"] == "email text NOT NULL UNIQUE" and sql_facts["public.users"]["span"] == {"start_line": 5, "end_line": 10}
    assert sql_facts["orders_user_idx"]["signature"] == "CREATE INDEX CONCURRENTLY orders_user_idx ON orders (user_id)"
    assert sql_facts["migrations.0001_initial"]["attrs"]["imports"] == [] and sql_facts["migrations.0001_initial"]["relations"] == []
    assert all(set(f["fingerprints"]) == {"signature", "shape", "docstring", "body"} for f in sql_facts.values())


BAD = ('CREATE TABLE t (a int);\nCREATE TABLE "t" (a int, b int);\n'
       "CREATE TABLE bad (a int GENERATED BY DEFAULT AS IDENTITY, b int, CONSTRAINT k UNIQUE (a));\n"
       'CREATE TABLE (z int);\nCREATE INDEX i ON t (a);\nCREATE INDEX "i" ON t (b);\n')


@needs_sql
def test_sql_repeated_objects_take_a_suffix_and_a_statement_with_errors_keeps_what_reads(no_pg, tmp_path):
    facts = _scan(tmp_path, BAD, "m")
    assert sorted(facts) == ["m", "m.bad", "m.bad.b", "m.i", "m.i~2", "m.t", "m.t.a", "m.t~2", "m.t~2.a", "m.t~2.b"], "no column with an error, nothing of a nameless table"
    assert (facts["m.t~2"]["qualified_name"], facts["m.t~2.b"]["qualified_name"], facts["m.i~2"]["qualified_name"]) == ("t~2", "t~2.b", "i~2"), '"t" is t'
    assert [facts[t]["attrs"].get("keys_partial") for t in ("m.bad", "m.t", "m.t~2")] == [True, None, None], "only the statement with an ERROR"
    modules = {f["id"]: f["attrs"] for f in _scan(tmp_path, "CREATE TABLE (z int);\n", "n").values() if f["kind"] == "module"}
    assert [(modules[m]["has_error"], modules[m]["parse_errors"]) for m in ("m", "n")] == [(False, True), (True, True)], "unparseable only when nothing reads"


@needs_pg
def test_with_pglast_a_column_the_grammar_does_not_parse_is_read_and_its_keys_too(tmp_path):
    facts = _scan(tmp_path, BAD, "m")
    assert sorted(facts) == ["m", "m.bad", "m.bad.a", "m.bad.b", "m.bad.k", "m.i", "m.i~2", "m.t", "m.t.a", "m.t~2", "m.t~2.a", "m.t~2.b"], "nothing of a nameless table"
    assert facts["m.bad.a"]["attrs"] | {"module": None} == {"native_kind": "ColumnDef", "module": None, "type": "int", "identity": True, "parse_partial": True}
    assert (facts["m.bad.a"]["signature"], facts["m.bad.a"]["span"]) == ("a int GENERATED BY DEFAULT AS IDENTITY", {"start_line": 3, "end_line": 3})
    assert _keys(facts) == {"m.bad.k": ("unique", ["a"], None)} and "keys_partial" not in facts["m.bad"]["attrs"], "Postgres parsed it: the keys are whole"


DJANGO = {"app_author": "table", "app_author.name": "column", "app_author.profile": "column", "app_author.created_at": "column",
          "app_book": "table", "app_book.title": "column", "app_book.pages": "column", "app_book.slug": "column", "app_book.author_id": "column",
          "app_book_slug_780ddf03_like": "index", "app_book_author_id_980d3e25": "index", "app_book_title_idx": "index"}
DJANGO_KEYS = {"app_author.id": "column", "app_book.id": "column", "app_book.slug_pages_uniq": "constraint",
               "app_book.app_book_title_author_id_f24131bb_uniq": "constraint", "app_book.app_book_author_id_980d3e25_fk_app_author_id": "constraint"}


def _django(name="0001_initial"):
    from sldb.code.scan import scan_file

    return {f["qualified_name"]: f for f in scan_file(f"django/{name}.sql", SQL)[1:]}


@needs_sql
def test_a_django_sqlmigrate_migration_gives_its_tables_columns_and_indexes(no_pg):
    facts = _django()
    assert {q: f["kind"] for q, f in facts.items()} == DJANGO, "inside BEGIN/COMMIT, unquoted; without the extra the IDENTITY id columns are left out"
    assert (facts["app_book"]["doc"], facts["app_book"]["name"], facts["app_book.slug"]["name"]) == ("Create model Book", "app_book", "slug")
    assert facts["app_book.author_id"]["relations"] == [{"type": "contained-in", "target": "django.0001_initial.app_book"}]
    assert facts["app_book_author_id_980d3e25"]["signature"] == 'CREATE INDEX "app_book_author_id_980d3e25" ON "app_book" ("author_id")'
    assert [facts[t]["attrs"].get("keys_partial") for t in ("app_author", "app_book")] == [True, True], "their statements have ERROR nodes"
    assert facts["app_book.slug"]["attrs"] == {"native_kind": "column_definition", "module": "django.0001_initial"}, "no column attributes"


@needs_pg
def test_a_django_migration_gives_the_identity_primary_key_and_the_keys_of_alter_table():
    facts = _django()
    assert {q: f["kind"] for q, f in facts.items()} == DJANGO | DJANGO_KEYS and not any("keys_partial" in f["attrs"] for f in facts.values())
    ident = facts["app_book.id"]
    assert ident["attrs"] | {"module": None} == {"native_kind": "ColumnDef", "module": None, "type": "bigint", "primary_key": True, "identity": True, "parse_partial": True}
    assert ident["relations"] == [{"type": "contained-in", "target": "django.0001_initial.app_book"}] and ident["name"] == "id"
    assert (facts["app_book.slug"]["attrs"].get("unique"), facts["app_book.pages"]["attrs"]["type"], facts["app_author.created_at"]["attrs"]["type"]) == (True, "integer", "timestamp with time zone")
    fk = facts["app_book.app_book_author_id_980d3e25_fk_app_author_id"]
    assert (fk["kind"], fk["name"], fk["attrs"]["native_kind"], fk["attrs"]["constraint_type"], fk["attrs"]["columns"]) == (
        "constraint", "app_book_author_id_980d3e25_fk_app_author_id", "Constraint", "foreign_key", ["author_id"])
    assert fk["attrs"]["references"] == {"table": "app_author", "columns": ["id"]}
    assert fk["relations"] == [{"type": "contained-in", "target": "django.0001_initial.app_book"}, {"type": "references", "target": "django.0001_initial.app_author"}]
    uniq = [facts[f"app_book.{n}"]["attrs"] for n in ("app_book_title_author_id_f24131bb_uniq", "slug_pages_uniq")]
    assert [(u["constraint_type"], u["columns"]) for u in uniq] == [("unique", ["title", "author_id"]), ("unique", ["slug", "pages"])], "a UniqueConstraint before a CheckConstraint"


@needs_pg
def test_a_foreign_key_to_a_table_of_another_migration_has_references_but_no_relation():
    facts = _django("blog_0001_initial")
    fk = facts["posts.posts_author_id_099b8aca_fk_auth_user_id"]
    assert fk["attrs"]["references"] == {"table": "auth_user", "columns": ["id"]}, "IR's blog fixture: auth_user lives in another app"
    assert fk["relations"] == [{"type": "contained-in", "target": "django.blog_0001_initial.posts"}]
    assert (facts["posts.id"]["attrs"]["primary_key"], facts["posts.published_at"]["attrs"]["type"]) == (True, "timestamp with time zone")


SHOP = '''BEGIN;
CREATE TABLE "shop_category" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "name" varchar(50) NOT NULL UNIQUE);
CREATE TABLE "shop_tag" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "label" varchar(20) NOT NULL);
CREATE TABLE "shop_product" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "sku" varchar(20) NOT NULL, "region" varchar(5) NOT NULL, "price" numeric(8, 2) NOT NULL, "category_id" bigint NOT NULL, "owner_id" integer NULL, CONSTRAINT "uniq_cat_sku" UNIQUE ("category_id", "sku"), CONSTRAINT "price_pos" CHECK ("price" >= 0));
CREATE TABLE "shop_product_tags" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "product_id" bigint NOT NULL, "tag_id" bigint NOT NULL);
ALTER TABLE "shop_product" ADD CONSTRAINT "shop_product_sku_region_4470a054_uniq" UNIQUE ("sku", "region");
ALTER TABLE "shop_product" ADD CONSTRAINT "shop_product_category_id_14d7eea8_fk_shop_category_id" FOREIGN KEY ("category_id") REFERENCES "shop_category" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "shop_product" ADD CONSTRAINT "shop_product_owner_id_c7c481d9_fk_auth_user_id" FOREIGN KEY ("owner_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "shop_product_tags" ADD CONSTRAINT "shop_product_tags_product_id_tag_id_a244154e_uniq" UNIQUE ("product_id", "tag_id");
ALTER TABLE "shop_product_tags" ADD CONSTRAINT "shop_product_tags_product_id_9a158885_fk_shop_product_id" FOREIGN KEY ("product_id") REFERENCES "shop_product" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "shop_product_tags" ADD CONSTRAINT "shop_product_tags_tag_id_dd30c4fb_fk_shop_tag_id" FOREIGN KEY ("tag_id") REFERENCES "shop_tag" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;
'''


@needs_pg
def test_a_real_sqlmigrate_migration_unique_then_check_m2m_and_deferrable_foreign_keys(tmp_path):
    facts = _scan(tmp_path, SHOP, "s")
    p, t = "s.shop_product.", "s.shop_product_tags."
    assert _keys(facts) == {
        p + "uniq_cat_sku": ("unique", ["category_id", "sku"], None), p + "shop_product_sku_region_4470a054_uniq": ("unique", ["sku", "region"], None),
        p + "shop_product_category_id_14d7eea8_fk_shop_category_id": ("foreign_key", ["category_id"], {"table": "shop_category", "columns": ["id"]}),
        p + "shop_product_owner_id_c7c481d9_fk_auth_user_id": ("foreign_key", ["owner_id"], {"table": "auth_user", "columns": ["id"]}),
        t + "shop_product_tags_product_id_tag_id_a244154e_uniq": ("unique", ["product_id", "tag_id"], None),
        t + "shop_product_tags_product_id_9a158885_fk_shop_product_id": ("foreign_key", ["product_id"], {"table": "shop_product", "columns": ["id"]}),
        t + "shop_product_tags_tag_id_dd30c4fb_fk_shop_tag_id": ("foreign_key", ["tag_id"], {"table": "shop_tag", "columns": ["id"]})}, "the UNIQUE before a CHECK; no fact for the CHECK"
    assert all(facts[f"s.{tb}.id"]["attrs"]["primary_key"] and facts[f"s.{tb}.id"]["attrs"]["identity"] for tb in ("shop_category", "shop_tag", "shop_product", "shop_product_tags"))
    assert (facts["s.shop_category.name"]["attrs"].get("unique"), facts[p + "price"]["attrs"]["type"]) == (True, "numeric(8, 2)")
    assert [r["target"] for r in facts[p + "shop_product_owner_id_c7c481d9_fk_auth_user_id"]["relations"]] == ["s.shop_product"]


@needs_pg
def test_keys_of_alter_table_unnamed_repeated_and_out_of_scope(tmp_path):
    facts = _scan(tmp_path, "ALTER TABLE z ADD CONSTRAINT zf FOREIGN KEY (a) REFERENCES t (a);\n"
                            "CREATE TABLE t (a int UNIQUE, b int, c int DEFAULT 'primary key', UNIQUE (a), UNIQUE (b), FOREIGN KEY (c) REFERENCES t (a));\n"
                            "ALTER TABLE t ADD CONSTRAINT tp PRIMARY KEY (a, b);\nALTER TABLE t ADD PRIMARY KEY (a);\nALTER TABLE t ADD COLUMN d int;\n"
                            "ALTER TABLE t ADD CONSTRAINT tc CHECK (a > 0);\nALTER INDEX t_idx RENAME TO u_idx;\n")
    assert sorted(_keys(facts)) == ["k.t.fk", "k.t.pk", "k.t.tp", "k.t.unique", "k.t.unique~2", "k.z.zf"], "ADD COLUMN, CHECK, ALTER INDEX: no fact"
    assert [facts[i]["attrs"]["columns"] for i in ("k.t.unique", "k.t.unique~2", "k.t.pk")] == [["a"], ["b"], ["a"]], "~2 in source order; ADD without a name is a key too"
    assert facts["k.z.zf"]["relations"] == [{"type": "contained-in", "target": "k"}, {"type": "references", "target": "k.t"}], "the table after it still counts"
    assert facts["k.t.tp"]["relations"] == [{"type": "contained-in", "target": "k.t"}] and facts["k.t.tp"]["attrs"]["columns"] == ["a", "b"]
    assert (facts["k.t.a"]["attrs"].get("unique"), "primary_key" in facts["k.t.c"]["attrs"]) == (True, False), "a quoted literal is no key"


EDGE = '''CREATE TABLE public.parent (id integer NOT NULL, code text, CONSTRAINT parent_pkey PRIMARY KEY (id));
CREATE TABLE "My Schema"."Child Table" ("Id" integer, "parent id" integer, note text -- primary key unique
, tag text CHECK (tag <> 'primary key unique'), PRIMARY KEY ("Id"), UNIQUE (note), UNIQUE (tag));
ALTER TABLE ONLY public.parent ADD CONSTRAINT parent_code_key UNIQUE (code);
ALTER TABLE IF EXISTS "My Schema"."Child Table" ADD CONSTRAINT "child→parent fk" FOREIGN KEY ("parent id") REFERENCES public.parent (id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
alter table public.parent add constraint parent_self_fk foreign key (code) references public.parent;
ALTER TABLE public.parent ADD CONSTRAINT a_uniq UNIQUE (id), ADD CONSTRAINT b_uniq UNIQUE (code);
ALTER TABLE public.parent ADD CONSTRAINT chk CHECK (id > 0);
ALTER TABLE ghost ADD CONSTRAINT ghost_fk FOREIGN KEY (x) REFERENCES public.parent (id);
CREATE TABLE odd ("a)b" int, "c,d" int, UNIQUE ("a)b"), FOREIGN KEY ("a)b", "c,d") REFERENCES odd ("c,d", "a)b"));
CREATE TABLE weird (id int, "unique" int, "primary key" int);
'''


@needs_pg
def test_the_first_testers_edges_quotes_schemas_only_if_exists_lower_case_and_several_adds(tmp_path):
    facts, child, par = _scan(tmp_path, EDGE, "e"), "e.My Schema.Child Table.", "e.public.parent."
    keys = _keys(facts)
    assert keys[child + "child→parent fk"] == ("foreign_key", ["parent id"], {"table": "public.parent", "columns": ["id"]})
    assert (keys[child + "pk"], keys[child + "unique"], keys[child + "unique~2"]) == (("primary_key", ["Id"], None), ("unique", ["note"], None), ("unique", ["tag"], None))
    assert [keys[par + k][:2] for k in ("parent_pkey", "parent_code_key", "a_uniq", "b_uniq")] == [("primary_key", ["id"]), ("unique", ["code"]), ("unique", ["id"]), ("unique", ["code"])]
    assert keys[par + "parent_self_fk"] == ("foreign_key", ["code"], {"table": "public.parent", "columns": []}), "no referenced columns: the primary key"
    assert {"type": "references", "target": "e.public.parent"} in facts[par + "parent_self_fk"]["relations"] and "e.ghost.ghost_fk" in keys
    assert keys["e.odd.unique"][1] == ["a)b"] and keys["e.odd.fk"][1:] == (["a)b", "c,d"], {"table": "odd", "columns": ["c,d", "a)b"]})
    assert [set(facts[f"e.weird.{c}"]["attrs"]) - {"native_kind", "module"} for c in ("unique", "primary key")] == [{"type"}, {"type"}], "a quoted name is no key"
    assert facts[child + "note"]["attrs"]["type"] == "text" and "unique" not in facts[child + "tag"]["attrs"], "neither a comment nor a literal is a key"


@needs_pg
def test_a_table_foreign_key_without_referenced_columns_named_or_not_last_or_not(tmp_path):
    facts = _scan(tmp_path, "CREATE TABLE t (id int PRIMARY KEY);\nCREATE TABLE d (id int, FOREIGN KEY (id) REFERENCES t);\n"
                            "CREATE TABLE f2 (id int, FOREIGN KEY (id) REFERENCES t ON DELETE CASCADE, PRIMARY KEY (id));\n"
                            "CREATE TABLE a3 (id int, x int, CONSTRAINT a3_fk FOREIGN KEY (x) REFERENCES t ON DELETE CASCADE, UNIQUE (id));\n"
                            "CREATE TABLE a5 (id int, x int, CONSTRAINT a5_fk FOREIGN KEY (x) REFERENCES t);\n"
                            "CREATE TABLE a6 (id int, x int, CONSTRAINT a6_fk FOREIGN KEY (x) REFERENCES public.t);\n"
                            "CREATE TABLE e (id int, CONSTRAINT e_fk FOREIGN KEY (id) REFERENCES t, CONSTRAINT e_u UNIQUE (id));\n"
                            "CREATE TABLE a8 (id int, x int, CONSTRAINT a8_fk FOREIGN KEY (x) REFERENCES t (id), CONSTRAINT a8_c CHECK (x > 0));\n", "a")
    to_pk = {"table": "t", "columns": []}
    assert _keys(facts) == {"a.d.fk": ("foreign_key", ["id"], to_pk), "a.f2.fk": ("foreign_key", ["id"], to_pk), "a.f2.pk": ("primary_key", ["id"], None),
                            "a.a3.a3_fk": ("foreign_key", ["x"], to_pk), "a.a3.unique": ("unique", ["id"], None), "a.a5.a5_fk": ("foreign_key", ["x"], to_pk),
                            "a.a6.a6_fk": ("foreign_key", ["x"], {"table": "public.t", "columns": []}), "a.e.e_fk": ("foreign_key", ["id"], to_pk),
                            "a.e.e_u": ("unique", ["id"], None), "a.a8.a8_fk": ("foreign_key", ["x"], {"table": "t", "columns": ["id"]})}
    assert {"type": "references", "target": "a.t"} in facts["a.a5.a5_fk"]["relations"] and [r["type"] for r in facts["a.a6.a6_fk"]["relations"]] == ["contained-in"], "public.t is not t"


@needs_pg
def test_escaped_double_quotes_in_table_constraint_and_column_names(tmp_path):
    facts = {f["qualified_name"]: f for f in _scan(tmp_path, 'CREATE TABLE "p""q" ("i""d" int NOT NULL, code text, CONSTRAINT "p""k" PRIMARY KEY ("i""d"), UNIQUE ("a""b", code));\n'
                                                         'CREATE TABLE c (code text, "c""1" int);\nALTER TABLE c ADD CONSTRAINT "g""h" FOREIGN KEY (code) REFERENCES "p""q" ("i""d");\n'
                                                         'ALTER TABLE "p""q" ADD CONSTRAINT "z""fk" UNIQUE (code);\n', "b").values()}
    assert (facts['p"q.i"d']["attrs"]["type"], facts['c.c"1']["attrs"]["type"], facts['p"q.p"k']["attrs"]["columns"]) == ("int", "int", ['i"d']), '"a""b" is a"b'
    assert (facts['p"q.unique']["attrs"]["columns"], facts['c.g"h']["name"]) == (['a"b', "code"], 'g"h')
    assert facts['c.g"h']["attrs"]["references"] == {"table": 'p"q', "columns": ['i"d']} and {"type": "references", "target": 'b.p"q'} in facts['c.g"h']["relations"]
    assert facts['p"q.z"fk']["relations"] == [{"type": "contained-in", "target": 'b.p"q'}], "an ALTER TABLE on a name with \"\" too"


@needs_pg
def test_a_references_written_in_a_column_marks_the_column_and_gives_no_key(tmp_path):
    facts = _scan(tmp_path, 'CREATE TABLE t (id int PRIMARY KEY);\nCREATE TABLE c (a int REFERENCES t (id), b int REFERENCES t, z int, w int NOT NULL REFERENCES "public"."t"("id"));\n', "c")
    assert [facts[c]["attrs"].get("references") for c in ("c.c.a", "c.c.b", "c.c.z", "c.c.w")] == [
        {"table": "t", "columns": ["id"]}, {"table": "t", "columns": []}, None, {"table": "public.t", "columns": ["id"]}]
    assert not _keys(facts) and {"type": "references", "target": "c.t"} in facts["c.c.b"]["relations"]
    assert (facts["c.c.a"]["attrs"]["type"], facts["c.c.w"]["attrs"]["type"]) == ("int", "int")


@needs_pg
def test_unnamed_keys_count_their_suffix_per_type_within_their_table(tmp_path):
    keys = _keys(_scan(tmp_path, "CREATE TABLE t (a int, b int, UNIQUE (a), FOREIGN KEY (a) REFERENCES t (b), UNIQUE (b), FOREIGN KEY (b) REFERENCES t (a), PRIMARY KEY (a));\n"
                                 "CREATE TABLE u (a int, FOREIGN KEY (a) REFERENCES t (a), UNIQUE (a));\n", "d"))
    assert {i: k[1] for i, k in keys.items()} == {"d.t.unique": ["a"], "d.t.fk": ["a"], "d.t.unique~2": ["b"], "d.t.fk~2": ["b"], "d.t.pk": ["a"], "d.u.fk": ["a"], "d.u.unique": ["a"]}


@needs_pg
def test_check_and_exclude_are_no_keys_and_do_not_swallow_the_next_statement(tmp_path):
    keys = _keys(_scan(tmp_path, 'CREATE TABLE "p" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "a" int NOT NULL, '
                                 'CONSTRAINT "a_pos" CHECK ("a" >= 0), CONSTRAINT "uniq_a" UNIQUE ("a"), CONSTRAINT "a_lt" CHECK ("a" < 9));\n'
                                 "CREATE TABLE n4 (id int, CONSTRAINT n4_pk PRIMARY KEY (id), CONSTRAINT n4_c CHECK (id>0));\n"
                                 "ALTER TABLE n4 ADD CONSTRAINT n4_x EXCLUDE USING gist (id WITH =);\n"
                                 "ALTER TABLE n4 ADD CONSTRAINT n4_u UNIQUE (id) DEFERRABLE INITIALLY DEFERRED;\n", "n"))
    assert keys == {"n.p.uniq_a": ("unique", ["a"], None), "n.n4.n4_pk": ("primary_key", ["id"], None), "n.n4.n4_u": ("unique", ["id"], None)}


@needs_pg
def test_names_keep_their_spelling_and_byte_spans_survive_non_ascii(tmp_path):
    facts = _scan(tmp_path, 'CREATE TABLE Users (Id int PRIMARY KEY, "ñandú" text UNIQUE, Note text);\n'
                            "CREATE TABLE o (uid int, CONSTRAINT o_fk FOREIGN KEY (uid) REFERENCES Users (Id));\n", "u")
    assert facts["u.o.o_fk"]["attrs"]["references"] == {"table": "Users", "columns": ["Id"]} and {"type": "references", "target": "u.Users"} in facts["u.o.o_fk"]["relations"]
    assert (facts["u.Users.ñandú"]["attrs"]["unique"], facts["u.Users.Note"]["attrs"]["type"], facts["u.Users.Id"]["attrs"]["primary_key"]) == (True, "text", True)
    assert facts["u.o.o_fk"]["signature"] == "CONSTRAINT o_fk FOREIGN KEY (uid) REFERENCES Users (Id)"


ENCODED = ("CREATE TABLE a (id int PRIMARY KEY, x int, -- comentario: " + "año " * 20 + "\n  CONSTRAINT a_u UNIQUE (x));\n"
           "CREATE TABLE b (k int, CONSTRAINT b_fk FOREIGN KEY (k) REFERENCES a (id));\n")


@needs_pg
@pytest.mark.parametrize("encoding", ["latin-1", "utf-8"])
def test_a_non_ascii_comment_in_latin_1_or_utf_8_does_not_shift_the_keys_of_the_next_table(tmp_path, encoding):
    from sldb.code.scan import scan_tree

    (tmp_path / "e.sql").write_bytes(ENCODED.encode(encoding))
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert _keys(facts) == {"e.a.a_u": ("unique", ["x"], None), "e.b.b_fk": ("foreign_key", ["k"], {"table": "a", "columns": ["id"]})}
    assert sorted(i for i in facts if i.startswith("e.b.")) == ["e.b.b_fk", "e.b.k"] and facts["e.a.id"]["attrs"]["primary_key"]
    assert [facts[i]["signature"] for i in ("e.a.a_u", "e.b.b_fk", "e.b.k")] == ["CONSTRAINT a_u UNIQUE (x)", "CONSTRAINT b_fk FOREIGN KEY (k) REFERENCES a (id)", "k int"]
    assert {"type": "references", "target": "e.a"} in facts["e.b.b_fk"]["relations"] and not any("keys_partial" in f["attrs"] for f in facts.values())


@needs_pg
def test_a_statement_postgres_rejects_keeps_tree_sitters_reading_and_marks_keys_partial(tmp_path):
    facts = _scan(tmp_path, "CREATE TABLE t (a int, b int, UNIQUE (a));\nCREATE TABLE r (a int, b int, UNIQUE (a), PRIMARY KEY (a) b);\n"
                            "ALTER TABLE t ADD CONSTRAINT tu UNIQUE (b) WHAT;\nCREATE TABLE ok (a int);\n", "r")
    assert [facts[t]["attrs"].get("keys_partial") for t in ("r.t", "r.r", "r.ok")] == [True, True, None], "r does not parse; the ALTER on t neither"
    assert sorted(_keys(facts)) == ["r.t.unique"] and {"r.r.a", "r.r.b"} <= set(facts)


@needs_sql
def test_without_the_extra_the_keys_are_not_read(no_pg, tmp_path):
    facts = _scan(tmp_path, SHOP, "s")
    assert not _keys(facts) and "s.shop_product.id" not in facts and facts["s.shop_product.price"]["attrs"] == {"native_kind": "column_definition", "module": "s"}
    assert all(facts[f"s.{t}"]["attrs"]["keys_partial"] for t in ("shop_category", "shop_tag", "shop_product", "shop_product_tags"))


def test_without_the_sql_grammar_sql_files_are_not_scanned(monkeypatch, tmp_path):
    import sldb.code.runtime as rt
    from sldb.code.scan import scan_tree

    real = rt.importlib.import_module
    monkeypatch.setattr(rt, "_RUNTIME", {})
    monkeypatch.setattr(rt.importlib, "import_module", lambda name: (_ for _ in ()).throw(ImportError(name, name=name)) if name == "tree_sitter_sql" else real(name))
    shutil.copytree(SQL, tmp_path / "db")
    (tmp_path / "db" / "m.py").write_text("def f(): pass\n", encoding="utf-8")
    assert not rt.available(".sql") and sorted(f["id"] for f in scan_tree(tmp_path / "db")) == ["m", "m.f"]


BLOG = Path(__file__).parent.parent / "fixtures" / "treesitter" / "blog_app"


@pytest.fixture
def blog():
    """The facts of IR's Django/DRF blog (a copy of IR's `tests/fixtures/blog_app`), through `sldb.api.code.code_facts`."""
    from sldb.api.code import code_facts

    return {f["id"]: f for f in code_facts(BLOG)["facts"]}


def _call(f):
    return f["attrs"]["call"]


def test_blog_bases_are_extends_relations_as_written(blog):
    for fid, base in [("blog.models.Post", "models.Model"), ("blog.views.PostViewSet", "viewsets.ModelViewSet"), ("blog.serializers.PostSerializer", "serializers.ModelSerializer")]:
        assert {"type": "extends", "target": base} in blog[fid]["relations"] and blog[fid]["attrs"]["bases"] == [base], fid
    assert blog["blog.models.Post.Meta"]["attrs"]["bases"] == [] and blog["blog.models.Post.Status"]["attrs"]["bases"] == ["models.TextChoices"]


def test_blog_action_decorator_carries_its_arguments(blog):
    assert blog["blog.views.PostViewSet.publish"]["attrs"]["decorators"] == [{"name": "action", "args": [], "kwargs": {"detail": "True", "methods": "['post']"}}]
    assert blog["blog.views.PostViewSet.perform_create"]["attrs"]["decorators"] == []


def test_blog_call_chain_handler_method_function(blog):
    handler, method = blog["blog.views.PostViewSet.publish"], blog["blog.models.Post.publish"]
    assert {"name": "post.publish", "line": 24} in handler["attrs"]["calls"] and {"type": "calls", "target": "post.publish"} in handler["relations"]
    assert {"name": "can_publish", "line": 26} in method["attrs"]["calls"] and {"type": "calls", "target": "can_publish"} in method["relations"]
    assert [c["name"] for c in method["attrs"]["calls"]] == ["can_publish", "PermissionError", "timezone.now", "self.save"], "source order, one per call"
    assert blog["blog.models.can_publish"]["kind"] == "function" and blog["blog.models.can_publish"]["attrs"]["calls"] == [{"name": "user.has_perm", "line": 35}]


def test_blog_model_fields_and_meta_are_assignments(blog):
    author, status = blog["blog.models.Post.author"], blog["blog.models.Post.status"]
    assert author["kind"] == "assignment" and author["qualified_name"] == "Post.author" and author["relations"] == [{"type": "contained-in", "target": "blog.models.Post"}]
    assert _call(author) == {"func": "models.ForeignKey", "args": ["settings.AUTH_USER_MODEL"], "kwargs": {"on_delete": "models.PROTECT", "related_name": "'posts'"}}
    assert _call(status) == {"func": "models.CharField", "args": [], "kwargs": {"max_length": "16", "choices": "Status.choices", "default": "Status.DRAFT"}}
    assert _call(blog["blog.models.Post.title"]) == {"func": "models.CharField", "args": [], "kwargs": {"max_length": "200"}}
    assert blog["blog.models.Post.Meta.db_table"]["attrs"]["value"] == "'posts'"
    assert blog["blog.models.Post.Meta.db_table"]["relations"] == [{"type": "contained-in", "target": "blog.models.Post.Meta"}]
    assert blog["blog.models.Post.Status.DRAFT"]["attrs"]["items"] == [{"value": "'draft'"}, {"value": "'Draft'"}]


def test_blog_serializer_meta_model_and_fields(blog):
    assert blog["blog.serializers.PostSerializer.Meta.model"]["attrs"]["value"] == "Post"
    fields = blog["blog.serializers.PostSerializer.Meta.fields"]["attrs"]
    assert fields["items"][:2] == [{"value": "'id'"}, {"value": "'author'"}] and len(fields["items"]) == 6
    assert fields["value"] == "['id', 'author', 'title', 'body', 'status', 'published_at']"
    assert _call(blog["blog.views.PostViewSet.queryset"]) == {"func": "Post.objects.all", "args": [], "kwargs": {}}


def test_blog_urls_path_and_router_register(blog):
    register = blog["blog.urls.router.register"]
    assert (register["kind"], register["name"], register["qualified_name"]) == ("call", "router.register", "router.register")
    assert _call(register) == {"func": "router.register", "args": ["'posts'", "PostViewSet"], "kwargs": {"basename": "'post'"}}
    assert _call(blog["blog.urls.router"]) == {"func": "SimpleRouter", "args": [], "kwargs": {"trailing_slash": "False"}}
    assert blog["blog.urls.urlpatterns"]["attrs"]["value"] == "router.urls"
    assert blog["blogsite.urls.urlpatterns"]["attrs"] == {"native_kind": "assignment", "module": "blogsite.urls", "items": [{"func": "path", "args": ["''", "include('blog.urls')"], "kwargs": {}}]}


STATEMENTS = '''"""Doc."""
reg.add("a")
reg.add("b", *rest, **more)
X: int = 1
a = b = 2
obj.attr = 3
if True:
    hidden = f()


@deco
@route("/x", methods=("GET",))
def view(): return [g(h(y)) for y in ys]


class C(Base, metaclass=Meta):
    def m(self):
        def inner(): nested()
        return self.n()
'''


def test_statements_and_calls_edge_cases(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "mod.py").write_text(STATEMENTS, encoding="utf-8")
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert sorted(i for i in facts if facts[i]["kind"] in ("call", "assignment")) == ["mod.X", "mod.a", "mod.b", "mod.reg.add", "mod.reg.add~2"], "attribute and if-nested statements are not facts"
    assert _call(facts["mod.reg.add~2"]) == {"func": "reg.add", "args": ["'b'", "*rest", "**more"], "kwargs": {}}
    assert facts["mod.X"]["attrs"]["value"] == "1" and facts["mod.X"]["span"] == {"start_line": 4, "end_line": 4}
    assert facts["mod.view"]["attrs"]["decorators"] == [{"name": "deco", "args": [], "kwargs": {}}, {"name": "route", "args": ["'/x'"], "kwargs": {"methods": "('GET',)"}}]
    assert [c["name"] for c in facts["mod.view"]["attrs"]["calls"]] == ["g", "h"]
    assert [r for r in facts["mod.C"]["relations"] if r["type"] == "extends"] == [{"type": "extends", "target": "Base"}]
    assert facts["mod.C.m"]["attrs"]["calls"] == [{"name": "self.n", "line": 19}], "a nested def's calls are its own"
    assert facts["mod.C.m.inner"]["attrs"]["calls"] == [{"name": "nested", "line": 18}]


def test_new_facts_leave_existing_fingerprints_and_normalization_alone(facts):
    from sldb.code.fingerprints import NORMALIZATION

    assert NORMALIZATION == 1, "kinds and attrs were added; no existing fact changed shape"
    assert set(facts["pkg.mod.K.m"]["fingerprints"]) == {"signature", "shape", "docstring", "body"}


def _clashing_tree(root):
    """`pkg/__init__.py` names an assignment, a module call and a class attribute like a sibling module or a method."""
    (root / "pkg").mkdir()
    (root / "pkg" / "__init__.py").write_text("x = 1\ny = make()\nregister(x)\nclass K:\n    m = 1\n    def m(self): pass\n", encoding="utf-8")
    for name, body in [("x", "def f(): pass\n"), ("y", "class C:\n    y = 2\n"), ("register", "")]:
        (root / "pkg" / f"{name}.py").write_text(body, encoding="utf-8")


def test_a_module_assignment_named_like_a_sibling_module_does_not_take_its_id(tmp_path):
    from sldb.api.code import code_facts
    from sldb.code.scan import scan_file, scan_tree

    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "pkg" / "x.py").write_text("def f(): pass\n", encoding="utf-8")
    for facts in ({f["id"]: f for f in scan_tree(tmp_path)}, {f["id"]: f for f in code_facts(tmp_path)["facts"]}):
        assert {i: f["kind"] for i, f in facts.items()} == {"pkg": "module", "pkg.x": "module", "pkg.x.f": "function", "pkg.x~2": "assignment"}
        assert facts["pkg.x.f"]["relations"] == [{"type": "contained-in", "target": "pkg.x"}] and facts["pkg.x~2"]["path"] == "pkg/__init__.py"
    assert [f["id"] for f in scan_file("pkg/__init__.py", tmp_path)] == ["pkg", "pkg.x"], "alone, a file's late ids are given before returning"


def test_with_clashes_existing_ids_are_those_of_a_scan_without_the_new_kinds(tmp_path, monkeypatch):
    import sldb.code.scan as scan
    from sldb.api.code import code_facts

    _clashing_tree(tmp_path)
    old = {"module", "class", "function", "method"}
    new = [{f["id"]: f["kind"] for f in run() if f["kind"] in old} for run in (lambda: scan.scan_tree(tmp_path), lambda: code_facts(tmp_path)["facts"])]
    late = {f["id"]: f["kind"] for f in scan.scan_tree(tmp_path) if f["kind"] not in old}
    monkeypatch.setattr(scan, "statement_facts", lambda *a: [])
    assert new[0] == new[1] == {f["id"]: f["kind"] for f in scan.scan_tree(tmp_path)}
    assert late == {"pkg.x~2": "assignment", "pkg.y~2": "assignment", "pkg.register~2": "call", "pkg.K.m~2": "assignment", "pkg.y.C.y": "assignment"}


URLS = '''from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [path("a/", a)]
urlpatterns += [path("b/", b), path("c/", c)]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
count = 0
count -= 1


class Post(models.Model):
    created = updated = models.DateTimeField(auto_now=True)
    x = obj.attr = y = 3
    p, q = f()
    z: int
'''


@pytest.fixture
def urls(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "urls.py").write_text(URLS, encoding="utf-8")
    return {f["id"]: f for f in scan_tree(tmp_path)}


def _attrs(f):
    return {k: v for k, v in f["attrs"].items() if k not in ("native_kind", "module")}


def test_an_augmented_list_assignment_gives_its_items_and_its_operator(urls):
    first, more = urls["urls.urlpatterns"], urls["urls.urlpatterns~2"]
    assert _attrs(first) == {"items": [{"func": "path", "args": ["'a/'", "a"], "kwargs": {}}]} and "op" not in first["attrs"]
    assert (more["kind"], more["name"], more["attrs"]["native_kind"]) == ("assignment", "urlpatterns", "augmented_assignment")
    assert _attrs(more) == {"op": "+=", "items": [{"func": "path", "args": ["'b/'", "b"], "kwargs": {}}, {"func": "path", "args": ["'c/'", "c"], "kwargs": {}}]}
    assert more["span"] == {"start_line": 6, "end_line": 6} and more["relations"] == [{"type": "contained-in", "target": "urls"}]


def test_an_augmented_call_assignment_gives_its_call_and_any_operator_is_kept(urls):
    static = {"func": "static", "args": ["settings.MEDIA_URL"], "kwargs": {"document_root": "settings.MEDIA_ROOT"}}
    assert _attrs(urls["urls.urlpatterns~3"]) == {"op": "+=", "call": static}
    assert _attrs(urls["urls.count"]) == {"value": "0"} and _attrs(urls["urls.count~2"]) == {"op": "-=", "value": "1"}


def test_a_chained_assignment_gives_one_fact_per_name_with_the_same_value(urls):
    field = {"func": "models.DateTimeField", "args": [], "kwargs": {"auto_now": "True"}}
    for name in ("created", "updated"):
        f = urls[f"urls.Post.{name}"]
        assert (f["kind"], f["name"], f["qualified_name"], _attrs(f)) == ("assignment", name, f"Post.{name}", {"call": field})
        assert f["relations"] == [{"type": "contained-in", "target": "urls.Post"}] and f["span"] == {"start_line": 13, "end_line": 13}
    assert _attrs(urls["urls.Post.x"]) == _attrs(urls["urls.Post.y"]) == {"value": "3"}
    assert sorted(i for i in urls if i.startswith("urls.Post.")) == ["urls.Post.created", "urls.Post.updated", "urls.Post.x", "urls.Post.y"], "an attribute or tuple target and a bare annotation are not facts"

FILE:instruccion
Cold-bundle de la tarea task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

