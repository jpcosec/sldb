FILE:desk/tasks/task-sldb-notations-from-graph-elige-el-campo-del-label-el-campo-que-da-kind-o-estilo-y-un-campo-de-agrup.md
---
sldb:
  by: agent
  at: '2026-11-16T06:20:19Z'
  authority: generated
  via: create_document
id: task-sldb-notations-from-graph-elige-el-campo-del-label-el-campo-que-da-kind-o-estilo-y-un-campo-de-agrup
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-004723-suggestion-sldb-notations-from-graph-elegir-campo-para-label-kind-estilo-y-agrupaci-n-heredado-de-spec2viz.md
depends_on: []
pills: []
files:
- src/sldb/cli/commands/notations_from_graph.py
- src/sldb/cli/parsers/notations.py
- tests/notations/test_notations_from_graph_cli.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb notations from-graph elige el campo del label, el campo que da kind o estilo y un campo de agrupación

## Rationale

_Explain why this task exists or the business driver behind it._

spec2viz diagram from-graph pasó a sldb notations from-graph --store/--snapshot (src/sldb/cli/commands/notations_from_graph.py) y conserva la limitación: el label del nodo es el id del documento (repo-chatbot-infra) y el kind es el modelo (RepositoryDoc), así que no se pueden colorear los repos por sistema o estado sin editar el spec generado. Lo pidió Governance (DAG de repos, 2026-10-21). Origen: desk/inbox/20261116-004723-suggestion-sldb-notations-from-graph-elegir-campo-para-label-kind-estilo-y-agrupaci-n-heredado-de-spec2viz.md.

## Goal

_Describe the concrete result this task must produce._

from-graph acepta --label-field <campo>, --kind-field <campo|tag:<namespace>> y --group-field <campo|tag:<namespace>>; con ellos, el label del nodo es el valor de ese campo del payload (o el id si falta), el kind es el valor del campo o del tag con ese namespace (o el modelo si falta), y los nodos con el mismo valor de agrupación quedan dentro de un nodo contenedor con aristas contains.

## Scope

_State what is in scope and what is out of scope._

Entra: los tres flags en el parser de from-graph (src/sldb/cli/parsers/notations.py, _add_from_graph y _from_graph_filters) y su aplicación en notations_from_graph.py y en la función de API que compila el grafo a spec (localizarla desde notations_from_graph.py). Un tag se lee de la lista tags del payload: "tag:system" toma el primer tag que empieza por "system:" y usa lo que sigue. Tests en tests/notations/test_notations_from_graph_cli.py: un store en tmp_path con dos RepositoryDoc-like (title y tags system:a / system:b); con --label-field title --kind-field tag:system los nodos tienen label = title y kind a/b; con --group-field tag:system hay dos contenedores con aristas contains. Sin flags, la salida es idéntica a hoy (golden del test existente). CHANGELOG.md. No entra: estilos o paletas nuevas; el --snapshot sin payload solo usa el id y el modelo (se documenta en el --help).

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer notations_from_graph.py, el parser y tests/notations/test_notations_from_graph_cli.py. 2) Agregar flags. 3) Aplicarlos al construir nodos. 4) Tests. 5) CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_notations_from_graph_cli.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_graph.py

## Done When

_Name the observable condition that makes the task complete._

Los dos comandos pasan con los tests nuevos; sin flags la salida no cambia; CHANGELOG y commit.

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

