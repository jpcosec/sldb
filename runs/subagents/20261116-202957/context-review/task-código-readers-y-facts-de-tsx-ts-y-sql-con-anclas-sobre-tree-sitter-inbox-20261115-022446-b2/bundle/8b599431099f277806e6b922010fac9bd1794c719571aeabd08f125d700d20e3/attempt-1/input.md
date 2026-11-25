FILE:desk/tasks/task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2.md
---
sldb:
  by: agent
  at: '2026-11-16T20:07:45Z'
  authority: generated
  via: save_document_payload
id: task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- pyproject.toml
- uv.lock
- src/sldb/code/runtime.py
- src/sldb/code/scan.py
- src/sldb/models/code_ref.py
- src/sldb/api/anchors/record_anchor.py
- tests/api/test_anchors.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb.code lee el frontend: TS, TSX, JS y JSX con un mismo reader sobre tree-sitter-typescript como extra (B2, parte TS; SQL va aparte)

## Rationale

_Explain why this task exists or the business driver behind it._

specIR ancla cada nodo extraído a su fuente con las anclas de código de sldb y debe leer Django (Python, cubierto), SQL y React TSX/TS. Decisión de JP 2026-11-15: lo genérico va a sldb y specIR solo mapea al dominio (IR08 e IR09 quedan como mapeo sobre estos extractores).

## Goal

_Describe the concrete result this task must produce._

El paquete sldb.code lee TypeScript y JavaScript (.ts, .tsx, .js, .jsx) con un mismo reader, publica sus hechos de fuente con la misma forma que los de Python y soporta anclas code:<ruta>.<ext>::<símbolo>, con tree-sitter-typescript como parte del extra code; SQL lo hace la tarea hermana.

## Scope

_State what is in scope and what is out of scope._

Amplía el pedido parcial del inbox sldb 20261115-022446, que solo pedía anclas: aquí entran readers y facts, no solo anclas. Hoy el escáner recorre solo .py con tree-sitter-python (extra code); sldb.code tiene readers, facts, fingerprints, ids, imports y scan. Alcance: TS/TSX (componentes, funciones, hooks, tipos, imports) y SQL (tablas, columnas, vistas, DDL y migraciones); hechos en la misma forma que los de Python (ver el atom del inventario de código como hechos de fuente); record_anchor y check_anchors con la misma referencia code:<ruta>::<qualified_name>, fingerprints por nodo, estados y reconexión; gramáticas como extras opcionales. Reutilizar la maquinaria existente de Python, no duplicarla. Fuera de alcance: mapear a conceptos de dominio (eso es specIR).

Precisiones (coordinador, 2026-11-16): esta tarea cubre TS y TSX; SQL va en la tarea hermana que depende de esta. kind de los hechos TS: component (función o const que devuelve JSX, nombre en mayúscula), hook (función cuyo nombre empieza por use), type (type o interface), function (el resto), module (el archivo). qualified_name del módulo: la ruta sin extensión con '.' como separador, igual que py_module_name. docstring: el comentario JSDoc /** */ inmediatamente anterior. NORMALIZATION no cambia si la salida de .py es la misma.

Precisiones (JP, 2026-11-16): el foco es el frontend. TS, TSX, JS y JSX se leen con un mismo reader (lang_ts.py); solo cambia la gramática según la extensión (typescript para .ts; tsx para .tsx, .js y .jsx). En JS no hay hechos kind type; component, hook, function y module aplican igual. El qualified_name del módulo sigue siendo la ruta sin extensión: si a.ts y a.js coexisten en la misma carpeta, el segundo en orden alfabético de ruta completa lleva el sufijo ~2, como hace Ids. No se reimplementa nada fuera del paquete sldb.code, salvo el registro de extensiones en code_ref y record_anchor que ya nombra Implementation Path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) pyproject.toml: agregar tree-sitter-typescript>=0.23 al extra code (la versión 0.23.2 está en PyPI) y correr `uv lock` (único cambio de uv.lock: el paquete nuevo; si uv.lock tiene cambios ajenos sin commitear, el ejecutor lo anota y deja al coordinador decidir cómo commitear el lock). 2) src/sldb/code/runtime.py: un runtime por lenguaje elegido por extensión (.py con la gramática de Python; .ts con la gramática typescript; .tsx, .js y .jsx con la gramática tsx del mismo paquete, que también parsea JavaScript) en lugar del Language de Python fijo; si falta la gramática, TreeSitterUnavailable nombra el extra. 3) Un módulo nuevo lang_ts.py en el paquete sldb.code con la query, los readers (JSDoc /** */ como docstring) y los imports de TS/TSX; scan_file (src/sldb/code/scan.py, 78 líneas efectivas: la dispatch por extensión saca código a módulos nuevos) despacha por extensión y find_files incluye .ts/.tsx/.js/.jsx solo si la gramática está. 4) src/sldb/models/code_ref.py (parse_code_ref) acepta .ts, .tsx, .js y .jsx; src/sldb/api/anchors/record_anchor.py (recorded_with) informa la gramática del archivo. 5) Fixtures en tests/fixtures/treesitter/ con un componente .tsx, un hook y un tipo, más un .js con una función y un componente .jsx; tests de intact/changed/lost/reconnected que se saltan sin la gramática.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_agreement.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; un ancla code:<ruta>.tsx::<Componente> se registra y check_anchors la informa intact, changed al cambiar el cuerpo, lost al borrarla y reconnected al moverla; un ancla code:<ruta>.js::<función> del fixture JS se registra y queda intact; sldb sin tree-sitter-typescript sigue escaneando .py; la salida de los .py no cambia (NORMALIZATION igual); CHANGELOG y commit; aviso a IR por deskops message send --desk-root a su desk. La tarea hermana de SQL depende de esta.

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

