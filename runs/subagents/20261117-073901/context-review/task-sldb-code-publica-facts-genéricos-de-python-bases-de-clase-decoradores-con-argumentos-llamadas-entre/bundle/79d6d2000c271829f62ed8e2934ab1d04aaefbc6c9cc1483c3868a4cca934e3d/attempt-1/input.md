FILE:desk/tasks/task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre.md
---
sldb:
  by: agent
  at: '2026-11-17T07:38:22Z'
  authority: generated
  via: save_document_payload
id: task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre
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
- src/sldb/code/scan.py
- src/sldb/code/readers.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb.code publica facts genéricos de Python: bases de clase, decoradores con argumentos, llamadas entre símbolos y asignaciones de clase con llamada (C3 de IR, parte genérica)

## Rationale

_Explain why this task exists or the business driver behind it._

specIR necesita derivar de un proyecto Django/DRF las rutas (path(), router.register()), las acciones (@action(detail, methods)), las bases de clase (models.Model, ModelViewSet, ModelSerializer), los campos de modelo con tipo, choices, ForeignKey y Meta.db_table, Meta.model y Meta.fields de serializers, y las llamadas entre símbolos (handler -> Post.publish -> can_publish). Hoy sldb.code solo da módulos, clases, funciones y métodos. Decisión del coordinador (reversible, alineada con el pill keep-sldb-generic y con el alcance de B2, donde mapear a conceptos de dominio es de specIR): sldb publica los hechos sintácticos genéricos y specIR los interpreta como Django/DRF. Origen: desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md.

## Goal

_Describe the concrete result this task must produce._

Los facts de Python llevan, sin conocer ningún framework: las bases de cada clase, los decoradores de cada definición con sus argumentos, las llamadas que hace cada función o método a otros nombres, y las asignaciones a nivel de módulo o de clase cuyo valor es una llamada (nombre, función llamada y argumentos), incluidas las de una clase anidada como Meta; con eso specIR reconstruye rutas, campos, serializers y cadenas de llamadas de un proyecto Django/DRF.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) relación extends desde la clase hacia cada base escrita (texto calificado tal cual, p. ej. models.Model). (2) attrs.decorators: lista de {name, args, kwargs} con los argumentos como texto normalizado. (3) relación calls desde cada función o método hacia cada nombre llamado (texto calificado tal cual: self.publish, Post.objects.create, can_publish), sin resolver tipos; attrs.calls con línea de cada llamada. (4) un kind nuevo assignment para asignaciones de nivel de módulo o de clase (incluida una clase anidada como Meta) cuyo valor es una llamada o un literal simple: name, attrs.call {func, args, kwargs} o attrs.value, contenido en su clase o módulo; así salen urlpatterns = [path(...)], router.register(...) como llamada de módulo (kind call, con func y args), title = models.CharField(max_length=200, choices=...), model = Post y fields = [...]. (5) NORMALIZATION: si cambia la forma de los facts existentes, se sube y se dice en el CHANGELOG. Fixture de Django/DRF mínimo en tests/fixtures/treesitter/ con models, serializers, views con @action, urls con path() y router.register(), y tests. CHANGELOG. No entra: interpretar Django o DRF (es specIR), resolver tipos o imports de las llamadas, TS/JS (otra tarea).

Precisiones (intento 2): (a) Una sentencia de módulo o de clase que es solo una llamada (router.register(...)) es un hecho kind call con attrs.call {func, args, kwargs}. Una asignación (nombre = valor) es kind assignment: si el valor es una llamada, attrs.call; si es una lista o tupla, attrs.items con un elemento por ítem, cada uno {func, args, kwargs} si es llamada o {value} si no (así urlpatterns = [path(...), path(...)] da dos ítems); si es un literal simple, attrs.value. (b) Literal simple: str, bytes, int, float, bool, None, un nombre o atributo con puntos (model = Post) y listas o tuplas de esos (fields = ["id", "title"]). Lo que no sea llamada, lista/tupla ni literal simple da attrs.value con su texto. (c) Todo texto de bases, func, args, kwargs y value se normaliza con py_norm, la misma función que usa signature; kwargs es un dict nombre -> texto. (d) El hecho call de módulo se nombra por su func con sufijo ~N si se repite.

