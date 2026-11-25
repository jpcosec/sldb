FILE:desk/tasks/task-corrección-de-j02-agents-md-clasificado-en-la-puerta-de-identidad-y-derived-guard-sin-importar-el-nú.md
---
sldb:
  by: agent
  at: '2026-11-17T00:47:03Z'
  authority: generated
  via: create_document
id: task-corrección-de-j02-agents-md-clasificado-en-la-puerta-de-identidad-y-derived-guard-sin-importar-el-nú
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- tools/check_identity.py
- tests/test_store_seams.py
depends_on: []
pills: []
files:
- tools/check_identity.py
- tests/store/test_update_fault_tolerance.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
---

# Corrección de j02: AGENTS.md clasificado en la puerta de identidad y derived_guard sin importar el núcleo fuera de los seams

## Rationale

_Explain why this task exists or the business driver behind it._

El integrador retiene j02 (merge driver y rebuild-index, commit 7dbb6bc9) por dos fallos que su tester no vio: (1) tools/check.sh --fast falla en la puerta identidad con 'ERROR archivo versionado sin clasificar en la raíz: AGENTS.md', porque j02 agregó AGENTS.md en la raíz y tools/check_identity.py no lo tiene en EXEMPT; (2) tests/test_store_seams.py::test_only_the_seams_import_the_core_the_models_or_the_runtime falla con 'io/derived_guard.py: sldb.core.exceptions': el módulo nuevo derived_guard del paquete sldb.store.io importa el núcleo fuera de los seams permitidos.

## Goal

_Describe the concrete result this task must produce._

tools/check.sh --fast y tests/test_store_seams.py pasan con j02 integrado, sin cambiar el comportamiento del merge driver, de rebuild-index ni del error que nombra el comando.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) agregar AGENTS.md a EXEMPT en tools/check_identity.py, con un comentario que diga que es la guía de procedimiento para agentes (merge de .sldb). (2) que el guard de índices derivados no importe sldb.core fuera de los seams: usar la excepción que ya usan los demás módulos de sldb.store.io (leer cómo lo hacen) o mover la importación a un seam permitido según tests/test_store_seams.py; el error y su mensaje no cambian. No entra: cambiar la lista de seams del test ni otros archivos de j02.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/test_store_seams.py y tools/check_identity.py. 2) Ver qué excepción usan los demás módulos de sldb.store.io. 3) Corregir el guard y EXEMPT. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_merkle_shards.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan, incluidos test_store_seams.py y check.sh --fast con todas sus puertas; el error de un índice derivado con marcadores sigue nombrando el comando exacto; commit.

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

FILE:desk/atoms/atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r.md
---
sldb:
  by: agent
  at: '2026-11-16T23:58:02Z'
  authority: generated
  via: create_document
id: atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r
title: Un conflicto de git en los índices derivados de .sldb se resuelve con el merge
  driver y sldb stores rebuild-index
five_wh_one_plus: what
tags:
- system:sldb
- topic:store
provenance: tarea j02 (decisión 2 de JP, integrada con H2 de velocidad-hooks), ejecutor
  deskops-e-d029d60e0080, tester deskops-t-1324db7bbee4 PASA
---

# Un conflicto de git en los índices derivados de .sldb se resuelve con el merge driver y sldb stores rebuild-index

## Answer

