FILE:desk/tasks/task-sldb-stores-add-guarda-tal-cual-un-enlace-absoluto-con-o-con-variable-de-entorno.md
---
sldb:
  by: agent
  at: '2026-11-16T06:03:57Z'
  authority: generated
  via: save_document_payload
id: task-sldb-stores-add-guarda-tal-cual-un-enlace-absoluto-con-o-con-variable-de-entorno
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-sldb-stores-add-guarda-siempre-el-enlace-relativo-no-resuelve-desde-worktrees-un-nivel-más-hondo.md
depends_on: []
pills: []
files:
- src/sldb/api/stores/link_store.py
- src/sldb/store/query.py
- tests/api/test_api_stores.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
---

# sldb stores add guarda tal cual un enlace absoluto, con ~ o con variable de entorno

## Rationale

_Explain why this task exists or the business driver behind it._

record_store_link (src/sldb/api/stores/link_store.py:71) guarda siempre rel = os.path.relpath(other, root) (línea 89), aunque se le pase una ruta absoluta. Con clones en /srv/repos/<repo> y worktrees en /srv/wt/<repo>/<rama>, un nivel más hondo, el mismo enlace versionado no resuelve en los dos (AntonIA: shared_llm-gateway 479b415 y manifest 9729506 quedaron con '../../../mnt/ssd/proyectos/SLDB_1/deskops-runtime/.sldb'). La lectura ya acepta entradas absolutas (_linked_stores en src/sldb/store/query.py:108-114 vía _resolve_path). Origen: desk/inbox/inbox-note-sldb-stores-add-guarda-siempre-el-enlace-relativo-no-resuelve-desde-worktrees-un-nivel-más-hondo.md.

## Goal

_Describe the concrete result this task must produce._

`sldb stores add <ruta>` guarda la ruta como la escribió el usuario si empieza por /, ~ o $ (absoluta, home o variable de entorno) y relativa a la raíz del proyecto en cualquier otro caso (como hoy); la lectura expande ~ y variables de entorno al resolver el enlace.

## Scope

_State what is in scope and what is out of scope._

Entra: en record_store_link decidir la forma guardada según el texto original (no según la ruta resuelta), lo que exige pasar el texto original desde el comando (src/sldb/cli/commands/ del verbo stores add) hasta la API; en _resolve_path / _linked_stores (src/sldb/store/query.py) aplicar os.path.expandvars y os.path.expanduser antes de resolver; stores remove y stores add --replace siguen funcionando con cualquiera de las tres formas. Tests en tests/api/test_api_stores.py: ruta absoluta guardada absoluta; ~/x guardada como ~/x y resuelta con HOME parcheado; $SLDB_TEST_ROOT/x guardada tal cual y resuelta con la variable puesta; ruta relativa guardada relativa como hoy. tests/api/test_unlink_store.py sigue verde. CHANGELOG.md y la sección de enlaces en docs/ (grep "stores add" docs/). No entra: resolver contra el git common dir (la otra opción de la nota), migrar enlaces ya guardados.

Precisiones (preflight-1): reglas de prefijo sobre el texto tal como lo escribió el usuario: empieza por "/" (absoluta), por "~" (incluido ~user) o por "$" (forma $VAR o ${VAR}) -> se guarda tal cual; cualquier otro texto -> relativo a la raíz como hoy. Un "$" literal en un nombre de carpeta no se soporta (queda como variable). El punto de paso del texto original es el comando de stores add en src/sldb/cli/commands/ (localizarlo con el grep de implementation_path) y la función de API a la que llama; se agrega un parámetro keyword-only raw: str | None = None. La doc a actualizar es docs/architecture/store-declaration.md (sección de enlaces o links).

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/stores/link_store.py (record_store_link y su llamador), el comando stores add en src/sldb/cli/commands/ (grep -rn "record_store_link\|link_store" src/sldb/cli), y src/sldb/store/query.py 100-120. 2) Pasar el texto original. 3) Guardar según prefijo. 4) Expandir al leer. 5) Tests, doc y CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm pytest -q tests/api/test_unlink_store.py
- TMPDIR=/dev/shm pytest -q tests/store/test_stores_build.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan con los cuatro casos nuevos; CHANGELOG y doc; commit; aviso a AntonIA con deskops message send --to AntonIA (si ese repo no está registrado para el envío, el aviso va como línea "Aviso a AntonIA" en el informe de cierre).

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

FILE:desk/atoms/atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre.md
---
id: atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre
title: Una operación de sldb se ancla al store más cercano, no al directorio desde
  donde se corre
