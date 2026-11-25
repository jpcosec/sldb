FILE:desk/tasks/task-separar-el-store-en-sldb-store-todo-lo-versionado-store-yaml-y-core-y-sldb-cache-todo-lo-regenerable.md
---
sldb:
  by: agent
  at: '2026-11-16T13:12:50Z'
  authority: generated
  via: create_document
id: task-separar-el-store-en-sldb-store-todo-lo-versionado-store-yaml-y-core-y-sldb-cache-todo-lo-regenerable
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
- task-merge-de-dos-sldb-sin-detenerse-merge-driver-de-sldb-un-comando-que-regenera-los-índices-derivados-y
pills: []
files:
- src/sldb/store/layout.py
- src/sldb/store/migration.py
- src/sldb/api/stores/init_store.py
- src/sldb/api/stores/store_declaration.py
- tests/store/test_legacy_layout_migration.py
- docs/architecture/derived-store-boundary.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
---

# Separar el store en .sldb_store (todo lo versionado: store.yaml y core/) y .sldb_cache (todo lo regenerable), con stores migrate-layout, lectura del layout viejo y migración del ecosistema

## Rationale

_Explain why this task exists or the business driver behind it._

Tarea nueva de JP (2026-11-16, vía supervisor): que sea obvio qué se trackea y qué se regenera. Hoy el store versionado vive en .sldb/ (store.yaml, core/ y README.md; .sldb/.config/ está en .gitignore pero nadie lo usa) y lo regenerable ya vive aparte en .sldb_cache/ (composed, edges, rules, sections, semantic, locks; ignorado). El nombre .sldb no dice que es lo versionado, y el literal ".sldb" está repartido en unos 35 archivos de src/sldb (por ejemplo src/sldb/api/stores/init_store.py:33, src/sldb/api/stores/store_declaration.py:86-108, src/sldb/api/edges/project_graph/project_store.py:32). El atom atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past ya fija la regla; esta tarea la hace visible en el nombre.

## Goal

_Describe the concrete result this task must produce._

Un store nuevo se crea en .sldb_store/ (store.yaml, core/ y README.md, todo versionado) con su cache en .sldb_cache/ (todo regenerable e ignorado); `sldb stores migrate-layout` lleva un store del layout viejo al nuevo con git mv; todo comando de sldb sigue leyendo un store en .sldb/ (layout viejo) con una alerta que dice que se migre; el store de sldb está migrado; y cada repo del ecosistema que tiene store recibió por inbox el aviso con el comando.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) una constante única STORE_DIR_NAME = ".sldb_store" y LEGACY_STORE_DIR_NAME = ".sldb" en src/sldb/store/layout.py (junto a CACHE_DIR_NAME), y reemplazar cada literal ".sldb" de src/sldb que nombra el directorio del store por esas constantes (inventario con `grep -rn '"\.sldb"' src/sldb`; un literal que forma parte de ".sldb_cache" no cuenta). (2) Descubrimiento y resolución (store_discovery, store_declaration, init_store, links de store.yaml): preferir .sldb_store; si solo existe .sldb, usarlo y emitir la alerta store/legacy-layout "this store uses the old .sldb/ layout: run `sldb stores migrate-layout`"; un enlace de store.yaml que nombra ../repo/.sldb resuelve también a ../repo/.sldb_store si el primero no existe. (3) `sldb stores migrate-layout` (el subcomando ya existe en src/sldb/cli/parsers/stores.py; hoy mueve el runtime a .sldb_cache): además, con el repo en git, `git mv .sldb .sldb_store` (sin git, rename), quita .sldb/.config si está vacío, actualiza .gitignore (.sldb_store/ versionado, .sldb_cache/ ignorado, sin la línea .sldb/.config/) y las rutas .sldb/ de .gitattributes si existen; es idempotente y no toca un store que ya está migrado. (4) `sldb stores init` crea .sldb_store/. (5) Migrar el store de este repo con el comando y commitear el resultado en el mismo commit; correr stores check y stores build --check (bajo flock /dev/shm/sldb1-tests.lock). (6) Documentación: .sldb_store/README.md y docs/architecture/derived-store-boundary.md explican qué va en cada carpeta; CHANGELOG.md marca el cambio de layout. (7) Avisos: deskops message send a deskops, IR, pron, graph_ui, spec2viz, scion y mepu (los que tengan store) con el comando de migración y la fecha desde la cual el layout viejo solo se lee con alerta; para un repo que no esté en el registro, el aviso va como línea "Aviso a <repo>" en result-summary.md. (8) Tests en tests/store/test_legacy_layout_migration.py: un store viejo en .sldb se lee con la alerta; migrate-layout lo deja en .sldb_store con el mismo contenido versionado (mismo store_hash) y es idempotente; init crea .sldb_store; un enlace a ../otro/.sldb resuelve a .sldb_store migrado. No entra: migrar los stores de otros repos (cada coordinador lo hace con el comando al recibir el aviso); quitar la lectura del layout viejo (otra tarea, cuando todos migren); cambiar el formato de los archivos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/layout.py, src/sldb/store/migration.py, el comando de migrate-layout (grep "migrate-layout" src/sldb/cli), src/sldb/api/stores/init_store.py, src/sldb/api/stores/store_discovery.py y store_declaration.py. 2) Inventario de literales y reemplazo por constantes. 3) Descubrimiento con fallback y alerta. 4) migrate-layout. 5) Tests. 6) Migrar este repo, stores check y build --check. 7) Docs y CHANGELOG. 8) Avisos. Ejecutar después de la tarea del merge driver (depends_on), porque esa escribe rutas .sldb/ en .gitattributes que esta migra.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_legacy_layout_migration.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_stores_build.py
- flock /dev/shm/sldb1-tests.lock env TMPDIR=/dev/shm uv run --frozen --extra code --extra dev sldb stores build --check --store .sldb_store

