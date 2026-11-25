FILE:desk/tasks/task-la-escritura-por-campos-save-document-payload-y-el-update-de-apply-batch-falla-nombrando-el-contenid.md
---
sldb:
  by: agent
  at: '2026-11-17T02:12:10Z'
  authority: generated
  via: create_document
id: task-la-escritura-por-campos-save-document-payload-y-el-update-de-apply-batch-falla-nombrando-el-contenid
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-223438-suggestion-save-document-payload-y-apply-batch-update-borran-en-silencio-contenido-que-el-modelo-no-declara-ws47-del-drawer-de-deskops.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/payload_save.py
- src/sldb/api/documents/payload_save_steps.py
- tests/api/test_structural_noise.py
- tests/api/test_transaction.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La escritura por campos (save_document_payload y el update de apply_batch) falla nombrando el contenido que se perdería en vez de borrarlo en silencio

## Rationale

_Explain why this task exists or the business driver behind it._

save_document_payload, y el update de apply_batch que pasa por él, re-renderiza el documento desde el payload sin mirar el archivo previo; refuse_structural_noise y refuse_undeclared_frontmatter solo se aplican al crear o trackear. Si el archivo trae ruido estructural o frontmatter que el modelo no declara, una escritura por campos lo borra sin aviso. graph_ui va a escribir por apply_batch update. Origen: desk/inbox/20261116-223438-suggestion-save-document-payload-y-apply-batch-update-borran-en-silencio-contenido-que-el-modelo-no-declara-ws47-del-drawer-de-deskops.md.

## Goal

_Describe the concrete result this task must produce._

Una escritura por campos sobre un documento cuyo archivo actual tiene ruido estructural o frontmatter no declarado falla antes de escribir, con un error que nombra lo que se perdería, y deja el archivo intacto; los documentos limpios se escriben igual que hoy.

## Scope

_State what is in scope and what is out of scope._

Entra: aplicar la misma guarda que al crear (refuse_structural_noise y refuse_undeclared_frontmatter sobre el texto actual del archivo) en el camino de save_document_payload (src/sldb/api/documents/payload_save.py y payload_save_steps.py) antes de re-renderizar, con el mismo tipo de excepción; tests en tests/api/test_structural_noise.py y en tests/api/test_transaction.py (apply_batch update sobre un archivo con frontmatter extra falla sin escritura parcial). CHANGELOG. No entra: un modo force para estas escrituras.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer payload_save.py, payload_save_steps.py, refuse_structural_noise.py, frontmatter_keys.py y transaction_ops.py. 2) Agregar la guarda. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_structural_noise.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_transaction.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_write_paths_validate.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a deskops y graph_ui.

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

