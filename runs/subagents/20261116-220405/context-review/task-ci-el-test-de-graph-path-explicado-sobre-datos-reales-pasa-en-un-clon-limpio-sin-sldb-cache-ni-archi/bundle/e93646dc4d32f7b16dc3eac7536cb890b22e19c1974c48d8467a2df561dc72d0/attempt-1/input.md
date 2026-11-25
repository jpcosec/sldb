FILE:desk/tasks/task-ci-el-test-de-graph-path-explicado-sobre-datos-reales-pasa-en-un-clon-limpio-sin-sldb-cache-ni-archi.md
---
sldb:
  by: agent
  at: '2026-11-16T21:47:52Z'
  authority: generated
  via: create_document
id: task-ci-el-test-de-graph-path-explicado-sobre-datos-reales-pasa-en-un-clon-limpio-sin-sldb-cache-ni-archi
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- tests/api/test_api_graph_analysis.py
depends_on: []
pills: []
files:
- tests/api/test_api_graph_analysis.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
---

# CI: el test de graph-path explicado sobre datos reales pasa en un clon limpio, sin .sldb_cache ni archivos generados

## Rationale

_Explain why this task exists or the business driver behind it._

El CI de GitHub sobre c5cb52f0 falla en 3.12 y 3.13 con TypeError 'NoneType' object is not subscriptable en tests/api/test_api_graph_analysis.py::test_explain_over_the_repo_own_index_names_origin_and_relation_doc (B3). El coordinador lo reprodujo en un clon limpio: graph_path sobre el .sldb del repo devuelve None porque las aristas entre rituales viven en el índice derivado .sldb_cache (ignorado por git); tras sldb stores update el camino aparece. El test dependía de la caché del checkout local.

## Goal

_Describe the concrete result this task must produce._

El test que cubre graph_path(..., explain=True) con aristas de origin relation_doc y schema reales pasa en un clon recién hecho, sin .sldb_cache, sin knowledge/symbols generados y con XDG_CACHE_HOME vacío, y sigue pasando en el checkout de trabajo.

## Scope

_State what is in scope and what is out of scope._

Entra: reescribir ese test para que no lea el .sldb del repo. Arma en tmp_path un store propio con documentos y al menos una arista de origin relation_doc y otra de origin schema (puede reutilizar el AnalysisWorld del mismo archivo si ya las tiene, o un fixture mínimo), y comprueba la misma propiedad: cada arista de los steps trae origin y relation_doc o field. Si hace falta construir el índice, el test lo construye en tmp_path con la API pública. No entra: cambiar código de src/ (path_steps, analyze); si el test revela que el código depende de la caché para algo que no debería, se anota en result-summary.md y lo decide el coordinador.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer el test y AnalysisWorld en tests/api/test_api_graph_analysis.py. 2) Reescribir el test como se describe. 3) Reproducir en un clon limpio: git clone del checkout a /dev/shm, y allí, con XDG_CACHE_HOME apuntando a un directorio vacío, correr el archivo de test con uv run --frozen --extra code --extra dev pytest -q -p no:cacheprovider. 4) Validation en el checkout de trabajo. 5) Borrar el clon de /dev/shm.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; result-summary.md tiene la salida del archivo de test corrido en un clon limpio sin .sldb_cache y con XDG_CACHE_HOME vacío, con rc 0; commit.

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

FILE:desk/atoms/atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia.md
---
sldb:
  by: agent
  at: '2026-11-16T20:56:59Z'
  authority: generated
  via: create_document
id: atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
title: graph_path con explain devuelve por cada tramo las aristas que lo justifican
  y su procedencia
five_wh_one_plus: what
tags:
- system:sldb
- topic:graph
provenance: tarea B3 (IR10), ejecutor deskops-e-884be32362ef, tester deskops-t-b4736317f0b4
  PASA
---

# graph_path con explain devuelve por cada tramo las aristas que lo justifican y su procedencia

## Answer

graph_path(..., explain=True) devuelve {path, steps}; graph_paths una lista de esos. Cada step es un par consecutivo {source, target, edges}; cada arista lleva relation, direction (forward|backward) y provenance {origin, relation_doc si origin es relation_doc, field si es schema, from_store si viene de un store enlazado}, sin claves vacías ni evidence. Orden: relation_doc > schema > structural > alias, desconocidos al final, empates por relation y luego relation_doc o field. Una arista espejo aparece como su directa en backward. Sin explain la forma no cambia. Expuesto como sldb graph path --explain y GET /graph/path?explain=1.