Precisiones (corrección 2, tras dos testers): (1) Los facts nuevos (assignment, call) toman su id después de todos los existentes (Ids.take_late y flush), en scan_tree, scan_file y code_facts; los facts que ya existían conservan el id de HEAD. (2) Una asignación aumentada (nombre += valor y los demás operadores) también es kind assignment, con attrs.op igual al operador ('+=') y el valor leído igual que en '=' (call, items o value); así urlpatterns += [path(...)] da sus ítems. (3) Una asignación encadenada (a = b = valor) da un fact por cada nombre, con el mismo valor. (4) Lo que siga fuera queda documentado en el docstring de py_statements.py. El diff de los intentos anteriores está guardado en runs/subagents/20261116-exec-k3-c1/executor-diff-c3py-c1.patch y es el punto de partida.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/code/readers.py, scan.py, facts.py y fingerprints.py. 2) Escribir los readers nuevos en módulos nuevos del paquete sldb.code (por la regla de 80 líneas). 3) Integrarlos en scan_file para .py. 4) Fixture y tests en tests/selfdoc/test_treesitter_symbols.py. 5) Comprobar que tests/selfdoc/test_treesitter_agreement.py y tests/notations/test_component_spec_python.py siguen pasando. 6) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_agreement.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; sobre el fixture de Django/DRF salen las bases, los decoradores @action con sus argumentos, las llamadas handler -> método -> función, los campos de modelo como assignment con su llamada y argumentos, Meta.db_table, Meta.model y Meta.fields, y las llamadas path() y router.register() de urls; las anclas existentes no cambian de estado; CHANGELOG y commit; aviso a IR.

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