five_wh_one_plus: where
tags:
- system:sldb
- topic:federation
- topic:store-context
provenance: src/sldb/store/resolver.py
---

# Una operación de sldb se ancla al store más cercano, no al directorio desde donde se corre

## Answer

sldb resuelve el contexto desde el store más cercano que encierra el directorio actual (sin contar el global ~/.sldb), salvo un --store explícito: así FAQ, explore, alias y federación leen lo mismo desde la raíz que desde un subdirectorio. La federación recorre los stores enlazados en anchura y una vez cada uno (src/sldb/store/edge_index/federation.py:federated_stores), así que dos stores que se enlazan entre sí no hacen ciclo. El catálogo global se mantiene al hacer init y se reconcilia de forma explícita (sldb stores reconcile).

FILE:src/sldb/api/stores/link_store.py
"""Link one store into another so its documents can be read through the linking store."""

from __future__ import annotations

import os
from pathlib import Path

from sldb.api.stores.doc_ref import LINK_NAME, LOCAL
from sldb.api.stores.linked_store import LinkedStore
from sldb.api.stores.open_store import open_store
from sldb.api.stores.unlink_store import drop_link
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index, save_store_index
from sldb.store.layout import store_exists
from sldb.store.models.store_entry import StoreEntry
from sldb.store.models.store_index import StoreIndex


def link_store(store: str | Path | None, other_store: str | Path, name: str | None = None, replace: bool = False) -> LinkedStore:
    """Record another store as linked into `store`.

    Args:
        store: The linking store (path, alias, or None to discover it).
        other_store: Path of the `.sldb` directory to link.
        name: Alias for the link; defaults to the name of the directory holding `other_store`.
        replace: Point a link already recorded under that name at `other_store` instead.

    Returns:
        The link as recorded in the store index.

    Raises:
        SLDBStoreError: When `other_store` is not a store or is the linking store itself, or
            the name is invalid, reserved (`local`) or already linked (and not `replace`).
    """
    location = open_store(store)
    other = Path(other_store).resolve()
    _check_other_exists(other)
    _check_not_self(location.store_path, other)
    link_name = name or other.parent.name
    _check_link_name(link_name)
    if replace and any(s.name == link_name for s in load_store_index(location.store_path).stores):
        drop_link(location.store_path, link_name)
    path = record_store_link(location.store_path, location.project_root, other, link_name)
    return LinkedStore(name=link_name, path=path)


def _check_other_exists(other: Path) -> None:
    """Refuse to link a directory that holds no store."""
    if not store_exists(other):
        raise SLDBStoreError(f"No store at {other}")


def _check_not_self(store_path: Path, other: Path) -> None:
    """Refuse to link a store into itself."""
    if store_path.resolve() == other:
        raise SLDBStoreError(f"A store cannot link to itself: {other}")


def _check_link_name(name: str) -> None:
    """Refuse an alias `alias:doc` references could not name, and the reserved `local`."""
    if not LINK_NAME.match(name) or name == LOCAL:
        raise SLDBStoreError(f"Invalid link name '{name}': use letters, digits, '.', '_' or '-' (starting with a letter or digit), not 'local'. Pass --name.")


def _check_store_linked(idx: StoreIndex, name: str) -> None:
    """Refuse a link name the store index already uses."""
    if any(s.name == name for s in idx.stores):
        raise SLDBStoreError(f"Store '{name}' already linked.")


def record_store_link(sp: Path, root: Path, other: Path, name: str) -> str:
    """Append a link entry to the store index without checking that `other` exists.

    Args:
        sp: The linking store's `.sldb` directory.
        root: The linking store's project root.
        other: Resolved `.sldb` directory being linked.
        name: Alias for the link.

    Returns:
        The path recorded for the link, always relative to `root` so the link survives a
        checkout of both repos at another location.

    Raises:
        SLDBStoreError: When the name is already linked.
    """
    idx = load_store_index(sp)
    _check_store_linked(idx, name)
    rel = os.path.relpath(other, root)
    idx.stores.append(StoreEntry(name=name, path=rel))
    save_store_index(sp, idx)
    return rel

FILE:src/sldb/store/query.py
from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from sldb.store.codec import StoreCodec, default_codec
from sldb.store.layout import project_root, store_exists
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_store_index,
)
from sldb.store.query_engine.models import RuntimeDocument
from sldb.store.source_read import guarded_text
from sldb.store.runtime_cache import cached_document, cached_store, invalidate_runtime_cache  # noqa: F401


