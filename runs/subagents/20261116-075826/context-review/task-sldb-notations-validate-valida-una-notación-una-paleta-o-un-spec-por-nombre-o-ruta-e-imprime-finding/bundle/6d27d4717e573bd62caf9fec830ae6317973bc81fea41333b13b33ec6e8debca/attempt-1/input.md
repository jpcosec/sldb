FILE:desk/tasks/task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding.md
---
sldb:
  by: agent
  at: '2026-11-16T07:38:02Z'
  authority: generated
  via: save_document_payload
id: task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-192054-suggestion-sldb-notations-validar-una-notaci-n-una-paleta-o-un-spec-por-nombre-o-ruta-desde-la-cli.md
depends_on: []
pills:
- desk/contexts/pill-pill-salida-y-orden-de-sldb-notations-validate.md
files:
- src/sldb/cli/parsers/notations.py
- src/sldb/cli/commands/notations.py
- tests/notations/test_notations_sync_spec_cli.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
---

# sldb notations validate valida una notación, una paleta o un spec por nombre o ruta e imprime findings

## Rationale

_Explain why this task exists or the business driver behind it._

La matriz de cobertura de spec2viz (IR 456b862, el doc matriz-de-cobertura de spec2viz en IR) deja la validación de notaciones y paletas (spec2viz notation validate / palette validate, con contraste WCAG) en "usar sldb directamente" y la de specs en "migrado a sldb". sldb ya tiene las comprobaciones pero ningún comando las expone: los subcomandos de sldb notations son list, sync, view, resolve y from-graph (src/sldb/cli/parsers/notations.py). Origen: desk/inbox/20261115-192054-suggestion-sldb-notations-validar-una-notaci-n-una-paleta-o-un-spec-por-nombre-o-ruta-desde-la-cli.md.

## Goal

_Describe the concrete result this task must produce._

`sldb notations validate <nombre|ruta>` detecta si el objetivo es una notación, una paleta o un spec, corre la validación que sldb ya tiene para ese tipo y devuelve findings en el formato de findings de sldb, con exit 0 si no hay errores y 1 si los hay.

## Scope

_State what is in scope and what is out of scope._

Entra: subcomando validate en src/sldb/cli/parsers/notations.py (nuevo _add_validate registrado en add_notations_group) y su comando en src/sldb/cli/commands/notations.py. Resolución del objetivo: una ruta existente se carga por extensión y contenido; un nombre se busca entre las notaciones y paletas builtin y del store. Validadores que se reusan sin reimplementar: load_notation (src/sldb/notations/notation_files.py), load_palette y check_palette (src/sldb/notations/palette_files.py, src/sldb/notations/palette_checks.py, contraste en src/sldb/notations/wcag_contrast.py), load_spec y validate_spec (src/sldb/api/notations/spec_models.py). Salida con --format text|json como el resto de la CLI. Tests en tests/notations/test_notations_sync_spec_cli.py: una notación builtin válida (exit 0), una paleta con contraste insuficiente (finding, exit 1), un spec inválido (exit 1), un nombre desconocido (exit 2 y mensaje "unknown notation, palette or spec: <nombre>"). CHANGELOG.md. No entra: portar las pruebas de spec2viz (tarea aparte), validar catálogos vistas.yml, ni cambiar las reglas de validación existentes.

Precisiones (preflight-1): detección por ruta: si el argumento es un archivo existente, .json o .yml/.yaml; un YAML con clave "palette" o "colors" en la raíz es paleta, con clave "type" de diagrama (la que lee load_spec) es spec, y el resto se intenta como notación con load_notation; si el contenido no cuadra con ningún loader, exit 1 con el error del último loader. Por nombre: primero el store (si --store se pasa), después las builtin; notación antes que paleta; si el nombre existe en dos tipos, se valida el primero y se avisa con una alerta. Una ruta que no existe y no es un nombre conocido da exit 2 con el mismo mensaje. Findings: la clase Finding de sldb.core.finding (las funciones error() y alert() que usa src/sldb/cli/commands/edges.py), impresas con el alert_sink de la CLI como hace stores check. La notación builtin del test es la primera que devuelve builtin_notations() (de sldb.notations), leída en el test, no fija.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/cli/parsers/notations.py y src/sldb/cli/commands/notations.py para copiar el patrón de un subcomando con --store y --format. 2) Escribir la detección de tipo. 3) Convertir las excepciones y los resultados de check_palette/validate_spec en findings (buscar el tipo Finding que usan otros comandos, p. ej. stores check). 4) Tests con tmp_path. 5) CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_notations_sync_spec_cli.py

## Done When

_Name the observable condition that makes the task complete._