FILE:src/sldb/cli/commands/notations_from_graph.py
"""`sldb notations from-graph`: a component spec from a snapshot, a store's edge index or a Python tree.

Ported from `spec2viz diagram from-graph` and `spec2viz diagram generate` (python-ast). The YAML
goes to stdout unless `--output`; the findings (alerts) go to stderr, so stdout stays YAML.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

from sldb.api import load_edge_index
from sldb.api.notations import component_spec_from_graph, component_spec_from_python, index_graph, load_node_link_graph, write_component_spec
from sldb.api.notations.component_spec_findings import dangling_edges
from sldb.cli.alert_sink import report

_GRAPH_ONLY = ("node_types", "models", "relations", "exclude_relations", "drop_isolated")


def from_graph(args: Any) -> int:
    """Dispatch `--python` to the code scanner and `--snapshot`/`--store` to the graph compiler."""
    if args.python:
        return _from_python(args)
    try:
        nodes, edges, attrs, source, default_id = _read_graph(args)
    except Exception as exc:
        print(f"Error reading graph: {exc}", file=sys.stderr)
        return 1
    _report(dangling_edges(nodes, edges))
    return _emit(_compile(args, nodes, edges, attrs, source, args.spec_id or default_id), args.output)


def _read_graph(args: Any) -> tuple:
    if args.store:
        nodes, edges = index_graph(load_edge_index(args.store))
        return nodes, edges, None, f"store {args.store}", "sldb-graph"
    nodes, edges, attrs = load_node_link_graph(args.snapshot)
    return nodes, edges, attrs, f"file {args.snapshot}", Path(args.snapshot).stem


def _compile(args: Any, nodes: dict, edges: list, attrs: dict | None, source: str, sid: str) -> dict:
    return component_spec_from_graph(
        nodes, edges, node_types=args.node_types, models=args.models, relations=args.relations,
        exclude_relations=args.exclude_relations or None, drop_isolated=args.drop_isolated,
        spec_id=sid, title=args.title or f"{sid} graph", source=source, attrs=attrs, module_prefixes=args.module_prefixes,
    )


def _from_python(args: Any) -> int:
    if any(getattr(args, name) for name in _GRAPH_ONLY) or len(args.module_prefixes) > 1:
        raise SystemExit("--python takes only --module-prefix (one root package), --id, --title and --output")
    pid = args.spec_id or Path(args.python).resolve().parent.name
    root = args.module_prefixes[0] if args.module_prefixes else None
    spec, findings = component_spec_from_python(args.python, project_id=pid, title=args.title or f"{pid} AST Architecture", root_package=root)
    _report(findings)
    return 1 if spec is None else _emit(spec, args.output)


def _report(findings: list) -> None:
    """Kept for the envelope like any alert, and printed to stderr (stdout carries the YAML)."""
    report(findings, text=False)
    for finding in findings:
        print(finding.line() + (f"\n    fix     : {finding.fix}" if finding.fix else ""), file=sys.stderr)


def _emit(spec: dict, output: str | None) -> int:
    if not output:
        print(yaml.safe_dump(spec, sort_keys=False, allow_unicode=True), end="")
        return 0
    write_component_spec(spec, output)
    print(f"Generated {output} ({len(spec['data']['nodes'])} nodes, {len(spec['data']['edges'])} edges)")
    return 0

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

FILE:tests/notations/test_notations_from_graph_cli.py
"""`sldb notations from-graph`: grafo sldb (node-link JSON o edge index) -> spec component.