## Done When

_Name the observable condition that makes the task complete._

Los cuatro comandos de Validation pasan; `grep -rn '"\.sldb"' src/sldb` solo deja la constante LEGACY_STORE_DIR_NAME; el repo de sldb tiene .sldb_store/ versionado y .sldb_cache/ ignorado, sin .sldb/; los avisos a los consumidores están enviados o anotados; README y doc explican el layout; CHANGELOG y commit.

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

FILE:desk/atoms/atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past.md
---
id: atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
title: The store is .sldb (versioned) plus .sldb_cache (regenerable, ignored); git
  history is the past
five_wh_one_plus: what
tags:
- system:sldb
- topic:store-layout
- topic:journal
---

# The store is .sldb (versioned) plus .sldb_cache (regenerable, ignored); git history is the past

## Answer

An sldb store is two sibling directories at the repo root: .sldb/ holds store.yaml and core/ (store_index, models, documents) and is versioned in git; .sldb_cache/ holds everything derived (edges, sections, semantic, graphs, caches, locks), is git-ignored and is rebuilt by stores build. There is no journal: the past of a store is asked of git history (sldb docs history). stores check fails with stores/core_ignored when core/ or store.yaml are ignored and alerts with stores/cache_not_ignored when the cache line is missing; stores migrate-layout moves an old .sldb/runtime/ into .sldb_cache/. Owner decision of 2026-10-29.

FILE:src/sldb/store/layout.py
"""`.sldb/` (`store.yaml`, `core/`: versioned whole, git holds its past) and its sibling `.sldb_cache/`
(the derived shards: regenerable, ignored; `.sldb/runtime/` until 2026-11-04). docs/architecture/derived-store-boundary.md."""

from __future__ import annotations

from pathlib import Path

CACHE_DIR_NAME = ".sldb_cache"


def project_root(store_path: Path) -> Path:
    return store_path.resolve().parent


def core_dir(store_path: Path) -> Path:
    return store_path / "core"


def cache_dir(store_path: Path) -> Path:
    """`.sldb_cache/` beside the store directory, whatever that one is named (`kb/.sldb_custom` -> `kb/.sldb_cache`)."""
    return store_path.parent / CACHE_DIR_NAME


def runtime_dir(store_path: Path) -> Path:  # the cache, under the name every derived-index writer uses
    return cache_dir(store_path)


def config_dir(store_path: Path) -> Path:
    return store_path / ".config"


def store_index_path(store_path: Path) -> Path:
    return core_dir(store_path) / "store_index.yaml"


def legacy_store_index_path(store_path: Path) -> Path:
    return store_path / "store_index.yaml"


def semantic_index_path(store_path: Path) -> Path:
    return runtime_dir(store_path) / "semantic_index.yaml"


def legacy_semantic_index_path(store_path: Path) -> Path:
    return store_path / "semantic_index.yaml"


def semantic_dag_path(store_path: Path) -> Path:
    return runtime_dir(store_path) / "semantic_dag.yaml"


def legacy_semantic_dag_path(store_path: Path) -> Path:
    return store_path / "semantic_dag.yaml"


def lock_path(store_path: Path) -> Path:
    return runtime_dir(store_path) / "locks" / "store.lock"


def _index_relpath(store_path: Path, *parts: str) -> str:
    """A store index's path relative to the project root, from the store's real directory name:
    a store named `.sldb_custom` records `.sldb_custom/core/...`, not a phantom `.sldb/core/...`."""
    root = project_root(store_path).resolve()
    return str((store_path.resolve() / Path(*parts)).relative_to(root))


def models_index_relpath(store_path: Path, model_name: str) -> str:
    return _index_relpath(store_path, "core", "models", f"{model_name}.yaml")