FILE:src/sldb/code/scan.py
"""Scan source files into symbol facts; `.ts`, `.tsx`, `.js` and `.jsx` go to `lang_ts`, `.sql` to `lang_sql`. A Python
file gives its module, classes, functions and methods, each with its qualified name, span, docstring, signature and fingerprints (from kimun's adapter).

A definition under `if`, `try` or any statement other than a class or function body is not
a symbol (its owner chain is not a chain of definitions), exactly like `ast`-based scanners.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from sldb.code.facts import fact, key_of, rels
from sldb.code.files import find_files
from sldb.code.fingerprints import fingerprints
from sldb.code.ids import Ids
from sldb.code.imports import py_imports, py_module_name, py_nested_imports
from sldb.code.readers import field_text, py_doc, py_end_line, py_native_kind, py_signature
from sldb.code.lang_sql import scan_sql_file
from sldb.code.lang_ts import scan_ts_file
from sldb.code.runtime import TS_SUFFIXES, parse, runtime

QUERY = "(class_definition) @class (function_definition) @function"
_TRANSPARENT = {"block", "decorated_definition"}


def scan_tree(root: Path) -> list[dict[str, Any]]:
    """Every source file under `root` (see `find_files`), facts sorted by id; one id space for the whole tree."""
    idgen, facts = Ids(), []
    for rel in find_files(root):
        facts.extend(scan_file(rel, root, idgen))
    return sorted(facts, key=lambda f: f["id"])


def scan_file(rel: str, root: Path, idgen: Ids | None = None) -> list[dict[str, Any]]:
    """The facts of one file: the module first, then its definitions in source order."""
    if rel.endswith(TS_SUFFIXES + (".sql",)):
        return (scan_sql_file if rel.endswith(".sql") else scan_ts_file)(rel, root, idgen or Ids())
    src, idgen = (root / rel).read_bytes(), idgen or Ids()
    rootn, module = parse(src).root_node, py_module_name(rel)
    digest = "sha256:" + hashlib.sha256(src).hexdigest()
    mid = idgen.take(module or "__init__")
    facts = [_module_fact(mid, module, rel, rootn, src, digest)]
    items, owners, names, captured = _analysis(rootn, src)
    return facts + _definition_facts(items, owners, names, captured, src, module, mid, rel, digest, idgen)


def _analysis(rootn: Any, src: bytes) -> tuple[list, dict, dict, dict]:
    """The captured definitions in source order, the owner of each and their qualified names."""
    captured = _captures(rootn)
    items = sorted(captured.values(), key=lambda cn: (cn[1].start_byte, -cn[1].end_byte))
    owners = {key_of(n): _owner_of(n, captured) for _, n in items}
    return items, owners, _qualified_names(items, owners, captured, src), captured


def _module_fact(mid: str, module: str, rel: str, rootn: Any, src: bytes, digest: str) -> dict[str, Any]:
    nlines = len(src.decode("utf-8", "replace").splitlines())
    imports, nested = sorted(py_imports(rootn, src)), sorted(py_nested_imports(rootn, src))
    return fact(id=mid, kind="module", name=module.rsplit(".", 1)[-1] if module else "__init__", qualified_name=module, path=rel,
                span={"start_line": 1, "end_line": max(nlines, 1)}, source_hash=digest, doc=py_doc(rootn, src), relations=rels(None, imports),
                attrs={"native_kind": rootn.type, "module": module, "imports": imports, "nested_imports": nested, "has_error": rootn.has_error}, fingerprints=fingerprints(rootn, src))


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

FILE:src/sldb/code/readers.py
"""Readers over tree-sitter Python nodes: text, docstring, signature, kind (from kimun's adapter)."""

from __future__ import annotations

import ast
import inspect
import re
from typing import Any


def text(node: Any, src: bytes) -> str:
    return src[node.start_byte:node.end_byte].decode("utf-8", "replace")


def field_text(node: Any, src: bytes, field: str) -> str | None:
    child = node.child_by_field_name(field)
    return text(child, src) if child is not None else None


def first_statement(block: Any) -> Any:
    """First non-comment named child of a body-like node."""
    for child in block.named_children if block is not None else []:
        if child.type != "comment":
            return child
    return None


def py_string_value(node: Any, src: bytes) -> str | None:
    """Evaluate a (possibly implicitly concatenated) string literal; None if not a plain str."""
    try:
        value = ast.literal_eval("(" + text(node, src) + "\n)")
    except (ValueError, SyntaxError):
        return None
    return value if isinstance(value, str) else None


def docstring_node(node: Any) -> Any:
    """The expression statement holding the docstring of a module, class or function, or None."""
    body = node if node.type == "module" else node.child_by_field_name("body")
    stmt = first_statement(body)
    if stmt is None or stmt.type != "expression_statement" or stmt.named_child_count != 1:
        return None
    return stmt if stmt.named_children[0].type in ("string", "concatenated_string") else None


def py_doc(node: Any, src: bytes) -> str | None:
    stmt = docstring_node(node)
    value = py_string_value(stmt.named_children[0], src) if stmt is not None else None
    return None if value is None else inspect.cleandoc(value)


def py_end_line(node: Any) -> int:
    """Line of the last real token: tree-sitter lets a block swallow trailing comment lines, ast does not."""
    while True:
        kids = [c for c in node.children if c.type != "comment"]
        if not kids:
            return node.end_point[0] + 1
        node = kids[-1]


def py_norm(t: str) -> str:
    """Whitespace-collapse and requote simple "x" strings as 'x' (what ast.unparse prints)."""
    return re.sub(r'(?<![\w"])"([^"\'\\\n]*)"(?!")', r"'\1'", " ".join(t.split()))


def py_param(p: Any, src: bytes) -> str:
    if p.type == "typed_default_parameter":
        return f"{field_text(p, src, 'name')}: {py_norm(field_text(p, src, 'type'))}={py_norm(field_text(p, src, 'value'))}"
    if p.type == "default_parameter":
        return f"{field_text(p, src, 'name')}={py_norm(field_text(p, src, 'value'))}"
    return py_norm(text(p, src))


def py_signature(node: Any, src: bytes) -> str | None:
    if node.type != "function_definition":
        return None
    params = node.child_by_field_name("parameters")
    inner = [py_param(c, src) for c in params.named_children if c.type != "comment"]
    return f"{field_text(node, src, 'name')}({', '.join(inner)})"


def py_native_kind(node: Any, src: bytes) -> str:
    if node.type == "class_definition":
        return "ClassDef"
    is_async = any(c.type == "async" for c in node.children if c.start_byte < node.child_by_field_name("name").start_byte)
    return "AsyncFunctionDef" if is_async else "FunctionDef"

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
                     "orders.user_id": "column", "orders.total": "column", "orders.pk": "constraint", "orders.fk": "constraint", "orders.unique": "constraint",
                     "active_users": "view", "order_totals": "view", "orders_user_idx": "index"}, "table constraints are keys, not columns"
    users, email = sql_facts["public.users"], sql_facts["public.users.email"]
    assert (users["name"], users["qualified_name"], email["name"], email["qualified_name"]) == ("users", "public.users", "email", "public.users.email")
    assert sql_facts["orders"]["qualified_name"] == "orders" and sql_facts["migrations.0001_initial"]["qualified_name"] == "migrations.0001_initial"
    assert email["relations"] == [{"type": "contained-in", "target": "migrations.0001_initial.public.users"}]
    assert (sql_facts["order_totals"]["attrs"]["native_kind"], sql_facts["active_users"]["attrs"]["native_kind"]) == ("create_materialized_view", "create_view")