Ported from spec2viz `tests/test_graph_import.py` (`test_cli_from_graph_*`), rewritten against
`sldb notations from-graph`: `GRAPH_JSON` is `--snapshot`, `--out` is `--output`, the spec2viz
`diagram validate` step is `load_spec` + `validate_spec`, and `diagram render`/`lint` stay in
spec2viz (renderers are out of scope): the nesting the mermaid output showed is asserted on the spec.
"""
import json
from types import SimpleNamespace

import yaml

from sldb.api.notations import load_spec, validate_spec
from sldb.cli import main
from tests.notations.test_component_spec_graph import EDGES, NODES, PY_GRAPH, _node_link, _validated


def test_cli_from_graph_writes_valid_spec(tmp_path, capsys):
    graph = _node_link(tmp_path / "snap.json")
    out = tmp_path / "graph.yml"
    assert main(["notations", "from-graph", "--snapshot", str(graph), "--model", "AtomDoc", "--output", str(out)]) == 0
    output = capsys.readouterr().out
    assert "Generated" in output and "3 nodes" in output

    spec = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert spec["id"] == "snap" and spec["title"] == "snap graph"
    assert "snap.json" in spec["metadata"]["description"]
    _validated(spec)

    validate_spec(load_spec(out))
    nodes = spec["data"]["nodes"]
    assert nodes["document_AtomDoc_atom_x"]["label"] == "atom-x" and nodes["document_AtomDoc_atom_x"]["contains"] == ["document_AtomDoc_atom_y"]
    assert nodes["document_AtomDoc_atom_y"]["label"] == "atom-y"


def test_cli_from_graph_prints_yaml_to_stdout_with_filters(tmp_path, capsys):
    graph = _node_link(tmp_path / "snap.json")
    rc = main(
        ["notations", "from-graph", "--snapshot", str(graph), "--id", "tags", "--title", "Tags", "--node-type", "document",
         "--node-type", "semantic_tag", "--relation", "tagged_as", "--drop-isolated"],
    )
    assert rc == 0
    spec = yaml.safe_load(capsys.readouterr().out)
    assert spec["id"] == "tags" and spec["title"] == "Tags"
    assert set(spec["data"]["nodes"]) == {"document_AtomDoc_atom_x", "semantic_tag_system_spec2viz"}
    assert spec["data"]["edges"][0]["relation"] == "tagged_as"
    _validated(spec)


def test_cli_from_graph_requires_exactly_one_source(tmp_path):
    graph = _node_link(tmp_path / "snap.json")
    assert main(["notations", "from-graph"]) == 2
    assert main(["notations", "from-graph", "--snapshot", str(graph), "--store", str(tmp_path)]) == 2


def test_cli_from_graph_store_goes_through_loader(monkeypatch, tmp_path, capsys):
    import sldb.cli.commands.notations_from_graph as cmd

    fake_index = SimpleNamespace(
        nodes={nid: SimpleNamespace(node_type=ntype) for nid, ntype in NODES.items()},
        edges=[SimpleNamespace(source=s, target=t, relation=r) for s, t, r in EDGES],
    )
    monkeypatch.setattr(cmd, "load_edge_index", lambda store: fake_index)
    assert main(["notations", "from-graph", "--store", str(tmp_path), "--relation", "has_document"]) == 0
    spec = yaml.safe_load(capsys.readouterr().out)
    assert spec["id"] == "sldb-graph"
    assert f"store {tmp_path}" in spec["metadata"]["description"]
    assert spec["data"]["edges"] == [{"from": "model_AtomDoc", "to": "document_AtomDoc_atom_x", "relation": "has_document"}]


def test_cli_from_graph_module_prefix(tmp_path, capsys):
    path = tmp_path / "python-source.graph.json"
    path.write_text(json.dumps(PY_GRAPH), encoding="utf-8")
    out = tmp_path / "selfdoc.yml"
    rc = main(["notations", "from-graph", "--snapshot", str(path), "--node-type", "python_module", "--node-type", "python_symbol", "--module-prefix", "sldb.selfdoc", "--output", str(out)])
    assert rc == 0
    assert "4 nodes, 1 edges" in capsys.readouterr().out
    validate_spec(load_spec(out))


def test_cli_from_graph_reports_dangling_edges_on_stderr(tmp_path, capsys):
    graph = tmp_path / "ghost.json"
    nodes = [{"id": nid, "type": ntype} for nid, ntype in NODES.items()]
    links = [{"source": "sldb://document/AtomDoc:atom-x", "target": "sldb://document/Ghost:g", "relation": "uses"}]
    graph.write_text(json.dumps({"nodes": nodes, "links": links}), encoding="utf-8")
    assert main(["notations", "from-graph", "--snapshot", str(graph)]) == 0
    captured = capsys.readouterr()
    assert "alert: [component-spec/dangling-edge] sldb://document/AtomDoc:atom-x -> sldb://document/Ghost:g" in captured.err
    _validated(yaml.safe_load(captured.out))

FILE:instruccion
Cold-bundle de la tarea task-sldb-notations-from-graph-elige-el-campo-del-label-el-campo-que-da-kind-o-estilo-y-un-campo-de-agrup: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/notations/test_notations_from_graph_cli.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_graph.py