FILE:src/sldb/api/documents/payload_save.py
"""Write a whole payload back to a tracked document: render, round-trip, rehash, reindex."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.doc_anchor_pinning import pin_payload
from sldb.api.documents.payload_save_steps import check_rules_on_write, load_document_entry, load_model_indexes, model_class, render_checked, save_document_indexes, write_rendered_document
from sldb.api.rules.rule_writes import refuse_unknown_family
from sldb.api.stores.open_store import open_store


def save_document_payload(store: str | Path | None, model_name: str, document_name: str, payload: dict[str, Any], pythonpath: str | None = None, actor: str | None = None) -> DocumentReference:
    """Replace a tracked document's content with the Markdown rendered from `payload`.

    Args:
        store: The store tracking the document (path, alias, or None to discover it).
        model_name: Registered model name of the document.
        document_name: Tracked document name.
        payload: The complete new payload; it has no fixed schema beyond the model's own.
        pythonpath: Directory to import the model module from; the store's project root
            is tried next, since a linked store's models import from where it lives.
        actor: Optional caller label, stamped into the document's provenance block.

    Returns:
        The document written.

    Raises:
        SLDBPayloadSaveError: When the model or document is not registered, or the rendered
            Markdown does not round-trip back to the payload.
        SLDBStoreError: When a RuleDoc's subject names a model the store does not register.
        SLDBRuleViolationError: When an `on_write` rule of severity error fails on the payload
            (after its anchors are pinned); nothing is written.
    """
    location = open_store(store)
    idx, m_entry, m_idx = load_model_indexes(location.store_path, location.project_root, model_name)
    doc_entry = load_document_entry(location.store_path, m_entry.name, document_name)
    model_type = model_class(m_entry.model_ref, pythonpath, location.project_root)
    _save(location, idx, m_idx, m_entry, doc_entry, model_type, payload, pythonpath, actor)
    return DocumentReference(model=m_entry.name, name=doc_entry.name, path=location.project_root / doc_entry.path)


def _save(location, idx, m_idx, m_entry, doc_entry, model_type, payload, pythonpath, actor) -> None:
    payload = pin_payload(location.store_path, model_type, payload)
    check_rules_on_write(location.store_path, model_type, f"{m_entry.name}:{doc_entry.name}", payload)
    rendered = render_checked(model_type, payload, location.project_root)
    refuse_unknown_family(location.store_path, model_type, payload, pythonpath)
    write_rendered_document(location.project_root, doc_entry, model_type, rendered, actor=actor, store_path=location.store_path)
    save_document_indexes(location.store_path, location.project_root, idx, m_idx, m_entry, doc_entry, pythonpath, model_type)

FILE:src/sldb/api/documents/payload_save_steps.py
"""The steps of `save_document_payload`, moved here from `sldb.cli.commands.fields_save`."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.core.exceptions import SLDBModelError, SLDBPayloadSaveError
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store import documents_hash
from sldb.store.hashing import hash_fields_with_map, hash_text
from sldb.store.io import load_models_index, load_store_index, save_models_index, store_lock
from sldb.store.io.shards import load_document_shard, save_document_shard
from sldb.store.layout import documents_shard_path
from sldb.store.models.document_entry import DocumentEntry
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.models_index import ModelsIndex
from sldb.store.models.store_index import StoreIndex
from sldb.store.model_node import stamp_model_node
from sldb.store.ops import cascade_store_hash
from sldb.store.edge_rebuild import rebuild_edges_indexes
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import rebuild_semantic_indexes
from sldb.store.source_read import refuse_unreadable
from sldb.store.source_guard import write_source_text
from sldb.models.provenance_block import index_block


def model_class(model_ref: str, pythonpath: str | None, root: Path) -> type:
    """The model class, imported with the caller's pythonpath first, then the store's own root.

    A linked store's models import from where that store lives.
    """
    try:
        return resolve_model_ref(model_ref, pythonpath)
    except SLDBModelError:
        return resolve_model_ref(model_ref, str(root))


def load_model_indexes(sp: Path, root: Path, model_name: str) -> tuple[StoreIndex, ModelEntry, ModelsIndex]:
    """The store index, the model's entry and its models index."""
    idx = load_store_index(sp)
    m_entry = next((m for m in idx.models if m.name == model_name), None)
    if m_entry is None:
        raise SLDBPayloadSaveError(f"Model '{model_name}' not registered.")
    return idx, m_entry, load_models_index(root / m_entry.models_index)


def load_document_entry(sp: Path, model_name: str, doc_name: str) -> DocumentEntry:
    """The document's index entry, from its shard."""
    doc_entry = load_document_shard(documents_shard_path(sp, model_name, doc_name))
    if doc_entry is None:
        raise SLDBPayloadSaveError(f"Doc '{doc_name}' not registered.")
    return doc_entry


def render_checked(model_type: type, payload: dict[str, Any], ref_root: Path, store_path: Path | None = None) -> str:
    """The payload rendered to Markdown, refused unless it round-trips.

    `ref_root` is the project root, so a composed field resolves its refs against the project
    rather than against whatever directory the caller happens to run in. With `store_path`, the
    unpinned document anchors of the payload are pinned first (GO07, `doc_anchor_pinning`).
    """
    from sldb.api.documents.doc_anchor_pinning import pin_payload

    payload = pin_payload(store_path, model_type, payload) if store_path is not None else payload
    rendered = render_model_markdown(model_type, payload, ref_root)
    valid, details = validate_model_input_roundtrip(model_type, rendered)
    if not valid:
        raise SLDBPayloadSaveError(f"Field mutation broke idempotency: {details}")
    return rendered


