FILE:desk/tasks/task-seguridad-live-stale-no-abre-archivos-fuera-de-la-raíz-no-sigue-symlinks-y-no-lee-archivos-sin-cambi.md
---
id: task-seguridad-live-stale-no-abre-archivos-fuera-de-la-raíz-no-sigue-symlinks-y-no-lee-archivos-sin-cambi
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/store/edge_index/live_stale.py
- src/sldb/store/edge_index/compose.py
- src/sldb/store/models/doc_edges.py
- src/sldb/store/
- tests/store/
- tests/api/
- docs/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-seguridad-live-stale-lee-todos-los-archivos-trackeados-y-sigue-symlinks-fuera-de-la-ra-z-al-cargar-el-ndice-de-aristas.md
---

# SEGURIDAD: live_stale no abre archivos fuera de la raíz, no sigue symlinks y no lee archivos sin cambios al cargar el índice de aristas

## Rationale

_Explain why this task exists or the business driver behind it._

Prioridad del overlord. Desde GO04 d7eefdeb, cargar el índice de aristas abre y hashea cada archivo trackeado y sigue symlinks fuera de la raíz, antes de que un consumidor (graph_ui) pueda aplicar sus guardas. Bloquea la integración de graph_ui (test_mindmap_workspace_reader).

## Goal

_Describe the concrete result this task must produce._

Cargar el índice de aristas no abre archivos fuera de la raíz, no sigue symlinks y no lee el contenido de archivos que no cambiaron desde el build; tests de regresión con symlink saliente y archivo protegido.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/store/edge_index/live_stale.py, src/sldb/store/edge_index/compose.py, src/sldb/store/models/doc_edges.py, src/sldb/store/, tests/store/, tests/api/, docs/, CHANGELOG.md. Fuera: rebuild y stale global (a2 de la nota).

## Implementation Path

_Outline the expected implementation route or affected surface._

SEGURIDAD (decisión del overlord, 2026-11-11, prioridad sobre CC34). Nota de origen: inbox 9c9dac6b (de la integración de graph_ui).

REPRODUCCIÓN (coordinador; log runs/subagents/20261111-repro-livestale/repro.log; sldb 9c9dac6b): un desk de prueba con dos documentos trackeados. Uno se reemplaza por un symlink a /dev/shm/outside-secret/secreto-externo.md, fuera de la raíz. Un proceso nuevo llama sldb.api.edges.edge_reading.load_edge_index(.sldb, include_linked=False) con un audit hook de 'open'. Abre 26 .md, entre ellos el archivo fuera de la raíz a través del symlink.

CAUSA: src/sldb/store/edge_index/live_stale.py (GO04 d7eefdeb). live_stale corre en cada lectura del índice (compose._with_live_stale) y, por cada documento trackeado, _file_hash hace path.stat() y path.read_text(), siguiendo symlinks, sin comprobar que la ruta resuelta quede dentro de la raíz. El caché _FILE_HASHES es por proceso, así que un proceso nuevo lee todo.

ARREGLO (s1-s6):
s1 (raíz): antes de abrir, path.resolve() tiene que quedar dentro de la raíz del proyecto (is_relative_to(root.resolve())). Un symlink que escapa, o una ruta que resuelve afuera, no se abre ni se hashea: el documento cuenta como stale (moved) sin leerlo y queda nombrado en un hallazgo (store/path-outside-root o similar), sin error.
s2 (sin seguir symlinks dentro de la raíz): un documento trackeado que es symlink, aunque apunte dentro de la raíz, no se lee por esta vía. Se compara con lstat y se marca como stale con su motivo. La decisión es revisable: si rompe un caso real de sldb, el worker lo escribe y propone.
s3 (no leer de más): al cargar el índice no se lee el contenido de un archivo cuyo lstat (mtime_ns, size) coincide con el registrado al construir el shard. Para eso el shard (DocEdges) guarda el stat del build, y si cambia el contrato de DocEdges se migra como en GO04. Solo se hashea un archivo cuyo stat cambió. Con esto, un proceso nuevo sobre un store recién construido no abre ningún .md del proyecto. Es lo que pide graph_ui: sus archivos protegidos no se abren mientras no cambien.
s4 (tests de regresión, tests/store/): con el audit hook de 'open' de la reproducción:
- un symlink trackeado que apunta fuera de la raíz no se abre y su documento sale stale con motivo;
- un archivo dentro de la raíz sin cambios desde el build no se abre en un proceso nuevo (el caso del archivo protegido de graph_ui);
- un archivo editado sí se lee y sale stale como hoy;
- test_stale_shard_hashes.py sigue verde.
s5 (servidores): el informe dice si sldb serve usa load_edge_index y en qué interfaz escucha por defecto (cli/parsers/serve.py: --host 127.0.0.1). Si hay un camino que escuche fuera de localhost por defecto, se avisa enseguida al coordinador.
s6 (fuera): el hueco a2 de la misma nota (rebuild no resuelve la stale de una edición externa; stale es global) no entra aquí; queda en la nota del inbox de sldb.