def documents_index_relpath(store_path: Path, model_name: str) -> str:
    return _index_relpath(store_path, "core", "documents", f"{model_name}.yaml")


def sections_index_relpath(store_path: Path, model_name: str) -> str:
    """A key, not a file: the shards live in `.sldb_cache/`, but the models index still records
    this legacy-shaped path and `SectionsIndexIO` reads the store and model name out of it."""
    return _index_relpath(store_path, "runtime", "sections", f"{model_name}.yaml")


def semantic_shards_dir(store_path: Path, model_name: str) -> Path:
    """One document's semantic contribution per file (PLAN 15 capa 5): a write touches only its own shard."""
    return runtime_dir(store_path) / "semantic" / model_name


def semantic_shard_path(store_path: Path, model_name: str, doc_name: str) -> Path:
    return semantic_shards_dir(store_path, model_name) / f"{doc_name}.yaml"


def sections_shards_dir(store_path: Path, model_name: str) -> Path:
    """One document's sections per file (PLAN 15 capa 5), keyed by the model name `sections_index_relpath` names."""
    return runtime_dir(store_path) / "sections" / model_name


def sections_shard_path(store_path: Path, model_name: str, doc_name: str) -> Path:
    return sections_shards_dir(store_path, model_name) / f"{doc_name}.yaml"


def edges_store_shard_path(store_path: Path) -> Path:
    """The store's own contribution to the edge index (store node, semantic DAG edges)."""
    return runtime_dir(store_path) / "edges.yaml"


def edges_shards_root(store_path: Path) -> Path:
    return runtime_dir(store_path) / "edges"


def edges_model_shard_path(store_path: Path, model_name: str) -> Path:
    """One model's contribution (model node, fields, extends), next to its documents' dir."""
    return edges_shards_root(store_path) / f"{model_name}.yaml"


def edges_shards_dir(store_path: Path, model_name: str) -> Path:
    """One document's edges per file, the same per-document pattern as sections."""
    return edges_shards_root(store_path) / model_name


def edges_shard_path(store_path: Path, model_name: str, doc_name: str) -> Path:
    return edges_shards_dir(store_path, model_name) / f"{doc_name}.yaml"


def model_name_of_sections_path(path: Path) -> str:
    """The model name a (legacy-shaped, still used as a key) per-model sections path names."""
    return path.stem


def documents_shards_dir(store_path: Path, model_name: str) -> Path:
    """One document's index entry per file (PLAN 15 capa 7): the Merkle tree's own leaf level."""
    return core_dir(store_path) / "documents" / model_name


def documents_shard_path(store_path: Path, model_name: str, doc_name: str) -> Path:
    return documents_shards_dir(store_path, model_name) / f"{doc_name}.yaml"


def model_name_of_documents_path(path: Path) -> str:
    """The model name a (legacy-shaped, still used as a key) per-model documents path names."""
    return path.stem


def store_exists(store_path: Path) -> bool:
    return (
        store_index_path(store_path).exists()
        or legacy_store_index_path(store_path).exists()
    )

FILE:src/sldb/store/migration.py
from __future__ import annotations

from pathlib import Path

from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_sections_index,
    load_semantic_dag,
    load_semantic_index,
    load_store_index,
    save_documents_index,
    save_models_index,
    save_sections_index,
    save_semantic_dag,
    save_semantic_index,
    save_store_index,
)
from sldb.store.migration_legacy_layout import relocate_legacy_layout
from sldb.store.layout import (
    documents_index_relpath,
    models_index_relpath,
    sections_index_relpath,
    semantic_index_path,
    store_index_path,
)


def _migrate_model(m_entry, store_path: Path, p_root) -> bool:
    m_idx = load_models_index(p_root / m_entry.models_index)
    rels = (models_index_relpath(store_path, m_entry.name), documents_index_relpath(store_path, m_entry.name), sections_index_relpath(store_path, m_entry.name))
    changed = m_idx.documents_index != rels[1] or m_entry.models_index != rels[0]
    _migrate_model_indexes(m_idx, p_root, rels)
    save_models_index(p_root / rels[0], m_idx)
    m_entry.models_index = rels[0]
    return changed


def _migrate_model_indexes(m_idx, p_root, rels: tuple[str, str, str]) -> None:
    n_m_rel, n_d_rel, n_s_rel = rels
    documents = load_documents_index(p_root / m_idx.documents_index)
    save_documents_index(p_root / n_d_rel, documents)
    if m_idx.sections_index:
        save_sections_index(p_root / n_s_rel, load_sections_index(p_root / m_idx.sections_index))
    m_idx.documents_index, m_idx.sections_index = n_d_rel, n_s_rel if m_idx.sections_index else ""
    m_idx.documents_count = len(documents.documents)


