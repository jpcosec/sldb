FILE:desk/tasks/task-sldb-api-expone-los-facts-de-código-de-un-archivo-o-de-un-árbol-con-span-y-source-hash-y-write-ancho.md
---
sldb:
  by: agent
  at: '2026-11-17T00:42:28Z'
  authority: generated
  via: save_document_payload
id: task-sldb-api-expone-los-facts-de-código-de-un-archivo-o-de-un-árbol-con-span-y-source-hash-y-write-ancho
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
- src/sldb/api/anchors/__init__.py
- CHANGELOG.md
- tests/api/test_anchors.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
---

# sldb.api expone los facts de código de un archivo o de un árbol, con span y source_hash, y write_anchor es público (C1, C2 y C5 de IR)

## Rationale

_Explain why this task exists or the business driver behind it._

specIR solo puede consumir sldb.api, y los facts de código (Python, TS, TSX, JS, JSX y SQL) solo existen en funciones internas: sldb.code.scan.scan_file y scan_tree. IR08 e IR09 quedan bloqueadas sin una función pública que los liste (C1), sin el span y el source_hash de cada símbolo, que la validación de IR pide como archivo, línea y hash (C2), y write_anchor de sldb.api.anchors.anchor_docs está fuera de __all__ (C5). Origen: desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md.

## Goal

_Describe the concrete result this task must produce._

specIR obtiene con una sola llamada pública de sldb.api los facts de un archivo o de un árbol del proyecto, cada uno con path, span (líneas de inicio y fin), source_hash del archivo, kind, qualified_name, signature, doc, relations y attrs, y puede escribir un ancla con write_anchor importado desde sldb.api.anchors.

## Scope

_State what is in scope and what is out of scope._

Entra: un paquete nuevo code dentro de sldb.api con code_facts(root, paths=None) que devuelve la lista de facts de los archivos dados (rutas relativas a root) o de todo el árbol si paths es None, reutilizando scan_file y scan_tree sin duplicar lógica; los facts salen con la forma que ya tienen (fact() de sldb.code.facts), garantizando que span y source_hash vengan llenos; si un archivo no tiene gramática disponible, se omite y la respuesta lo lista en un campo aparte (skipped). Exportar code_facts en el __all__ del paquete nuevo y documentarlo en el docstring. Agregar write_anchor al __all__ de sldb.api.anchors. Tests de la API con un árbol de prueba que mezcle .py, .tsx y .sql. CHANGELOG. No entra: facts nuevos (otras tareas C3 y C4), cambiar la forma de los facts, la CLI.

Precisiones (intento 2): code_facts(root, paths=None) devuelve un dict {"facts": [...], "skipped": [...]}: facts es la lista de facts y skipped la lista de rutas (relativas a root, ordenadas) que no se escanearon por falta de gramática. path en cada fact es relativo a root, con / como separador, como ya lo da scan_file. span es el que ya producen los readers: {"start_line", "end_line"}, base 1 e inclusivo. source_hash es el que ya producen los readers: "sha256:<hex>" de los bytes del archivo; code_facts no lo recalcula, solo garantiza que no venga vacío. Los tests de code_facts van en tests/api/test_anchors.py porque ese archivo ya cubre la API pública de código y anclas; no se crea un archivo de test nuevo. El aviso a IR lo manda el coordinador por deskops message send.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer sldb.code.scan (scan_file, scan_tree), sldb.code.files (find_files), sldb.code.facts y cómo se calcula source_hash. 2) Escribir el paquete nuevo con code_facts. 3) Agregar write_anchor al __all__ de sldb.api.anchors. 4) Tests de la API nueva en tests/api/test_anchors.py. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; from sldb.api.code import code_facts y from sldb.api.anchors import write_anchor funcionan; cada fact devuelto tiene span y source_hash no vacíos; CHANGELOG y commit; aviso a IR.

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

FILE:src/sldb/api/anchors/__init__.py
"""Code anchors (docs/architecture/code-anchoring.md): record what a symbol looks like, check
every anchor of a store against the code now, reconnect what moved by name. Document anchors
(anchoring.md §6): `check_doc_anchors` reports the ones whose target moved or is gone.

`record_anchor` reads one symbol; `check_anchors` only reads unless asked to `record` the
reconnections (owner's decision 3). States are `sldb.models.anchor_state.AnchorState`.
"""