@needs_sql
def test_sql_unnamed_table_keys_and_the_keys_written_in_a_column(sql_facts):
    fk, pk, uniq = sql_facts["orders.fk"], sql_facts["orders.pk"], sql_facts["orders.unique"]
    assert [(k["name"], k["qualified_name"], k["attrs"]["constraint_type"], k["attrs"]["columns"]) for k in (pk, fk, uniq)] == [
        ("pk", "orders.pk", "primary_key", ["id"]), ("fk", "orders.fk", "foreign_key", ["user_id"]), ("unique", "orders.unique", "unique", ["user_id", "id"])]
    assert fk["attrs"]["references"] == {"table": "public.users", "columns": ["id"]} and "references" not in pk["attrs"]
    assert fk["relations"] == [{"type": "contained-in", "target": "migrations.0001_initial.orders"}, {"type": "references", "target": "migrations.0001_initial.public.users"}]
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


@needs_sql
def test_sql_repeated_objects_take_a_suffix_and_a_statement_with_errors_keeps_what_reads(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "m.sql").write_text('CREATE TABLE t (a int);\nCREATE TABLE "t" (a int, b int);\n'
                                    "CREATE TABLE bad (a int GENERATED BY DEFAULT AS IDENTITY, b int, CONSTRAINT k UNIQUE (a));\n"
                                    'CREATE TABLE (z int);\nCREATE INDEX i ON t (a);\nCREATE INDEX "i" ON t (b);\n', encoding="utf-8")
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert sorted(facts) == ["m", "m.bad", "m.bad.a", "m.bad.b", "m.bad.k", "m.i", "m.i~2", "m.t", "m.t.a", "m.t~2", "m.t~2.a", "m.t~2.b"], "nothing of a nameless table"
    assert facts["m.bad.a"]["attrs"] | {"module": None} == {"native_kind": "column_definition", "module": None, "type": "int", "identity": True, "parse_partial": True}
    assert (facts["m.bad.k"]["kind"], facts["m.bad.k"]["attrs"]["constraint_type"], facts["m.bad.k"]["attrs"]["columns"]) == ("constraint", "unique", ["a"])
    assert (facts["m.t~2"]["qualified_name"], facts["m.t~2.b"]["qualified_name"], facts["m.i~2"]["qualified_name"]) == ("t~2", "t~2.b", "i~2"), '"t" is t'
    (tmp_path / "n.sql").write_text("CREATE TABLE (z int);\n", encoding="utf-8")
    modules = {f["id"]: f["attrs"] for f in scan_tree(tmp_path) if f["kind"] == "module"}
    assert [(modules[m]["has_error"], modules[m]["parse_errors"]) for m in ("m", "n")] == [(False, True), (True, True)], "unparseable only when nothing reads"