FILE:tests/api/test_api_graph_analysis.py
"""The whole-graph analyses over a real store, and the `sldb graph` commands that print them."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from sldb import api
from sldb.api.graph import graph_central, graph_components, graph_cycles, graph_isolated, graph_order, graph_path, graph_paths, graph_similar
from sldb.cli import main as cli_main
from sldb.cli.serve.graph_routes import path_payload
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.graph.analysis.path_steps import explain_path
from sldb.store.models import EdgeNodeRecord, EdgeRecord

MODULE = "sldb_analysis_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Spec(StructuredNLDoc):
    __semantics__ = {"type": ["doc", "spec"]}
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


class AnalysisWorld:
    """A store whose specs form a chain: 3 -> 2 -> 1, plus one spec nobody relates to."""

    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        api.add_model(self.store, f"{MODULE}:Spec", self.py)
        api.init_relations(self.store, self.py)
        self._populate()

    def _populate(self) -> None:
        for name in ("s1", "s2", "s3", "lonely"):
            self.create("Spec", name, {"title": name.upper()})
        self.relation_type("refines")
        self.relation("s2-s1", "Spec:s2", "Spec:s1")
        self.relation("s3-s2", "Spec:s3", "Spec:s2")

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def relation_type(self, name: str) -> None:
        self.create("RelationTypeDoc", f"rt-{name}", {"title": name, "name": name, "direction": "directed", "cardinality": "many_to_many", "axis": "WHY", "source_types": ["Spec"], "target_types": ["Spec"], "condition": "", "description": f"{name}."})

    def relation(self, name: str, src: str, tgt: str) -> None:
        self.create("RelationDoc", name, {"title": name, "source_id": src, "target_id": tgt, "relation_type": "refines", "condition": "", "notes": ""})


@pytest.fixture
def world(tmp_path: Path) -> AnalysisWorld:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    return AnalysisWorld(tmp_path)


S1, S2, S3 = (f"sldb://document/Spec:{n}" for n in ("s1", "s2", "s3"))


def test_the_authored_relation_is_what_gets_walked_not_the_structural_spine(world: AnalysisWorld):
    """Without this, every pair of specs is two hops apart through their model node."""
    assert graph_path(world.store, S3, S1) == [S3, S2, S1]
    assert graph_path(world.store, S3, S1, relations=["has_document"]) == [S3, "sldb://model/Spec", S1]


def test_order_and_cycles_over_what_the_store_asserts(world: AnalysisWorld):
    assert graph_cycles(world.store) == []
    order = graph_order(world.store)
    assert order.index(S1) < order.index(S2) < order.index(S3)


def test_a_document_nobody_relates_to_shows_up_as_isolated(world: AnalysisWorld):
    """Restricted to one class: unrestricted, every field and section node is isolated too."""
    assert graph_isolated(world.store, node_types=["Spec"]) == ["sldb://document/Spec:lonely"]
    assert graph_components(world.store, node_types=["Spec"])[0] == [S1, S2, S3]
    assert "sldb://field/RelationDoc.condition" in graph_isolated(world.store)


def test_centrality_and_resemblance_over_a_real_store(world: AnalysisWorld):
    assert graph_central(world.store, kind="in_degree", limit=1) == [(S1, 1.0)]
    resembling = dict(graph_similar(world.store, S1, node_types=["Spec"]))
    assert resembling == {S2: 3, S3: 3, "sldb://document/Spec:lonely": 3}


def test_the_cli_prints_each_analysis(world: AnalysisWorld, capsys):
    for argv in (["graph", "cycles"], ["graph", "order"], ["graph", "components"], ["graph", "central", "--kind", "degree"], ["graph", "similar", S1], ["graph", "path", S3, S1]):
        assert cli_main([*argv, "--store", str(world.store)]) == 0
    assert S1 in capsys.readouterr().out


def test_the_cli_says_so_when_there_is_no_path_and_exits_nonzero(world: AnalysisWorld, capsys):
    assert cli_main(["graph", "path", S1, "sldb://document/Spec:lonely", "--store", str(world.store)]) == 1
    assert "No path" in capsys.readouterr().out


def _refines(relation_doc: str, direction: str = "forward") -> dict:
    return {"relation": "refines", "direction": direction, "provenance": {"origin": "relation_doc", "relation_doc": relation_doc}}


def test_explain_says_which_edge_joins_each_hop_and_where_it_came_from(world: AnalysisWorld):
    """The authored chain read both ways: forward from s3, backward from s1; the plain form stays a list."""
    assert graph_path(world.store, S3, S1, explain=True) == {"path": [S3, S2, S1], "steps": [{"source": S3, "target": S2, "edges": [_refines("s3-s2")]}, {"source": S2, "target": S1, "edges": [_refines("s2-s1")]}]}
    backward = graph_path(world.store, S1, S3, explain=True)
    assert [e["direction"] for step in backward["steps"] for e in step["edges"]] == ["backward", "backward"]
    assert graph_paths(world.store, S3, S1, explain=True) == [graph_path(world.store, S3, S1, explain=True)]
    assert graph_paths(world.store, S3, S1) == [[S3, S2, S1]]


def test_a_hop_lists_every_edge_by_precedence_and_a_mirror_is_its_authored_edge_read_backward():
    a, b = "sldb://document/M:a", "sldb://document/M:b"
    meta = {"origin": "relation_doc", "relation_doc": "r1", "evidence": "x"}
    edges = [EdgeRecord(source=b, target=a, relation="peer", metadata=meta), EdgeRecord(source=a, target=b, relation="peer", metadata={**meta, "reverse": True}),
             EdgeRecord(source=a, target=b, relation="mentions", metadata={"origin": "alias"}), EdgeRecord(source=a, target=b, relation="owns", metadata={"origin": "schema", "field": "owner", "from_store": "other"}),
             EdgeRecord(source=a, target=b, relation="odd", metadata={"origin": "custom"})]
    index = EdgeIndex(nodes={n: EdgeNodeRecord(id=n, node_type="M") for n in (a, b)}, edges=edges)
    peer = {"relation": "peer", "direction": "backward", "provenance": {"origin": "relation_doc", "relation_doc": "r1"}}
    owns = {"relation": "owns", "direction": "forward", "provenance": {"origin": "schema", "field": "owner", "from_store": "other"}}
    rest = [{"relation": "mentions", "direction": "forward", "provenance": {"origin": "alias"}}, {"relation": "odd", "direction": "forward", "provenance": {"origin": "custom"}}]
    assert explain_path(index, [a, b], "*")["steps"][0]["edges"] == [peer, owns, *rest]
    assert explain_path(index, [a, b], ["peer"], directed=True)["steps"][0]["edges"] == [peer]


def test_the_cli_and_serve_expose_the_explained_path(world: AnalysisWorld, capsys):
    assert cli_main(["graph", "path", S3, S1, "--explain", "--store", str(world.store)]) == 0
    assert json.loads(capsys.readouterr().out)["steps"][0]["edges"] == [_refines("s3-s2")]
    plain, explained = (path_payload(SimpleNamespace(path=f"/graph/path?source={S3}&target={S1}{q}"), world.store) for q in ("", "&explain=1"))
    assert plain == ({"path": [S3, S2, S1]}, 200)
    assert explained[0]["path"] == [S3, S2, S1] and explained[0]["steps"][1]["edges"] == [_refines("s2-s1")]


def test_explain_over_the_repo_own_index_names_origin_and_relation_doc():
    """The desk's rituals: execution activates testing, testing hands to closeout."""
    store = str(Path(__file__).resolve().parents[2] / ".sldb")
    found = graph_path(store, "sldb://document/RitualDoc:ritual-execution", "sldb://document/RitualDoc:ritual-closeout", explain=True, include_linked=False)
    edges = [e for step in found["steps"] for e in step["edges"]]
    assert edges and all(e["provenance"]["origin"] and ("relation_doc" in e["provenance"] or "field" in e["provenance"]) for e in edges)

FILE:instruccion
Cold-bundle de la tarea task-ci-el-test-de-graph-path-explicado-sobre-datos-reales-pasa-en-un-clon-limpio-sin-sldb-cache-ni-archi: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