def check_rules_on_write(store_path: Path, model_type: type, node: str, payload: dict[str, Any]) -> None:
    """The `on_write` rules on the pinned payload of `node` (GO08), before anything is written:
    an error raises `SLDBRuleViolationError`; a store without RuleDoc is not read."""
    from sldb.api.rules.rules_on_write import check_on_write

    check_on_write(store_path, model_type, node, payload)


def write_rendered_document(root: Path, doc_entry: DocumentEntry, model_type: type, rendered: str, via: str = "save_document_payload", actor: str | None = None, store_path: Path | None = None) -> None:
    """Write the rendered Markdown, signed with its provenance block (plus final newline), and
    record its source and content hashes. With `store_path`, the block's unpinned `from:`
    document anchors are pinned (GO07)."""
    from sldb.api.documents.doc_anchor_pinning import pin_provenance
    from sldb.api.documents.provenance_stamp import stamped_file

    refuse_unreadable(root, root / doc_entry.path)  # a symlink, or a path out of the root, is not written through
    text = stamped_file(root / doc_entry.path, rendered + "\n", model_type, via, actor)
    text = pin_provenance(store_path, text) if store_path is not None else text
    write_source_text(root / doc_entry.path, text)  # O_NOFOLLOW: a symlink swapped in after the check is not written through
    doc_entry.source_hash = hash_text(text)
    doc_entry.content_hash, doc_entry.field_hashes = hash_fields_with_map(model_type, text)
    doc_entry.provenance = index_block(text)


def save_document_indexes(sp: Path, root: Path, idx: StoreIndex, m_idx: ModelsIndex, m_entry: ModelEntry, doc_entry: DocumentEntry, pythonpath: str | None, model_type: type | None = None) -> None:
    """Save the document shard and model hashes, then rebuild derived indexes, under the store lock.

    The model's roster hash covers its documents' hashes: a field write must move it, or
    `stores check` fails and consumers keyed on the model node never see the change.
    """
    with store_lock(sp):
        save_document_shard(documents_shard_path(sp, m_entry.name, doc_entry.name), doc_entry)
        documents_hash.note(sp, m_entry.name, doc_entry)
        stamp_model_node(m_idx, documents_hash.roster_hash_of(sp, m_entry.name), model_type)
        m_idx.documents_count = documents_hash.count_of(sp, m_entry.name)
        save_models_index(root / m_entry.models_index, m_idx)
        rebuild_semantic_indexes(sp, root, resolve_model_ref, pythonpath)
        rebuild_sections_indexes(sp, root, resolve_model_ref, pythonpath)
        rebuild_edges_indexes(sp, root, resolve_model_ref, pythonpath)
        cascade_store_hash(sp, root, idx)