DJANGO = {"app_author": "table", "app_author.id": "column", "app_author.name": "column", "app_author.profile": "column", "app_author.created_at": "column",
          "app_book": "table", "app_book.id": "column", "app_book.title": "column", "app_book.pages": "column", "app_book.slug": "column", "app_book.author_id": "column",
          "app_book.slug_pages_uniq": "constraint", "app_book.app_book_title_author_id_f24131bb_uniq": "constraint",
          "app_book.app_book_author_id_980d3e25_fk_app_author_id": "constraint",
          "app_book_slug_780ddf03_like": "index", "app_book_author_id_980d3e25": "index", "app_book_title_idx": "index"}


@needs_sql
def test_a_django_sqlmigrate_migration_gives_its_tables_columns_and_indexes():
    from sldb.code.scan import scan_file

    facts = {f["qualified_name"]: f for f in scan_file("django/0001_initial.sql", SQL)[1:]}
    assert {q: f["kind"] for q, f in facts.items()} == DJANGO, "inside BEGIN/COMMIT, unquoted, with the IDENTITY id columns and the keys"
    assert (facts["app_book"]["doc"], facts["app_book"]["name"], facts["app_book.slug"]["name"]) == ("Create model Book", "app_book", "slug")
    assert facts["app_book.author_id"]["relations"] == [{"type": "contained-in", "target": "django.0001_initial.app_book"}]
    assert facts["app_book_author_id_980d3e25"]["signature"] == 'CREATE INDEX "app_book_author_id_980d3e25" ON "app_book" ("author_id")'


@needs_sql
def test_a_django_migration_gives_the_identity_primary_key_and_the_keys_of_alter_table():
    from sldb.code.scan import scan_file

    facts = {f["qualified_name"]: f for f in scan_file("django/0001_initial.sql", SQL)[1:]}
    ident = facts["app_book.id"]
    assert ident["attrs"] | {"module": None} == {"native_kind": "column_definition", "module": None, "type": "bigint", "primary_key": True, "identity": True, "parse_partial": True}
    assert ident["relations"] == [{"type": "contained-in", "target": "django.0001_initial.app_book"}] and ident["name"] == "id"
    assert (facts["app_book.slug"]["attrs"].get("unique"), facts["app_book.pages"]["attrs"]["type"], facts["app_author.created_at"]["attrs"]["type"]) == (True, "integer", "timestamp with time zone")
    fk = facts["app_book.app_book_author_id_980d3e25_fk_app_author_id"]
    assert (fk["kind"], fk["name"], fk["attrs"]["native_kind"], fk["attrs"]["constraint_type"], fk["attrs"]["columns"]) == (
        "constraint", "app_book_author_id_980d3e25_fk_app_author_id", "add_constraint", "foreign_key", ["author_id"])
    assert fk["attrs"]["references"] == {"table": "app_author", "columns": ["id"]}
    assert fk["relations"] == [{"type": "contained-in", "target": "django.0001_initial.app_book"}, {"type": "references", "target": "django.0001_initial.app_author"}]
    uniq = [facts[f"app_book.{n}"]["attrs"] for n in ("app_book_title_author_id_f24131bb_uniq", "slug_pages_uniq")]
    assert [(u["constraint_type"], u["columns"]) for u in uniq] == [("unique", ["title", "author_id"]), ("unique", ["slug", "pages"])]