VALIDACIÓN: los 7 pasos del workflow de sldb (.github/workflows): bash tools/check.sh --fast; pytest, un proceso por archivo; python -m build; make world en pron; sldb stores build en deskops; sldb stores build --check; sldb stores build && sldb selfdoc check. Los corre el coordinador en clon limpio. El worker corre los archivos de test que toca y los de tests/store/ y tests/api/ que usan el índice de aristas.

## Validation

_List the checks required before this task can close._

- Test con audit hook: symlink saliente no abierto y stale con motivo
- Test: archivo sin cambios no abierto en un proceso nuevo; editado sí y stale
- test_stale_shard_hashes y tests de edge_index verdes
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

s1-s5 hechos con causa raíz escrita y tests verdes; CHANGELOG y docs.

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

FILE:src/sldb/store/edge_index/live_stale.py
"""What the shards cannot say about themselves (inbox 20261102-065705): a Markdown file edited
from outside sldb (its text no longer hashes to the `source_hash` its shard was built from) and
a model whose contract moved (its fields or declared reference names: a new `__references__`
entry moves no document hash). Checked on every read of the index, not kept with the composed
index: neither moves a shard file. A file's hash is kept while its mtime and size hold."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.store import documents_hash
from sldb.store.edge_index.node_ids import doc_node_id
from sldb.store.hashing import hash_text
from sldb.store.io import load_store_index
from sldb.store.io.shard_compose import compose_edges_documents
from sldb.store.layout import project_root
from sldb.store.models import DocEdges

#: (model_ref, the store's project root) -> the model class, or None when it cannot be loaded.
ModelTypeOf = Callable[[str, Path], Any]
_FILE_HASHES: dict[str, tuple[tuple[int, int], str]] = {}


def live_stale(store_path: Path, model_type_of: ModelTypeOf | None) -> list[str]:
    """Export ids whose file or model contract moved since their shard was built. Without
    `model_type_of` the contract is not compared (the store alone cannot import a class)."""
    root = project_root(store_path)
    stale: list[str] = []
    for m in load_store_index(store_path).models:
        signature = _signature(m.model_ref, root, model_type_of)
        paths = {e.name: root / e.path for e in documents_hash.entries_of(store_path, m.name)}
        shards = [s for s in compose_edges_documents(store_path, m.name) if s.doc_name in paths]
        stale += [f"{m.name}:{s.doc_name}" for s in shards if _moved(s, doc_node_id(f"{m.name}:{s.doc_name}"), paths[s.doc_name], signature)]
    return stale


def _signature(model_ref: str, root: Path, model_type_of: ModelTypeOf | None) -> str | None:
    from sldb.store.model_contract import contract_signature

    return None if model_type_of is None else contract_signature(model_type_of(model_ref, root))


def _moved(shard: DocEdges, node_id: str, path: Path, signature: str | None) -> bool:
    current = _file_hash(path)
    if current is not None and current != shard.source_hash:
        return True
    node = next((n for n in shard.nodes if n.id == node_id), None)
    return signature is not None and node is not None and node.contract_signature != signature


def _file_hash(path: Path) -> str | None:
    """The file's source_hash as sldb computes it on track; None when it cannot be read."""
    try:
        st = path.stat()
        key = (st.st_mtime_ns, st.st_size)
        hit = _FILE_HASHES.get(str(path))
        if hit is None or hit[0] != key:
            hit = _FILE_HASHES[str(path)] = (key, hash_text(path.read_text(encoding="utf-8")))
        return hit[1]
    except (OSError, UnicodeDecodeError):
        return None

