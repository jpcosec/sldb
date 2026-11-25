FILE:desk/tasks/task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar.md
---
sldb:
  by: agent
  at: '2026-11-16T06:18:04Z'
  authority: generated
  via: save_document_payload
id: task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar
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
- src/sldb/store/query.py
- src/sldb/api/documents/document_payload.py
- tests/api/test_views_linked.py
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-vista-de-todo-el-store-no-puede-depender-de-que-importen-todos-sus-modelos
from_drawer: desk/drawer/tasks/task-docs-show-sobre-un-store-enlazado-reporta-unknown-document-target-cuando-lo-que-falla-es-importar-el-modelo.md
---

# docs show sobre un store enlazado dice que no pudo importar el modelo en vez de Unknown document target

## Rationale

_Explain why this task exists or the business driver behind it._

Desde el store central de deskops (enlazado a ../sldb/.sldb), `sldb docs show sldb:ArchitectureNarrativeDoc/arch-code-docstring-indexing --store .sldb` respondió "Unknown document target" cuando lo que fallaba era importar el modelo del store enlazado. _resolve_model_type (src/sldb/store/query.py:47-60) ya prueba la raíz del proyecto enlazado, pero traga toda excepción (except Exception: continue) y devuelve None, así que los documentos de ese modelo desaparecen en silencio y runtime_document (src/sldb/api/documents/document_payload.py:23-37) lanza el genérico _unknown_target (línea 61). Origen: drawer desk/drawer/tasks/task-docs-show-sobre-un-store-enlazado-reporta-unknown-document-target-cuando-lo-que-falla-es-importar-el-modelo.md.

## Goal

_Describe the concrete result this task must produce._

Cuando el documento pedido existe en el índice pero su modelo no se pudo importar, docs show (y runtime_document) lanza un error que dice "could not import model <Modelo> of store <store>: <excepción original>"; y se sabe, con un test, por qué la raíz enlazada no bastó en el caso de deskops.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) reproducir con un test en tests/api/test_views_linked.py: store A enlaza a store B cuyo modelo importa un módulo que no existe; docs show del documento de B da hoy Unknown document target. (2) Guardar en _resolve_model_type el error de import por modelo (dict modelo -> excepción) en vez de descartarlo, y en document_payload.py, cuando el ref nombra un documento cuyo modelo falló, lanzar el error de Goal. (3) Reproducir también un choque de nombres en sys.modules (dos stores con un paquete del mismo nombre, el caso probable de deskops) y anotar en el informe si es la causa; si lo es, el mensaje lo dice ("module <m> already imported from <ruta>"). CHANGELOG.md. No entra: cambiar la estrategia de import de modelos enlazados más allá del mensaje.

Precisiones (preflight-1): Validation tiene dos comandos pytest; "los tres comandos" de Done When debe leerse "los dos comandos de Validation". El mensaje del choque es exactamente "module <nombre> already imported from <module.__file__>", con el __file__ del módulo que ya estaba en sys.modules. Este contrato solo detecta y reporta el choque: no lo mitiga (no se cambia la estrategia de import). "Se sabe por qué la raíz enlazada no bastó" se cumple cuando result-summary.md del run dice cuál de los dos tests reproduce el síntoma de deskops (modelo que no importa, o choque en sys.modules) y con qué salida.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/query.py 40-75 y document_payload.py 20-65. 2) Test que falla hoy. 3) Guardar errores y cambiar el mensaje. 4) Test del choque en sys.modules. 5) Informe.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_views_linked.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py

## Done When

_Name the observable condition that makes the task complete._

Los dos comandos de Validation pasan; el test del modelo que no importa ve el mensaje nuevo; el informe dice si el choque de sys.modules reproduce el caso de deskops; CHANGELOG y commit.

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

FILE:desk/atoms/atom-una-vista-de-todo-el-store-no-puede-depender-de-que-importen-todos-sus-modelos.md
---
id: atom-una-vista-de-todo-el-store-no-puede-depender-de-que-importen-todos-sus-modelos
title: Una vista de todo el store no puede depender de que importen todos sus modelos
five_wh_one_plus: why
tags:
- system:sldb
---

# Una vista de todo el store no puede depender de que importen todos sus modelos

## Answer