@needs_sql
def test_a_foreign_key_to_a_table_of_another_migration_has_references_but_no_relation():
    from sldb.code.scan import scan_file

    facts = {f["qualified_name"]: f for f in scan_file("django/blog_0001_initial.sql", SQL)[1:]}
    fk = facts["posts.posts_author_id_099b8aca_fk_auth_user_id"]
    assert fk["attrs"]["references"] == {"table": "auth_user", "columns": ["id"]}, "IR's blog fixture: auth_user lives in another app"
    assert fk["relations"] == [{"type": "contained-in", "target": "django.blog_0001_initial.posts"}]
    assert (facts["posts.id"]["attrs"]["primary_key"], facts["posts.published_at"]["attrs"]["type"]) == (True, "timestamp with time zone")


@needs_sql
def test_keys_of_alter_table_unnamed_repeated_and_out_of_scope(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "k.sql").write_text("ALTER TABLE z ADD CONSTRAINT zf FOREIGN KEY (a) REFERENCES t (a);\n"
                                    "CREATE TABLE t (a int UNIQUE, b int, c int DEFAULT 'primary key', UNIQUE (a), UNIQUE (b), FOREIGN KEY (c) REFERENCES t (a));\n"
                                    "ALTER TABLE t ADD CONSTRAINT tp PRIMARY KEY (a, b);\nALTER TABLE t ADD PRIMARY KEY (a);\nALTER TABLE t ADD COLUMN d int;\n"
                                    "ALTER TABLE t ADD CONSTRAINT tc CHECK (a > 0);\n", encoding="utf-8")
    found = [f for f in scan_tree(tmp_path) if f["kind"] == "constraint"]
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert sorted(f["id"] for f in found) == ["k.t.fk", "k.t.tp", "k.t.unique", "k.t.unique~2", "k.z.zf"], "ADD without a name, ADD COLUMN, CHECK: no fact"
    assert [facts[i]["attrs"]["columns"] for i in ("k.t.unique", "k.t.unique~2")] == [["a"], ["b"]], "~2 in source order"
    assert facts["k.z.zf"]["relations"] == [{"type": "contained-in", "target": "k"}, {"type": "references", "target": "k.t"}], "the table after it still counts"
    assert facts["k.t.tp"]["relations"] == [{"type": "contained-in", "target": "k.t"}] and facts["k.t.tp"]["attrs"]["columns"] == ["a", "b"]
    assert (facts["k.t.a"]["attrs"].get("unique"), "primary_key" in facts["k.t.c"]["attrs"]) == (True, False), "a quoted literal is no key"


@needs_sql
def test_a_foreign_key_without_referenced_columns_references_the_primary_key(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "s.sql").write_text("CREATE TABLE public.parent (id int PRIMARY KEY, code int);\n"
                                    "ALTER TABLE public.parent ADD CONSTRAINT parent_self_fk FOREIGN KEY (code) REFERENCES public.parent;\n", encoding="utf-8")
    fk = {f["id"]: f for f in scan_tree(tmp_path)}["s.public.parent.parent_self_fk"]
    assert fk["attrs"]["references"] == {"table": "public.parent", "columns": []}, "columns [] is the referenced table's primary key"
    assert {"type": "references", "target": "s.public.parent"} in fk["relations"]


@needs_sql
def test_key_columns_respect_double_quotes(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "q.sql").write_text('CREATE TABLE odd ("a)b" int, "c,d" int, UNIQUE ("a)b"), FOREIGN KEY ("a)b", "c,d") REFERENCES odd ("c,d", "a)b"));\n', encoding="utf-8")
    facts = {f["id"]: f["attrs"] for f in scan_tree(tmp_path)}
    assert facts["q.odd.unique"]["columns"] == ["a)b"]
    assert (facts["q.odd.fk"]["columns"], facts["q.odd.fk"]["references"]) == (["a)b", "c,d"], {"table": "odd", "columns": ["c,d", "a)b"]})