def _model_canonical(m_entry, store_path: Path, p_root: Path) -> bool:
    """PLAN 15 capa 5/7: a model's sections and documents are canonical once their old single
    per-model files are gone (sharded into `<store>/{runtime/sections,core/documents}/<model>/`,
    or a section-less model that never had one)."""
    if m_entry.models_index != models_index_relpath(store_path, m_entry.name) or not (p_root / m_entry.models_index).exists():
        return False
    m_idx = load_models_index(p_root / m_entry.models_index)
    if m_idx.documents_index != documents_index_relpath(store_path, m_entry.name) or (p_root / m_idx.documents_index).exists():
        return False
    if m_idx.sections_index and m_idx.sections_index != sections_index_relpath(store_path, m_entry.name):
        return False
    return not m_idx.sections_index or not (p_root / m_idx.sections_index).exists()


def _already_canonical(store_index, store_path: Path, p_root: Path) -> bool:
    """True when every model index already sits at its canonical path, points at canonical
    document and section indexes (capa 5: sections already sharded, the old file gone), and
    the old store-wide semantic index file is gone too (capa 5: sharded): nothing to migrate."""
    if semantic_index_path(store_path).exists():
        return False
    return all(_model_canonical(m_entry, store_path, p_root) for m_entry in store_index.models)


def migrate_store_layout(store_path: Path, project_root: Path) -> bool:
    changed = relocate_legacy_layout(store_path, project_root)
    store_index = load_store_index(store_path)
    if store_index_path(store_path).exists() and _already_canonical(store_index, store_path, project_root):
        return changed   # the common case: an up-to-date store is not rewritten on every context
    changed = _migrate_models(store_index, store_path, project_root) or changed
    _migrate_derived_indexes(store_path)
    if changed: save_store_index(store_path, store_index)
    return changed


def _migrate_models(store_index, store_path: Path, project_root: Path) -> bool:
    """Every model's indexes to their canonical sharded paths; True when any of them moved."""
    changed = not store_index_path(store_path).exists()
    for m_entry in store_index.models:
        if _migrate_model(m_entry, store_path, project_root): changed = True
    return changed


def _migrate_derived_indexes(store_path: Path) -> None:
    """Rewrite the semantic index and DAG from their old single files into their shards."""
    save_semantic_dag(store_path, load_semantic_dag(store_path))
    save_semantic_index(store_path, load_semantic_index(store_path))

FILE:src/sldb/api/stores/init_store.py
"""Create a new, empty store in a project directory."""

from __future__ import annotations

import shutil
from pathlib import Path

from sldb.api.stores.gitignore_lines import ensure_cache_ignored
from sldb.api.stores.store_location import StoreLocation
from sldb.api.stores.store_skeleton import register_in_global_catalog, write_empty_store
from sldb.core.exceptions import SLDBStoreError
from sldb.store.layout import store_exists


def init_store(path: str | Path = ".", force: bool = False) -> StoreLocation:
    """Create `<path>/.sldb`, ignore `<path>/.sldb_cache/` and register the store in the global catalog.

    The root `.gitignore` gets the line `.sldb_cache/` unless a line already says it; nothing
    else in that file is touched. `.sldb/` itself is versioned whole.

    Args:
        path: The project root that will hold the `.sldb` directory.
        force: Delete an existing store there and create it again, empty.

    Returns:
        The new store's `.sldb` directory and project root.

    Raises:
        SLDBStoreError: When a store already exists at `path` and `force` is False, or the
            store cannot be written there (`StoreInitError`; nothing is left behind).
    """
    root = Path(path).resolve()
    store_path = root / ".sldb"
    if store_exists(store_path):
        _replace_existing(store_path, force)
    _write_or_undo(store_path)
    ensure_cache_ignored(root / ".gitignore")
    register_in_global_catalog(store_path)
    return StoreLocation(store_path=store_path, project_root=root)


def _replace_existing(store_path: Path, force: bool) -> None:
    """Delete an existing store when forced; refuse otherwise."""
    if not force:
        raise SLDBStoreError(f"Store already exists at {store_path}. Use --force to reinitialize.")
    shutil.rmtree(store_path)


class StoreInitError(SLDBStoreError):
    """The store could not be written; `precondition` when the place itself refused it
    (permissions, a file in the way), not a failure half-way through."""

    def __init__(self, message: str, precondition: bool):
        super().__init__(message)
        self.precondition = precondition


def _write_or_undo(store_path: Path) -> None:
    """Write the empty store, or remove what was written and say why: a failed init used to
    leave a partial `.sldb/` and a bare `Unexpected: [Errno 13]` (deskops, inbox 20260614-000000)."""
    existed = store_path.exists()
    try:
        write_empty_store(store_path)
    except OSError as exc:
        if not existed:
            shutil.rmtree(store_path, ignore_errors=True)
        precondition = isinstance(exc, (PermissionError, FileExistsError, NotADirectoryError))
        raise StoreInitError(f"Cannot create the store at {store_path}: {exc.strerror or exc}. Check that {store_path.parent} exists and is writable.", precondition) from exc

