FILE:desk/tasks/task-rule-graph-en-frío-y-deskops-show-task-perfilar-de-nuevo-y-bajar-el-costo-de-leer-el-índice-local-me.md
---
sldb:
  by: agent
  at: '2026-11-16T05:44:41Z'
  authority: generated
  via: save_document_payload
id: task-rule-graph-en-frío-y-deskops-show-task-perfilar-de-nuevo-y-bajar-el-costo-de-leer-el-índice-local-me
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on:
- task-v0-benchmark-fijo-de-velocidad-sldb-bench-y-punto-de-partida
pills: []
files:
- src/sldb/store/io/shards.py
- src/sldb/store/io/__init__.py
- src/sldb/api/rules/rule_graph.py
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-lectura-del-ndice-local-yaml-puro-y-deepcopy-dejan-rule-graph-en-1-2-s-en-fr-o.md
---

# rule_graph en frío y deskops show task: perfilar de nuevo y bajar el costo de leer el índice local (meta rule_graph < 1 s en frío)

## Rationale

_Explain why this task exists or the business driver behind it._

Residual de la tarea de rule_graph (wt/rule-graph-local bdb9b0ff, informe runs/subagents/rg-worker-report.md): rule_graph en frío tarda 1,2-2,1 s en stores grandes y deskops show task 2,8 s en el desk de deskops. La nota atribuía el costo a yaml en Python puro y a deepcopy, pero eso ya no es así: src/sldb/store/io/utils.py:26 usa CSafeLoader desde 50c2fd88 y las copias usan _fast_copy (model_validate(model_dump()), src/sldb/store/io/__init__.py:34-49). Hay que perfilar de nuevo antes de arreglar. Ojo: el .venv del repo no tiene yaml (ModuleNotFoundError); usar el intérprete de la instalación de sldb (el de `head -1 $(which sldb)`). Origen: drawer desk/drawer/tasks/task-lectura-del-ndice-local-yaml-puro-y-deepcopy-dejan-rule-graph-en-1-2-s-en-fr-o.md.

## Goal

_Describe the concrete result this task must produce._

Con un perfil nuevo (cProfile) guardado en el informe, rule_graph en frío sobre una copia en /dev/shm del store del desk de deskops tarda menos de 1 s y deskops show task menos de 2 s, con los mismos findings que antes del cambio.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) medir con sldb bench (verbo de V0, b60f0891) o con python -m cProfile sobre una copia en /dev/shm de /mnt/ssd/proyectos/SLDB_1/deskops/.sldb y desk/, en frío (sin .sldb_cache) y en caliente, y guardar las 20 funciones más caras en el informe; (2) arreglar el costo dominante si está en src/sldb/store/io/ (lectura de shards, src/sldb/store/io/shards.py:68-95, o copias de modelos) o en src/sldb/api/rules/rule_graph.py; (3) medir después y comparar findings (rules check antes y después, mismo resultado). Si el costo dominante está fuera de esos módulos, la tarea se detiene con el perfil y una propuesta en el informe. CHANGELOG.md si hubo cambio. No entra: la federación de stores enlazados (resuelta en 84eb7f75), run_view (otra tarea), cambiar el formato de los shards.

Precisiones (preflight-1): el perfil se toma con python -m cProfile -s cumtime y las 20 primeras filas van a result-summary.md; sldb bench sirve para los tiempos, no reemplaza al perfil. La tarea de muestra para deskops show task es la primera de `deskops list tasks --root <copia>` en orden alfabético. Findings: `sldb rules check --store <copia>/.sldb --format json` antes y después, comparados como conjuntos de (code, subject, level) con jq o python.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Copiar el desk de deskops a /dev/shm. 2) Perfilar rule_graph y deskops show task en frío y caliente. 3) Arreglar el punto caro. 4) Medir y comparar findings. 5) Tests de Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_rules_evaluation.py
- TMPDIR=/dev/shm pytest -q tests/api/test_transaction_rules_dirty.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rules_linked_reach.py