FILE:tests/api/test_structural_noise.py
"""Structural noise: a heading inside a field is a field the model is missing.

The document is not corrupt — it extracts and re-renders — but the section is
swallowed into a field value and its own identity is lost. The refusal is at
registration, and the way out is a child model declaring the sections `optrev`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from pydantic import Field

from sldb import StructuredNLDoc
from sldb.api import add_model, check_store, init_store, track_document_file
from sldb.api.documents.frontmatter_keys import (
    refuse_undeclared_frontmatter,
    undeclared_frontmatter_keys,
)
from sldb.api.stores.scan_structural_noise import scan_structural_noise
from sldb.core.exceptions import SLDBValidationError

MODULE = "sldb_noise_test_models"

# NoteDoc declares one heading; NoteWithSections inherits it and declares the two more
# that the noisy document carries, as optrev so plain notes still validate.
MODELS_SOURCE = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n## Answer\\n\\n⸢rev•body⸥"
    title: str = Field(description="Note title.")
    body: str = Field(description="Note body.")


class NoteWithSections(NoteDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n## Answer\\n\\n⸢rev•body⸥\\n\\n## Entidades\\n\\n⸢optrev•entidades⸥\\n\\n## Medicion 1\\n\\n⸢optrev•medicion_1⸥"
    entidades: str = Field(default="", description="Referenced atoms.")
    medicion_1: str = Field(default="", description="First verifiable criterion.")
'''

CLEAN = "# Alpha\n\n## Answer\n\nJust prose, no headings inside the body.\n"
NOISY = "# Alpha\n\n## Answer\n\nBody text\n\n## Entidades\n\n- one\n\n## Medicion 1\n\n- two\n"


@pytest.fixture
def noise_store(tmp_path: Path):
    """A store with NoteDoc and its child NoteWithSections registered."""
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS_SOURCE, encoding="utf-8")
    root = tmp_path / "repo"
    root.mkdir()
    init_store(root)
    store = root / ".sldb"
    for name in ("NoteDoc", "NoteWithSections"):
        add_model(store, f"{MODULE}:{name}", str(tmp_path))
    yield SimpleStore(root, store, str(tmp_path))
    sys.modules.pop(MODULE, None)


class SimpleStore:
    """Paths of a throwaway store, plus a way to drop a Markdown file into it."""

    def __init__(self, root: Path, store: Path, pythonpath: str) -> None:
        self.root, self.store, self.pythonpath = root, store, pythonpath

    def write(self, name: str, text: str) -> Path:
        """Write `text` to `root/<name>.md` without tracking it."""
        path = self.root / f"{name}.md"
        path.write_text(text, encoding="utf-8")
        return path


def test_track_refuses_a_document_whose_headings_the_model_does_not_declare(noise_store):
    """The refusal is an error that names every offending heading, not a warning."""
    path = noise_store.write("noisy", NOISY)
    with pytest.raises(SLDBValidationError) as excinfo:
        track_document_file(noise_store.store, "NoteDoc", path, pythonpath=noise_store.pythonpath)
    message = str(excinfo.value)
    assert "ruido estructural en 'noisy'" in message
    assert "## Entidades" in message and "## Medicion 1" in message
    assert excinfo.value.details["undeclared"] == ["## Entidades", "## Medicion 1"]
    assert "herede de NoteDoc" in message


def test_the_refusal_leaves_the_document_untracked(noise_store):
    """Nothing enters the store: the refusal is a block, not a logged complaint."""
    path = noise_store.write("noisy", NOISY)
    with pytest.raises(SLDBValidationError):
        track_document_file(noise_store.store, "NoteDoc", path, pythonpath=noise_store.pythonpath)
    assert scan_structural_noise(noise_store.store, noise_store.root, noise_store.pythonpath) == []


def test_a_document_that_fits_its_model_still_tracks(noise_store):
    """The happy path is untouched: no headings beyond the template, no refusal."""
    path = noise_store.write("clean", CLEAN)
    tracked = track_document_file(noise_store.store, "NoteDoc", path, pythonpath=noise_store.pythonpath)
    assert (tracked.model, tracked.name) == ("NoteDoc", "clean")


def test_a_child_model_declaring_the_sections_optrev_accepts_the_document(noise_store):
    """The way out: inherit, declare the sections, and the same bytes are admitted."""
    path = noise_store.write("noisy", NOISY)
    tracked = track_document_file(noise_store.store, "NoteWithSections", path, pythonpath=noise_store.pythonpath)
    assert (tracked.model, tracked.name) == ("NoteWithSections", "noisy")


def test_the_noise_is_swallowed_into_a_field_value_under_the_parent(noise_store):
    """Why it matters: under the parent both sections end up as raw markdown inside `body`.

    That is the loss the refusal exists to stop: the document still round-trips, so
    nothing else in the system ever complains. Declaring the sections keeps `body` to
    the answer and gives each section a field of its own.
    """
    from sldb.api import resolve_model_ref
    from sldb.runtime.validation import extract_model_data

    parent = resolve_model_ref(f"{MODULE}:NoteDoc", noise_store.pythonpath)
    child = resolve_model_ref(f"{MODULE}:NoteWithSections", noise_store.pythonpath)
    assert "## Entidades" in extract_model_data(parent, NOISY)["body"]
    assert extract_model_data(child, NOISY)["body"] == "Body text"


def test_undeclared_frontmatter_key_is_refused():
    """A frontmatter key the model never declares was silently dropped; now refused.

    Symmetric with the heading refusal: `docs track` rejects a heading the model
    never declares, but a frontmatter key it never declares used to vanish on the
    first re-render. The same document, the same contract, the same refusal.
    """

    class CardDoc(StructuredNLDoc):
        __template__ = "---\nid: ⸢rev•id⸥\ntitle: ⸢rev•title⸥\n---\n\n# ⸢rev•title⸥"
        id: str = Field(description="Stable id.")
        title: str = Field(description="Card title.")

    clean = "---\nid: c1\ntitle: Card\n---\n\n# Card"
    assert undeclared_frontmatter_keys(CardDoc, clean) == []
    with_owner = clean.replace("---\nid:", "---\nowner: jp\nid:", 1)
    assert undeclared_frontmatter_keys(CardDoc, with_owner) == ["owner"]
    with pytest.raises(SLDBValidationError, match="owner"):
        refuse_undeclared_frontmatter(CardDoc, with_owner, "card")


def test_a_dict_placeholder_frontmatter_declares_every_key():
    """A frontmatter that is one `dict` placeholder carries any key through extraction and
    back on re-render, so no key is lost and none is refused (deskops' TaskDoc)."""

    class TaskDoc(StructuredNLDoc):
        __template__ = "---\n⸢rev,dict•frontmatter⸥\n---\n\n# ⸢rev•title⸥"
        title: str = Field(description="Task title.")
        frontmatter: dict | None = Field(default=None, description="Metadata.")

    assert undeclared_frontmatter_keys(TaskDoc, "---\npriority: p0\ndomain: x\n---\n\n# T") == []


def test_stores_check_reports_noise_already_tracked_without_blocking(noise_store):
    """`stores check` diagnoses what `docs track` would now refuse; force put it there."""
    path = noise_store.write("noisy", NOISY)
    track_document_file(noise_store.store, "NoteDoc", path, pythonpath=noise_store.pythonpath, force=True)
    report = check_store(noise_store.store, noise_store.root, noise_store.pythonpath)
    entry = next(item for item in report["structural_noise"] if item["document"] == "noisy")
    assert entry["model"] == "NoteDoc"
    assert entry["undeclared"] == ["## Entidades", "## Medicion 1"]


def test_the_cli_refusal_is_loud_and_exits_nonzero(noise_store, capsys):
    """Not a warning and not an empty dict: the CLI names the headings and fails.

    Guards the recurring failure mode of this codebase, where a document that does
    not fit its contract is skipped (`store/query.py::_load_one`) or reduced to a
    `logger.warning` plus `{}` (`cli/graph_ops/map_fields.py`).
    """
    from sldb.cli import main as cli_main

    path = noise_store.write("noisy", NOISY)
    with pytest.raises(SystemExit) as excinfo:
        cli_main(["docs", "track", str(path), "--model", "NoteDoc", "--store", str(noise_store.store), "--pythonpath", noise_store.pythonpath])
    assert excinfo.value.code != 0
    assert "## Entidades" in str(excinfo.value)


def test_stores_check_prints_every_noisy_heading_not_just_a_count(noise_store, capsys):
    """The diagnosis is actionable: each document, its model, and the headings."""
    from sldb.cli import main as cli_main

    path = noise_store.write("noisy", NOISY)
    track_document_file(noise_store.store, "NoteDoc", path, pythonpath=noise_store.pythonpath, force=True)
    capsys.readouterr()
    assert cli_main(["stores", "check", "--store", str(noise_store.store), "--pythonpath", noise_store.pythonpath]) == 0, "noise on a model with declared headings is an alert (policy default)"
    out = capsys.readouterr().out
    assert "alert: [store/structural-noise] NoteDoc:noisy" in out
    assert "## Entidades" in out and "## Medicion 1" in out

FILE:tests/api/test_transaction.py
"""`sldb.api.transaction` and `sldb.api.apply_batch`: writes visible at once, undone together.

The fixture store is `tests/api/conftest.py`'s (TicketDoc, one tracked document `login`); the
moves test registers a referencing pair of models so an incoming edge can be followed.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from typing import Any

import pytest

import sldb.api as api
from sldb.api.documents import transaction_ops
from sldb.core.exceptions import ConflictError, SLDBStoreError, SLDBValidationError
from sldb.store.io.rollback import RollbackError
from sldb.store.io import rollback
from sldb.store.io.shards import load_document_shard
from sldb.store.layout import documents_shard_path

from .conftest import PAYLOAD

PROVENANCE = re.compile(rb"\A---\nsldb:\n(?:  .*\n)*---\n\n")
REF_MODULE = "sldb_transaction_ref_models"
REF_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Linked(StructuredNLDoc):
    __references__ = ["about"]
    __template__ = "---\\nabout: ⸢rev•about⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    about: str = Field(default="", description="Referenced document export id.")
'''


def _files(root: Path) -> dict[str, str]:
    """sha256 of every file under the project (lock files and the on-disk composed index aside): bytes, entries and shards.
    The composed index is a cache H11 keeps outside a transaction (prevalidation reads it before one opens)."""
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file() and "locks" not in p.parts and "composed" not in p.parts}


def _edges(store: Path) -> list:
    return [e.model_dump() for e in api.load_edge_index(store).edges]


def _title(api_store, name: str) -> str:
    return next(d.payload["title"] for d in api.load_runtime_documents(api_store.store, api_store.pythonpath) if d.name == name)


def _entry(api_store, name: str):
    return load_document_shard(documents_shard_path(api_store.store, "TicketDoc", name))


def _failing_create(monkeypatch, at_call: int):
    """`create_document` as the transaction sees it, raising on call number `at_call`."""
    calls, real = {"n": 0}, transaction_ops.create_document

    def injected(*args: Any, **kwargs: Any):
        calls["n"] += 1
        if calls["n"] == at_call:
            raise SLDBValidationError("injected validation failure")
        return real(*args, **kwargs)

    monkeypatch.setattr(transaction_ops, "create_document", injected)


def test_a_batch_whose_third_change_fails_leaves_bytes_entries_and_index_as_before(api_store, monkeypatch):
    before, edges_before = _files(api_store.root), _edges(api_store.store)
    assert api.check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]
    _failing_create(monkeypatch, 3)
    changes = [{"id": f"t{i}", "action": "create", "model": "TicketDoc", "payload": {**PAYLOAD, "title": f"T{i}"}} for i in (1, 2, 3)]
    with pytest.raises(SLDBValidationError, match="injected"):
        api.apply_batch(api_store.store, changes, api_store.pythonpath)
    assert _files(api_store.root) == before
    assert _edges(api_store.store) == edges_before
    assert api.check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]
    assert not (api_store.root / "t1.md").exists() and api.doc_status(api_store.store, "t1").exists is False


def test_nested_transactions_the_inner_ending_well_and_the_outer_failing_revert_both(api_store):
    before = _files(api_store.root)
    with pytest.raises(RuntimeError, match="outer"):
        with api.transaction(api_store.store, api_store.pythonpath) as outer:
            outer.update("login", {**PAYLOAD, "title": "Outer"})
            with api.transaction(api_store.store, api_store.pythonpath) as inner:
                inner.create("TicketDoc", "inner", {**PAYLOAD, "title": "Inner"}, "inner.md")
            assert (api_store.root / "inner.md").exists()
            raise RuntimeError("outer failed")
    assert _files(api_store.root) == before
    assert _title(api_store, "login") == "Broken login"


def test_an_update_is_read_with_its_new_value_inside_the_transaction(api_store):
    with api.transaction(api_store.store, api_store.pythonpath) as tx:
        saved = tx.update("login", {**PAYLOAD, "title": "Inside"})
        assert "# Inside" in saved.path.read_text(encoding="utf-8")
        assert _title(api_store, "login") == "Inside"
    assert _title(api_store, "login") == "Inside"


def test_write_file_with_another_sha256_fails_without_writing(api_store):
    notes = api_store.root / "notes.txt"
    notes.write_text("v1", encoding="utf-8")
    with pytest.raises(ConflictError) as info:
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.write_file("notes.txt", b"v2", expected_sha256="0" * 64)
    assert (info.value.ref, info.value.expected, info.value.actual) == ("notes.txt", "0" * 64, hashlib.sha256(b"v1").hexdigest())
    assert notes.read_text(encoding="utf-8") == "v1"


def test_write_file_and_record_are_restored_by_the_rollback(api_store):
    (api_store.root / "own.txt").write_text("mine", encoding="utf-8")
    with pytest.raises(RuntimeError):
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.write_file("new.txt", b"new", expected_sha256=None)
            (api_store.root / tx.record("own.txt")).write_text("changed", encoding="utf-8")
            raise RuntimeError("boom")
    assert not (api_store.root / "new.txt").exists()
    assert (api_store.root / "own.txt").read_text(encoding="utf-8") == "mine"


def test_a_stale_expected_source_hash_is_a_conflict_and_writes_nothing(api_store):
    actual = _entry(api_store, "login").source_hash
    with pytest.raises(ConflictError) as info:
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.update("login", {**PAYLOAD, "title": "Nope"}, expected_source_hash="stale")
    assert (info.value.ref, info.value.expected, info.value.actual) == ("login", "stale", actual)
    assert _title(api_store, "login") == "Broken login"


def test_the_source_hash_guard_is_checked_before_the_payload_guard(api_store):
    with pytest.raises(ConflictError) as info:
        api.apply_batch(api_store.store, [{"id": "login", "action": "update", "payload": PAYLOAD, "expected_source_hash": "stale", "expected": {"title": "also stale"}}], api_store.pythonpath)
    assert info.value.expected == "stale"
    with pytest.raises(ConflictError) as info:
        api.apply_batch(api_store.store, [{"id": "login", "action": "update", "payload": PAYLOAD, "expected": {"title": "also stale"}}], api_store.pythonpath)
    assert (info.value.expected, info.value.actual) == ({"title": "also stale"}, PAYLOAD)


def test_a_failure_during_the_rollback_is_raised_with_the_unrestored_paths(api_store, monkeypatch):
    real = rollback._restore

    def refusing(path: Path, data: bytes | None) -> None:
        if path.name == "login.md":
            raise OSError("disk says no")
        real(path, data)

    monkeypatch.setattr(rollback, "_restore", refusing)
    with pytest.raises(RollbackError) as info:
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.update("login", {**PAYLOAD, "title": "Half"})
            raise RuntimeError("original failure")
    assert info.value.unrestored == ["login.md"]
    assert isinstance(info.value.__cause__, RuntimeError) and str(info.value.__cause__) == "original failure"


def test_apply_batch_refuses_everything_when_one_change_is_invalid_and_writes_nothing(api_store):
    before = _files(api_store.root)
    changes = [{"id": "fine", "action": "create", "model": "TicketDoc", "payload": PAYLOAD}, {"id": "login", "action": "update", "payload": {"title": 7}, "expected": PAYLOAD}]
    with pytest.raises(SLDBValidationError, match="login"):
        api.apply_batch(api_store.store, changes, api_store.pythonpath)
    assert _files(api_store.root) == before


def test_apply_batch_orders_creates_updates_moves_untracks_and_deletes(api_store):
    api_store.write_document("loose", PAYLOAD)
    api.track_document_file(api_store.store, "TicketDoc", "loose.md", pythonpath=api_store.pythonpath)
    report = api.apply_batch(api_store.store, [
        {"id": "loose", "action": "delete", "expected": PAYLOAD},
        {"id": "login", "action": "move", "path": "moved/login.md", "expected_source_hash": _entry(api_store, "login").source_hash},
        {"id": "fresh", "action": "create", "model": "TicketDoc", "payload": {**PAYLOAD, "title": "Fresh"}},
        {"id": "untracked", "action": "track", "model": "TicketDoc", "path": str(api_store.write_document("untracked", PAYLOAD).relative_to(api_store.root))},
    ], api_store.pythonpath)
    assert report.saved == ["fresh", "untracked", "login", "loose"]
    assert (api_store.root / "TicketDoc" / "fresh.md").exists() is False and (api_store.root / "fresh.md").exists()
    assert _entry(api_store, "login").path == "moved/login.md" and not (api_store.root / "loose.md").exists()


def test_create_and_move_refuse_a_path_outside_the_project_root(api_store, tmp_path):
    with pytest.raises(SLDBStoreError, match="outside"):
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.create("TicketDoc", "escaped", PAYLOAD, tmp_path / "escaped.md")
    with pytest.raises(SLDBStoreError, match="outside"):
        api.move_document(api_store.store, "login", tmp_path / "login.md", api_store.pythonpath)


@pytest.fixture
def linked_store(tmp_path: Path):
    """`n1` (Note) referenced by `l1` (Linked.about = Note:n1)."""
    (tmp_path / f"{REF_MODULE}.py").write_text(REF_MODELS, encoding="utf-8")
    root = tmp_path / "world"
    root.mkdir()
    store = api.init_store(root).store_path
    for model in ("Note", "Linked"):
        api.add_model(store, f"{REF_MODULE}:{model}", str(tmp_path))
    api.create_document(store, "Note", "n1.md", {"title": "n1"}, "n1", str(tmp_path))
    api.create_document(store, "Linked", "l1.md", {"title": "l1", "about": "Note:n1"}, "l1", str(tmp_path))
    yield root, store, str(tmp_path)
    sys.modules.pop(REF_MODULE, None)


def test_move_keeps_the_name_and_the_incoming_edges_keep_resolving(linked_store):
    root, store, py = linked_store
    incoming = [e.model_dump() for e in api.edges_to(store, "Note:n1", "references")]
    assert incoming
    with api.transaction(store, py) as tx:
        moved = tx.move("n1", "notes/n1.md")
    assert (moved.model, moved.name, moved.path) == ("Note", "n1", (root / "notes" / "n1.md").resolve())
    assert not (root / "n1.md").exists()
    assert [e.model_dump() for e in api.edges_to(store, "Note:n1", "references")] == incoming
    assert api.check_store(store, root, py)["ok"]


def test_a_failed_move_puts_the_file_and_the_entry_back(linked_store):
    root, store, py = linked_store
    before = _files(root)
    with pytest.raises(RuntimeError):
        with api.transaction(store, py) as tx:
            tx.move("n1", "notes/n1.md")
            raise RuntimeError("after the move")
    assert _files(root) == before
    assert api.check_store(store, root, py)["ok"]


def _state(api_store) -> tuple[dict, dict, dict]:
    """Payloads, index entries and Markdown bytes of every tracked document, the provenance
    aside: the undo is stamped like any write (its `sldb:` front matter and the source hash)."""
    docs = api.load_runtime_documents(api_store.store, api_store.pythonpath)
    entries = {d.name: _entry(api_store, d.name).model_dump(exclude={"source_hash", "provenance"}) for d in docs}
    unstamped = {d.name: PROVENANCE.sub(b"", (api_store.root / entries[d.name]["path"]).read_bytes()) for d in docs}
    return {d.name: d.payload for d in docs}, entries, unstamped


def _create_update_delete(api_store):
    api_store.write_document("loose", PAYLOAD)
    api.track_document_file(api_store.store, "TicketDoc", "loose.md", pythonpath=api_store.pythonpath)
    before = _state(api_store)
    report = api.apply_batch(api_store.store, [
        {"id": "fresh", "action": "create", "model": "TicketDoc", "payload": {**PAYLOAD, "title": "Fresh"}},
        {"id": "login", "action": "update", "payload": {**PAYLOAD, "title": "Changed"}},
        {"id": "loose", "action": "delete"},
    ], api_store.pythonpath)
    return before, report


def test_applying_the_inverse_puts_payloads_entries_and_bytes_back(api_store):
    before, report = _create_update_delete(api_store)
    assert {c["id"]: c["action"] for c in report.inverse} == {"fresh": "delete", "login": "update", "loose": "create"}
    api.apply_batch(api_store.store, report.inverse, api_store.pythonpath)
    assert _state(api_store) == before
    assert not (api_store.root / "fresh.md").exists()
    assert api.check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]


def test_the_inverse_after_another_write_is_a_conflict_and_writes_nothing(api_store):
    _, report = _create_update_delete(api_store)
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "Someone else"}, api_store.pythonpath)
    touched = _files(api_store.root)
    with pytest.raises(ConflictError) as info:
        api.apply_batch(api_store.store, report.inverse, api_store.pythonpath)
    assert info.value.ref == "login"
    assert _files(api_store.root) == touched

FILE:instruccion
Cold-bundle de la tarea task-la-escritura-por-campos-save-document-payload-y-el-update-de-apply-batch-falla-nombrando-el-contenid: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_structural_noise.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_transaction.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_write_paths_validate.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