@needs_sql
def test_a_table_foreign_key_without_referenced_columns_has_references(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "a.sql").write_text("CREATE TABLE t (id int PRIMARY KEY);\nCREATE TABLE d (id int, FOREIGN KEY (id) REFERENCES t);\n"
                                    "CREATE TABLE f2 (id int, FOREIGN KEY (id) REFERENCES t ON DELETE CASCADE, PRIMARY KEY (id));\n", encoding="utf-8")
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert [facts[k]["attrs"]["references"] for k in ("a.d.fk", "a.f2.fk")] == [{"table": "t", "columns": []}] * 2, "last key or not, CREATE TABLE"
    assert {"type": "references", "target": "a.t"} in facts["a.d.fk"]["relations"] and facts["a.f2.pk"]["attrs"]["columns"] == ["id"]


@needs_sql
def test_escaped_double_quotes_in_table_constraint_and_column_names(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "b.sql").write_text('CREATE TABLE "p""q" ("i""d" int NOT NULL, code text, CONSTRAINT "p""k" PRIMARY KEY ("i""d"), UNIQUE ("a""b", code));\n'
                                    'CREATE TABLE c (code text);\nALTER TABLE c ADD CONSTRAINT "g""h" FOREIGN KEY (code) REFERENCES "p""q" ("i""d");\n', encoding="utf-8")
    facts = {f["qualified_name"]: f for f in scan_tree(tmp_path)}
    assert facts['p"q.i"d']["attrs"]["type"] == "int" and facts['p"q.p"k']["attrs"]["columns"] == ['i"d'], '"a""b" is a"b'
    assert (facts['p"q.unique']["attrs"]["columns"], facts['c.g"h']["name"]) == (['a"b', "code"], 'g"h')
    assert facts['c.g"h']["attrs"]["references"] == {"table": 'p"q', "columns": ['i"d']} and {"type": "references", "target": 'b.p"q'} in facts['c.g"h']["relations"]


@needs_sql
def test_a_references_written_in_a_column_marks_the_column_and_gives_no_key(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "c.sql").write_text("CREATE TABLE t (id int PRIMARY KEY);\nCREATE TABLE c (a int REFERENCES t (id), b int REFERENCES t, z int);\n", encoding="utf-8")
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert [facts[c]["attrs"].get("references") for c in ("c.c.a", "c.c.b", "c.c.z")] == [{"table": "t", "columns": ["id"]}, {"table": "t", "columns": []}, None]
    assert not [f for f in facts.values() if f["kind"] == "constraint"] and {"type": "references", "target": "c.t"} in facts["c.c.b"]["relations"]
    assert (facts["c.c.a"]["attrs"]["type"], facts["c.c.b"]["attrs"]["type"]) == ("int", "int")


@needs_sql
def test_unnamed_keys_count_their_suffix_per_type_within_their_table(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "d.sql").write_text("CREATE TABLE t (a int, b int, UNIQUE (a), FOREIGN KEY (a) REFERENCES t (b), UNIQUE (b), FOREIGN KEY (b) REFERENCES t (a), PRIMARY KEY (a));\n"
                                    "CREATE TABLE u (a int, FOREIGN KEY (a) REFERENCES t (a), UNIQUE (a));\n", encoding="utf-8")
    keys = {f["id"]: f["attrs"]["columns"] for f in scan_tree(tmp_path) if f["kind"] == "constraint"}
    assert keys == {"d.t.unique": ["a"], "d.t.fk": ["a"], "d.t.unique~2": ["b"], "d.t.fk~2": ["b"], "d.t.pk": ["a"], "d.u.fk": ["a"], "d.u.unique": ["a"]}


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
Cold-bundle de la tarea task-sldb-code-publica-facts-genéricos-de-python-bases-de-clase-decoradores-con-argumentos-llamadas-entre: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_agreement.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