FILE:src/sldb/api/stores/store_declaration.py
"""`.sldb/store.yaml`: what a store declares, the part of it that is source and lives in git.

Everything else in `.sldb/core/` (the store index, the model and document indexes) is derived
from this file, the tracked Markdown and the models' Python classes, and `sldb stores build`
regenerates it (docs/architecture/derived-store-boundary.md). `.sldb/` is versioned whole so
that git holds the tree's past; what is only a cache lives in `.sldb_cache/`, ignored.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any

import yaml
from pydantic import AfterValidator, BaseModel, Field, SerializerFunctionWrapHandler, field_validator, model_serializer

from sldb.api.stores.seed import Seed
from sldb.api.stores.tag_namespace import TagNamespace, unique_namespaces

DECLARATION_FILE = "store.yaml"
SCAFFOLD_KEYS = ("folders", "seeds")
OPTIONAL_KEYS = (*SCAFFOLD_KEYS, "project_graph", "tag_models", "tag_namespaces")


class StoreDeclaration(BaseModel):
    """Models registered, links to other stores, predicates, and which file is tracked how."""

    version: int = Field(default=1, description="Declaration format version.")
    links: list[dict[str, str]] = Field(default_factory=list, description="`{name, path}` of each linked store; paths relative to the project.")
    models: list[dict[str, Any]] = Field(default_factory=list, description="`{name, model_ref}` plus `path` (a local model's source) or `origin` (the link alias it is inherited from), and `canonical` when true.")
    predicates: dict[str, dict[str, str]] = Field(default_factory=dict, description="Predicate name -> `{axis, description}`.")
    generate: list[dict[str, Any]] = Field(default_factory=list, description="Generators run before tracking, e.g. `{command: selfdoc python-sync, args: [...]}`.")
    derived: list[str] = Field(default_factory=list, description="Project paths (directory prefixes) the generators write: derived, so not versioned and left out of a rebuild check's copy. `.sldb/core/` and `.sldb_cache/` always are.")
    include: list[dict[str, Any]] = Field(default_factory=list, description="`{model, glob}` (each match tracked under its file stem) or `{model, paths: [path | {path, name}]}`.")
    graph_backend: str = Field(default="networkx", description="Graph analysis backend; only `networkx` is admitted in this phase (docs/architecture/graph-backend.md).")
    policy: dict[str, dict[str, str]] = Field(default_factory=dict, description="Model name (or `*`) -> finding code -> `ignore | allow | alert | error | reindex | hook: <command>` (docs/architecture/provenance.md §5).")
    folders: list[str] = Field(default_factory=list, description="Directories `stores scaffold` creates, relative to the project root (docs/architecture/store-declaration.md).")
    seeds: list[Seed] = Field(default_factory=list, description="Files `stores scaffold` writes from a declared source: `{path, mode, text | file | document, track}`.")
    project_graph: dict[str, Any] | None = Field(default=None, description="The project's graph configuration as data (`sldb.api.ProjectGraphConfig.from_mapping`; docs/architecture/project-graph.md), read by `sldb.api.project_graph`.")
    tag_models: list[str] = Field(default_factory=list, description="Models whose documents (and their descendants' by `base_models`) the `tag_namespaces` family checks; empty means every document (docs/architecture/tags.md).")
    tag_namespaces: Annotated[list[TagNamespace], AfterValidator(unique_namespaces)] = Field(default_factory=list, description="The tag namespaces the store declares (`{name, hierarchical, folder_axis, anchored_by}`, names unique); a store that declares any checks every namespaced tag it writes (docs/architecture/tags.md).")

    @field_validator("project_graph")
    @classmethod
    def _project_graph_loads(cls, value: dict[str, Any] | None) -> dict[str, Any] | None:
        """An unknown key or a value that is not data is refused naming its path (`project_graph.surfaces[0].x`)."""
        from sldb.api.edges.project_graph.project_graph_config_mapping import config_from_mapping

        if value is not None:
            config_from_mapping(value, "project_graph")
        return value

    @model_serializer(mode="wrap")
    def _without_empty_optional_keys(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        """A declaration without folders, seeds, project_graph, tag_models or tag_namespaces dumps as before they existed; a seed dumps only the keys it was written with (a namespace does the same on its own)."""
        dumped = handler(self)
        for key in OPTIONAL_KEYS:
            if not dumped.get(key):
                dumped.pop(key, None)
        if dumped.get("seeds"):
            dumped["seeds"] = [{k: v for k, v in seed.items() if v is not None} for seed in dumped["seeds"]]
        return dumped


def declaration_path(store_path: Path) -> Path:
    """Where a store's declaration lives."""
    return Path(store_path) / DECLARATION_FILE