def _resolve_path(base: Path, maybe_relative: str) -> Path:
    """Resolves a potentially relative path against a base path."""
    path = Path(maybe_relative)
    return path if path.is_absolute() else (base / path).resolve()


def _extract_doc(doc, root, model_type, m_entry, s_name, s_path, codec: StoreCodec) -> RuntimeDocument | None:
    if (text := guarded_text(root, root / doc.path)) is None:
        return None  # missing, or not read (source_read): `stores check` names it
    return RuntimeDocument(store_name=s_name, store_path=s_path, model_name=m_entry.name, model_type=model_type, name=doc.name, path=doc.path, payload=codec.extract(model_type, text), semantic_tags=list(doc.semantic_tags), source_hash=doc.source_hash, content_hash=doc.content_hash, field_hashes=dict(doc.field_hashes or {}), provenance=doc.provenance)


def _load_doc(doc, root, model_type, m_entry, s_name, s_path, codec: StoreCodec = default_codec) -> RuntimeDocument | None:
    """One document, from the per-document cache when the default codec is in use."""
    if codec is not default_codec:
        return _extract_doc(doc, root, model_type, m_entry, s_name, s_path, codec)
    return cached_document(doc, root, s_path, s_name, m_entry.name, model_type, lambda: _extract_doc(doc, root, model_type, m_entry, s_name, s_path, codec))


def _load_accepted(*args) -> RuntimeDocument | None:
    """`_load_doc`, None for a document its model rejects: `stores check` names it once, as
    `store/doc-invalid` (inbox 3895e9f7 H1), and its scans read the rest."""
    try:
        return _load_doc(*args)
    except ValidationError:
        return None


def _resolve_model_type(resolver, model_ref: str, p_path, store_root: Path):
    """Resolve a model, trying the store's own project root before giving up.

    Linked stores register model_refs (e.g. ``docs.models:X``) that resolve
    relative to that store's repo root, not the caller's pythonpath. We try the
    caller path first, then the store root, and return None if neither works so a
    single unresolvable model does not abort a federated query.
    """
    for candidate in (p_path, str(store_root)):
        try:
            return resolver(model_ref, candidate)
        except Exception:  # noqa: BLE001 - graceful degradation across repos
            continue
    return None


def _load_one(s_path: Path, s_name: str, resolver, p_path, codec: StoreCodec = default_codec, accepted_only: bool = False) -> list[RuntimeDocument]:
    root, docs = project_root(s_path), []
    load = _load_accepted if accepted_only else _load_doc
    for m in load_store_index(s_path).models:
        m_type = _resolve_model_type(resolver, m.model_ref, p_path, root)
        if m_type is None:
            continue
        d_idx = load_documents_index(root / load_models_index(root / m.models_index).documents_index)
        docs.extend([d for doc in d_idx.documents if (d := load(doc, root, m_type, m, s_name, s_path, codec))])
    return docs


def load_runtime_documents(store_path: Path, resolve_model_ref, pythonpath: str | None = None, include_linked: bool = False, codec: StoreCodec = default_codec, store_name: str = "local", accepted_only: bool = False) -> list[RuntimeDocument]:
    """The tracked documents of a store, extracted. With the default codec the load is cached
    by the state of the files it comes from (sldb.store.runtime_cache), so repeated queries
    do not read the store again. The list is fresh per call; the documents are shared.
    `store_name` is the name the documents carry: the alias when a linked store is read alone.
    `accepted_only` leaves out each document its model rejects instead of raising (uncached:
    `stores check` scans, inbox 3895e9f7 H1)."""
    def one(path: Path, name: str) -> list[RuntimeDocument]:
        loader = lambda: _load_one(path, name, resolve_model_ref, pythonpath, codec, accepted_only)  # noqa: E731
        return cached_store(path, name, pythonpath, loader) if codec is default_codec and not accepted_only else loader()

    return _load_federated_documents(store_path, one) if include_linked else list(one(store_path, store_name))


def _load_federated_documents(store_path: Path, load_one) -> list[RuntimeDocument]:
    """Traverse explicit links once per canonical store, safely across cycles."""
    documents: list[RuntimeDocument] = []
    pending: list[tuple[Path, str]] = [(store_path.resolve(), "local")]
    visited: set[Path] = set()
    while pending:
        _visit_federated_store(pending.pop(0), pending, visited, documents, load_one)
    return documents


def _visit_federated_store(item, pending, visited, documents, load_one) -> None:
    current, name = item
    if current in visited or not store_exists(current):
        return
    visited.add(current)
    documents.extend(load_one(current, name))
    pending.extend(_linked_stores(current))