`sldb notations validate default` (o el nombre de una notación builtin) sale con 0 (el nombre exacto se toma de `sldb notations list`); los cuatro casos de test pasan; `sldb notations --help` lista validate; CHANGELOG commiteado.

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

FILE:desk/contexts/pill-pill-salida-y-orden-de-sldb-notations-validate.md
---
sldb:
  by: agent
  at: '2026-11-16T07:37:41Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-salida-y-orden-de-sldb-notations-validate
status: active
summary: salida y orden de sldb notations validate
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: salida y orden de sldb notations validate

## What

_Define the context or guardrail this pill carries._

Las respuestas del bundle-1 de la tarea: precisiones de implementación que la revisión en frío pidió y que el contrato deja abiertas.

## Why

_Explain why this context matters for safe execution._

La revisión cold-bundle (bundle-1) mostró que sin estas precisiones el ejecutor tendría que inventar estos detalles.

## When

_Describe when an agent should apply this pill._

Al ejecutar la tarea, antes de tocar código.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/sldb/cli/parsers/notations.py, src/sldb/cli/commands/notations.py

## How

_Describe the correct way to apply this guidance._

La salida usa el mismo flag que sync (--json); no se inventa --format. Las alertas no cambian el exit code: 0 sin errores, 1 con algún error, 2 si el objetivo es desconocido. Orden de intentos para un archivo: paleta (clave palette o colors en la raíz), spec (clave type, y los tipos válidos son los que acepta load_spec, sin enumerarlos aquí) y notación (load_notation). Sin --store se usan solo las builtin.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.

FILE:desk/atoms/atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve.md
---
id: atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
title: Las vistas de notacion y proyeccion se resuelven en sldb.api.notations, por
  CLI y por sldb serve
five_wh_one_plus: where
tags:
- system:sldb
- topic:notations
- topic:serve
provenance: docs/architecture/notations-and-views.md
---

# Las vistas de notacion y proyeccion se resuelven en sldb.api.notations, por CLI y por sldb serve

## Answer

resolve_view, resolve_documents y evaluate_projection_view viven en sldb.api.notations y leen directamente del store; se exponen como sldb notations (list, sync, view, resolve) y en sldb serve bajo GET /notations, GET /notations/view, POST /notations/resolve y GET|POST /views/projection*. /views/<nombre> queda libre para las vistas compuestas de GD25. Ningun consumidor necesita YAML intermedio ni spec2viz para proyectar el grafo con una notacion. Decidido en SV02 (plan absorber-spec2viz-y-modelos-ui), integrado en ddc049b4 y 6ba8bb20.

FILE:src/sldb/cli/parsers/notations.py
"""`sldb notations`: Visual notations, palettes, views, and resolving from the command line."""

from __future__ import annotations

import argparse


def _store_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Project path")


def _add_list(sub: argparse._SubParsersAction) -> None:
    p_list = sub.add_parser("list", help="List notations or projection views in the store or builtins.")
    p_list.add_argument("--views", action="store_true", help="List projection views instead of notations")
    _store_args(p_list)


def _add_sync(sub: argparse._SubParsersAction) -> None:
    p_sync = sub.add_parser("sync", help="Synchronize a notation, a palette, diagram specs or a vistas.yml catalog into the store.")
    p_sync.add_argument("--notation", help="Notation name or YAML file to sync; with --spec, the notation the specs are drawn with (`none` for none)")
    p_sync.add_argument("--palette", help="Palette name or YAML file to sync")
    p_sync.add_argument("--spec", action="append", default=[], help="Diagram spec YAML to reconcile (SpecDoc, SpecNodeDoc, RelationDoc); repeatable")
    p_sync.add_argument("--catalog", help="vistas.yml whose specs are synced with their notation and catalog metadata")
    p_sync.add_argument("--check", action="store_true", help="With --catalog: only validate it (paths, specs, notations); write nothing")
    p_sync.add_argument("--prune", action="store_true", help="With --catalog: delete the catalog SpecDocs the vistas.yml no longer lists")
    p_sync.add_argument("--strict", action="store_true", help="With --spec/--catalog: exit 1 when a ref does not exist or the edge index reports errors")
    p_sync.add_argument("--json", action="store_true", help="With --spec/--catalog: print the list of reports as JSON")
    _store_args(p_sync)


def _add_view(sub: argparse._SubParsersAction) -> None:
    p_view = sub.add_parser("view", help="Resolve a SpecDoc or projection view.")
    p_view.add_argument("spec", help="SpecDoc reference (e.g. SpecDoc:arch or arch) or ViewDoc reference")
    p_view.add_argument("--projection", action="store_true", help="Evaluate as projection view instead of SpecDoc")
    _store_args(p_view)