def load_declaration(store_path: Path) -> StoreDeclaration:
    """The store's declaration; a missing file is an error, not an empty store."""
    path = declaration_path(store_path)
    if not path.is_file():
        raise FileNotFoundError(f"{path} does not exist: run `sldb stores declare --write` first")
    definition = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if definition.get("graph_backend", "networkx") != "networkx":  # a backend this phase cannot run
        raise ValueError(f'graph_backend {definition["graph_backend"]} no admitido; admitidos: ["networkx"]')
    return StoreDeclaration.model_validate(definition)


def declared_graph_backend(store_path: str | Path | None = None) -> str:
    """The store's `graph_backend`, or `networkx` when it has no declaration or no key."""
    if store_path is None:
        return "networkx"
    path = Path(store_path)
    path = path / ".sldb" if path.name != ".sldb" and (path / ".sldb").is_dir() else path
    if not declaration_path(path).is_file():
        return "networkx"
    return load_declaration(path).graph_backend


def save_declaration(store_path: Path, declaration: StoreDeclaration) -> Path:
    """Write the declaration in a stable, reviewable order."""
    path = declaration_path(store_path)
    path.write_text(yaml.safe_dump(declaration.model_dump(), sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    return path


def declared_store(store_arg: str | None) -> tuple[Path, Path]:
    """`(store, project root)` of the store a build targets: `--store` (a `.sldb` directory or its project)
    or the nearest ancestor holding `.sldb/store.yaml` (a store only declared has no index for the usual discovery)."""
    if store_arg:
        store = Path(store_arg).resolve()
        store = store if store.name == ".sldb" else store / ".sldb"
        return store, store.parent
    for folder in (Path.cwd().resolve(), *Path.cwd().resolve().parents):
        if declaration_path(folder / ".sldb").is_file():
            return folder / ".sldb", folder
    raise FileNotFoundError(f"No .sldb/{DECLARATION_FILE} here or above {Path.cwd()}")

FILE:tests/store/test_legacy_layout_migration.py
"""A store from before `.sldb/core` existed keeps every index at the store root.

`open_store` migrates a store it finds (`migrate_store_layout`), but that migration started by
loading `core/store_index.yaml`, so on a root-level store it raised `FileNotFoundError: No
store_index.yaml` before migrating anything and `open_store` crashed. Any command against such
a store was unusable, and the files stayed untouched.

The legacy layout is written into its own directory: hand-editing a store the process already
read would leave every process-wide cache (documents, runtime, io) pointing at a layout that no
longer exists on disk, which is a test artefact and not what a fresh process sees.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.open_store import open_store
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_semantic_index,
    load_store_index,
)
from sldb.store.io.utils import yaml_dump
from sldb.store.layout import (
    legacy_semantic_index_path,
    legacy_store_index_path,
    store_index_path,
)
from sldb.store.migration import migrate_store_layout

from tests.store.test_documents_shards import _store


def _legacy_store(tmp_path: Path) -> tuple[Path, Path, dict]:
    """A root-level legacy store built beside the normal one, plus its semantic documents."""
    (tmp_path / "built").mkdir()
    built, built_root = _store(tmp_path / "built", 3)
    before = load_semantic_index(built).documents
    store, root = tmp_path / "legacy" / ".sldb", tmp_path / "legacy"
    (store / "models").mkdir(parents=True)
    (store / "documents").mkdir()
    index = load_store_index(built)
    for model in index.models:
        _write_model_files(store, built_root, model)
        model.models_index = f".sldb/models/{model.name}.yaml"
    (legacy_semantic_index_path(store)).write_text(yaml_dump(load_semantic_index(built).model_dump()), encoding="utf-8")
    (legacy_store_index_path(store)).write_text(yaml_dump(index.model_dump()), encoding="utf-8")
    assert not store_index_path(store).exists()
    return store, root, before


def _write_model_files(store: Path, built_root: Path, model) -> None:
    """One model's legacy index files, pointing at the paths a root-level store would name."""
    model_index = load_models_index(built_root / model.models_index)
    documents = load_documents_index(built_root / model_index.documents_index)
    (store / "documents" / f"{model.name}.yaml").write_text(
        yaml_dump({"documents": [doc.model_dump() for doc in documents.documents]}), encoding="utf-8"
    )
    data = model_index.model_dump()
    data["documents_index"] = f".sldb/documents/{model.name}.yaml"
    data.pop("sections_index", None)
    (store / "models" / f"{model.name}.yaml").write_text(yaml_dump(data), encoding="utf-8")


def test_open_store_migrates_a_root_level_legacy_layout(tmp_path: Path):
    store, root, before = _legacy_store(tmp_path)

    open_store(str(store))

    assert store_index_path(store).exists() and not legacy_store_index_path(store).exists()
    assert not (store / "models").exists() and not (store / "documents").exists()
    assert not legacy_semantic_index_path(store).exists()
    assert load_semantic_index(store).documents == before


def test_migrating_a_root_level_legacy_layout_is_idempotent(tmp_path: Path):
    store, root, _ = _legacy_store(tmp_path)

    assert migrate_store_layout(store, root) is True
    assert migrate_store_layout(store, root) is False


def test_migrated_documents_are_readable_from_the_canonical_index(tmp_path: Path):
    store, root, _ = _legacy_store(tmp_path)
    before = [doc.name for doc in _documents(root, store)]

    open_store(str(store))

    assert sorted(doc.name for doc in _documents(root, store)) == sorted(before)


def _documents(root: Path, store: Path) -> list:
    return [
        doc
        for model in load_store_index(store).models
        for doc in load_documents_index(root / load_models_index(root / model.models_index).documents_index).documents
    ]

FILE:docs/architecture/derived-store-boundary.md
# Qué del store se versiona y qué se regenera

Estado (2026-11-04): implementado. Decisión del dueño (2026-10-29): el pasado del árbol del
store se pregunta a git, y eso exige que los shards de `core/` estén versionados. El store se
parte físicamente en dos directorios hermanos: `.sldb/` (operacional, versionado entero) y
`.sldb_cache/` (regenerable, ignorado), y sldb declara la caché en el `.gitignore` de la raíz
para que la separación sea correcta por construcción. Reemplaza la frontera del 2026-10-19,
que ignoraba `.sldb/core/` y `.sldb/runtime/` con declaración; la medición de entonces (2.816
archivos bajo `.sldb/`, 66dac43b tocando 5.045 por un hash) sigue siendo el costo asumido:
un cambio de un campo derivado reescribe muchos shards, y ese ruido es lo que git versiona.

## 1. El layout

```
<raíz>/                      el directorio padre de .sldb/ (precisión 11 de la tarea)
  .gitignore                 contiene la línea `.sldb_cache/`
  .sldb/                     versionado entero
    store.yaml               la declaración (modelos, links, predicados, generadores, include, policy)
    core/
      store_index.yaml       raíz del árbol Merkle (store_hash) y registro de modelos
      models/<Model>.yaml    nodo de cada modelo (model_hash, contract_hash, roster)
      documents/<Model>/<doc>.yaml   una hoja por documento (source_hash, content_hash)
  .sldb_cache/               ignorado; `sldb stores build` lo regenera
    edges.yaml, edges/       índice de aristas (el shard del store, uno por modelo, uno por documento)
    sections/<Model>/<doc>.yaml      secciones de cada documento
    semantic/<Model>/<doc>.yaml      contribución semántica de cada documento
    semantic_dag.yaml        padres y equivalencias declaradas de los tags
    graphs/                  grafos generados (`selfdoc python-sync` escribe python-source.graph.json)
    corpus/                  índice del corpus del servidor
    locks/store.lock         lock del store
```

`src/sldb/store/layout.py` resuelve las rutas: `cache_dir(store)` es `store.parent / ".sldb_cache"`,
hermano del directorio del store cualquiera sea su nombre (un store abierto como
`kb/.sldb_custom` cachea en `kb/.sldb_cache`); `runtime_dir` es el mismo directorio bajo el
nombre que siempre usaron los escritores de índices derivados. Nada de `.sldb/` se escribe en
una lectura: las cachés de proceso (payloads extraídos, modelos construidos) viven en
`$XDG_CACHE_HOME/sldb` (`sldb.store.user_cache`), fuera del repo.

La clave `sections_index` del índice de cada modelo conserva su forma vieja
(`.sldb/runtime/sections/<Model>.yaml`): es una clave, no un archivo, y `SectionsIndexIO` lee
de ella el store y el nombre del modelo. Cambiarla reescribiría `core/` de todos los stores sin
ganar nada.

## 2. Qué es fuente, qué es índice y qué es caché

**Fuente:** los Markdown escritos o editados por personas y agentes (`docs/`, `desk/`, `ledger/`,
`sldb/relation_types/`, `knowledge/commands/`, `knowledge/surfaces/`), el código y los modelos
Python, y `.sldb/store.yaml`, que declara qué modelos se registran, qué stores se enlazan, qué
predicados existen, qué generadores corren, qué archivo se trackea con qué modelo y la policy
de hallazgos.

**Índice versionado (`.sldb/core/`):** se deriva de la fuente y `stores build` lo reconstruye,
pero se versiona porque su historia es la historia del árbol: `git log` sobre un shard de
`documents/` dice quién movió el hash de ese documento y cuándo, y `sldb docs history <doc>`
lo lee de ahí. Es lo que antes pedía el journal ([journal-authority.md](journal-authority.md)).

**Caché (`.sldb_cache/`):** se deriva del índice y de la fuente, no guarda nada que no se pueda
recomputar y no se versiona. Borrarla entera y correr `sldb stores build` (o `edges rebuild`)
la trae de vuelta; `tests/store/test_runtime_wiped.py` lo prueba.

`knowledge/symbols/` sigue siendo derivado (lo escribe `selfdoc python-sync`) y la declaración
lo lista en `derived`, con `.sldb/core/` y `.sldb_cache/` que siempre lo son para la copia de
`stores build --check`.

## 3. Los comandos

- `sldb stores init` crea `.sldb/` y agrega la línea `.sldb_cache/` al `.gitignore` de la raíz si
  ninguna línea ya la nombra (idempotente); nunca borra ni reordena otra línea.
- `sldb stores build` lee `.sldb/store.yaml`, registra modelos y links, corre los generadores,
  trackea cada `include` y reconstruye los índices y la caché. Es idempotente. En un clon limpio
  (que trae `.sldb/` entero), `stores build` seguido de `stores check` da PASS. `stores build
  --check` construye una copia de los fuentes sin `.sldb/core/`, `.sldb_cache/` ni lo declarado
  en `derived`, y falla si esa copia no pasa `stores check`, si algo trackeado no está declarado
  o si trackea distinto que el store local.
- `sldb stores check` emite dos hallazgos sobre el `.gitignore` (`src/sldb/core/finding.py`),
  evaluados con `git check-ignore --no-index` desde la raíz del repo:
  - error `stores/core_ignored` (exit 1) si git ignora `.sldb/core/` o `.sldb/store.yaml`: el
    pasado del store se lee de git, así que nada de `.sldb/` puede estar ignorado;
  - alert `stores/cache_not_ignored` (exit 0) si `.sldb_cache/` no está ignorada.
  Fuera de un work tree de git no hay policy y no hay hallazgos.
- `sldb stores migrate-layout [--store PATH] [--force]` lleva un store del layout anterior al
  actual: mueve el contenido de `.sldb/runtime/` a `.sldb_cache/` (edges, sections, semantic,
  graphs, locks), se niega si `.sldb_cache/` existe con contenido salvo `--force` (que la borra
  primero), borra `.sldb/runtime/journal/` sin archivarlo, elimina `.sldb/runtime/` y reescribe
  el `.gitignore` de la raíz: quita solo las líneas cuyo patrón, sin barras inicial ni final,
  es `.sldb/core` o `.sldb/runtime`, pone `.sldb_cache/` donde estaba la primera de ellas (al
  final si no había ninguna) y conserva las demás líneas y comentarios tal cual. Sin
  `.sldb/runtime/` no hay nada que mover y solo corrige el `.gitignore`, así que correrlo dos
  veces es inocuo. Sin `--store` descubre el store como los demás comandos `stores`.

## 4. Adoptar el layout en un repo que versionaba lo viejo

1. `sldb stores migrate-layout --store .sldb`.
2. `git add .sldb .gitignore` (entra `core/` entero, salen las líneas viejas del `.gitignore`).
3. `sldb stores check`: sin `stores/core_ignored` ni `stores/cache_not_ignored`.
4. En el CI, `stores build --check` sigue siendo la verificación; la copia que construye ya no
   necesita que `.sldb/core/` esté ignorado, porque lo excluye por sí misma.

Los cinco stores de SLDB_1 (deskops, sldb, spec2viz, pron, scion) se migran con este
procedimiento al integrar la tarea; pron construye su `.sldb/` con `make world` y sigue sin
versionarlo por decisión del coordinador (ver sección 5).

## 5. Lo que sigue bloqueando un clon limpio

- 15 modelos (48 documentos del desk) se heredan del store de deskops por el link
  `../deskops/.sldb`. Un clon solo de sldb no los resuelve: el CI necesita deskops al lado,
  con la misma ruta relativa.
- 3 modelos de pron (AnchorDoc, ProjectionDoc, MoveDoc, con documentos en `ledger/`) viven en
  el store de pron y sldb los hereda por `../pron/.sldb` (106ed3c0). pron no versiona su
  `.sldb/` y lo construye con su propio CLI (`make world`); el CI de sldb corre `make world`
  en el checkout hermano de pron antes de reconstruir el de sldb. Un generador de `store.yaml`
  solo corre subcomandos de sldb, a propósito.

FILE:instruccion
Cold-bundle de la tarea task-separar-el-store-en-sldb-store-todo-lo-versionado-store-yaml-y-core-y-sldb-cache-todo-lo-regenerable: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_legacy_layout_migration.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_stores_build.py
- flock /dev/shm/sldb1-tests.lock env TMPDIR=/dev/shm uv run --frozen --extra code --extra dev sldb stores build --check --store .sldb_store