## Done When

_Name the observable condition that makes the task complete._

El informe tiene el perfil antes y después y los tiempos medidos bajo las metas (o el motivo por el que se detuvo); los tres comandos pasan; findings de rules check iguales antes y después; commit.

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

FILE:src/sldb/store/io/shards.py
"""Per-document shards for the semantic, sections and edges indexes (PLAN 15 capa 5): one small file
per document under `.sldb_cache/{semantic,sections,edges}/<Model>/<doc>.yaml` instead of one file
for the whole store, so a write touches only its own shard. Each shard carries the `source_hash`
it was built from. Loads are cached by (path, mtime, size) — its own small cache, not
`sldb.store.io`'s (that module imports this one; importing back would be circular)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, TypeVar

from sldb.store.io.utils import StoreIOUtils, yaml_dump, yaml_load
from sldb.store.models import DocSections, DocumentEntry, EdgeContribution, SemanticDocumentRecord

T = TypeVar("T")
E = TypeVar("E", bound=EdgeContribution)

_SHARDS: dict[str, tuple[tuple, Any]] = {}


def _signature(path: Path) -> tuple:
    try:
        st = path.stat()
        return (st.st_mtime_ns, st.st_size)
    except OSError:
        return (0, 0)


# Loads hand out a copy, never the cached instance: a caller that edits what it loaded and saves
# it back would otherwise be compared against its own edit, and `_save_shard` would skip the write.
def _cached_shard(path: Path, loader: Callable[[], T]) -> T:
    return _cached_instance(path, loader).model_copy(deep=True)


def _cached_instance(path: Path, loader: Callable[[], T]) -> T:
    key = str(path)
    sig = _signature(path)
    hit = _SHARDS.get(key)
    if hit is None or hit[0] != sig:
        hit = (sig, loader())
        _SHARDS[key] = hit
    return hit[1]


def _forget_shard(path: Path) -> None:
    _SHARDS.pop(str(path), None)


def invalidate_shard_cache() -> None:
    _SHARDS.clear()


def _save_shard(path: Path, value: Any, loader: Callable[[], T]) -> None:
    """Write only when the content differs from the shard already there (the same "leave the
    file alone" guarantee the single-file indexes always gave): a rebuild or a re-save of the
    same value costs a read of the cached/on-disk shard, not a write."""
    if path.exists() and _cached_instance(path, loader) == value:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    StoreIOUtils._atomic_write(path, yaml_dump(value.model_dump()))
    _SHARDS[str(path)] = (_signature(path), value.model_copy(deep=True))


def load_semantic_shard(path: Path) -> SemanticDocumentRecord | None:
    if not path.exists():
        _forget_shard(path)
        return None
    return _cached_shard(path, lambda: SemanticDocumentRecord(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def save_semantic_shard(path: Path, record: SemanticDocumentRecord) -> None:
    _save_shard(path, record, lambda: SemanticDocumentRecord(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def load_sections_shard(path: Path) -> DocSections | None:
    if not path.exists():
        _forget_shard(path)
        return None
    return _cached_shard(path, lambda: DocSections(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def save_sections_shard(path: Path, doc_sections: DocSections) -> None:
    _save_shard(path, doc_sections, lambda: DocSections(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def load_edges_shard(path: Path, shard_type: type[E], copy: bool = True) -> E | None:
    """An edges shard (DocEdges, ModelEdges or the store's EdgeContribution); `copy=False`: the cached one, read-only."""
    if not path.exists():
        _forget_shard(path)
        return None
    return (_cached_shard if copy else _cached_instance)(path, lambda: shard_type(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def save_edges_shard(path: Path, shard: EdgeContribution) -> None:
    _save_shard(path, shard, lambda: type(shard)(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def load_document_shard(path: Path) -> DocumentEntry | None:
    if not path.exists():
        _forget_shard(path)
        return None
    return _cached_shard(path, lambda: DocumentEntry(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def save_document_shard(path: Path, entry: DocumentEntry) -> None:
    _save_shard(path, entry, lambda: DocumentEntry(**(yaml_load(path.read_text(encoding="utf-8")) or {})))


def delete_shard(path: Path) -> None:
    path.unlink(missing_ok=True)
    _forget_shard(path)


def list_shard_names(shards_dir: Path) -> list[str]:
    if not shards_dir.is_dir():
        return []
    return sorted(p.stem for p in shards_dir.glob("*.yaml"))


def prune_shards(shards_dir: Path, current_names: set) -> None:
    """Delete every shard whose document is no longer tracked (PLAN 15 capa 5: a document
    untracked or deleted loses its semantic/sections shard right away, not just its entry
    in an aggregate that happens to get rebuilt without it)."""
    for name in list_shard_names(shards_dir):
        if name not in current_names:
            delete_shard(shards_dir / f"{name}.yaml")

FILE:src/sldb/store/io/__init__.py
from pathlib import Path
from sldb.store.io.lock import StoreIOLock
from sldb.store.io.store_index import StoreIndexIO
from sldb.store.io.models_index import ModelsIndexIO
from sldb.store.io.documents_index import DocumentsIndexIO
from sldb.store.io.sections_index import SectionsIndexIO
from sldb.store.io.semantic_dag import SemanticDAGIO
from sldb.store.io.semantic_index import SemanticIndexIO
from sldb.store.models import DocumentsIndex, ModelsIndex, SectionsIndex, SemanticDAG, SemanticIndex, StoreIndex

def store_lock(store_path: Path, wait: bool = False):
    return StoreIOLock(store_path).acquire(wait)

# -- index cache ---------------------------------------------------------------------------
#
# The three yaml indexes are read by every query and every operation, many times per call
# chain. Each parsed index is kept keyed by its file's path, mtime and size, and returned as
# a deep copy so a caller that mutates and saves it never changes the cached object; the save
# changes the file, and the next load sees a new signature.

from sldb.store.layout import semantic_dag_path as _semantic_dag_path, store_index_path as _store_index_path

_INDEXES: dict[str, tuple[tuple, object]] = {}


def _file_signature(path: Path) -> tuple:
    try:
        st = path.stat()
        return (st.st_mtime_ns, st.st_size)
    except OSError:
        return (0, 0)


def _fast_copy(index):
    """An independent copy of a parsed index, cheaper than `model_copy(deep=True)`: pydantic's
    own dump/validate round-trip instead of the generic recursive `copy.deepcopy` it uses
    internally (PLAN 15 M2) — ~4x faster on a realistic SectionsIndex in this codebase's own
    measurements, and every caller through `_cached` already only reads validated data back."""
    return type(index).model_validate(index.model_dump())


def _cached(path: Path, loader):
    key = str(path)
    sig = _file_signature(path)
    hit = _INDEXES.get(key)
    if hit is None or hit[0] != sig:
        hit = (sig, loader())
        _INDEXES[key] = hit
        _SAVED[key] = (sig, _digest(hit[1]))
    return _fast_copy(hit[1])


def invalidate_index_cache() -> None:
    _INDEXES.clear()
    _SAVED.clear()


_SAVED: dict[str, tuple[tuple, str]] = {}   # path -> (file signature, digest of what was last saved there)


def _digest(index) -> str:
    import hashlib
    import json
    return hashlib.sha256(json.dumps(index.model_dump(), sort_keys=True, default=str).encode()).hexdigest()


def _save_if_changed(path: Path, index, saver) -> None:
    """Write only when the content differs from what the file already holds: a rebuild that
    changes nothing leaves the file, its mtime and every cache keyed on it alone."""
    digest = _digest(index)
    prior = _SAVED.get(str(path))
    if prior is not None and prior[1] == digest and prior[0] == _file_signature(path):
        return
    saver()
    _SAVED[str(path)] = (_file_signature(path), digest)
    _INDEXES[str(path)] = (_file_signature(path), _fast_copy(index))


def load_store_index(store_path: Path) -> StoreIndex:
    return _cached(_store_index_path(store_path), lambda: StoreIndexIO.load(store_path))

def save_store_index(store_path: Path, index: StoreIndex) -> None:
    _save_if_changed(_store_index_path(store_path), index, lambda: StoreIndexIO.save(store_path, index))

def load_models_index(path: Path) -> ModelsIndex:
    return _cached(path, lambda: ModelsIndexIO.load(path))

def save_models_index(path: Path, index: ModelsIndex) -> None:
    _save_if_changed(path, index, lambda: ModelsIndexIO.save(path, index))

def load_documents_index(path: Path) -> DocumentsIndex:
    # PLAN 15 capa 7: composed from per-document shards, not one file at `path` (which may not
    # exist at all once sharded) — see load_sections_index for why the (path, mtime/size)
    # cache above cannot be reused here.
    return DocumentsIndexIO.load(path)

def save_documents_index(path: Path, index: DocumentsIndex) -> None:
    DocumentsIndexIO.save(path, index)

def load_sections_index(path: Path) -> SectionsIndex:
    # PLAN 15 capa 5: composed from per-document shards, not one file at `path` (which may not
    # exist at all once sharded) — the (path, mtime/size) cache above would freeze on its first
    # ever call for this path (signature (0, 0), forever, once there is no file there). Shards
    # already cache themselves, per shard, in sldb.store.io.shards.
    return SectionsIndexIO.load(path)

def save_sections_index(path: Path, index: SectionsIndex) -> None:
    SectionsIndexIO.save(path, index)

def load_semantic_dag(store_path: Path) -> SemanticDAG:
    return _cached(_semantic_dag_path(store_path), lambda: SemanticDAGIO.load(store_path))

def save_semantic_dag(store_path: Path, dag: SemanticDAG) -> None:
    _save_if_changed(_semantic_dag_path(store_path), dag, lambda: SemanticDAGIO.save(store_path, dag))

def load_semantic_index(store_path: Path) -> SemanticIndex:
    # PLAN 15 capa 5: composed from per-document shards, not the one (now legacy) file this
    # cache is keyed on — see load_sections_index for why that cache cannot be reused here.
    return SemanticIndexIO.load(store_path)

def save_semantic_index(store_path: Path, index: SemanticIndex) -> None:
    SemanticIndexIO.save(store_path, index)

FILE:src/sldb/api/rules/rule_graph.py
"""The store a rule is evaluated over: its edge index, loaded once into the store's
`GraphBackend`, and which documents are the local store's own. The index holds the linked
stores, except for the rules' own evaluations (`rule_graph(store, None)`), which compose them
only when the rules may read them (`rule_reach`): otherwise the index is the store's own, and a
local document reads exactly as it would in the composed one.

`with_payload(node, payload)` is the same graph where `node` reads `payload` instead of its
projection (GO08: the payload a write is about to persist, or the subject a transition reads);
paths still follow the index's edges."""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import cached_property
from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.graph.analyze import backend_for
from sldb.api.rules.rule_reach import needs_linked
from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.node_ids import bare, kind
from sldb.store.graph.backend.index_view import index_view
from sldb.store.graph.language.predicate_api import node_finding
from sldb.store.graph.language.predicate_view import node as view_node, with_node


@dataclass(frozen=True)
class RuleGraph:
    """`eval` over one store: `holds` is the finding of a predicate on one document."""

    backend: Any
    index: Any
    local: frozenset[str]
    store_path: Path
    override: tuple[str, dict[str, Any]] | None = None
    linked: bool = True

    def holds(self, predicate: str, node: str) -> dict[str, Any]:
        """The eval finding (node, holds, clause, seen) of `predicate` on the document `node`."""
        if self.override is None or node != self.override[0]:
            return self.backend.eval(predicate, node)[0]
        view, item = self.located(node)
        return node_finding(predicate, view, item)

    def located(self, node: str) -> tuple[dict[str, Any], dict[str, Any]]:
        """The graph view and the element of `node` an evaluation reads (the override's payload)."""
        known = self._view["node"](node) or self._unindexed(node)
        if self.override is None or node != self.override[0]:
            return self._view, known
        item = {**known, "payload": self.override[1]}
        return with_node(self._view, item), item

    def _unindexed(self, node: str) -> dict[str, Any]:
        """A document the index does not hold yet: its family from the store's model registry
        (`indexed_model_bases`, no class imported), so `model <= Base` reads as for an indexed one."""
        from sldb.api.stores.resolve_indexed_document import indexed_model_bases

        model = node.rsplit(":", 1)[0].rsplit(":", 1)[-1]
        return view_node(node, model, {}, indexed_model_bases(self.store_path).get(model, []))

    def with_payload(self, node: str, payload: dict[str, Any]) -> "RuleGraph":
        """This graph, with `node` reading `payload` (its model and edges stay the index's)."""
        return replace(self, override=(node, payload))

    @cached_property
    def index_documents(self) -> list[str]:
        """Every document of the index (the linked stores' too when `linked`), by export id."""
        return [bare(n.id) for n in self.index.nodes.values() if kind(n.id) == "document"]

    @cached_property
    def _view(self) -> dict[str, Any]:
        return index_view(self.index)

    def domain(self, predicate: str) -> list[str]:
        """The local documents `predicate` holds on, over its domain (rules-language.md §6)."""
        return [f["node"] for f in self.backend.eval(predicate) if f["holds"] == "true" and f["node"] in self.local]

    def semantics(self, node: str) -> dict[str, Any]:
        """What the index records of a document: its name, model and path."""
        record = self.index.node(node)
        return dict(record.semantics) if record is not None else {}

    def payload(self, node: str) -> dict[str, Any]:
        record = self.index.node(node)
        return dict(record.payload) if record is not None else {}


def rule_graph(store: str | Path | None, linked: bool | None = True) -> RuleGraph:
    """The store's graph with its linked stores, every document's projection loaded. With
    `linked` None (the rules' evaluations) they are composed only when the store's rules may
    read them (`rule_reach.needs_linked`); with False, never."""
    store_path = open_store(store, mode="readonly").store_path
    own = load_edge_index(store_path, False)
    local = _documents(own)
    if linked is None:
        graph = _loaded(own, local, store_path, False)
        linked = needs_linked(graph)
        if not linked:
            return graph
    return _loaded(load_edge_index(store_path, True) if linked else own, local, store_path, linked)


def reading(graph: RuleGraph, node: str) -> RuleGraph:
    """`graph`, or the store's graph with its linked stores when `node` is not a local document
    (a subject behind `alias:`): a rule on it reads what the composed index says."""
    return graph if graph.linked or node in graph.local else rule_graph(graph.store_path, True)


def _loaded(index: Any, local: frozenset[str], store_path: Path, linked: bool) -> RuleGraph:
    backend = backend_for(store_path)
    backend.load(index, {bare(n.id): n.payload for n in index.nodes.values() if kind(n.id) == "document"})
    return RuleGraph(backend, index, local, store_path, linked=linked)


def _documents(index: Any) -> frozenset[str]:
    return frozenset(bare(n.id) for n in index.nodes.values() if kind(n.id) == "document")

FILE:instruccion
Cold-bundle de la tarea task-rule-graph-en-frío-y-deskops-show-task-perfilar-de-nuevo-y-bajar-el-costo-de-leer-el-índice-local-me: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_rules_evaluation.py
- TMPDIR=/dev/shm pytest -q tests/api/test_transaction_rules_dirty.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rules_linked_reach.py