FILE:src/sldb/store/edge_index/compose.py
"""Shards -> one EdgeIndex: every store's contributions merged (the same node id is one node,
the first contributor's), the cross-document rules applied. Composed once per state of the
shards: the result is kept while no shard file, and no store index, has moved."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.store.edge_index.composition_targets import resolve_composition_edges
from sldb.store.edge_index.doc_anchor_states import with_anchor_states
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.federation import federated_stores, qualify
from sldb.store.edge_index.live_stale import ModelTypeOf, live_stale
from sldb.store.edge_index.resolve import resolve_edges_reporting
from sldb.store.edge_index.shard_reading import read_store_contributions
from sldb.store.edge_index.shard_signature import shards_signature
from sldb.store.io import load_store_index
from sldb.store.models import EdgeContribution, EdgeNodeRecord, EdgeRecord, ModelEdges

_COMPOSED: dict[tuple, tuple[tuple, EdgeIndex]] = {}


def compose_edge_index(store_path: Path, include_linked: bool = True, exclude_tags: Iterable[str] = (), model_type_of: ModelTypeOf | None = None) -> EdgeIndex:
    """The store's edge index, read from its shards (never rebuilt here).

    Args:
        store_path: The store's `.sldb` directory.
        include_linked: Also read the linked stores' indexes, their ids qualified by name.
        exclude_tags: Documents carrying one of these tags are left out (their nodes, their
            sections, their edges); the index itself holds everything.
        model_type_of: Loads a model class (`(model_ref, project_root) -> class | None`), so
            `stale` also names documents built under another contract of their model, and a
            document node's payload gains `<field>__anchor_state` for each of its model's
            `__doc_anchors__` (GO07: on copies, never in a shard; without it, none).

    Returns:
        The composed index; shared between callers, so treat it as read-only. Its `stale` is
        checked on every call against the files on disk (`live_stale`), not only the shards.
    """
    stores = federated_stores(Path(store_path), include_linked)
    key = (str(stores[0][0]), include_linked, frozenset(exclude_tags), model_type_of)
    signature = tuple(shards_signature(path) for path, _ in stores)
    hit = _COMPOSED.get(key)
    if hit is None or hit[0] != signature:
        hit = _COMPOSED[key] = (signature, _compose(stores, frozenset(exclude_tags), model_type_of))
    return _with_live_stale(hit[1], stores, model_type_of)


def _with_live_stale(index: EdgeIndex, stores: list[tuple[Path, str | None]], model_type_of: ModelTypeOf | None) -> EdgeIndex:
    moved, known = [f"{name}:{e}" if name else e for path, name in stores for e in live_stale(path, model_type_of)], set(index.stale)
    extra = [e for e in dict.fromkeys(moved) if e not in known]
    return index.model_copy(update={"stale": index.stale + extra}) if extra else index


def invalidate_composed_edge_indexes() -> None:
    """Forget every composed index (tests, or a caller that rewrote shards by hand)."""
    _COMPOSED.clear()


def _compose(stores: list[tuple[Path, str | None]], exclude_tags: frozenset[str], model_type_of: ModelTypeOf | None) -> EdgeIndex:
    nodes: dict[str, EdgeNodeRecord] = {}
    edges: list[EdgeRecord] = []
    stale: list[str] = []
    fields: dict[str, list[str]] = {}
    for path, name in stores:
        stale += _merge_store(path, name, exclude_tags, nodes, edges, fields)
    nodes = with_anchor_states(nodes, [path for path, _ in stores], model_type_of, fields)
    kept, problems, unresolved = resolve_edges_reporting(nodes, resolve_composition_edges(nodes, edges))
    return EdgeIndex(nodes=nodes, edges=kept, problems=problems, stale=stale, unresolved_references=unresolved, payload_fields=fields)


def _merge_store(path: Path, name: str | None, exclude_tags: frozenset[str], nodes: dict, edges: list[EdgeRecord], fields: dict[str, list[str]]) -> list[str]:
    parts, stale_here = read_store_contributions(path, exclude_tags)
    for part in parts:
        if isinstance(part, ModelEdges):
            fields.setdefault(part.model_name, part.projected_fields)
    _merge((qualify(p, name) for p in parts), nodes, edges, _source(path))
    return [f"{name}:{export_id}" if name else export_id for export_id in stale_here]


def _merge(parts: Iterable[EdgeContribution], nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord], source: dict) -> None:
    for part in parts:
        edges += part.edges
        for node in part.nodes:
            nodes.setdefault(node.id, _stamped(node, source))


def _stamped(node: EdgeNodeRecord, source: dict) -> EdgeNodeRecord:
    return node.model_copy(update={"facets": {**node.facets, "source": source}})


def _source(store_path: Path) -> dict:
    return {"generated_from": "sldb.store.edge_index", "store_path": str(store_path), "hash_a": load_store_index(store_path).hash_a}

FILE:src/sldb/store/models/doc_edges.py
"""One document's shard of the edge index: `.sldb_cache/edges/<Model>/<doc>.yaml`."""

from __future__ import annotations

from pydantic import Field

from sldb.store.models.edge_contribution import EdgeContribution


class DocEdges(EdgeContribution):
    """What a document contributes, stamped with the `source_hash` it was built from: a document
    whose `source_hash` still matches is never processed again."""

    doc_name: str = Field(description="Name of the contributing document within its model.")
    model_name: str = Field(default="", description="Model the contributing document is tracked under.")
    source_hash: str = Field(default="", description="The document's source_hash this shard was built from; the shard's cache key.")
    content_hash: str = Field(default="", description="The document's content_hash (its fields under the model's contract): it moves when the model changes even if the text, and so source_hash, does not.")
    contract_hash: str = Field(default="", description="The model's contract_hash this shard was built under: a contract change (a new `__reference_models__`) moves the edges without moving the document's hashes.")
    semantic_tags: list[str] = Field(default_factory=list, description="The contributing document's tags, so a reader can leave out whole shards by tag (exclude_tags).")

FILE:instruccion
Cold-bundle de la tarea task-seguridad-live-stale-no-abre-archivos-fuera-de-la-raíz-no-sigue-symlinks-y-no-lee-archivos-sin-cambi: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Test con audit hook: symlink saliente no abierto y stale con motivo
- Test: archivo sin cambios no abierto en un proceso nuevo; editado sí y stale
- test_stale_shard_hashes y tests de edge_index verdes
- 7 pasos del workflow de sldb en clon limpio