Un store registra modelos de varios paquetes (deskops, pron, el propio repo) y no todos están instalados en cada entorno. Una vista que recorre todos los modelos (el AST del store en src/sldb/api/records/build_ast.py) tiene que registrar el que no importa como no resuelto, con su error, y seguir: si aborta, cualquier consulta de otro modelo cae con él.

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

FILE:src/sldb/api/documents/document_payload.py
"""One tracked document's runtime record and payload addressing, api-side.

``runtime_document`` narrows ``load_runtime_documents`` to one document by name,
path or ``Model/name``, optionally behind ``alias:`` for a linked store; it is the one
resolver the CLI's ``resolve_runtime_doc`` and the serve routes share. ``leaf_paths`` names every
addressable field of a payload with the dotted paths ``deep_get`` reads.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.doc_ref import LOCAL, matches_doc_ref, qualifier, split_doc_ref
from sldb.api.stores.store_links import find_link
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.store.layout import project_root
from sldb.store.query import load_runtime_documents
from sldb.store.source_guard import unread_line


def runtime_document(store_path: Path, pythonpath: str | None, doc_ref: str) -> Any:
    """The RuntimeDocument of one doc; unknown or ambiguous refs raise SLDBDocumentTargetError.

    `alias:ref` reads only the store directly linked under `alias` (see `sldb.api.stores.doc_ref`);
    a bare ref reads only the local store.
    """
    alias, ref = split_doc_ref(store_path, doc_ref)
    docs = _scoped_documents(store_path, alias, pythonpath)
    candidates = [doc for doc in docs if matches_doc_ref(ref, doc.name, doc.path, doc.model_name)]
    if not candidates:
        _refuse_unread(store_path, alias, ref)
        raise SLDBDocumentTargetError(_unknown_target(doc_ref, alias))
    if len(candidates) > 1:
        raise SLDBDocumentTargetError(f"Ambiguous document target '{doc_ref}'. Use 'Model/DocName' or a tracked path.")
    return candidates[0]


def _refuse_unread(store_path: Path, alias: str | None, ref: str) -> None:
    """A tracked document the read guard refuses is not loaded (`store.query`): when `ref` names
    one, fail with its finding (`store/path-outside-root`, `store/symlink-not-read`), not as unknown."""
    from sldb.api.stores.declared_includes import tracked_rows

    scoped = store_path if alias is None else Path(find_link(store_path, alias)["resolved"])
    root = project_root(scoped)
    for model, path, name in tracked_rows(scoped, root):
        if matches_doc_ref(ref, name, path, model) and (line := unread_line(root, root / path, f"{model}:{name}")) is not None:
            raise SLDBDocumentTargetError(line)


def _scoped_documents(store_path: Path, alias: str | None, pythonpath: str | None) -> list[Any]:
    if alias is None:
        return load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    link = find_link(store_path, alias)
    if link["status"] != "ok":
        raise SLDBDocumentTargetError(f"Linked store '{alias}' is {link['status']}: {link['resolved']}")
    return load_runtime_documents(Path(link["resolved"]), resolve_model_ref, pythonpath, store_name=alias)


def _unknown_target(doc_ref: str, alias: str | None) -> str:
    prefix = qualifier(doc_ref)
    hint = f" (no linked store named '{prefix}')" if alias is None and prefix not in (None, LOCAL) else ""
    return f"Unknown document target: {doc_ref}{hint}"


def leaf_paths(payload: dict[str, Any]) -> list[str]:
    """Every leaf address (dotted path) of a payload, shallow lists by index."""
    paths: list[str] = []
    _walk(payload, "", paths)
    return [path for path in paths if path]


def _walk(value: Any, prefix: str, paths: list[str]) -> None:
    if isinstance(value, dict):
        _walk_mapping(value, prefix, paths)
        return
    if isinstance(value, list):
        _walk_sequence(value, prefix, paths)
        return
    paths.append(prefix)


def _walk_mapping(value: dict[str, Any], prefix: str, paths: list[str]) -> None:
    if not value and prefix:
        paths.append(prefix)
        return
    for key, item in value.items():
        _walk(item, f"{prefix}.{key}" if prefix else key, paths)


def _walk_sequence(value: list[Any], prefix: str, paths: list[str]) -> None:
    if not value and prefix:
        paths.append(prefix)
        return
    for index, item in enumerate(value):
        _walk(item, f"{prefix}.{index}", paths)

FILE:tests/api/test_views_linked.py
"""H9: a ViewDoc tracked by a linked store (DA4: deskops' views ship only in its package store).

Store A links to B; the view `board` lives only in B. `run_view(A, "board")` finds it, reads
its file from B's root (through the read guard) and evaluates it over A's documents."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.core.exceptions import SLDBDocumentTargetError

MODULE = "sldb_h9_linked_view_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


def board(key: str, title: str = "Board") -> dict:
    return {"id": "board", "name": "board", "title": title, "sections": [{"key": key, "select": {"model": "Note"}, "fields": ["title"]}]}


class Store:
    def __init__(self, base: Path, name: str, py: str) -> None:
        self.root, self.py = base / name, py
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for ref in (f"{MODULE}:Note", "sldb.models.notation_models:ViewDoc"):
            api.add_model(self.store, ref, py)

    def doc(self, model: str, name: str, payload: dict) -> Path:
        path = self.root / model.lower() / f"{name}.md"
        api.create_document(self.store, model, path, payload, name, self.py)
        return path

    def link(self, other: "Store", name: str) -> None:
        api.link_store(self.store, other.store, name=name)


@pytest.fixture
def stores(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        a, b = Store(tmp_path, "A", str(tmp_path)), Store(tmp_path, "B", str(tmp_path))
        a.doc("Note", "a1", {"title": "from A"})
        b.doc("Note", "b1", {"title": "from B"})
        b.doc("ViewDoc", "board", board("notes"))
        a.link(b, "B")
        yield a, b
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def test_a_view_only_in_the_linked_store_is_found_and_evaluated_over_the_calling_store(stores) -> None:
    a, _ = stores
    (a.root / "viewdoc").mkdir()
    (a.root / "viewdoc" / "board.md").write_text("# not the view: B's root is read, not A's\n", encoding="utf-8")
    result = api.run_view(a.store, "board")
    assert result["view"] == "board"
    assert [(r["export_id"], r["fields"]) for r in result["sections"]["notes"]["rows"]] == [("Note:a1", {"title": "from A"})]
    assert api.run_view(a.store, "B:board")["revision"] == result["revision"]


def test_list_views_lists_the_linked_view(stores) -> None:
    a, _ = stores
    assert api.list_views(a.store) == [{"name": "board", "title": "Board", "params": [], "sections": ["notes"]}]


def test_two_linked_views_with_one_name_are_ambiguous_and_listed_qualified(stores, tmp_path: Path) -> None:
    a, _ = stores
    c = Store(tmp_path, "C", str(tmp_path))
    c.doc("ViewDoc", "board", board("other"))
    a.link(c, "C")
    with pytest.raises(SLDBDocumentTargetError) as caught:
        api.run_view(a.store, "board")
    assert str(caught.value) == "Ambiguous view: board (linked in B, C)"
    assert [v["name"] for v in api.list_views(a.store)] == ["B:board", "C:board"]
    assert list(api.run_view(a.store, "C:board")["sections"]) == ["other"]


def test_a_local_view_wins_over_a_linked_one(stores) -> None:
    a, _ = stores
    a.doc("ViewDoc", "board", board("mine", "Mine"))
    assert list(api.run_view(a.store, "board")["sections"]) == ["mine"]
    assert list(api.run_view(a.store, "B:board")["sections"]) == ["notes"]
    assert [(v["name"], v["title"]) for v in api.list_views(a.store)] == [("B:board", "Board"), ("board", "Mine")]


def test_the_revision_moves_when_the_linked_view_changes(stores) -> None:
    a, b = stores
    before = api.run_view(a.store, "board")["revision"]
    api.save_document_payload(b.store, "ViewDoc", "board", board("notes", "Board v2"), b.py)
    assert api.run_view(a.store, "board")["revision"] != before


def test_a_linked_view_file_swapped_for_a_symlink_out_of_its_root_is_not_read(stores, tmp_path: Path) -> None:
    a, b = stores
    path = b.root / "viewdoc" / "board.md"
    outside = tmp_path / "outside.md"
    outside.write_bytes(path.read_bytes())
    path.unlink()
    path.symlink_to(outside)
    with pytest.raises(SLDBDocumentTargetError, match="outside-root"):
        api.run_view(a.store, "board")

FILE:instruccion
Cold-bundle de la tarea task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_views_linked.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py