from sldb.api.anchors.check_anchors import check_anchors
from sldb.api.anchors.check_doc_anchors import check_doc_anchors
from sldb.api.anchors.record_anchor import record_anchor

__all__ = ["check_anchors", "check_doc_anchors", "record_anchor"]

FILE:tests/api/test_anchors.py
"""The anchoring rules, executable (docs/architecture/code-anchoring.md §9): one test per rule of
anchoring.md §3, the error-versus-alert split, and no alert ever silent."""
from __future__ import annotations

import json
import shutil
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


TSX = '/** A card. */\nexport function Card({ title }: { title: string }) {\n  return <div>{title}</div>;\n}\n\nexport const helper = (x: number) => x + 1;\n'
needs_ts = pytest.mark.skipif(not available(".tsx"), reason="tree-sitter-typescript not installed (extra [code])")


@pytest.fixture
def front(tmp_path):
    root = tmp_path / "front"
    (root / "src").mkdir(parents=True)
    (root / "src" / "Card.tsx").write_text(TSX, encoding="utf-8")
    (root / "src" / "util.js").write_text("/** Doubles. */\nexport function double(n) {\n  return n * 2;\n}\n", encoding="utf-8")
    store = api.init_store(root).store_path
    api.add_model(store, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    recorded = record_anchor(root, "code:src/Card.tsx::Card")
    write_anchor(store, None, root / "anchors" / "card.md", recorded, "Card renders its title")
    yield root, store, recorded
    for name in [m for m in sys.modules if m.startswith("tmpdocs")]:
        del sys.modules[name]


@needs_ts
def test_a_tsx_component_anchor_is_intact_changed_reconnected_and_lost(front):
    root, store, recorded = front
    assert recorded["kind"] == "component" and recorded["recorded_with"].startswith("treesitter-symbols/1 (tree-sitter-typescript ") and recorded["recorded_with"].endswith(", tsx)")
    assert _state(store) == (AnchorState.INTACT, [])
    card = root / "src" / "Card.tsx"
    card.write_text(TSX.replace("<div>{title}</div>", "<section>{title}</section>"), encoding="utf-8")
    assert _state(store) == (AnchorState.CHANGED, ["body"])
    card.write_text(TSX.replace("function Card(", "function Tile("), encoding="utf-8")
    [report] = check_anchors(store)
    assert (report.state, report.to) == (AnchorState.RECONNECTED, "code:src/Card.tsx::Tile")
    card.write_text("export const helper = (x: number) => x + 1;\n", encoding="utf-8")
    [report] = check_anchors(store)
    assert report.state is AnchorState.LOST and report.candidates == []


@needs_ts
def test_a_js_function_anchor_records_and_stays_intact(front):
    root, store, _ = front
    recorded = record_anchor(root, "code:src/util.js::double")
    assert recorded["kind"] == "function" and recorded["recorded_with"].endswith(", tsx)") and record_anchor(root, "code:src/Card.tsx::")["kind"] == "module"
    write_anchor(store, None, root / "anchors" / "double.md", recorded, "double doubles")
    assert sorted(r.state.value for r in check_anchors(store)) == ["intact", "intact"]


def test_python_anchors_keep_their_recorded_with_and_ts_refs_parse(world):
    from sldb.models.code_ref import parse_code_ref

    root, _store = world
    assert record_anchor(root, REF)["recorded_with"].startswith("treesitter-symbols/1 (tree-sitter-python ") and record_anchor(root, REF)["recorded_with"].endswith(")")
    assert [parse_code_ref(f"code:a/b{ext}::X") for ext in (".ts", ".tsx", ".js", ".jsx", ".sql")] == [(f"a/b{ext}", "X") for ext in (".ts", ".tsx", ".js", ".jsx", ".sql")]
    assert parse_code_ref("code:a/b.css::X") is None


DDL = ("-- Accounts.\nCREATE TABLE IF NOT EXISTS public.users (\n    id bigserial PRIMARY KEY,\n    email text NOT NULL UNIQUE,\n    profile jsonb\n);\n\n"
       "CREATE TABLE orders (id serial, total numeric(10, 2), PRIMARY KEY (id));\n\n"
       "CREATE MATERIALIZED VIEW totals AS SELECT sum(total) AS total FROM orders;\n\nCREATE INDEX CONCURRENTLY orders_total_idx ON orders (total);\n")
needs_sql = pytest.mark.skipif(not available(".sql"), reason="tree-sitter-sql not installed (extra [code])")


@pytest.fixture
def db(tmp_path):
    root = tmp_path / "db"
    (root / "migrations").mkdir(parents=True)
    (root / "migrations" / "0001_initial.sql").write_text(DDL, encoding="utf-8")
    store = api.init_store(root).store_path
    api.add_model(store, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    yield root, store
    for name in [m for m in sys.modules if m.startswith("tmpdocs")]:
        del sys.modules[name]


def _sql_anchor(db, symbol: str) -> dict:
    root, store = db
    recorded = record_anchor(root, f"code:migrations/0001_initial.sql::{symbol}")
    write_anchor(store, None, root / "anchors" / "a.md", recorded, f"{symbol} is in the schema")
    return recorded


def _rewrite(db, old: str, new: str) -> None:
    (db[0] / "migrations" / "0001_initial.sql").write_text(DDL.replace(old, new), encoding="utf-8")


@needs_sql
@pytest.mark.parametrize(("symbol", "kind", "edit", "rename", "to"), [
    ("public.users", "table", ("profile jsonb", "profile json"), ("public.users", "public.people"), "public.people"),
    ("public.users.email", "column", ("NOT NULL UNIQUE", "NOT NULL"), ("email text", "mail text"), "public.users.mail"),
])
def test_a_sql_table_and_column_anchor_are_intact_changed_reconnected_and_lost(db, symbol, kind, edit, rename, to):
    recorded = _sql_anchor(db, symbol)
    assert recorded["kind"] == kind and recorded["recorded_with"].startswith("treesitter-symbols/1 (tree-sitter-sql ") and recorded["recorded_with"].endswith(", sql)")
    assert _state(db[1]) == (AnchorState.INTACT, [])
    _rewrite(db, *edit)
    assert _state(db[1]) == (AnchorState.CHANGED, ["signature", "body"])
    _rewrite(db, *rename)
    [report] = check_anchors(db[1])
    assert (report.state, report.to) == (AnchorState.RECONNECTED, f"code:migrations/0001_initial.sql::{to}")
    _rewrite(db, DDL.split("\n\n")[0], "")
    [report] = check_anchors(db[1])
    assert report.state is AnchorState.LOST and report.candidates == []


@needs_sql
def test_sql_views_indexes_and_the_module_are_anchored_too(db):
    root, store = db
    assert [record_anchor(root, f"code:migrations/0001_initial.sql::{s}")["kind"] for s in ("totals", "orders_total_idx", "orders.total", "")] == ["view", "index", "column", "module"]
    with pytest.raises(ValueError, match="no symbol 'users'"):
        record_anchor(root, "code:migrations/0001_initial.sql::users")
    write_anchor(store, None, root / "anchors" / "v.md", record_anchor(root, "code:migrations/0001_initial.sql::totals"), "totals sums orders")
    assert [r.state.value for r in check_anchors(store)] == ["intact"]


@needs_sql
def test_anchors_on_a_django_sqlmigrate_migration_use_the_unquoted_names(tmp_path):
    root = tmp_path / "dj"
    shutil.copytree(Path(__file__).parent.parent / "fixtures" / "treesitter" / "sql" / "django", root / "m")
    store = api.init_store(root).store_path
    api.add_model(store, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    kinds = [record_anchor(root, f"code:m/0001_initial.sql::{s}")["kind"] for s in ("app_book", "app_book.title", "app_book_author_id_980d3e25")]
    assert kinds == ["table", "column", "index"]
    write_anchor(store, None, root / "anchors" / "b.md", record_anchor(root, "code:m/0001_initial.sql::app_book.title"), "books have a title")
    assert [r.state.value for r in check_anchors(store)] == ["intact"]
    for name in [m for m in sys.modules if m.startswith("tmpdocs")]:
        del sys.modules[name]

FILE:instruccion
Cold-bundle de la tarea task-sldb-api-expone-los-facts-de-código-de-un-archivo-o-de-un-árbol-con-span-y-source-hash-y-write-ancho: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