Una vez por clon: sldb stores merge-driver --install (idempotente) registra en .gitattributes y git config un driver para .sldb/store.yaml, .sldb/core/store_index.yaml y .sldb/core/models/*.yaml: une stores, modelos, links, predicados e include de los dos lados, sin marcadores. Después de cada merge o rebase que toque .sldb/: sldb stores rebuild-index regenera los índices derivados (también repara un archivo con marcadores o que no parsea). Sin driver, cargar un índice con marcadores o corrupto falla con un error que nombra el comando a correr. stores init alerta si otra rama local ya tiene un store: un store por repositorio. Procedimiento en AGENTS.md y docs/versionado-y-colaboracion.md.

FILE:tools/check_identity.py
#!/usr/bin/env python3
"""Puerta de identidad: la frontera entre el producto y su autoaplicación.

Este repositorio es dos cosas: una biblioteca genérica, y esa biblioteca aplicada
a sí misma. La frontera entre las dos existía en el código y no estaba escrita en
ninguna parte, así que nadie podía decidir si una pieza nueva pertenecía.

El contrato está en `contracts/identity.toml`. Acá solo se verifica.

Qué rechaza:

- un modelo de autoaplicación importado desde un paquete del producto — la
  dirección que convierte una biblioteca en un programa de un solo sitio
- un paquete sin grupo asignado
- un directorio de primer nivel versionado y sin clasificar

Qué no ve: si una función es autoaplicable, y si un documento escrito a mano
debería derivarse. Ambas exigen juicio y están marcadas como no mecanizadas en
el contrato.

    python tools/check_identity.py
    python tools/check_identity.py --show    # la identidad declarada
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "sldb"
CONTRACT = ROOT / "contracts" / "identity.toml"

#: Directorios y archivos de primer nivel que no se clasifican: son del entorno,
#: no del sistema.
EXEMPT = {
    "src", "tests", "docs", "tools", "scripts", "build", "dist", "uv.lock",
    "pyproject.toml", "README.md", "CHANGELOG.md", "LICENSE", "standards.md",
    "propuesta",
}


def load() -> dict:
    if not CONTRACT.is_file():
        sys.exit(f"falta el contrato de identidad: {CONTRACT.relative_to(ROOT)}")
    return tomllib.loads(CONTRACT.read_text(encoding="utf-8"))


def executable_source(path: Path) -> str:
    """El código de un archivo sin comentarios ni cadenas de documentación.

    Citar una ruta de ejemplo en una docstring —«un ref es una ruta de proyecto,
    como `desk/tasks/task-a.md`»— no cruza ninguna frontera: explica. Lo que la
    cruza es código que depende de esa ruta.

    Sin esta distinción la puerta reporta como violación toda buena
    documentación, que es la forma más rápida de enseñar a ignorarla.
    """
    import ast as _ast

    text = path.read_text(encoding="utf-8", errors="ignore")
    try:
        tree = _ast.parse(text)
    except SyntaxError:
        return text

    # Las docstrings son expresiones de cadena solas en su enunciado.
    drop: set[int] = set()
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Expr) and isinstance(node.value, _ast.Constant) \
                and isinstance(node.value.value, str):
            drop.update(range(node.lineno, (node.end_lineno or node.lineno) + 1))

    return "\n".join(
        "" if i in drop else re.sub(r"#.*$", "", line)
        for i, line in enumerate(text.splitlines(), 1))


def versioned_top_level() -> set[str]:
    """Lo que está bajo control de versiones, en el primer nivel.

    `-z` da las rutas crudas: sin él, `core.quotepath` cita las que tienen caracteres no
    ASCII (`"docs/...\\303\\251..."`) y el primer componente salía como `"docs`.
    """
    done = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                          capture_output=True, text=True, encoding="utf-8")
    return {path.split("/")[0] for path in done.stdout.split("\0") if path}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show", action="store_true",
                        help="imprime la identidad declarada y sale")
    args = parser.parse_args()

    contract = load()
    product = contract["product"]["packages"]
    self_app = contract["self_application"]
    self_models = self_app["models"]

    if args.show:
        print(contract["statement"].strip())
        print(f"\n  producto        {', '.join(product)}")
        print(f"  autoaplicación  {', '.join(self_app['packages'] + self_models)}")
        print(f"                  {', '.join(self_app['directories'])}")
        print(f"  ajeno           {', '.join(f['path'] for f in contract['foreign'])}")
        state = contract.get("status", {})
        if state:
            print(f"\n  estado: {state['state']} — {state['former_claim']} "
                  f"no ocurrió ({state['commits_after_claim']} commits después)")
        return 0

    problems: list[str] = []

    # La frontera que importa: el producto es genérico, así que no puede nombrar
    # el contenido concreto de ESTE repositorio.
    #
    # La versión anterior de esta puerta compraba los modelos de `selfdoc` como
    # «autoaplicación» y verificaba que el producto no los importara. Al corregir
    # la identidad esa lista quedó vacía, y con ella la puerta pasó a no medir
    # nada mientras seguía imprimiendo PASS. Una puerta vacía es peor que ninguna:
    # afirma una garantía inexistente.
    #
    # La regla correcta es sobre rutas, no sobre modelos: un paquete genérico que
    # menciona `knowledge/` o `desk/` dejó de ser genérico.
    owned = [d for d in self_app["directories"] if not d.startswith(".")]
    paths = {d: re.compile(rf"['\"]{re.escape(d)}/") for d in owned}
    for pkg in product:
        for path in sorted((SRC / pkg).rglob("*.py")):
            code = executable_source(path)
            known_debt = {d["at"].split("#")[0] for d in contract.get("boundary_debt", [])}
            if str(path.relative_to(ROOT)) in known_debt:
                continue
            for directory, pattern in paths.items():
                if pattern.search(code):
                    problems.append(
                        f"{path.relative_to(ROOT)}: el producto ({pkg}) nombra "
                        f"`{directory}/`, que es contenido de este repositorio")

    # Y los modelos del producto declarados en el contrato tienen que existir.
    # Sin esto, el contrato puede listar cualquier cosa y nadie se enteraría.
    declared_models = [m for group in contract["product"].get("models", {}).values()
                       for m in group]
    for model in declared_models:
        if not (SRC / "models" / f"{model}.py").is_file():
            problems.append(
                f"el contrato declara el modelo `{model}` y no existe en "
                f"src/sldb/models/")

    # El inverso: un modelo que existe y el contrato no clasifica.
    for path in sorted((SRC / "models").glob("*.py")):
        if path.stem not in {*declared_models, "__init__"}:
            problems.append(
                f"el modelo `{path.stem}` existe y el contrato no lo clasifica")

    # Los paquetes mezclados cuentan deuda, no violación: la frontera corre por
    # dentro de ellos y no se puede verificar hasta separarlos.
    mixed = contract["product"].get("mixed", {}).get("packages", [])
    self_models = self_models or []

    # Un paquete sin grupo no se puede juzgar, así que agregar uno obliga a
    # decidir de qué lado de la frontera queda.
    classified = set(product) | set(self_app["packages"]) | set(mixed)
    for pkg in sorted(p.name for p in SRC.iterdir()
                      if p.is_dir() and not p.name.startswith("__")):
        if pkg not in classified and pkg not in {"examples", "assets", "templates", "links"}:
            problems.append(f"paquete sin grupo en el contrato: {pkg}")

    # Un directorio versionado y sin clasificar hace que la identidad sea
    # indecidible: nadie puede responder si pertenece.
    known = (set(self_app["directories"]) |
             {f["path"] for f in contract["foreign"]} |
             {o["path"] for o in contract.get("orphan", [])} | EXEMPT)
    for entry in sorted(versioned_top_level()):
        if entry in known or entry.startswith("."):
            continue
        kind = "directorio" if (ROOT / entry).is_dir() else "archivo"
        problems.append(
            f"{kind} versionado sin clasificar en la raíz: {entry} — "
            f"decide si es producto, autoaplicación o ajeno")

    for problem in problems:
        print(f"  ERROR  {problem}")

    if mixed:
        print(f"  deuda  {', '.join(mixed)}: contienen producto y autoaplicación "
              f"mezclados; la frontera no se verifica ahí dentro")

    if debt := contract.get("boundary_debt", []):
        print(f"  deuda  {len(debt)} cruces de frontera contados: código del "
              f"producto que nombra contenido de este repositorio")
        print(f"  deuda  mientras existan, «el producto es genérico» es aspiracional")

    if orphans := contract.get("orphan", []):
        print(f"  deuda  {len(orphans)} huérfanos en la raíz, contados en el "
              f"contrato con la acción pendiente de cada uno")

    foreign = len(contract["foreign"])
    manual = sum(1 for r in contract["rejects"] if not r["mechanized"])
    print(f"  nota   {foreign} directorios declarados ajenos")
    print(f"  nota   {len(declared_models)} modelos del producto clasificados, "
          f"{len(owned)} directorios de contenido vigilados")
    print(f"  nota   {manual} de {len(contract['rejects'])} reglas de rechazo "
          f"no son mecanizables y quedan para revisión humana")
    state = contract.get("status", {})
    if state.get("state") == "activo":
        print(f"  nota   estado: activo (resuelto {state['resolved']}); "
              f"el congelamiento declarado no ocurrió")
    print(f"{'FAIL' if problems else 'PASS'}: identidad — "
          f"{len(product)} paquetes de producto, "
          f"{len(declared_models)} modelos clasificados, "
          f"{len(problems)} violaciones")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

FILE:tests/store/test_update_fault_tolerance.py
from __future__ import annotations

import os
import subprocess
import sys
import time

import pytest
from sldb.cli import main as cli_main
from pathlib import Path


_SRC = str(Path(__file__).resolve().parent.parent.parent / "src")


def _setup_store(root: Path) -> Path:
    """Create a minimal store with one model for testing."""
    cli_main(["stores", "init", "--path", str(root)])
    store_path = root / ".sldb"
    model_py = root / "models.py"
    model_py.write_text(
        "from pydantic import Field\nfrom sldb import StructuredNLDoc\n"
        "class MyDoc(StructuredNLDoc):\n"
        "    __template__ = '\u2e22rev\u2022title\u2e25'\n"
        "    title: str = Field(description='The title')"
    )
    cli_main(
        [
            "models",
            "add",
            "models:MyDoc",
            "--store",
            str(store_path),
            "--pythonpath",
            str(root),
        ]
    )
    doc_path = root / "doc.md"
    cli_main(
        [
            "docs",
            "create",
            "--model",
            "MyDoc",
            "-o",
            str(doc_path),
            '{"title": "Hello"}',
            "--store",
            str(store_path),
            "--pythonpath",
            str(root),
        ]
    )
    return store_path, doc_path


def test_store_update_skips_missing_doc(tmp_path, capsys):
    root = tmp_path / "root"
    root.mkdir()
    store_path, doc_path = _setup_store(root)

    doc_path.unlink()

    exit_code = cli_main(
        ["stores", "update", "--store", str(store_path), "--pythonpath", str(root)]
    )

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Skipped missing documents: doc" in captured.out
    assert "Updated store at" in captured.out


_LOCK_HOLDER_SCRIPT = """\
import os, sys, time
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from sldb.store.io import store_lock
sp = Path(sys.argv[2])
ready_file = Path(sys.argv[4])
duration = float(sys.argv[3])
with store_lock(sp):
    ready_file.write_text("ready")
    time.sleep(duration)
"""


def test_store_lock_fails_fast_when_busy(tmp_path):
    """A subprocess holding the store lock causes parallel write to fail fast."""
    root = tmp_path / "root"
    root.mkdir()
    store_path, _doc_path = _setup_store(root)

    ready_file = tmp_path / "lock_ready"
    lock_holder = subprocess.Popen(
        [sys.executable, "-c", _LOCK_HOLDER_SCRIPT, _SRC, str(store_path), "5.0", str(ready_file)],
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )

    for _ in range(50):
        if ready_file.exists():
            break
        time.sleep(0.1)

    assert ready_file.exists(), "Subprocess never acquired the lock"

    with pytest.raises(SystemExit) as exc:
        cli_main(
            ["stores", "update", "--store", str(store_path), "--pythonpath", str(root)]
        )

    lock_holder.terminate()
    lock_holder.wait()
    assert "busy" in str(exc.value.code).lower() or exc.value.code != 0


def test_store_lock_wait_blocks_until_released(tmp_path):
    """The --wait flag blocks until the lock is released, then succeeds."""
    root = tmp_path / "root"
    root.mkdir()
    store_path, _doc_path = _setup_store(root)

    ready_file = tmp_path / "lock_ready_wait"
    lock_holder = subprocess.Popen(
        [sys.executable, "-c", _LOCK_HOLDER_SCRIPT, _SRC, str(store_path), "1.5", str(ready_file)],
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )

    for _ in range(30):
        if ready_file.exists():
            break
        time.sleep(0.1)

    assert ready_file.exists(), "Subprocess never acquired the lock"

    exit_code = cli_main(
        [
            "stores",
            "update",
            "--wait",
            "--store",
            str(store_path),
            "--pythonpath",
            str(root),
        ]
    )

    lock_holder.wait()
    assert exit_code == 0


def test_atomic_write_cleans_up_temp_file(tmp_path):
    """_atomic_write leaves no .tmp file behind after success."""
    from sldb.store.io.utils import StoreIOUtils
    _atomic_write = StoreIOUtils._atomic_write

    target = tmp_path / "test.yaml"
    _atomic_write(target, "hello: world\n")
    assert target.exists()
    assert target.read_text() == "hello: world\n"
    leftover = list(tmp_path.glob("*.tmp"))
    assert leftover == []


def test_atomic_write_creates_parent_dirs(tmp_path):
    """_atomic_write creates intermediate directories."""
    from sldb.store.io.utils import StoreIOUtils
    _atomic_write = StoreIOUtils._atomic_write

    target = tmp_path / "a" / "b" / "c.yaml"
    _atomic_write(target, "key: val\n")
    assert target.exists()
    assert target.read_text() == "key: val\n"


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=root, capture_output=True, text=True, check=True).stdout


def test_a_conflicted_derived_index_says_which_command_to_run(tmp_path):
    """The exact message, for the store index and for a model index, with markers or unparseable."""
    from sldb.core.exceptions import SLDBStoreError
    from sldb.store.io import invalidate_index_cache, load_models_index, load_store_index

    store_path, _ = _setup_store(tmp_path)
    index_file, model_file = store_path / "core" / "store_index.yaml", store_path / "core" / "models" / "MyDoc.yaml"
    index_file.write_text("<<<<<<< HEAD\nstore_hash: a\n=======\nstore_hash: b\n>>>>>>> other\n", encoding="utf-8")
    model_file.write_text("name: [unclosed\n", encoding="utf-8")
    invalidate_index_cache()
    for path, load in ((index_file, lambda: load_store_index(store_path)), (model_file, lambda: load_models_index(model_file))):
        with pytest.raises(SLDBStoreError) as raised:
            load()
        assert str(raised.value) == f"{path} is a derived index that git could not merge: run `sldb stores rebuild-index` (and `sldb stores merge-driver --install` once per clone)"


def test_merge_driver_install_is_idempotent(tmp_path):
    _git(tmp_path, "init", "-q")
    cli_main(["stores", "init", "--path", str(tmp_path)])
    for _ in range(2):
        assert cli_main(["stores", "merge-driver", "--install", "--store", str(tmp_path / ".sldb")]) == 0
    lines = (tmp_path / ".gitattributes").read_text(encoding="utf-8").splitlines()
    assert lines == [".sldb/core/store_index.yaml merge=sldb", ".sldb/core/models/*.yaml merge=sldb", ".sldb/store.yaml merge=sldb"]
    assert _git(tmp_path, "config", "--get", "merge.sldb.driver").strip() == "sldb stores merge-driver %O %A %B %P"
    assert _git(tmp_path, "config", "--get", "merge.sldb.name").strip()


def test_stores_init_alerts_when_another_branch_already_has_a_store(tmp_path, capsys):
    _git(tmp_path, "init", "-q", "-b", "main")
    cli_main(["stores", "init", "--path", str(tmp_path)])
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "store")
    _git(tmp_path, "checkout", "-q", "--orphan", "dev")
    _git(tmp_path, "rm", "-rq", "--cached", ".")
    import shutil
    shutil.rmtree(tmp_path / ".sldb")
    capsys.readouterr()
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert "alert: branch 'main' already has a store at .sldb/" in capsys.readouterr().err

FILE:instruccion
Cold-bundle de la tarea task-corrección-de-j02-agents-md-clasificado-en-la-puerta-de-identidad-y-derived-guard-sin-importar-el-nú: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_merkle_shards.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