FILE:pyproject.toml
[project]
name = "structuredLanguageDB"
version = "0.1.13"
description = "Structured Language Database - structured Markdown to Pydantic and back"
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"
license-files = ["LICENSE"]
keywords = ["markdown", "pydantic", "structured-data", "templating", "cli"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Software Development :: Libraries",
    "Topic :: Text Processing :: Markup",
]
dependencies = [
    "pydantic>=2.0",
    "markdown-it-py>=3.0",
    "mdit-py-plugins>=0.4",
    "linkify-it-py>=2.0",
    "jinja2>=3.1",
    "pyyaml>=6.0",
    "networkx>=3.0",
]

[project.scripts]
sldb = "sldb.cli:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project.optional-dependencies]
click = [
    "click>=8.1",
]
graph = [
    "scipy>=1.10",
]
mcp = [
    "mcp>=2.2",
]
code = [
    "tree-sitter>=0.25",
    "tree-sitter-python>=0.23",
]
dev = [
    "scipy>=1.10",
    "build>=1.2",
    "pytest>=8.0",
    "pytest-cov>=5.0",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
sldb = []
"sldb.examples.pandoc_cv" = ["*.md"]
"sldb.assets.skills" = ["*.md"]
"sldb.examples.reference_bundle" = ["*.md", "*.yaml"]
"sldb.notations.palettes" = ["*.yml"]
"sldb.notations.builtin" = ["*.yml"]

[tool.pytest.ini_options]
pythonpath = ["src", "."]
asyncio_default_fixture_loop_scope = "function"

FILE:src/sldb/code/runtime.py
"""tree-sitter and the Python grammar, imported lazily: the optional extra `[code]`."""

from __future__ import annotations

import importlib
from typing import Any

_RUNTIME: list[tuple[Any, Any]] = []


class TreeSitterUnavailable(ImportError):
    """tree-sitter or its Python grammar is not installed: `pip install 'structuredLanguageDB[code]'`."""


def runtime() -> tuple[Any, Any]:
    """`(tree_sitter module, Python Language)`, imported once per process."""
    if not _RUNTIME:
        try:
            ts, grammar = importlib.import_module("tree_sitter"), importlib.import_module("tree_sitter_python")
        except ImportError as exc:
            raise TreeSitterUnavailable(f"tree-sitter runtime missing ({exc.name}): pip install 'structuredLanguageDB[code]'") from exc
        _RUNTIME.append((ts, ts.Language(grammar.language())))
    return _RUNTIME[0]


def available() -> bool:
    try:
        runtime()
    except TreeSitterUnavailable:
        return False
    return True


def parse(src: bytes) -> Any:
    """The tree of `src`; `tree.root_node.has_error` says whether it parsed clean."""
    ts, language = runtime()
    return ts.Parser(language).parse(src)

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
from sldb.code.imports import py_imports, py_module_name, py_nested_imports
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

FILE:src/sldb/models/code_ref.py
"""`code:<path>::<qualified_name>`: an anchor's reference to a Python symbol, by name, never by line.

`<path>` is relative to the project root, with `/`; `<qualified_name>` is the lexical owner
chain the tree-sitter scanner emits (`Class.method`, `function.nested`), empty for the module
itself; a repeated name carries the scanner's `~2`, `~3` suffix.
"""

from __future__ import annotations

PREFIX = "code:"
SEPARATOR = "::"


def parse_code_ref(ref: str) -> tuple[str, str] | None:
    """`(path, qualified_name)`, or None when `ref` does not have the form."""
    if not isinstance(ref, str) or not ref.startswith(PREFIX) or SEPARATOR not in ref:
        return None
    path, _, name = ref[len(PREFIX):].partition(SEPARATOR)
    if not path or path.startswith("/") or ".." in path.split("/") or not path.endswith(".py"):
        return None
    return path, name.strip()


def code_ref(path: str, qualified_name: str) -> str:
    return f"{PREFIX}{path}{SEPARATOR}{qualified_name}"

FILE:src/sldb/api/anchors/record_anchor.py
"""What a symbol looks like now: the `code` block an anchor keeps (code-anchoring.md §2)."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from sldb.models.code_ref import code_ref, parse_code_ref
from sldb.code.fingerprints import NORMALIZATION

SCANNER = "treesitter-symbols/1"


def record_anchor(root: Path, ref: str) -> dict[str, Any]:
    """`{ref, kind, seen, normalization, recorded_with}` of the symbol `ref` names under `root`.

    Raises:
        ValueError: The reference is malformed, the file is missing or does not parse, or the
            symbol is not in it (the message names which).
        TreeSitterUnavailable: The `[code]` extra is not installed.
    """
    parsed = parse_code_ref(ref)
    if parsed is None:
        raise ValueError(f"invalid code reference: {ref!r} (expected code:<path>::<qualified_name>)")
    path, name = parsed
    found = symbol_of(root, path, name)
    if found is None:
        raise ValueError(f"no symbol {name!r} in {path} (or the file is missing)")
    return {"ref": code_ref(path, name), "kind": found["kind"], "seen": dict(found["fingerprints"]), "normalization": NORMALIZATION, "recorded_with": recorded_with()}


def symbols_of(root: Path, path: str) -> list[dict[str, Any]] | None:
    """The facts of one file, or None when it is missing; `attrs.has_error` on the module fact says it did not parse clean."""
    from sldb.code.scan import scan_file

    return scan_file(path, root) if (root / path).is_file() else None


def symbol_of(root: Path, path: str, name: str) -> dict[str, Any] | None:
    """The fact whose qualified name (with its `~n` suffix, if any) is `name`; the module for an empty name."""
    facts = symbols_of(root, path)
    if facts is None:
        return None
    wanted = name or facts[0]["qualified_name"]
    module = facts[0]["id"]
    return next((f for f in facts if (f["id"] if f["kind"] == "module" else f["id"].removeprefix(module + ".")) == wanted or (f["kind"] == "module" and not name)), None)


def recorded_with() -> str:
    try:
        grammar = version("tree-sitter-python")
    except PackageNotFoundError:
        grammar = "?"
    return f"{SCANNER} (tree-sitter-python {grammar})"

FILE:tests/api/test_anchors.py
"""The anchoring rules, executable (docs/architecture/code-anchoring.md §9): one test per rule of
anchoring.md §3, the error-versus-alert split, and no alert ever silent."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

import sldb.api as api
from sldb.api.anchors import check_anchors, record_anchor
from sldb.api.anchors.anchor_docs import write_anchor
from sldb.cli import main as cli_main
from sldb.models.anchor_state import AnchorState
from sldb.code.runtime import available

pytestmark = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")

CODE = 'class K:\n    """K doc."""\n\n    def m(self, x: int = 1) -> int:\n        """M doc."""\n        y = x + 1\n        return y\n\n\ndef free(a):\n    """Free doc."""\n    return a\n'
REF = "code:src/x.py::K.m"


@pytest.fixture
def world(tmp_path):
    root = tmp_path / "repo"
    (root / "src").mkdir(parents=True)
    (root / "src" / "x.py").write_text(CODE, encoding="utf-8")
    store = api.init_store(root).store_path
    api.add_model(store, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    write_anchor(store, None, root / "anchors" / "m.md", record_anchor(root, REF), "m adds one")
    yield root, store
    for name in [m for m in sys.modules if m.startswith("tmpdocs")]:
        del sys.modules[name]


def _edit(root: Path, old: str, new: str) -> None:
    path = root / "src" / "x.py"
    path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")


def _state(store) -> tuple[AnchorState, list[str]]:
    [report] = check_anchors(store)
    return report.state, report.changed


def test_rule_1_docstring_and_body_are_distinct_nodes_and_formatting_is_not_a_mutation(world):
    root, store = world
    assert _state(store) == (AnchorState.INTACT, [])
    _edit(root, "M doc.", "Other doc.")
    assert _state(store) == (AnchorState.CHANGED, ["docstring"])
    _edit(root, "return y", "return y + 1")
    assert _state(store) == (AnchorState.CHANGED, ["docstring", "body"])
    _edit(root, "Other doc.", "M doc.")
    assert _state(store) == (AnchorState.CHANGED, ["body"])
    _edit(root, "return y + 1", "return y")
    _edit(root, "y = x + 1\n", "y   =   x+1\n\n")
    assert _state(store) == (AnchorState.INTACT, [])


def test_rule_2_changed_is_an_alert_with_exit_0_visible_in_text_json_and_envelope(world, capsys):
    root, store = world
    _edit(root, "return y", "return y + 1")
    assert cli_main(["anchors", "check", "--store", str(store)]) == 0
    out = capsys.readouterr().out
    assert "1 changed" in out and "alert: [anchors/changed] CodeAnchorDoc:m: changed(body)" in out
    assert cli_main(["anchors", "check", "--store", str(store), "--format", "json"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["anchors"][0]["state"] == "changed" and [a["code"] for a in report["alerts"]] == ["anchors/changed"] and report["errors"] == []
    assert cli_main(["--envelope", "anchors", "check", "--store", str(store), "--format", "json"]) == 0
    assert [w["code"] for w in json.loads(capsys.readouterr().out)["warnings"]] == ["anchors/changed"]


def test_rule_3_a_rename_reconnects_and_only_record_writes_it(world):
    root, store = world
    _edit(root, "def m(", "def renamed(")
    [report] = check_anchors(store)
    assert (report.state, report.to) == (AnchorState.RECONNECTED, "code:src/x.py::K.renamed")
    assert (root / "anchors" / "m.md").read_text(encoding="utf-8").count("K.renamed") == 0, "check reads only"
    [report] = check_anchors(store, record=True)
    assert report.state is AnchorState.RECONNECTED
    text = (root / "anchors" / "m.md").read_text(encoding="utf-8")
    assert "ref: code:src/x.py::K.renamed" in text and "event: reconnected" in text and "from: code:src/x.py::K.m" in text
    assert _state(store) == (AnchorState.INTACT, [])


def test_rule_3_deleted_or_ambiguous_is_lost_and_lists_the_candidates(world):
    root, store = world
    _edit(root, "def m(", "def m1(")
    _edit(root, "def free(a):\n    \"\"\"Free doc.\"\"\"\n    return a\n", "def free(a):\n    \"\"\"Free doc.\"\"\"\n    return a\n\n\nclass J:\n    def m2(self, x: int = 1) -> int:\n        \"\"\"M doc.\"\"\"\n        y = x + 1\n        return y\n")
    [report] = check_anchors(store)
    assert report.state is AnchorState.LOST and sorted(report.candidates) == ["code:src/x.py::J.m2", "code:src/x.py::K.m1"]
    (root / "src" / "x.py").write_text("def other():\n    return 0\n", encoding="utf-8")
    [report] = check_anchors(store)
    assert report.state is AnchorState.LOST and report.candidates == []


def test_errors_fail_the_command_and_alerts_do_not(world, capsys):
    root, store = world
    (root / "src" / "x.py").write_text("def broken(:\n", encoding="utf-8")
    assert cli_main(["anchors", "check", "--store", str(store)]) == 1
    assert "error: [anchors/unparseable]" in capsys.readouterr().out
    (root / "src" / "x.py").write_text(CODE, encoding="utf-8")
    api.save_document_payload(store, "CodeAnchorDoc", "m", {**record_anchor(root, REF), "ref": "nonsense", "claim": "x"})
    [report] = check_anchors(store)
    assert report.state is AnchorState.INVALID


def test_record_refuses_what_it_cannot_see(world):
    root, _store = world
    with pytest.raises(ValueError, match="invalid code reference"):
        record_anchor(root, "src/x.py::K")
    with pytest.raises(ValueError, match="no symbol"):
        record_anchor(root, "code:src/x.py::K.nope")
    assert record_anchor(root, "code:src/x.py::")["kind"] == "module"


def test_the_cli_records_and_writes_a_signed_theorem(world, capsys):
    root, store = world
    assert cli_main(["anchors", "record", "code:src/x.py::free", "--write", "anchors/free.md", "--claim", "free returns its argument", "--store", str(store)]) == 0
    text = (root / "anchors" / "free.md").read_text(encoding="utf-8")
    assert "authority: theorem" in text and "ref: code:src/x.py::free" in text and "free returns its argument" in text
    assert cli_main(["anchors", "check", "--store", str(store)]) == 0
    assert "2 checked" in capsys.readouterr().out

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

    monkeypatch.setattr(rt, "_RUNTIME", [])
    monkeypatch.setattr(rt.importlib, "import_module", lambda name: (_ for _ in ()).throw(ImportError(name, name=name)))
    with pytest.raises(rt.TreeSitterUnavailable, match=r"\[code\]"):
        rt.runtime()
    assert not rt.available()

FILE:instruccion
Cold-bundle de la tarea task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_agreement.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