def _linked_stores(store_path: Path) -> list[tuple[Path, str]]:
    root = project_root(store_path)
    return [
        (_resolve_path(root, entry.path).resolve(), entry.name)
        for entry in load_store_index(store_path).stores
        if store_exists(_resolve_path(root, entry.path))
    ]


from sldb.store.query_engine.structural import (  # noqa: E402
    list_structural as list_structural,
    get_structural as get_structural,
)
from sldb.store.query_engine.structural_queries import (  # noqa: E402
    glob_structural as glob_structural,
    find_structural as find_structural,
)
from sldb.store.query_engine.semantic import (  # noqa: E402
    list_semantic as list_semantic,
    get_semantic as get_semantic,
    glob_semantic as glob_semantic,
    find_semantic as find_semantic,
)
from sldb.store.query_engine.global_semantic import (  # noqa: E402
    get_global_semantic as get_global_semantic,
    list_global_semantic as list_global_semantic,
)

FILE:tests/api/test_api_stores.py
"""`sldb.api` store operations: open, link, refresh indexes; and the `sldb.cli` bridges over them."""

from __future__ import annotations

import pytest

from sldb.api import link_store, open_store, update_store_indexes
from sldb.cli import main as cli_main
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index


def test_open_store_resolves_store_and_project_root(api_store):
    location = open_store(str(api_store.store))
    assert location.store_path == api_store.store.resolve()
    assert location.project_root == api_store.root.resolve()
    assert get_store_context(str(api_store.store)) == (location.store_path, location.project_root)


def test_open_store_without_store_outside_any_project_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    with pytest.raises(SLDBStoreError, match="init --path"):
        open_store(None)


def test_link_store_records_link_and_refuses_duplicates(api_store, tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    assert cli_main(["stores", "init", "--path", str(other)]) == 0
    linked = link_store(api_store.store, other / ".sldb", "shared")
    assert (linked.name, linked.path) == ("shared", "../other/.sldb")
    assert [s.name for s in load_store_index(api_store.store).stores] == ["shared"]
    with pytest.raises(SLDBStoreError, match="already linked"):
        link_store(api_store.store, other / ".sldb", "shared")


def test_link_store_refuses_a_directory_without_store(api_store, tmp_path):
    with pytest.raises(SLDBStoreError, match="No store at"):
        link_store(api_store.store, tmp_path / "nowhere" / ".sldb", "ghost")


def test_update_store_indexes_reports_a_complete_refresh(api_store):
    report = update_store_indexes(api_store.store, api_store.pythonpath)
    assert report.complete
    assert report.store_path == api_store.store.resolve()
    assert report.semantic_index.docs_processed >= 0


def test_update_store_indexes_skips_a_missing_document(api_store):
    (api_store.root / "login.md").unlink()
    report = update_store_indexes(api_store.store, api_store.pythonpath)
    assert report.skipped_documents == ["login"]
    assert not report.complete
    assert cli_main(["stores", "update", "--store", str(api_store.store), "--pythonpath", api_store.pythonpath]) == 1


def test_scaffold_store_and_build_store_are_public_and_bridged_by_the_cli(api_store, capsys):
    """GD26: the scaffold of folders and seeds is an `sldb.api` function and a `stores` subcommand."""
    from sldb.api import ScaffoldReport, Seed, StoreDeclaration, build_store, scaffold_store
    from sldb.api.stores.declare_store import declare_store
    from sldb.api.stores.store_declaration import save_declaration

    save_declaration(api_store.store, declare_store(api_store.store, api_store.root))
    declaration = StoreDeclaration(folders=["inbox"], seeds=[Seed(path="inbox/.keep", text="")])
    report = scaffold_store(api_store.store, declaration=declaration, apply=True)
    assert isinstance(report, ScaffoldReport) and report.created == ["inbox", "inbox/.keep"]
    assert build_store(api_store.store)["scaffold"] == {"created": [], "rewritten": [], "present": [], "conflicts": []}
    assert cli_main(["stores", "scaffold", "--store", str(api_store.store), "--format", "json"]) == 0
    assert "created" in capsys.readouterr().out

FILE:instruccion
Cold-bundle de la tarea task-sldb-stores-add-guarda-tal-cual-un-enlace-absoluto-con-o-con-variable-de-entorno: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm pytest -q tests/api/test_unlink_store.py
- TMPDIR=/dev/shm pytest -q tests/store/test_stores_build.py