def _add_resolve(sub: argparse._SubParsersAction) -> None:
    p_resolve = sub.add_parser("resolve", help="Resolve documents under a notation without a SpecDoc.")
    p_resolve.add_argument("--notation", required=True, help="NotationDoc reference (e.g. NotationDoc:uml-class or uml-class)")
    p_resolve.add_argument("--docs", nargs="+", required=True, help="Document references to style (Model:name)")
    p_resolve.add_argument("--relations", nargs="*", help="Optional RelationDoc references to style")
    _store_args(p_resolve)


def _add_from_graph(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("from-graph", help="Compile an sldb graph (snapshot JSON or store index) or a Python tree into a component spec.")
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--snapshot", help="Node-link JSON (`sldb graph snapshot save`, or the Python source graph of `sldb selfdoc python-sync`)")
    source.add_argument("--store", help="Read the edge index of this .sldb (or project) dir via sldb.api")
    source.add_argument("--python", help="Directory of .py files, scanned with sldb.code (extra [code]); nodes module/class/external")
    _from_graph_filters(p)
    p.add_argument("--id", dest="spec_id", help="Spec id. Defaults to the file stem, 'sldb-graph', or the parent dir of --python")
    p.add_argument("--title", help="Spec title. Defaults to '<id> graph' ('<id> AST Architecture' with --python)")
    p.add_argument("--output", help="Write the YAML spec here instead of stdout")


def _from_graph_filters(p: argparse.ArgumentParser) -> None:
    p.add_argument("--node-type", dest="node_types", action="append", default=[], help="Node type to keep (document, model, semantic_tag, ...); repeatable. Default: document, model")
    p.add_argument("--model", dest="models", action="append", default=[], help="Keep only documents of this model (e.g. AtomDoc); repeatable")
    p.add_argument("--relation", dest="relations", action="append", default=[], help="Keep only these relations; repeatable. Overrides the default exclusions")
    p.add_argument("--exclude-relation", dest="exclude_relations", action="append", default=[], help="Drop this relation; repeatable. Default: structural relations")
    p.add_argument("--drop-isolated", action="store_true", help="Drop nodes left without edges after filtering")
    p.add_argument("--module-prefix", dest="module_prefixes", action="append", default=[], help="Keep only Python nodes of this module or below; repeatable. With --python, the one root package")


def add_notations_group(s: argparse._SubParsersAction) -> None:
    """Register `notations list|sync|view|resolve|from-graph`."""
    p = s.add_parser("notations", help="Visual notations, palettes, views and diagram resolver.")
    sub = p.add_subparsers(dest="notations_command", required=True)
    for add in (_add_list, _add_sync, _add_view, _add_resolve, _add_from_graph):
        add(sub)

FILE:src/sldb/cli/commands/notations.py
"""`sldb notations` command handler: list, sync, view, and resolve notations/views; from-graph."""

from __future__ import annotations

import json
from typing import Any

from sldb.api import (
    evaluate_projection_view,
    list_projection_views,
    resolve_documents,
    resolve_view,
    sync_notation,
    sync_palette,
)
from sldb.api.notations.notation_listing import list_notations
from sldb.cli.commands.notations_from_graph import from_graph
from sldb.cli.commands.notations_spec_sync import is_spec_sync, spec_sync


class NotationsCLI:
    """CLI surface for visual notations, palettes, views and diagram resolver."""

    def run(self, args: Any) -> int:
        """Dispatch to the handler of `args.notations_command`."""
        handler = {"list": self._list, "sync": self._sync, "view": self._view, "resolve": self._resolve, "from-graph": from_graph}
        return handler[args.notations_command](args)

    def _dump(self, payload: Any) -> int:
        """Print the payload as JSON; returns the exit code."""
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    def _list(self, args: Any) -> int:
        store_path = args.store or "."
        if args.views:
            return self._dump(list_projection_views(store_path, args.pythonpath))
        return self._dump(list_notations(store_path, args.pythonpath))

    def _sync(self, args: Any) -> int:
        """Specs or a catalog (`--spec`/`--catalog`), else a notation and/or a palette."""
        return spec_sync(args) if is_spec_sync(args) else self._sync_notation(args)

    def _sync_notation(self, args: Any) -> int:
        store_path = args.store or "."
        if not args.notation and not args.palette:
            raise SystemExit("Specify --spec, --catalog, --notation <name|path> or --palette <name|path> to sync")
        reports = []
        if args.palette:
            reports.append(sync_palette(store_path, args.palette, pythonpath=args.pythonpath).to_dict())
        if args.notation:
            reports.append(sync_notation(store_path, args.notation, pythonpath=args.pythonpath).to_dict())
        return self._dump(reports[0] if len(reports) == 1 else {"reports": reports})

    def _view(self, args: Any) -> int:
        store_path = args.store or "."
        resolver = evaluate_projection_view if args.projection else resolve_view
        return self._dump(resolver(store_path, args.spec, pythonpath=args.pythonpath))

    def _resolve(self, args: Any) -> int:
        store_path = args.store or "."
        result = resolve_documents(store_path, args.notation, args.docs, relation_refs=args.relations, pythonpath=args.pythonpath)
        return self._dump(result)


__all__ = ["NotationsCLI"]

FILE:tests/notations/test_notations_sync_spec_cli.py
"""`sldb notations sync --spec/--catalog/--check/--prune/--json`: lo nuevo de la CLI en sldb.

Los tests portados de spec2viz estan en test_spec_sync.py y test_spec_catalog_sync.py; aqui, la
reconciliacion del catalogo (`--prune`), el informe JSON y los avisos en formato de findings.
"""
import json

import yaml

import sldb.api as sldb_api
from sldb.cli import main
from tests.notations.test_spec_sync import ARQ, FLOW


def _catalog(tmp_path, specs):
    if not (tmp_path / ".sldb").exists():
        sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir(exist_ok=True)
    for spec in (ARQ, FLOW):
        (tmp_path / "docs" / f"{spec['id']}.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
    vistas = [{"id": "v", "category": "Cat", "nav": "N", "desc": "D", "specs": [f"{s}.yml" for s in specs]}]
    (tmp_path / "docs" / "vistas.yml").write_text(yaml.safe_dump({"vistas": vistas}), encoding="utf-8")
    return tmp_path / "docs" / "vistas.yml"


def _names(tmp_path, model):
    return sorted(d.name for d in sldb_api.load_runtime_documents(tmp_path / ".sldb", None, include_linked=False) if str(d.model_name) == model)


def test_catalog_orphan_is_a_finding_and_prune_deletes_it(tmp_path, capsys):
    config = _catalog(tmp_path, ["arq", "flow"])
    assert main(["notations", "sync", "--catalog", str(config), "--store", str(tmp_path / ".sldb")]) == 0
    config = _catalog(tmp_path, ["arq"])
    capsys.readouterr()
    assert main(["notations", "sync", "--catalog", str(config), "--store", str(tmp_path / ".sldb")]) == 0
    captured = capsys.readouterr()
    assert "orphan SpecDoc:flow" in captured.out and "[spec-sync/orphan-spec]" in captured.err
    assert _names(tmp_path, "SpecDoc") == ["arq", "flow"]

    assert main(["notations", "sync", "--catalog", str(config), "--store", str(tmp_path / ".sldb"), "--prune", "--json"]) == 0
    reports = json.loads(capsys.readouterr().out)
    pruned = reports[-1]
    assert pruned["spec_id"] == "catalog vistas.yml" and "SpecDoc:flow" in pruned["deleted"]
    assert "SpecNodeDoc:flow.a" in pruned["deleted"] and any(d.startswith("RelationDoc:flow.") for d in pruned["deleted"])
    assert _names(tmp_path, "SpecDoc") == ["arq"] and not any(n.startswith("flow.") for n in _names(tmp_path, "SpecNodeDoc"))


def test_spec_sync_without_catalog_metadata_is_never_an_orphan(tmp_path, capsys):
    config = _catalog(tmp_path, ["arq"])
    assert main(["notations", "sync", "--spec", str(config.parent / "flow.yml"), "--store", str(tmp_path / ".sldb")]) == 0
    assert main(["notations", "sync", "--catalog", str(config), "--store", str(tmp_path / ".sldb"), "--prune"]) == 0
    assert _names(tmp_path, "SpecDoc") == ["arq", "flow"]


def test_unresolved_ref_is_a_finding_and_json_lists_reports(tmp_path, capsys):
    config = _catalog(tmp_path, ["arq"])
    assert main(["notations", "sync", "--spec", str(config.parent / "arq.yml"), "--json"]) == 0
    captured = capsys.readouterr()
    (report,) = json.loads(captured.out)
    assert report["spec_id"] == "arq" and report["problems"] == report["unresolved"] == ["arq.renderers: 'AtomDoc:atom-nope' no existe en el store"]
    assert "[spec-sync/unresolved-ref] arq" in captured.err


def test_check_writes_nothing(tmp_path, capsys):
    config = _catalog(tmp_path, ["arq", "flow"])
    assert main(["notations", "sync", "--catalog", str(config), "--check"]) == 0
    assert "Valid: v: arq.yml" in capsys.readouterr().out and _names(tmp_path, "SpecDoc") == []

FILE:instruccion
Cold-bundle de la tarea task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/notations/test_notations_sync_spec_cli.py

