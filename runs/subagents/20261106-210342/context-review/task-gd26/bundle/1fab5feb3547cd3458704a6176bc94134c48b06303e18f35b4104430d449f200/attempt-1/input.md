FILE:desk/tasks/task-gd26-scaffold-de-store-desde-carpetas-y-semillas-declaradas.md
---
id: task-gd26-scaffold-de-store-desde-carpetas-y-semillas-declaradas
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
- src/sldb/api/stores/store_declaration.py
- src/sldb/api/stores/scaffold_store.py
- src/sldb/api/stores/build_store.py
- src/sldb/api/__init__.py
- src/sldb/cli/commands/stores_build.py
- src/sldb/cli/parsers/stores.py
- src/sldb/cli/commands/stores.py
- tests/api/test_scaffold_store.py
- tests/store/test_stores_build.py
- tests/api/test_api_stores.py
- docs/architecture/store-declaration.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/generalizar-desde-deskops/dag.yaml
---

# GD26: Scaffold de store desde carpetas y semillas declaradas

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GD26 del plan desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PG2. Depende de: nada. Gates requeridos: ninguno.

## Goal

_Describe the concrete result this task must produce._

StoreDeclaration gana folders y seeds (modos if_missing y managed; fuentes text, file con pkg: y document con track); sldb.api.scaffold_store(store, *, declaration=None, apply=False, template_root) idempotente con reporte created/rewritten/present/conflicts; sldb.api.build_store ejecuta apply_declaration y luego scaffold_store; CLI sldb stores scaffold [--apply] y stores build con sección scaffold; doc en docs/architecture/store-declaration.md.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/stores/store_declaration.py, scaffold_store.py y build_store.py (nuevos), src/sldb/api/__init__.py, src/sldb/cli/commands/stores_build.py, src/sldb/cli/parsers/stores.py, src/sldb/cli/commands/stores.py, tests, docs/architecture/store-declaration.md, CHANGELOG.md. Fuera: las semillas de deskops (las declara CC36), cambiar la forma de store.yaml existente, nombres del caso deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3, GD26). SCOPE: StoreDeclaration (api/stores/store_declaration.py:20) gana dos claves (GP5): folders (lista de rutas relativas a la raíz) y seeds (lista de Seed = {path, mode: if_missing | managed, y una fuente: text (literal), file (ruta a una plantilla relativa a store.yaml o a un paquete Python como pkg:modulo/ruta) o document {model, name, payload} renderizado con el renderizador del modelo (api/documents/document_render.py:31 render_model_template); track: bool (default true si es document)}). Función sldb.api.scaffold_store(store, *, declaration=None, apply=False) → ScaffoldReport (declaration = un StoreDeclaration parcial con folders y seeds pasado en proceso por el consumidor; si se pasa, se usa en lugar de las claves de store.yaml y no se escribe en store.yaml: así un consumidor declara sus semillas en su paquete sin cambiar el formato de su store; las rutas file: relativas se resuelven contra el directorio que el consumidor indique con template_root) {created, rewritten, present, conflicts}: if_missing nunca sobrescribe (present si existe); managed compara bytes y, si difieren, lo reporta como rewritten (con apply) o como pendiente (sin apply); un document con track se trackea con el modelo y nombre declarados; idempotente: una segunda corrida con apply no cambia nada y todo sale present. Escribe dentro de sldb.api.transaction si GD24 ya cerró; si no, por archivo con rollback_on_error. build_store pasa de cli/commands/stores_build.py:35 a sldb.api.build_store(store, *, apply) y la CLI lo llama; build_store ejecuta apply_declaration (links, models, predicates, includes) y después scaffold_store, en ese orden, en un solo reporte. CLI: sldb stores scaffold [--apply] con envelope; sldb stores build incluye el reporte de scaffold. Doc en docs/architecture/store-declaration.md (sección folders y seeds).

ACCEPTANCE: En un store temporal: una declaración con dos carpetas, una semilla text if_missing, una file managed y una document if_missing con track: sin --apply el reporte lista todo como created pendiente y no escribe nada (hashes iguales); con --apply se crean y el documento queda trackeado con su nombre; una segunda corrida da todo present; editar el archivo managed hace que la siguiente corrida lo reporte rewritten y lo restaure; editar el if_missing no lo toca; una plantilla pkg: de un paquete de prueba se resuelve; la misma declaración pasada como declaration= produce el mismo resultado y store.yaml queda igual (hash); una clave desconocida en seeds falla al cargar nombrando la clave; sldb stores build sin cambios en la declaración produce el mismo reporte de links/models/includes que antes (golden existente) más la sección scaffold vacía; CHANGELOG; doc; nota de cierre a deskops.

OUTPUT_SCOPE: src/sldb/api/stores/store_declaration.py, src/sldb/api/stores/scaffold_store.py, src/sldb/api/stores/build_store.py, src/sldb/api/__init__.py, src/sldb/cli/commands/stores_build.py, src/sldb/cli/parsers/stores*.py, src/sldb/cli/commands/stores*.py, tests/, docs/architecture/store-declaration.md, CHANGELOG.md

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de sldb, con `--task-type` y `files` completos; antes, preflight TaskDoc-only y cold-bundle (ritual-context-review). Las revisiones en frío las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`; nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de sldb aparte del de grafo-operable (otras áreas: edges, documents, serve, stores). Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor sobre el resultado integrado. Un nodo no cierra con tests rojos ni saltados.
3. Toda capacidad nueva entra con: función pública en `sldb.api` (reexportada en `sldb/api/__init__.py`), comando CLI con envelope JSON, ruta de `sldb serve` cuando el consumidor la necesita, pruebas, entrada en `CHANGELOG.md` y doc en `docs/architecture/`. Nada queda solo en el código.
4. Genericidad: ningún nombre del caso deskops (TaskDoc, Board, ritual, pill, atom, closeout) aparece en `src/sldb/` ni en sus tests, salvo como dato en fixtures. Un grep lo comprueba en la aceptación de cada nodo.
5. Compatibilidad: ninguna salida existente de la CLI ni de `sldb serve` cambia (goldens existentes verdes); lo nuevo es aditivo. Si un nodo necesita cambiar un contrato existente (p. ej. `/save` pasa a ser atómico), lo nombra en su aceptación y en el CHANGELOG.
6. Ante un contrato ausente de un nodo GO no cerrado, el nodo registra la hipótesis en su TaskDoc, implementa la parte que no depende de él y no inventa la API de grafo-operable.
7. Cada nodo, al cerrar, manda nota a deskops (`deskops message send --to deskops --kind suggestion`) con la función, el comando y la ruta nuevos y el código de deskops que quedan sin motivo (tabla de arriba); así se satisface el gate `G_GDxx` del plan de deskops.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-06):
q1 (GD24): GD24 se promueve a la vez y no hay arista entre ambos; si GD24 no cerró al ejecutar GD26, se escribe por archivo con rollback_on_error (src/sldb/store/io/rollback.py) como dice el scope; no se espera a GD24.
q2 (doc): docs/architecture/store-declaration.md no existe hoy; se crea con la sección folders y seeds.
q3 (base): commit base 6b80df36 de main de sldb.

PRECISIONES DEL PREFLIGHT (review-task-gd26-preflight-1, 2026-11-06):
q4 (firma): scaffold_store(store, *, declaration=None, apply=False, template_root=None) -> ScaffoldReport; template_root=None = el directorio de store.yaml.
q5 (folders): cada carpeta se crea con sus padres (mkdir parents); si ya existe como directorio va a present; si existe como archivo va a conflicts y no se toca; sin apply, las faltantes se reportan en created como pendientes. folders no tiene modo.
q6 (GD24): decide el ejecutor al implementar mirando main: si sldb.api.transaction existe (GD24 cerrado), se usa; si no, rollback_on_error (store/io/rollback.py:11) por archivo. Sin detección en tiempo de ejecución.
q7 (track): un seed document con track se trackea con track_document_file(store, model, path, name) (api/documents/track_document_file.py:20).
q8 (reporte vacío): la sección scaffold de stores build es siempre el objeto {created: [], rewritten: [], present: [], conflicts: []} (listas de rutas relativas); vacía = las cuatro listas vacías.
q9 (pkg:): pkg:modulo/ruta se resuelve con importlib.resources.files("modulo").joinpath("ruta") sobre el paquete importable (instalado o en pythonpath); no se resuelve relativo a nada más.
q10 (clave desconocida): Seed y la parte nueva de StoreDeclaration usan model_config = ConfigDict(extra="forbid"); load_declaration levanta pydantic.ValidationError, cuyo mensaje nombra la clave (loc). Las claves existentes de StoreDeclaration no cambian de comportamiento.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_scaffold_store.py
- TMPDIR=/dev/shm pytest -q tests/store/test_stores_build.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_stores.py
- grep -rniE 'taskdoc|board|ritual|pill|atom|closeout' src/sldb/ sin nombres nuevos contra el commit base 6b80df36 (salida de ambos en esta sección)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- sldb stores scaffold --format json y sldb stores scaffold --apply sobre el store temporal del test; segunda corrida todo present
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, límite de clases por archivo; cuenta como test de los archivos tocados aunque output_scope no lo nombre)
- git fetch y rebase sobre origin/main antes de integrar (main trae SV01, SV02, SV04 en 6ba8bb20 y GO04 en d7eefdeb); en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio

## Done When

_Name the observable condition that makes the task complete._

En un store temporal: una declaración con dos carpetas, una semilla text if_missing, una file managed y una document if_missing con track: sin --apply el reporte lista todo como created pendiente y no escribe nada (hashes iguales); con --apply se crean y el documento queda trackeado con su nombre; una segunda corrida da todo present; editar el archivo managed hace que la siguiente corrida lo reporte rewritten y lo restaure; editar el if_missing no lo toca; una plantilla pkg: de un paquete de prueba se resuelve; la misma declaración pasada como declaration= produce el mismo resultado y store.yaml queda igual (hash); una clave desconocida en seeds falla al cargar nombrando la clave; sldb stores build sin cambios en la declaración produce el mismo reporte de links/models/includes que antes (golden existente) más la sección scaffold vacía; CHANGELOG; doc; nota de cierre a deskops.

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

FILE:src/sldb/api/stores/store_declaration.py
"""`.sldb/store.yaml`: what a store declares, the part of it that is source and lives in git.

Everything else in `.sldb/core/` (the store index, the model and document indexes) is derived
from this file, the tracked Markdown and the models' Python classes, and `sldb stores build`
regenerates it (docs/architecture/derived-store-boundary.md). `.sldb/` is versioned whole so
that git holds the tree's past; what is only a cache lives in `.sldb_cache/`, ignored.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

DECLARATION_FILE = "store.yaml"


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


def declaration_path(store_path: Path) -> Path:
    """Where a store's declaration lives."""
    return Path(store_path) / DECLARATION_FILE


def load_declaration(store_path: Path) -> StoreDeclaration:
    """The store's declaration; a missing file is an error, not an empty store."""
    path = declaration_path(store_path)
    if not path.is_file():
        raise FileNotFoundError(f"{path} does not exist: run `sldb stores declare --write` first")
    definition = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    _validate_graph_backend(definition)
    return StoreDeclaration.model_validate(definition)


def _validate_graph_backend(definition: dict[str, Any]) -> None:
    """Reject a backend this phase cannot run, naming the only admitted one."""
    backend = definition.get("graph_backend", "networkx")
    if backend != "networkx":
        raise ValueError(f'graph_backend {backend} no admitido; admitidos: ["networkx"]')


def declared_graph_backend(store_path: str | Path | None = None) -> str:
    """The store's `graph_backend`, or `networkx` when it has no declaration or no key."""
    if store_path is None:
        return "networkx"
    path = Path(store_path)
    if path.name != ".sldb" and (path / ".sldb").is_dir():
        path = path / ".sldb"
    if not declaration_path(path).is_file():
        return "networkx"
    return load_declaration(path).graph_backend


def save_declaration(store_path: Path, declaration: StoreDeclaration) -> Path:
    """Write the declaration in a stable, reviewable order."""
    path = declaration_path(store_path)
    path.write_text(yaml.safe_dump(declaration.model_dump(), sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    return path


def declared_store(store_arg: str | None) -> tuple[Path, Path]:
    """`(store, project root)` of the store a build targets: `--store` (a `.sldb` directory or
    its project) or the nearest ancestor holding `.sldb/store.yaml`. A store that is only
    declared has no index yet, so the usual discovery, which looks for one, cannot find it."""
    if store_arg:
        store = Path(store_arg).resolve()
        store = store if store.name == ".sldb" else store / ".sldb"
        return store, store.parent
    for folder in (Path.cwd().resolve(), *Path.cwd().resolve().parents):
        if declaration_path(folder / ".sldb").is_file():
            return folder / ".sldb", folder
    raise FileNotFoundError(f"No .sldb/{DECLARATION_FILE} here or above {Path.cwd()}")

FILE:src/sldb/api/__init__.py
"""sldb's library API: the store, model and document operations the CLI performs, as functions.

Consumers (pron, deskops, graph_ui...) call these instead of instantiating `sldb.cli` command
classes with fake argparse namespaces. Each operation that names a store opens it the way a
CLI command does (`open_store`), returns a pydantic model instead of printing, and raises
`sldb.core.exceptions` errors instead of exiting. Layering: `sldb.cli` -> `sldb.api` ->
`sldb.store` / `sldb.runtime` / `sldb.core`; nothing here imports `sldb.cli`.
"""

from __future__ import annotations

from sldb.api.anchors.check_doc_anchors import check_doc_anchors
from sldb.api.documents.apply_batch import apply_batch
from sldb.api.documents.batch_report import BatchReport
from sldb.api.documents.create_document import create_document
from sldb.api.documents.delete_document import delete_document
from sldb.api.documents.move_document import move_document
from sldb.api.documents.transaction import RollbackError, Transaction, transaction
from sldb.api.documents import document_ast, build_document_ir_json, leaf_paths, runtime_document, extract_document_payload, render_document_markdown, render_model_template
from sldb.api.documents.runtime_documents import load_runtime_documents
from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.document_serialization import serialize_document
from sldb.api.documents.payload_path_reading import deep_get, ensure_list
from sldb.api.documents.payload_path_writing import deep_delete, deep_set
from sldb.api.documents.payload_save import save_document_payload
from sldb.api.documents.track_document_file import track_document_file
from sldb.api.documents.untrack_document import untrack_document
from sldb.api.edges.check_edges import check_edges
from sldb.api.edges.edge_check_report import EdgeCheckReport
from sldb.api.edges.edge_reading import edge_node, edge_nodes_of_type, edges_from, edges_to, load_edge_index
from sldb.api.edges.apply_effects import apply_effects
from sldb.api.edges.edge_effects import effects_of
from sldb.api.edges.edges_holding import edges_holding
from sldb.api.model_registry.remove_model import remove_model
from sldb.api.model_registry.inherit_model import inherit_model
from sldb.models.structured_doc import StructuredNLDoc
from sldb.models.notation_models import (
    GlyphDoc,
    LinkDoc,
    NotationDoc,
    PaletteDoc,
    SpecDoc,
    SpecNodeDoc,
    ViewDoc,
)
from sldb.api.notations import (
    evaluate_projection_view,
    list_projection_views,
    resolve_documents,
    resolve_view,
    save_projection_view,
    sync_notation,
    sync_palette,
)
from sldb.api.edges.unresolved_references import unresolved_references
from sldb.store.edge_index.unresolved_reference import UnresolvedReference
from sldb.api.edges.edge_serialization import serialize_edge_node_record, serialize_edge_node_records, serialize_edge_record, serialize_edge_records
from sldb.api.edges.init_relations import init_relations
from sldb.api.edges.rebuild_edges import rebuild_edges
from sldb.api.edges.relations_init_report import RelationsInitReport
from sldb.api.journal import journal, verify_journal
from sldb.api.model_drafts.draft_document_check import DraftDocumentCheck
from sldb.api.model_drafts.draft_validation import promote_model_draft, validate_model_draft
from sldb.api.model_drafts.draft_validation_report import DraftValidationReport
from sldb.api.model_drafts.field_drafts import add_model_field, remove_model_field
from sldb.api.model_drafts.model_draft import ModelDraft
from sldb.api.model_drafts.model_source import ModelSource
from sldb.api.model_drafts.source_location import locate_model_source
from sldb.api.model_drafts.template_drafts import edit_model_template
from sldb.api.model_drafts.metadata_drafts import edit_model_metadata
from sldb.api.model_create.create_model import create_model
from sldb.api.model_create.field_decl import FieldDecl
from sldb.api.model_create.model_check import ModelCheck
from sldb.api.model_registry.add_model import add_model
from sldb.api.search import search
from sldb.api.rules import refuse_unknown_family, rules_check, rules_explain
from sldb.api.where import where_matches
from sldb.store.query_engine.where_parse import WherePredicateError
from sldb.core.exceptions import ConflictError
from sldb.api.model_registry.describe_model import describe_model
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_description import ModelDescription
from sldb.api.model_registry.model_document_summary import ModelDocumentSummary
from sldb.api.model_registry.model_field_summary import ModelFieldSummary
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.model_registry.registered_model import RegisteredModel
from sldb.api.model_registry.reindex_model import reindex_model
from sldb.api.schema.describe_field import describe_field, describe_model_fields
from sldb.api.schema.field_description import FieldDescription
from sldb.api.segments import CompositionPiece, CompositionSpec, DocumentSegments, FieldSegment, LiteralSegment, Segment, SourceRef, build_document_segments
from sldb.api.stores.doc_ref import split_doc_ref
from sldb.api.stores.doc_ref_status import DocRefStatus
from sldb.api.stores.doc_status import doc_exists, doc_status
from sldb.api.stores.tracked_documents import tracked_documents
from sldb.api.stores.ambiguous_document import AmbiguousDocument
from sldb.api.stores.resolve_indexed_document import indexed_model_bases, resolve_indexed_document
from sldb.api.stores.init_store import init_store
from sldb.api.stores.link_store import link_store
from sldb.api.stores.unlink_store import unlink_store
from sldb.api.model_registry.registration_query import is_model_registered, registered_models
from sldb.api.stores.linked_store import LinkedStore
from sldb.api.stores.migrate_hash_names import migrate_store_hash_names
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_check import check_store
from sldb.api.stores.store_fingerprint import store_fingerprint
from sldb.api.stores.store_links import store_links
from sldb.api.stores.store_location import StoreLocation
from sldb.api.stores.store_update_report import StoreUpdateReport
from sldb.api.stores.update_store_indexes import update_store_indexes
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.edge_rebuild_report import EdgeRebuildReport
from sldb.store.edge_index.node_ids import anchor_node_id, bare, doc_node_id, field_node_id, kind, model_node_id, relation_type_node_id, section_node_id, tag_node_id
from sldb.store.journal import JournalEntry, JournalVerifyReport
from sldb.store.models.edge_node_record import EdgeNodeRecord
from sldb.store.models.edge_record import EdgeRecord
from sldb.store.models.document_hashes import DocumentHashes
from sldb.store.models.store_fingerprint import StoreFingerprint
from sldb.api.corpus import (
    Corpus,
    CorpusEntry,
    FieldEntry,
    FieldHit,
    FieldProjection,
    Hit,
    IndexProjection,
    field_id,
    split_field_id,
)

__all__ = [
    "Corpus", "CorpusEntry", "FieldEntry", "FieldHit", "FieldProjection",
    "Hit", "IndexProjection", "field_id", "split_field_id",
    "CompositionPiece", "CompositionSpec", "DocumentSegments", "FieldSegment",
    "LiteralSegment", "Segment", "SourceRef", "build_document_segments",
    "DocumentHashes", "DocumentReference", "DraftDocumentCheck", "DraftValidationReport",
    "EdgeCheckReport", "EdgeIndex", "EdgeNodeRecord", "EdgeRebuildReport",
    "EdgeRecord", "FieldDecl", "FieldDescription", "JournalEntry",
    "JournalVerifyReport", "LinkedStore", "ModelCheck", "ModelDescription",
    "ModelDocumentSummary", "ModelDraft", "ModelFieldSummary", "ModelRegistration",
    "ModelSource", "RegisteredModel", "RelationsInitReport", "StoreFingerprint",
    "StoreLocation", "StoreUpdateReport", "add_model", "add_model_field",
    "create_model", "anchor_node_id", "bare", "check_doc_anchors", "check_edges", "check_store",
    "store_fingerprint", "create_document", "deep_delete", "deep_get", "deep_set",
    "delete_document", "describe_field", "describe_model", "describe_model_fields",
    "doc_node_id", "document_ast", "edge_node", "edge_nodes_of_type", "edges_from",
    "edges_to", "edit_model_metadata", "edit_model_template", "ensure_list", "extract_document_payload",
    "field_node_id", "init_relations", "init_store", "journal", "kind", "link_store", "unlink_store",
    "load_edge_index", "leaf_paths", "load_runtime_documents", "migrate_store_hash_names",
    "load_registered_model", "locate_model_source", "model_node_id", "open_store",
    "promote_model_draft", "rebuild_edges", "reindex_model", "relation_type_node_id",
    "remove_model_field", "render_document_markdown", "render_model_template",
    "resolve_model_ref", "runtime_document", "save_document_payload", "search",
    "section_node_id", "serialize_document", "serialize_edge_node_records",
    "serialize_edge_records", "tag_node_id", "track_document_file", "untrack_document",
    "update_store_indexes", "validate_model_draft", "verify_journal",
    "DocRefStatus", "doc_exists", "doc_status", "tracked_documents", "AmbiguousDocument", "indexed_model_bases", "resolve_indexed_document", "split_doc_ref", "store_links",
    "WherePredicateError", "apply_effects", "edges_holding", "effects_of", "refuse_unknown_family", "rules_check", "rules_explain", "remove_model", "where_matches", "inherit_model", "is_model_registered", "registered_models",
    "StructuredNLDoc", "UnresolvedReference", "unresolved_references",
    "BatchReport", "ConflictError", "RollbackError", "Transaction", "apply_batch", "move_document", "transaction",
    "GlyphDoc", "LinkDoc", "NotationDoc", "PaletteDoc", "SpecDoc", "SpecNodeDoc", "ViewDoc",
    "resolve_view", "resolve_documents", "evaluate_projection_view", "list_projection_views", "save_projection_view", "sync_notation", "sync_palette",
]

FILE:src/sldb/cli/commands/stores_build.py
"""`sldb stores declare` and `sldb stores build`: the store rebuilt from what it declares.

`declare` writes `.sldb/store.yaml` from the current index (once, to adopt the layout). `build`
makes the store match the declaration: links, models, predicates, generators (such as
`selfdoc python-sync`), the tracked files, then the indexes. `build --check` does it in a
scratch copy of the sources and fails when that copy is not a valid store, or when what it
tracks differs from the local store.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.stores.apply_declaration import apply_includes, apply_links, apply_models, apply_predicates, missing_declared, undeclared
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import declared_store, load_declaration, save_declaration
from sldb.api.stores.store_skeleton import write_empty_store
from sldb.api.stores.update_store_indexes import update_store_indexes
from sldb.cli.output_format import emit
from sldb.cli.store_context import get_store_context
from sldb.store.layout import store_exists


def declare_command(args: Any) -> int:
    store, root = get_store_context(args.store, mode="readonly")
    declaration = declare_store(store, root)
    if args.write:
        print(f"Wrote {save_declaration(store, declaration)}")
        return 0
    emit(declaration.model_dump(), "yaml", "")
    return 0


def build_store(store: Path, root: Path) -> dict[str, Any]:
    """Apply the declaration to the store at `store` (created when absent) and report it."""
    declaration = load_declaration(store)
    if not store_exists(store):
        write_empty_store(store)
    report = {"links": apply_links(store, root, declaration), "models": apply_models(store, root, declaration)}
    report["predicates_changed"] = apply_predicates(store, declaration)
    report.update(_track(store, root, declaration))
    update_store_indexes(store, str(root))
    report["undeclared"] = undeclared(store, root, declaration)
    report["missing"] = missing_declared(root, declaration)
    return report


def _track(store: Path, root: Path, declaration) -> dict[str, list[str]]:
    """Sources first (generators read them), then what the generators wrote."""
    from sldb.cli.commands.stores_build_generators import run_generators

    tracked = apply_includes(store, root, declaration)
    generated = run_generators(store, root, declaration)
    return {"tracked": tracked + apply_includes(store, root, declaration), "generated": generated}


def build_command(args: Any) -> int:
    if args.check:
        from sldb.cli.commands.stores_build_check import check_command

        return check_command(args)
    store, root = declared_store(args.store)
    report = build_store(store, root)
    emit(report, args.format, _summary(report))
    return 1 if report["undeclared"] or report["missing"] else 0


def _summary(report: dict[str, Any]) -> str:
    counts = ", ".join(f"{k}: {len(v)}" for k, v in report.items() if isinstance(v, list))
    flagged = "".join(f"\n{key}: " + ", ".join(report[key]) for key in ("undeclared", "missing") if report[key])
    return f"built: {counts}{flagged}"

FILE:src/sldb/cli/parsers/stores.py
from __future__ import annotations
import argparse

def add_stores_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("stores", help="Store lifecycle and federation.")
    sub = p.add_subparsers(dest="stores_command", required=True)
    _init(sub); _add(sub); _remove(sub); _check(sub); _update(sub); _reconcile(sub)
    _semantic_map(sub); _semantic_export(sub); _list(sub); _migrate_hashes(sub)
    _migrate_layout(sub); _declare(sub); _build(sub)

def _init(s):
    i = s.add_parser("init", help="Init .sldb store.")
    i.add_argument("--path", default=".")
    i.add_argument("--force", action="store_true")

def _add(s):
    a = s.add_parser("add", help="Link federated store.")
    a.add_argument("path", help="Store path")
    a.add_argument("--name", help="Store name")
    a.add_argument("--store", help="Local store path")
    a.add_argument("--replace", action="store_true", help="Point a link already recorded under that name here")

def _remove(s):
    r = s.add_parser("remove", help="Remove a store link; refused while a model here is inherited from it.")
    r.add_argument("name", help="Link name")
    r.add_argument("--store", help="Local store path")

def _check(s):
    c = s.add_parser("check", help="Integrity check: reports each finding and its category.")
    c.add_argument("--store", help="Store path")
    c.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    c.add_argument("--quiet", action="store_true", help="Only the PASS/FAIL line, without per-document findings")
    c.add_argument("--apply", action="store_true", help="Run what the store's policy answers to each finding: `reindex` and `hook: <command>`")
    c.add_argument("--pythonpath", help="Project path")

def _update(s):
    u = s.add_parser("update", help="Recompute store hashes.")
    u.add_argument("--wait", action="store_true", help="Wait for store lock if busy")
    u.add_argument("--verbose", action="store_true", help="Print individual skip details")
    u.add_argument("--prune-missing", action="store_true", help="Untrack documents whose file no longer exists (reports which)")
    u.add_argument("--store", help="Store path")
    u.add_argument("--pythonpath", help="Project path")

def _migrate_hashes(s):
    m = s.add_parser("migrate-hashes", help="Rename hash_a..hash_d to store/model/source/content.")
    m.add_argument("--store", help="Store path")

def _migrate_layout(s):
    m = s.add_parser("migrate-layout", help="Move the cache from .sldb/runtime/ to .sldb_cache/ (sibling of .sldb/), drop the journal and fix the root .gitignore.")
    m.add_argument("--store", help="Store path")
    m.add_argument("--force", action="store_true", help="Replace an existing, non-empty .sldb_cache/")

def _reconcile(s):
    r = s.add_parser("reconcile", help="Explicitly reconcile a catalog against a subtree.")
    r.add_argument("--path", default=".", help="Subtree to discover")
    r.add_argument("--catalog", help="Catalog store path; defaults to ~/.sldb")
    r.add_argument("--apply", action="store_true", help="Replace catalog entries with discovered stores")
    r.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _semantic_map(s):
    m = s.add_parser("semantic-map", help="Map equivalent semantic concepts.")
    m.add_argument("concept_a", help="First concept")
    m.add_argument("concept_b", help="Second concept")
    m.add_argument("--store", help="Store path")

def _semantic_export(s):
    e = s.add_parser("semantic-export", help="Export semantic payloads.")
    e.add_argument("--store", help="Store path")
    e.add_argument("--pythonpath", help="Project path")
    e.add_argument("--format", choices=("sldb",), default="sldb", help="Payload contract: sldb_kgdb_semantic_export v1")
    e.add_argument("--encoding", choices=("json", "yaml"), default="json")
    e.add_argument("--output", "-o", default="-", help="Output path or -")
    e.add_argument("--rebuild", action="store_true", help="Refresh semantic and section indexes")

def _list(s):
    l = s.add_parser("list", help="List federated stores.")
    l.add_argument("--store", help="Store path")
    l.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _declare(s):
    d = s.add_parser("declare", help="Print the store.yaml declaration the current index implies.")
    d.add_argument("--store", help="Store path")
    d.add_argument("--write", action="store_true", help="Write it to .sldb/store.yaml")

def _build(s):
    b = s.add_parser("build", help="Rebuild the store from .sldb/store.yaml, the tracked Markdown and the models.")
    b.add_argument("--store", help="Store path")
    b.add_argument("--check", action="store_true", help="Rebuild a scratch copy of the sources and compare, writing nothing here")
    b.add_argument("--format", choices=("text", "json", "yaml"), default="text")

FILE:src/sldb/cli/commands/stores.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from sldb.api.stores.store_links import store_links
from sldb.cli.commands.store import StoreCLI
from sldb.cli.store_context import get_store_context
from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.utils import write_text
from sldb.store.export import export_semantic_payload
from sldb.store.catalog_reconcile import reconcile_catalog
from sldb.store.resolver import global_store_path


class StoresCLI:
    """Plural store surface for the redesigned CLI."""

    def __init__(self) -> None:
        self._store = StoreCLI()

    def run(self, args: Any) -> int:
        own = {"list": self.list, "semantic-export": self.semantic_export, "reconcile": self.reconcile, "declare": _declare, "build": _build}
        if args.stores_command in own:
            return own[args.stores_command](args)
        args.store_command = args.stores_command
        return self._store.run(args)

    def reconcile(self, args: Any) -> int:
        catalog = Path(args.catalog).resolve() if args.catalog else global_store_path().resolve()
        if not catalog.exists():
            raise ValueError(f"Catalog store does not exist at {catalog}")
        report = reconcile_catalog(catalog, Path(args.path).resolve(), args.apply)
        self._print_reconcile(report, args.format)
        return 0

    def _print_reconcile(self, report: dict, encoding: str) -> None:
        if encoding == "text":
            print(f"discovered={len(report['discovered'])} missing={len(report['missing'])} stale={len(report['stale'])}")
            return
        print(self._format_payload(report, encoding).strip())

    def semantic_export(self, args: Any) -> int:
        sp, root = get_store_context(args.store, mode="readonly")
        payload = export_semantic_payload(
            sp, root, resolve_model_ref, args.pythonpath, rebuild=args.rebuild,
            command=["sldb", "stores", "semantic-export", "--format", args.format],
        )
        content = self._format_payload(payload, args.encoding)
        write_text(args.output, content)
        return 0

    def _format_payload(self, payload: Any, encoding: str) -> str:
        if encoding == "json":
            return json.dumps(payload, indent=2) + "\n"
        return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)

    def list(self, args: Any) -> int:
        sp, _root = get_store_context(args.store, mode="readonly")
        stores = store_links(sp)
        payload = {"store": str(sp), "stores": stores}
        
        if args.format in ("json", "yaml"):
            print(self._format_payload(payload, args.format).strip())
            return 0
        
        return self._print_text_list(sp, stores)

    def _print_text_list(self, sp: Any, stores: list[dict[str, str]]) -> int:
        if not stores:
            print(f"No federated stores linked in {sp}")
            return 0
        print(f"Federated stores in {sp}:")
        for item in stores:
            state = "" if item["status"] == "ok" else f"  [{item['status']}: {item['resolved']}]"
            print(f"- {item['name']} -> {item['path']}{state}")
        return 0


def _declare(args: Any) -> int:
    from sldb.cli.commands.stores_build import declare_command

    return declare_command(args)


def _build(args: Any) -> int:
    from sldb.cli.commands.stores_build import build_command

    return build_command(args)

FILE:tests/store/test_stores_build.py
"""`stores declare` / `stores build`: the derived store comes back from what the store declares."""
from __future__ import annotations

import shutil
import subprocess
import sys

import pytest
import yaml

from sldb.api.stores.apply_declaration import undeclared
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.declared_includes import tracked_rows
from sldb.api.stores.store_declaration import load_declaration, save_declaration
from sldb.cli import main as cli_main
from sldb.cli.commands.stores_build import build_store
from sldb.cli.commands.stores_build_check import check_build
from sldb.store.io import invalidate_index_cache

from .test_semantic_export import _build_tracked_store


@pytest.fixture(autouse=True)
def _forget_the_tmp_model_package():
    yield
    for name in [m for m in sys.modules if m == "tmpdocs" or m.startswith("tmpdocs.")]:
        del sys.modules[name]


def _declared(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)
    save_declaration(store, declare_store(store, root))
    return store, root


def test_the_declaration_names_what_is_tracked_and_nothing_else(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    declaration = load_declaration(store)
    assert [m["name"] for m in declaration.models] == ["TaskDoc"]
    assert declaration.include == [{"model": "TaskDoc", "paths": ["task.md"]}]
    assert undeclared(store, root, declaration) == []


def test_a_store_rebuilt_from_its_declaration_tracks_the_same(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    before = tracked_rows(store, root)
    for derived in (store / "core", store.parent / ".sldb_cache"):
        shutil.rmtree(derived, ignore_errors=True)
    invalidate_index_cache()
    report = build_store(store, root)
    assert report["models"] == ["TaskDoc"] and report["tracked"] == ["task.md"]
    assert tracked_rows(store, root) == before
    assert cli_main(["stores", "check", "--store", str(store), "--quiet"]) == 0


def test_building_a_current_store_changes_nothing(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    report = build_store(store, root)
    assert report["links"] == report["models"] == report["tracked"] == report["undeclared"] == []
    assert report["predicates_changed"] is False


def test_a_tracked_document_no_rule_names_is_reported(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    declaration = load_declaration(store)
    declaration.include = []
    assert undeclared(store, root, declaration) == ["task.md"]


def test_the_check_rebuilds_a_scratch_copy_and_compares(tmp_path, capsys):
    project = tmp_path / "project"
    project.mkdir()
    store, root = _declared(project, capsys)
    (root / ".gitignore").write_text(".sldb_cache/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    report = check_build(store, root, tmp_path / "scratch")
    assert report == {"ok": True, "integrity_exit": 0, "undeclared": [], "missing": [], "differences": [], "errors": [], "alerts": []}
    assert yaml.safe_load((store / "store.yaml").read_text(encoding="utf-8"))["include"]


def test_build_finds_a_store_that_is_only_declared(tmp_path, capsys, monkeypatch):
    """A fresh clone has `.sldb/store.yaml` and no index: the usual discovery, which looks for
    the index, missed it and fell back to the global store."""
    store, root = _declared(tmp_path, capsys)
    for derived in (store / "core", store.parent / ".sldb_cache"):
        shutil.rmtree(derived, ignore_errors=True)
    invalidate_index_cache()
    monkeypatch.chdir(root)
    assert cli_main(["stores", "build"]) == 0
    assert cli_main(["stores", "check", "--store", str(store), "--quiet"]) == 0


def test_a_model_outside_the_project_is_declared_by_reference_only(tmp_path, capsys):
    """deskops and spec2viz register sldb's relation models from the installed package: their
    absolute path would pin the declaration to one checkout."""
    from sldb.api import add_model

    store, root = _build_tracked_store(tmp_path, capsys)
    add_model(store, "sldb.models.relation_doc:RelationDoc")
    models = {m["name"]: m for m in declare_store(store, root).models}
    assert models["RelationDoc"] == {"name": "RelationDoc", "model_ref": "sldb.models.relation_doc:RelationDoc"}
    assert models["TaskDoc"]["path"] == "tmpdocs/models.py"


def test_a_folder_with_one_tracked_file_is_listed_not_globbed(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)
    (root / "boards").mkdir()
    (root / "boards" / "board.md").write_text("# Board\n\n## Overview\n\nBody\n", encoding="utf-8")
    assert cli_main(["docs", "track", str(root / "boards" / "board.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    rules = [r for r in declare_store(store, root).include if "boards/board.md" in str(r)]
    assert rules == [{"model": "TaskDoc", "paths": ["boards/board.md"]}]


def test_untracking_a_document_takes_it_out_of_the_declaration(tmp_path, capsys):
    """deskops retire untracks a note; the declaration kept listing it, so a clean clone
    could not rebuild (CI run 39274588896)."""
    store, root = _declared(tmp_path, capsys)
    assert cli_main(["docs", "untrack", "task", "--store", str(store)]) == 0
    assert load_declaration(store).include == []


def test_tracking_a_document_no_rule_covers_adds_it_to_the_declaration(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    (root / "second.md").write_text("# Beta\n\n## Overview\n\nMore\n", encoding="utf-8")
    assert cli_main(["docs", "track", str(root / "second.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    assert load_declaration(store).include == [{"model": "TaskDoc", "paths": ["task.md", "second.md"]}]
    assert undeclared(store, root, load_declaration(store)) == []


def test_a_declared_file_that_is_gone_is_reported_not_raised(tmp_path, capsys):
    """The clean-clone failure: the declaration names a file git no longer has."""
    project = tmp_path / "project"
    project.mkdir()
    store, root = _declared(project, capsys)
    declaration = load_declaration(store)
    declaration.include[0]["paths"].append("gone.md")
    save_declaration(store, declaration)
    (root / ".gitignore").write_text(".sldb_cache/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    report = check_build(store, root, tmp_path / "scratch")
    assert report["ok"] is False and report["missing"] == ["gone.md"]
    assert report["integrity_exit"] == 0


def test_a_document_outside_the_project_does_not_break_the_declaration(tmp_path, capsys):
    """spec2viz synced a repo spec into a tmp store: create_document raised pathlib's raw
    ValueError from the declaration sync. A file outside the project cannot be declared."""
    from sldb.api import create_document

    (tmp_path / "project").mkdir()
    store, root = _declared(tmp_path / "project", capsys)
    outside = tmp_path / "elsewhere" / "far.md"
    create_document(store, "TaskDoc", outside, {"title": "Far", "body": "Away"}, pythonpath=str(root))
    assert load_declaration(store).include == [{"model": "TaskDoc", "paths": ["task.md"]}]


def test_the_check_reaches_a_link_that_climbs_more_than_one_level(tmp_path, capsys):
    """Governance links deskops through `../../../...`: a copy one level under the scratch
    resolved that link outside it (Permission denied on /tmp's parent, or a symlink left there)."""
    project = tmp_path / "a" / "b" / "project"
    project.mkdir(parents=True)
    store, root = _declared(project, capsys)
    owner = tmp_path / "owner"
    owner.mkdir()
    assert cli_main(["stores", "init", "--path", str(owner)]) == 0
    assert cli_main(["stores", "add", str(owner / ".sldb"), "--name", "owner", "--store", str(store)]) == 0
    save_declaration(store, declare_store(store, root))
    assert load_declaration(store).links[0]["path"] == "../../../owner/.sldb"
    (root / ".gitignore").write_text(".sldb_cache/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    assert check_build(store, root, tmp_path / "scratch")["ok"]
    assert not (tmp_path.parent / "owner").exists()


def test_a_declared_store_that_was_not_built_fails_the_check(tmp_path, capsys):
    """`stores check` passed on it with 0 documents in 0 models (inbox 20261020-024137)."""
    store, root = _declared(tmp_path, capsys)
    for derived in (store / "core", store.parent / ".sldb_cache"):
        shutil.rmtree(derived, ignore_errors=True)
    invalidate_index_cache()
    capsys.readouterr()
    assert cli_main(["stores", "check", "--store", str(store)]) == 1
    assert "error: [store/unbuilt]" in capsys.readouterr().out


def test_a_declared_store_left_empty_by_a_failed_build_fails_the_check(tmp_path, capsys):
    """Governance's case: the build stopped on a broken link after writing an empty index."""
    from sldb.api.stores.store_skeleton import write_empty_store

    store, root = _declared(tmp_path, capsys)
    for derived in (store / "core", store.parent / ".sldb_cache"):
        shutil.rmtree(derived, ignore_errors=True)
    write_empty_store(store)
    invalidate_index_cache()
    capsys.readouterr()
    assert cli_main(["stores", "check", "--store", str(store)]) == 1
    assert "error: [store/unbuilt]" in capsys.readouterr().out


def test_declare_write_keeps_an_authored_glob_and_adds_only_what_is_missing(tmp_path, capsys):
    """`declare --write` turned `glob: notes/*.md` into the list of its matches (93 lines in
    deskops). The glob is the owner's intent: it stays, and a new link is added beside it."""
    store, root = _declared(tmp_path, capsys)
    (root / "notes").mkdir()
    for stem in ("a", "b"):
        (root / "notes" / f"{stem}.md").write_text(f"# {stem}\n\n## Overview\n\nBody\n", encoding="utf-8")
        assert cli_main(["docs", "track", str(root / "notes" / f"{stem}.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    authored = load_declaration(store)
    authored.include = [{"model": "TaskDoc", "glob": "notes/*.md"}, {"model": "TaskDoc", "paths": ["task.md"]}]
    save_declaration(store, authored)
    owner = tmp_path / "owner"
    owner.mkdir()
    assert cli_main(["stores", "init", "--path", str(owner)]) == 0
    assert cli_main(["stores", "add", str(owner / ".sldb"), "--name", "owner", "--store", str(store)]) == 0
    (root / "late.md").write_text("# Late\n\n## Overview\n\nBody\n", encoding="utf-8")
    assert cli_main(["docs", "track", str(root / "late.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    assert cli_main(["stores", "declare", "--store", str(store), "--write"]) == 0
    written = load_declaration(store)
    assert written.include[0] == {"model": "TaskDoc", "glob": "notes/*.md"}
    assert written.include == [{"model": "TaskDoc", "glob": "notes/*.md"}, {"model": "TaskDoc", "paths": ["task.md", "late.md"]}]
    assert [link["name"] for link in written.links] == ["owner"]
    assert undeclared(store, root, written) == []


def test_declare_write_is_stable_on_a_declaration_it_already_completed(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    before = (store / "store.yaml").read_text(encoding="utf-8")
    assert cli_main(["stores", "declare", "--store", str(store), "--write"]) == 0
    assert (store / "store.yaml").read_text(encoding="utf-8") == before


def _model_package(project, package, name="NoteDoc"):
    (project / package).mkdir()
    (project / package / "__init__.py").write_text("", encoding="utf-8")
    (project / package / "models.py").write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        f"class {name}(StructuredNLDoc):\n"
        "    __template__ = '# ⸢rev•title⸥'\n"
        "    title: str = Field(description='Title')\n",
        encoding="utf-8",
    )
    return f"{package}.models:{name}"


def test_registering_a_model_declares_it_so_a_clean_clone_rebuilds(tmp_path, capsys):
    """`deskops desk update --apply` registered the new task types in the index but not in
    store.yaml: the CI rebuild said `Model 'TaskCodeDoc' not registered.` (sldb 8b60e889)."""
    project = tmp_path / "project"
    project.mkdir()
    store, root = _declared(project, capsys)
    ref = _model_package(root, "tmpnotes")
    try:
        assert cli_main(["models", "add", ref, "--store", str(store), "--pythonpath", str(root)]) == 0
        (root / "note.md").write_text("# A note\n", encoding="utf-8")
        assert cli_main(["docs", "track", str(root / "note.md"), "--model", "NoteDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
        declared = {m["name"]: m for m in load_declaration(store).models}
        assert declared["NoteDoc"] == {"name": "NoteDoc", "model_ref": ref, "path": "tmpnotes/models.py"}
        (root / ".gitignore").write_text(".sldb_cache/\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        assert check_build(store, root, tmp_path / "scratch")["ok"] is True
    finally:
        for name in [m for m in sys.modules if m.startswith("tmpnotes")]:
            del sys.modules[name]


def test_inheriting_a_model_declares_it_with_its_origin(tmp_path, capsys):
    (tmp_path / "project").mkdir()
    store, root = _declared(tmp_path / "project", capsys)
    owner = tmp_path / "owner"
    owner.mkdir()
    ref = _model_package(owner, "ownernotes")
    try:
        assert cli_main(["stores", "init", "--path", str(owner)]) == 0
        assert cli_main(["models", "add", ref, "--store", str(owner / ".sldb"), "--pythonpath", str(owner)]) == 0
        assert cli_main(["stores", "add", str(owner / ".sldb"), "--name", "owner", "--store", str(store)]) == 0
        assert cli_main(["models", "inherit", "owner:NoteDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
        declared = {m["name"]: m for m in load_declaration(store).models}
        assert declared["NoteDoc"] == {"name": "NoteDoc", "model_ref": ref, "origin": "owner"}
        before = (store / "store.yaml").read_text(encoding="utf-8")
        assert cli_main(["models", "inherit", "owner:NoteDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
        assert (store / "store.yaml").read_text(encoding="utf-8") == before
    finally:
        for name in [m for m in sys.modules if m.startswith("ownernotes")]:
            del sys.modules[name]


def test_declare_keeps_a_glob_whose_generated_files_are_not_on_disk_yet(tmp_path, capsys):
    """In a clean clone the generator has not run: `declare --write` listed the 2561 symbol
    docs `knowledge/symbols/*.md` already covers. A glob covers by its pattern."""
    store, root = _declared(tmp_path, capsys)
    (root / "gen").mkdir()
    for stem in ("a", "b"):
        (root / "gen" / f"{stem}.md").write_text(f"# {stem}\n\n## Overview\n\nBody\n", encoding="utf-8")
        assert cli_main(["docs", "track", str(root / "gen" / f"{stem}.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    authored = load_declaration(store)
    authored.include = [{"model": "TaskDoc", "glob": "gen/*.md"}, {"model": "TaskDoc", "paths": ["task.md"]}]
    save_declaration(store, authored)
    shutil.rmtree(root / "gen")
    assert cli_main(["stores", "declare", "--store", str(store), "--write"]) == 0
    assert load_declaration(store).include == [{"model": "TaskDoc", "glob": "gen/*.md"}, {"model": "TaskDoc", "paths": ["task.md"]}]

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

FILE:CHANGELOG.md
# Changelog

Version note (2026-09-13, updated 2026-10-18): `pyproject.toml` declares `0.1.12`; it was `0.1.0` while PyPI already had `0.1.1`. Existing entries below are historical development records, not a verified registry release inventory. The product-generation label “v1” is separate from package versioning. No new package version or release is created by this documentation reconciliation.

## 0.1.13 — not released yet (no tag, not on PyPI)

- Anclas a documentos con hash de contrato (GO07, plan grafo-operable; `docs/architecture/anchoring.md` §6):
  - `StructuredNLDoc.__doc_anchors__` (nuevo atributo de clase): campos `str` o `list[str]` cuyos valores son vacíos o `doc:Model:name[@sha256:<64 hex>]`; la forma la valida un validador pydantic del modelo base (`sldb.models.doc_anchor_value`) y un valor malformado es `ValidationError` al escribir. `Provenance.from_` valida igual cada elemento que empieza por `doc:`; los demás (`code:...`) no cambian.
  - Al cargar un modelo (`resolve_model_ref`), `__doc_anchors__` que nombra algo que no es un campo `str`/`list[str]`, o un campo con el sufijo reservado `__anchor_state`, es `SLDBModelError` (`sldb.store.model_contract.doc_anchor_fields`).
  - `save_document_payload` pinnea: un ancla sin `@sha256` (en un campo `__doc_anchors__` o en `from:`) se guarda con el hash de contrato actual del destino (`contract_hash`, GO02 §5); un destino no trackeado deja el valor sin hash.
  - Cada ancla de un campo `__doc_anchors__` es una arista `references` con el nombre del campo hacia `Model:name` (sin el sufijo); `from:` no genera aristas.
  - `compose_edge_index` agrega en memoria `<campo>__anchor_state` (`intact` | `changed` | `lost`; lista alineada para `list[str]`) a la facet `payload`; no se escribe al shard y `EDGE_INDEX_VERSION` sigue en 5. El alias `anchor_state` del lenguaje también se lee al atravesar `^F` (desde el elemento alcanzado, que tiene el campo `F`).
  - `sldb.api.check_doc_anchors(store, pythonpath=None)` (también en `sldb.api.anchors`): alertas `anchors/doc_changed`, `anchors/doc_lost`, `anchors/provenance_changed`, `anchors/provenance_lost`; `sldb anchors check` las agrega (`doc_anchors` en la salida JSON, en `warnings` con `--envelope`), exit 0 si solo hay alertas. No hay `reconnected` para documentos.
- Transiciones como datos de la arista (GO09, plan grafo-operable; `docs/architecture/edges.md`):
  - Convención de `RelationDoc.attributes` para una transición: `sets` (mapa campo → escalar YAML o lista de escalares; `null` asignable) y `terminal` (booleano que sldb solo transporta); ausentes o `null` valen `sets = {}` y `terminal = false`; otras claves se conservan y no entran a los efectos. Es un validador pydantic de `RelationDoc` (`sldb.models.transition_attributes`): escribir un `RelationDoc` con `attributes` no mapa, `sets` no mapa, `terminal` no booleano o un valor de `sets` mapa o lista anidada se rechaza con `ValidationError`.
  - `EdgeRecord.effects` (nuevo, opcional): solo lo llena `edges_holding`, como `{sets, terminal}` con `{campo}` sustituido desde el sujeto (sintaxis de `where_subject`, escalar en su forma YAML: `true`/`false`, números, strings tal cual). Un `{campo}` ausente, `null` o no escalar hace que la arista no se cumpla. Con `effects = None` la clave no aparece en ningún dump: la salida de `edges_from`, `edges_to`, `sldb edges show` y los shards no cambia; `sldb edges show --holds-for` sí la muestra.
  - `sldb.api.effects_of(attributes, subject)` (la resolución) y `sldb.api.apply_effects(subject, effects, model)`: función pura que reemplaza o agrega las claves de primer nivel de `sets` en una copia del sujeto y valida el payload completo contra la clase `model` (levanta su `ValidationError`); nunca persiste.
- Transacción multi-documento y `/save` atómico (GD24, plan generalizar-desde-deskops; `docs/architecture/transactions.md`):
  - `sldb.api.transaction(store, pythonpath=None)` → `Transaction`, anidable (una transacción interna sobre el mismo store se une a la externa; solo la más externa revierte). Escribe en el momento y, ante excepción, restaura bytes, entradas y shards de cada archivo tocado (generaliza `store/io/rollback.py`, que ahora expone `snapshot` y `restore_all`), después invalida las cachés existentes. Operaciones: `create`, `update` (guardas `expected_source_hash` y `expected`), `delete`, `move`, `track`, `untrack`, `write_file` (guarda `expected_sha256`) y `record`.
  - `sldb.api.move_document(store, ref, new_path)`: mueve el archivo y re-trackea con el mismo nombre; las aristas entrantes siguen resolviendo.
  - `sldb.api.apply_batch(store, changes)` → `BatchReport`: prevalida todos los cambios (forma, modelo, round-trip, guardas, destinos) y los aplica en una transacción en orden create/track → update → move → untrack/delete.
  - Excepciones nuevas: `ConflictError(SLDBStoreError)` (`ref`, `expected`, `actual`; en `sldb.core.exceptions` y `sldb.api`) y `RollbackError(SLDBStoreError)` (`unrestored`, encadenada a la excepción original; en `sldb.store.io.rollback`, reexportada por `sldb.api`).
  - **Cambio de contrato (DA2)** en `POST /save`: una falla a mitad de lote ya no deja `completed` parcial; responde 500 `{"ok": false, "error": ..., "rolled_back": true}` con el store como antes. Mismo request, misma respuesta exitosa, mismos 409/422; acepta además `expected_source_hash` y las acciones `move`, `track` y `untrack`. Un `update` con payload inválido responde 422 (antes se perdía en un 500).
  - G4: `tests/api/test_write_paths_validate.py` prueba que `sldb fields update`, `sldb docs update`, `/save`, `apply_batch` y `transaction` rechazan un payload que el `model_validator` del modelo rechaza, sin mover archivo, entrada ni índice.
- Reglas como documentos (GO06, plan grafo-operable; `docs/architecture/rules.md`):
  - `sldb.models.rule_doc.RuleDoc` (exportado en `sldb.models`): `subject` (`model <= X` o una conjunción de nivel superior de esos términos), `where` opcional, `condition`, `severity` (`error` | `alert`), `moment` (`on_write` | `on_transition` | `on_check`) y `message` opcional. Sus validadores pydantic rechazan una `condition` o un `where` que no parsean, un `subject` con otra forma y un valor fuera del vocabulario; escribir una RuleDoc cuyo `subject` nombra un modelo no registrado se rechaza con el error existente `Model 'X' not registered.` (`create_document`, `save_document_payload`, `sldb docs create|update`).
  - `sldb.api.rules` (`rules_check`, `rules_explain`, `explain_exit`, `refuse_unknown_family`; también en `sldb.api`): las reglas son las RuleDoc del store local, leídas de la proyección del índice y evaluadas con `GraphBackend.eval`.
  - CLI `sldb rules check [--subject DOC]`: cada resultado `false` es un `Finding` de core con la severidad de la regla y código `rules/<nombre>`; cada `incomplete`, un alert `rules/<nombre>/incomplete`. Sale 1 solo si hay algún error. Sin `--subject`, solo las reglas `on_check` sobre los documentos locales de su familia.
  - CLI `sldb rules explain RULE SUBJECT`: `data = {rule, subject, finding}` con el finding de eval (`node`, `holds`, `clause`, `seen`), también cuando se cumple; exit 0/1/2 por `holds` y 3 cuando la regla no aplica (`applies: false`, `reason: subject|where`, `detail`).
  - `contracts/layers.toml`: la arista `models → store` (el parser del lenguaje, importado de forma diferida por los validadores de `RuleDoc`) queda contada como R6 pendiente.
  - `docs/opsys/bridge_primitives/README.md`: la sección `Constraint` se marca como reemplazada por `RuleDoc`.
- Lenguaje de predicados unificado (GO05, plan grafo-operable; `docs/architecture/rules-language.md`):
  - `sldb.store.graph.language`: parser (`parse_predicate` → `Predicate`) y evaluador del lenguaje de GO02: `and`/`or`/`not` con paréntesis, caminos `campo`, `rel:<tipo>`, `^` y clausura `+` (pasos unidos por `.`), cuantificadores `any`/`all`/`none`, `count(...) cmp n`, sustitución `{campo}` desde el sujeto, `incomplete` (Kleene fuerte) en el borde de links y findings `{node, holds, clause, seen}`. `sldb.store.query_engine.rules` es la fachada de los tests de spec (52 verdes).
  - `GraphBackend.eval` evalúa caminos sobre el índice compuesto y, sin sujeto, el dominio entero (la proyección cargada, o todos los documentos). Al atravesar un campo `F` con `F__anchor_state` en el origen, cada elemento expone `anchor_state`.
  - API única: `where_matches`, `edges_holding`, `StructuredQuery` y `--where` evalúan con el lenguaje; nuevas `sldb.api.where.where_findings` (un store, sin re-extraer) y `where_records`.
  - CLI: `sldb find --where` acepta el lenguaje completo (caminos sobre el índice del store) y `--explain` agrega `findings` por documento evaluado. `sldb --envelope graph query` con filtros `FieldCondition` lleva un warning `deprecated/field-condition` que nombra el predicado de reemplazo; la salida no cambia.
  - Deprecados (GO10 los retira): `where_parse.compile_where`, `where_parse.where_parse` y construir `FieldCondition` emiten `DeprecationWarning`.
  - Cambios de resultado declarados (tabla de equivalencia, goldens en `tests/fixtures/where_goldens/`): `f != <número>` ya no cumple sobre un campo ausente; ordenar `None` o tipos mezclados da `false` en vez de `TypeError`; en `StructuredQuery`, `contains` sobre una cadena es subcadena e `is_null`/`is_not_null` tratan `""` como ausente.
- Transclusión de campos y segmentos ricos de diagramas y vistas en /document/segments (SV03):
  - `sldb.api.segments`:
    - `source_ref.py`: `SourceRef` incorpora el campo opcional `field: str | None = None`.
    - `composition_spec.py`: Soporta `ref: Literal["document", "field", "view", "spec"]`.
    - `composition_piece.py` y `field_segment.py`: incorporan los campos opcionales `projection: dict | None = None` y `table_data: dict | None = None`.
    - `field_ref_resolver.py`: `FieldRefResolver` resuelve referencias `Model:name#campo`, `docs/<Model>/<name>/<campo>` y `docs/<name>/<campo>` devolviendo `{model, doc, path, field, value, payload}`.
    - `segment_enrichment.py`: Enriquecimiento de segmentos con vistas resueltas (`resolve_view` / `evaluate_projection_view`) y tablas estructuradas (`table_data`).
    - `build_document_segments.py`: Inyecta `FieldRefResolver` en `render_with_spans` y enriquece los nodos con `projection` y `table_data`.
  - `sldb.models.structured_doc`: `StructuredNLDoc.compose_field` y `render_payload` aceptan `field_resolver`; cuando `ref == "field"`, resuelve campos remotos emitiendo `CompositionPiece` con `SourceRef(model, doc, path, field)`. Sin resolver inyectado, rinde vacío preservando la pureza del renderizador.
  - Documentación de arquitectura en `docs/architecture/segments-and-transclusion.md`.
  - Suite de tests en `tests/segments/test_field_transclusion_and_diagram_segments.py`.
- Visual notation and projection view resolver, store synchronization, CLI, and serve routes (SV02):
  - `sldb.api.notations`:
    - `notation_view.py`: `resolve_view` and `resolve_documents` resolving glyphs, compartments (`data.attributes`), template/keyword interpolation, edge ordering, UML fragments, and legends.
    - `projection_view.py`: `evaluate_projection_view`, `list_projection_views`, and `save_projection_view` evaluating node where-predicates, relation filters, layout, palette ink, and notation styling.
    - `notation_sync.py`: `sync_palette` and `sync_notation` writing `PaletteDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, and `RelationTypeDoc` into stores without intermediate YAML dependencies.
    - Re-exported in `sldb.api` and `sldb.api.notations`.
  - CLI: `sldb notations (list, sync, view, resolve)` with JSON output and envelope support (`sldb --envelope notations ...`).
  - HTTP serve routes in `sldb serve`: `GET /notations`, `GET /notations/view`, `POST /notations/resolve`, `GET /views/projection`, `GET|POST /views/projection/evaluate`, `POST /views/projection/save`.
  - Documentation updated in `docs/architecture/notations-and-views.md`.
  - Comprehensive test suite in `tests/notations/test_notation_view_and_routes.py`.
- Declaración y edición draft de containment, references, compositions, semantics y authority en modelos (SV04):
  - `sldb.api.create_model` y `ModelSource` aceptan `containment`, `references`, `compositions`, `semantics`, `authority`; validan que los campos referenciados existan y que las composiciones tengan marcador `⸢render•<name>⸥` en template (o lo generan en `default_template`), emitiendo las asignaciones correspondientes en el código Python generado.
  - `describe_model` y `ModelDescription` exponen `containment`, `references`, `compositions`, `semantics_map`, `authority`, `template`, `has_draft`, `draft_path`.
  - `sldb.api.edit_model_metadata` en `sldb.api.model_drafts` edita `__containment__`, `__references__`, `__compositions__`, `__semantics__` y `__authority__` en el `.draft.py` (`.py.temp`) mediante manipulación AST en `metadata_literals.py`, y sincroniza secciones de composiciones en el template.
  - `validate_template_contract` y `check_and_plan` validan coherencia de referencias/containment/compositions contra campos declarados y template, rechazando errores con `SLDBModelEditError`. `promote_model_draft(..., backfill=True)` re-renderiza documentos y reconstruye índices de modelo, semántico y de aristas.
  - Expuesto en CLI (`sldb models metadata edit`, `sldb models validate --promote --backfill`, y flags de creación) y HTTP serve (`POST /models/create`, `POST /models/metadata-edit`, `POST /models/promote` con `backfill`).
  - Documentación de arquitectura en `docs/architecture/model-authoring.md`.
- Visual vocabulary models, palettes and builtin notations absorbed from spec2viz (SV01):
  - 7 models in `sldb.models.notation_models` (re-exported in `sldb.models` and `sldb.api`):
    `SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, and `ViewDoc`.
    `ViewDoc` adds optional `params: dict` and `sections: list` for GD25 convergence.
  - Submodule `sldb.notations` containing palette (`palette.py`), notation (`notation.py`),
    and styling (`styling.py`) engines, along with builtin `palettes/default.yml` and the 8 builtin
    notations in `builtin/` (`uml-class`, `statechart`, `component`, `deployment`, `uml-sequence`,
    `activity`, `component-view-matrix`, `reflection`).
  - `resolve_model_ref` maps legacy `spec2viz.sldb_models:<Model>` references to
    `sldb.models.notation_models:<Model>` for transparent backwards compatibility with existing stores.
  - Architecture documentation in `docs/architecture/notations-and-views.md`.
- Each document node of the edge index carries its projected payload (GO04): `EdgeNodeRecord`
  gains `payload` (top-level fields holding a scalar or a list of scalars; dicts and lists of
  non-scalars are left out; a model's `__indexed__` picks exactly those names), `field_hashes`
  (the entry's whole map), `source_hash` (hash_c) and `contract_signature` (sha256 of the model's
  field names and `__references__` / `__containment__` / `__compositions__` names), persisted in
  the shard; other nodes leave them empty. `EDGE_INDEX_VERSION` 4 -> 5: a version-4 shard reads
  as stale and is rebuilt on the next write or `stores build`. `EdgeIndex.stale` now also names
  a document whose Markdown was edited outside sldb and one built under another contract
  signature of its model (a new `__references__` entry). `StructuredQuery` filters on
  `FacetFilter(facet="payload", ...)` from the shard, with no re-extraction; a filter on a field
  no model projects raises `SLDBGraphArgumentError` naming it. An `__indexed__` name that is not
  a field or not scalar is `SLDBModelError` when the model loads. Existing queries answer as
  before. Edge index of this repo after `sldb stores build` (`du -sb` of the edges shards root,
  MB = 10^6; shards = `.yaml` files there; 2026-11-06): before (main 804f1ad4) 47.64 MB in
  3116 shards; after (wt/go04 on c1e50419, which tracks more documents) 58.54 MB in 3277 shards.
  `docs/architecture/graph-backend.md` documents the projection and what it leaves out.
- A bare id in a reference field that allows a model also names a document of one of its submodels
  (`depends_on: task-x` with `TaskDoc` allowed names `TaskCodeDoc:task-x`), read from `base_models`
  of the model nodes in the composed index (an inherited model's node takes them from its class, since
  its local index keeps none). The allowed model itself wins; several submodels with that
  name stay `ambiguous`. `resolve_indexed_document` also reads the bases of an inherited model from
  its owner store.
- `sldb.api.resolve_indexed_document(store_path, model, name)` finds `Model:name` when the document is
  tracked under a submodel of `Model` (`TaskDoc:task-x` finds `TaskCodeDoc:task-x`): an instance of a
  submodel is an instance of its bases, read from `base_models` in the model indexes, without importing
  any class. An exact match on the model wins; two submodels tracking the same name raise
  `AmbiguousDocument`. Consumers such as graph_ui resolve ids through it instead of comparing model names.
- The whole-graph analyses sit behind a `GraphBackend` seam (`load`, `eval`, `analyze`).
  `NetworkXBackend` wraps `sldb.store.graph.analysis` unchanged, so the six `sldb graph`
  analyses and the ten `api/graph/analyze.py` functions print the same output as before and
  can be given another backend by Python for tests. A store selects it with
  `graph_backend` in `.sldb/store.yaml`: absent means `networkx`; any other value fails on
  load with `graph_backend <value> no admitido; admitidos: ["networkx"]`. `eval` implements
  the GO02 subset without paths (finding shape in `rules-language.md` §4 and §6); a path
  raises `NotImplementedError` until GO05. `docs/architecture/graph-backend.md` fixes the
  seam: a future engine (Kùzu, Neo4j, Datalevin) enters behind it and the rules never see it.
- A project's declared-edge graph as a library (`sldb.api.edges.project_graph`): `ProjectGraph(root,
  ProjectGraphConfig)` reads the documents of configured surfaces and the files path rules
  classify as nodes, the schema edges and unresolved values of the project's own store from its
  cached composed edge index (`include_linked=False`), and from each document's text what its
  model does not declare (configured mapping fields, fenced YAML blocks, mentions under headings
  or on every line). `edges_from(node)` / `missing_from(node)` read one source alone and give
  what `extraction()` gives for it, so a reader asking about a few documents reads only those.
  The project owns only the configuration (deskops' desk is the first, `deskops/graph/desk_graph.py`).
  New `sldb.api.tracked_documents(store, refs)`: `doc_status` for many references from one read
  of the documents index.
- The store splits in two sibling directories: `.sldb/` (`store.yaml` and `core/`) is
  versioned whole, so that git holds the tree's past, and `.sldb_cache/` (edges, sections,
  semantic shards, graphs, locks; `.sldb/runtime/` until now) is regenerable and ignored
  (`docs/architecture/derived-store-boundary.md`; owner's decision, 2026-10-29).
  `sldb stores init` adds the line `.sldb_cache/` to the root `.gitignore` (idempotent, no
  other line touched); `sldb stores check` reports the error `stores/core_ignored` (exit 1)
  when git ignores `.sldb/core/` or `.sldb/store.yaml` and the alert `stores/cache_not_ignored`
  (exit 0) when the cache is not ignored; `stores build --check` leaves `.sldb_cache/` out of
  its copy. New `sldb stores migrate-layout [--store PATH] [--force]` moves the content of
  `.sldb/runtime/` to `.sldb_cache/` (refusing a non-empty cache unless `--force`, which
  deletes it first), deletes the journal without archiving it, removes `.sldb/runtime/` and
  rewrites the root `.gitignore`: only the lines whose pattern is `.sldb/core` or
  `.sldb/runtime` go, `.sldb_cache/` comes in, everything else stays verbatim. The
  `selfdoc python-sync` graph defaults to `.sldb_cache/graphs/python-source.graph.json`.
- The write journal is retired (2026-11-04): no write through `sldb.api` produces one, and
  `sldb journal show` (and `verify`) print `El journal fue retirado el 2026-11-04; el pasado
  del store se consulta con sldb docs history <doc>.` and exit 0. `sldb.api.journal()` answers
  `[]` and `verify_journal()` a valid, empty report, for importers; `SLDB_JOURNAL_OFF` is gone;
  the `actor` parameters stay (they still stamp a document's provenance where they did).
  `docs/architecture/journal-authority.md` records the decision: the tree is the authority
  and git is its memory.
- Edges can carry their evidence, on request: `sldb edges show --evidence` and
  `sldb.api.edges.edge_evidence.stamp_evidence` add `metadata.evidence` with `ref_hash` (the
  target's `content_hash`, a model's `model_hash`; for a section its document's, flagged
  `ref: document`, since sections have no hash of their own), `contract` (the source model's
  `contract_hash`) and `engine` (`{name, version}`) or, for an authored edge, `actor`
  (`relation_doc:<name>`). No timestamp. Computed on read, so the shards do not change, and
  `ref_hash` is the target's current hash: telling an edge went stale takes a caller that kept
  an earlier evidence to compare.
- `sldb --envelope <command> ...` prints one JSON value per run, `{ok, command, store,
  revision, data, warnings}` or `{ok: false, error: {type: "ns/name", message}, exit}`, and
  exits with a typed code: 0 ok, 1 missing, 2 ambiguous, 3 rejected input, 4 busy, 5 store or
  runtime failure, 6 usage, 70 unexpected (`docs/cli-envelope.md`). Opt-in: without the flag
  the CLI prints and exits as before, because callers parse that output today.
- `sldb stores declare` and `sldb stores build`. A store's source is `.sldb/store.yaml`: the
  models it registers (local, or inherited from a linked store), its links, its predicates,
  the generators that write derived documents (such as `selfdoc python-sync`), the paths
  they write, and `include` rules saying which file is tracked under which model and name.
  The index and the model and document indexes are rebuilt from it by `stores build`
  (idempotent); `stores build --check` rebuilds a scratch copy of the sources and fails when
  that copy does not pass `stores check`, a tracked document is not declared, or it tracks
  something other than the local store. `stores declare --write` writes the declaration the
  current index implies, to adopt the layout. Tracking or untracking a document through the
  API keeps the declaration current (a file outside the project is not declared), `stores
  check` notes a declared store whose `.sldb/core/` is versioned rather than ignored, and a
  declared file that is gone is reported by `build` as `missing`. `declare --write` writes
  the declaration the index implies: a model whose source is outside the project
  (sldb's own, from the installed package) is declared by `model_ref` alone, and a glob is
  written only for a folder with more than one tracked file, all of one model. Design:
  `docs/architecture/derived-store-boundary.md`.
- An inherited model whose owner uses a `src/` layout imports again. The import root was the
  owner's project root, so pron's models, which live under its `src/` directory, stayed unimportable in a
  store that inherits them; it is now the directory the owner's registered path puts the
  package in (`sldb.store.model_import_root`). sldb's own store inherits AnchorDoc,
  ProjectionDoc and MoveDoc from pron through a relative link (`../pron/.sldb`) instead of
  registering copies pinned to an absolute path that no longer existed.
- **Python 3.12 or newer is required** (`requires-python >=3.12`; it was `>=3.10`). Python
  3.10 reaches end of life this month, and the whole suite (sldb, deskops, spec2viz, graph_ui)
  moves to the same floor. CI tests 3.12 and 3.13. The compatibility code for 3.10 is gone:
  the `tomllib`/`tomli` fallback in the `tools/check_*.py` gates and the conditional `tomli`
  dev dependency. `uv.lock` is regenerated for the new floor.
- The pre-redesign singular groups `sldb store`, `sldb model` and `sldb doc` run again: they
  were parsed (and listed by `sldb doc --help`) but had no handler, so `sldb doc untrack`
  answered `Unknown command: doc`. The plural groups (`stores`, `models`, `docs`) remain the
  documented spelling.
- A change to a model's contract now rebuilds the edges of its documents. Adding
  `__reference_models__` to a model and running `stores update` used to reuse every document's
  edges shard (its hashes had not moved), so the new references never reached the index and
  `edges rebuild` walked nothing until the shards were deleted by hand. Each shard now records
  the contract it was built under; the first rebuild after upgrading rewrites every shard once.
- A store link can be removed or pointed elsewhere: `sldb.api.unlink_store(store, name)` /
  `sldb stores remove <name>`, and `link_store(..., replace=True)` / `stores add --replace`.
  Removing a link a model here is inherited from is refused (replace it instead). A link to a
  directory that is gone was only fixable by editing `store_index.yaml`; `stores check` now
  notes it (`broken_links` in `check_store`).
- A scalar list item reads back as written. An item whose text markdown reads as block syntax
  was lost or mangled on extract: `validation: ["```bash", "pytest", "```"]` came back as
  `["pytest"]` (so any rewrite of the document deleted the fence lines), and `# x`, `> x`,
  `- x`, `1. x`, `***`, `<b>` or a leading space lost their syntax. Such an item is now rendered
  with one leading backslash (a CommonMark escape) and extracted without it; only a value that
  opens its item (`- ⸢rev,list•x⸥`) is escaped. A hand-written item that already began with
  `\` before such syntax now reads without that backslash.
- Extracting and validating no longer re-parse the model's template each time: a template's
  recipes are computed once per template, `validate` renders once instead of twice, and the
  sections index reuses one markdown-it parser. On sldb's own store, extracting 153 documents
  went from ~420 ms to ~275 ms and their sections from ~205 ms to ~175 ms.
- The markdown AST keeps what a token carries beyond its text, in `SLDBNode.metadata`: a
  fence's language (`info`), its opening markup (`markup`) and its attributes.
- `sldb edges show <name>` with something that is no node of the index fails, and suggests the
  document's export id (`Did you mean PillDoc:pill-008?`), instead of printing `[]` as for a
  real node without edges.
- `models show`, `models template show` and `docs update` take `--format text|json|yaml`
  (`models show` keeps YAML as its default; the template comes wrapped as
  `{model, draft, path, template}`; `docs update` reports `{updated, model, path}`). An
  argument a subcommand does not know is reported with that subcommand's usage, not the
  root's.
- A model's `__family__` changed in the class reaches the store: `stores update` and
  `models update` re-read it (it was written only at `models add`).
- `sldb.api.registered_models(store)` and `is_model_registered(store, model)` (by name,
  `module:Class` or `module.Class`), and `sldb models check <model>...`, which reports each as
  registered or missing and exits 1 if any is missing.
- `stores check` notes ignore rules that break the store's split (`.sldb/core` ignored, or
  `.sldb/runtime` not ignored); `check_store` returns it as `gitignore_policy`.
- A registered model that does not import here no longer takes the store's AST down: it is
  listed with `resolved: false` and the error (a healthy model's entry is unchanged), so `models show` and `ast show` of the rest
  answer (in an environment without `pron`, `models show TaskDoc` failed).
- `models template show` (and every draft operation) finds a model's source by importing its
  `model_ref` when the recorded path is not a file here: a store copied without its models,
  an absolute path from another machine, or an inherited model, whose path is empty and
  failed with `Is a directory`. When neither works, the error names the model and the store.
- A template's literal paragraph (deskops' `_Describe the incoming message..._`) anchors only a
  paragraph with that text. A document written without the placeholder had its first real
  paragraph taken for it and dropped on extract, so any rewrite deleted it (the first
  paragraph of inbox notes; `why`, `goal` and `done_when` of a task). Documents that lacked
  the placeholder now extract more: `stores check` reports them as `data_mutation` until
  `sldb models update <Model>` re-extracts the model (`stores update` trusts a document whose
  text did not move). Headings still anchor by position.
- A document that ends before its template does keeps its last section: a field of a section
  the document does not have (`## When`, after a document that stops at `## Why`) no longer
  claims the last section's paragraph, which came out empty and was erased by any rewrite.
  Past a missing heading, only later headings end a section. The `purpose` of three of
  sldb's rituals came back (`models update RitualDoc`).
- `stores check` names the documents a rewrite would lose content from: blocks of the file
  that do not survive `render(extract(text))`, because the model does not read them (written
  by hand, or by an older template). Their hashes are consistent over the poor extraction, so
  nothing else showed it. Sections the template fills only with `render`/`py` markers are
  regenerated and not counted. `check_store` returns it as `rewrite_loss`.
- `stores check --quiet` prints the PASS/FAIL line alone, as documented: it printed the
  per-document notes too, and now also skips the scans behind them.
- A `data_mutation` over text that did not move (and an unchanged contract) is explained as
  what it is, sldb reading the same file differently after an upgrade, and points to
  `sldb models update <Model>`: `stores check` said `stores update` would accept it, but
  `stores update` trusts unchanged text and did nothing. It no longer asks for a decision.
- `stores check` says, for a document whose text disagrees with its index, where the indexed
  text sits in the file's git history: `stale` (an earlier committed version, with the commit:
  the index fell behind), `unmatched` (no committed version has it: an edit indexed and never
  committed, or damage), `orphan` (the file is gone) or `undetermined` (not a git work tree),
  with the `git log` command that shows it. The JSON report carries it as `history`.
- `sldb.store` imports the rest of sldb through three seams only: `store/exceptions.py`
  (errors), `store/runtime_codec.py` (extraction) and `store/model_contract.py` (what a model
  class declares, and the built-in relation types); it imports nothing from `sldb.api`, `cli`
  or `selfdoc`, and `tests/test_store_seams.py` keeps it so. `describe_field` and the field
  kinds moved to `sldb.models.field_schema` (still importable from `sldb.api.schema`), which
  closes the store → api edge R4 in `contracts/layers.toml`.
- `selfdoc python-check` and `python-sync` work again: a property with a setter (or an
  `@overload`) was two symbols with one document id, and both commands failed with "Python
  symbols collide". A name redefined in its scope is now one symbol.
- kgdb is part of sldb, and nothing invokes an external `kgdb` any more. `selfdoc python-sync`
  writes the source graph with sldb's own graph IO instead of running `kgdb ingest` (it failed
  once the separate package was gone). `--kgdb-command` and `--kgdb-output` were removed and
  are refused with a clear error; the graph goes to `--graph-output`, by default
  `.sldb/runtime/graphs/python-source.graph.json` (it was `.kgdb/python-source.graph.json`).
  `sldb.selfdoc.kgdb_sync` is now `sldb.selfdoc.source_graph_file` (`write_source_graph`), and
  the selfdoc report's `kgdb_stale` is `graph_stale`. The data contract
  `sldb_kgdb_semantic_export` keeps its name (see the entry on kgdb names below).
- Docstring metadata is parsed strictly (`sldb.selfdoc.docstring_metadata`, spec section 2):
  only an opening line exactly `---` starts it, a closing `---` is required, and the block is a
  YAML mapping with unique keys among `id` (required), `kind` and `tags` (`namespace:value`,
  deduplicated). Malformed metadata and an id declared twice are reported as `path:line:
  problem` in the selfdoc report's `metadata_errors`, and `selfdoc python-sync` writes nothing
  while any remain; they were silently ignored and the declaration lost its identity.
- The source graph gives every module and symbol node its `local_tags` and `effective_tags`,
  inherited along the lexical chain package -> module -> class/function -> nested declaration
  within the scan (spec section 3): `system:*` and `workspace:*` from the nearest declaration,
  `topic:*` as a union, any other tag local only; nothing through imports, base classes or
  siblings. Each effective tag names the declaration and `path:line` it comes from. Two
  `system:` (or `workspace:`) tags on one declaration are a metadata error.
- An import in the source graph follows explicit re-export chains to the definition
  (`from sldb.api import open_store` reaches `sldb.api.stores.open_store:open_store`), through
  module-level imports only, with the chain in the edge's `via`; `from pkg import submodule`
  reaches the submodule. A star import, a cycle or a module outside the scan stays
  unresolved. A relative import inside a package's `__init__.py` resolves against that
  package (it was resolved against the parent: `pkg.impl` for `pkg.inner.impl`).
- `stores check` reuses its per-document content scans (rewrite loss and structural noise)
  while a document's text, its model's contract and the sldb that reads it have not moved, in
  the user's cache directory; the rewrite-loss scan also reuses the extraction the check
  already has instead of extracting again. On sldb's store (2775 documents) a full check went
  from 43 s to 23 s cold and 7 s warm, with the same findings.
- The source graph keeps the condition an import lives under (`context`: `type_checking`,
  `conditional`, `try`), and marks an import a later same-scope binding shadows
  (`shadowed_at`); a reference after the shadowing no longer resolves to the import.
- `selfdoc python-check` reports, apart from errors and drift, the declarations without
  metadata (`undeclared`), the declared ones without an explanation (`unexplained`) and the
  annotation references nothing resolves (`unresolved_references`, which were dropped).
- A symbol document's `purpose` is generated from the first paragraph of its docstring when it
  is a placeholder or was generated before; an authored purpose is kept and listed in
  `purpose_conflicts` for a decision.
- `selfdoc python-sync` reports on what is on disk after writing: it reported the plans made
  before writing, so a sync that wrote everything returned 1.
- Deleting `.sldb/runtime/` and rebuilding brings the sections and semantic indexes back. The
  user cache (`~/.cache/sldb/runtime-cache-built/`) and the in-process dirty set vouched for
  shards that were gone, so a rebuild wrote only the edges and a graph snapshot lost
  `has_section` and `semantic_parent` (reported by graph-ui).
- The last kgdb names in sldb's public surface are sldb's now (kgdb merged into sldb):
  - `sldb.store.export.export_kgdb_semantic_payload` is `export_semantic_payload`;
  - the semantic export contract keeps its name, `sldb_kgdb_semantic_export` version 1, and so
    do its schema and fixture (`contracts/schemas/sldb_kgdb_semantic_export.schema.json`,
    `contracts/fixtures/sldb_kgdb_semantic_export.v1.json`). It is a frozen data identifier,
    like the `sldb://...` node ids: renaming a data contract breaks every reader of files
    already written, so a format change goes behind a new contract version, never a rename.
    Main wrote `sldb_semantic_export` for a while before release; an export under that name is
    still read, never written. `tests/store/test_export_contract_frozen.py` pins the contract,
    the ids and the keys of the store index and of the document entries. The reading function is `sldb_semantic_export_to_snapshot`;
  - `stores semantic-export --format kgdb` is `--format sldb`;
  - the `sldb serve` route `/kgdb/snapshot` is `/semantic-export`;
  - the store's tracked relation types moved from `kgdb/relation_types/` to
    `sldb/relation_types/`, where `edges init` already wrote the new ones.
- `stores init` fails cleanly: what a failed init wrote is removed, the message says where it
  failed and what to check (instead of `Unexpected: [Errno 13] ...`), and the exit code tells
  a caller what happened: 0 created or already there, 2 the place refused it (permissions),
  1 failed half-way. `init_store` raises `StoreInitError` (an `SLDBStoreError`).

## 0.1.12 - 2026-10-18 — declared references resolve bare ids and paths, and report what names nothing

- Declared references resolve bare ids and paths. A value of a `__references__` or
  `__containment__` field names its document as an export id, as the path a tracked document
  lives at, or as a bare id tried against the models the field allows — the new
  `__reference_models__ = {"field": ["Model", ...]}`, or the containment list; one match
  resolves, several are `ambiguous`. It is decided when the index is composed, so tracking the
  target later resolves it. What names nothing is reported, never an edge:
  `sldb.api.unresolved_references(store)` / `sldb edges unresolved` /
  `EdgeIndex.unresolved_references` (`UnresolvedReference`: source, model, field, target,
  target_export_id, relation, reason, source_path). A free reference field only reports export
  ids. `EDGE_INDEX_VERSION` is 4: shards rebuild. `__reference_models__` enters the contract
  hash only for a model that declares it.
- An edge sldb derives (structural, schema, alias) is checked against sldb's own definition of
  its builtin type, even where the store authored a type under that name (selfdoc's code
  `contains` / `references`).
- `edges check` of a store that links others fails only on its own edges: what only a linked
  store's edges commit (an owner's stale shards, its cardinality violations) is reported apart
  (`EdgeCheckReport.linked_errors`, `linked_stale`; a `note:` line in the CLI). Edges read
  from a linked store carry `metadata["from_store"]`.
- Inheriting a model into a store (`models inherit`, or `alias:Model` on first use) signs its
  empty roster, so `stores check` passes without a `stores update` first.
- A section no longer counts as the owner of a path: a bare composition or reference value
  equal to a heading path resolved to that section instead of a document.

## 0.1.11 - 2026-10-18 — models are defined once and inherited; a free `attributes` on relations

- `RelationDoc.attributes`: a free dict of the edge's own attributes (a multiplicity, a role, a
  transition's action), written in the frontmatter and copied to the index edge as
  `metadata["attributes"]`. A RelationDoc written before has none. Its contract moved: run
  `sldb stores update` in a store that tracks RelationDoc documents.
- `sldb.api.StructuredNLDoc`: the base class of models, from the public surface.
- `sldb.api.graph.query_snapshot(snapshot, query)`: a StructuredQuery over a GraphSnapshot held
  in memory, no store needed. `sldb.api.graph` also exports `Edge` and `SystemIdentity`.
- `models inherit` and the `stores check` note tell a copy by its class, not by the reference
  string: `deskops.models.atom:AtomDoc` is a copy of `deskops.models:AtomDoc` when the package
  re-exports it. A converted copy takes the owner's `model_ref`.
- `edges check` over linked stores: one edge that two stores both emit (a shared model's
  `has_field`) counts once for cardinality; `has_model` is many-to-many, since stores share a
  model they inherit; `links_to` is a builtin relation type. `sldb edges init` now also
  rewrites a tracked builtin relation type whose spec moved (`updated` in its report), and no
  longer writes a builtin over an authored relation type of the same name.
- Models are defined once, in the store that owns them, and inherited by the others.
  `sldb models inherit alias:Model` / `sldb.api.inherit_model` registers an inherited entry
  (`origin: <alias>`, no source path) or converts a local copy in place, keeping its documents,
  roster and signed contract. Using `alias:Model` as a model name now inherits instead of
  copying. An inherited model imports from the owner's project root, so no `--pythonpath` is
  needed and a moved owner is one link to update; with the owner unreachable the store keeps
  working on its own signature. `stores check` notes a local model under a name a linked store
  owns (a convertible copy, or an override to rename). The graph gains `links_to` between
  stores and `origin_store` on `has_model`. A store with no inherited models writes no
  `origin` key, so existing indexes do not change.
- `stores update` re-signs the roster of a model whose class does not import. It used to skip
  the model whole, so a stale roster (a merge that brought its shards in, say) stayed
  `roster stale` in `stores check`. Its documents are still not rehashed, it is still reported
  as skipped, and it keeps the contract it signed.
- `stores check` no longer reports a moved contract for a model with `extra="allow"` (deskops'
  TaskDoc) whose documents carry undeclared frontmatter keys. Such a key is still produced by
  the current class, so it is not a field the model dropped; the check only counts a key the
  current extraction of the same document no longer yields. `stores update` could never clear
  the old finding.
- A template whose frontmatter is one `dict` placeholder (`⸢rev,dict•frontmatter⸥`) declares
  every key: `docs track` and `docs create` no longer refuse a document's extra keys, which that
  dict carries back on re-render.
- `producer.version` in a semantic export is the real package version: read from the source
  checkout's `pyproject.toml`, else from the installed `structuredLanguageDB` metadata. It
  asked for a distribution named `sldb`, which never exists, and always fell back to `0.1.0`.
- `click` is an optional extra (`pip install structuredLanguageDB[click]`), imported only when
  `ClickScanner` is used; it was imported unconditionally without being declared.
- `sldb.examples.pandoc_cv` ships in the wheel, with its Markdown files.
- `tools/check_identity.py` reads `git ls-files -z`: a quoted non-ASCII path no longer shows
  up as a top-level entry named `"docs`.

## 0.1.10 - 2026-10-17 — references to a relation type reach it; a document by absolute path

- A `__references__` field that points at `RelationTypeDoc:<doc>` now lands on the
  `sldb://relation_type/<name>` node. The index stores relation types under that node, so the
  schema edge used to point at a document node that does not exist and was dropped silently
  while `doc_exists` said yes. `resolve_edges` moves that end to the relation-type node.
- `find_doc` (behind untrack and delete) accepts a document's absolute path as well as the path
  relative to the project root.
- Design notes for the surface in `docs/surface/`, with tests for the MachineDoc editor and an
  optimistic-lock client. The editor test compiles on Python 3.10/3.11 (no nested PEP 701
  f-string).

## 0.1.9 - 2026-10-16 — a dropped field is a contract move, and `stores update` fixes it

- A document whose `field_hashes` name a field its model no longer declares was signed under
  another contract. Any write of another document of the model re-stamps the model's contract,
  so the model looked unmoved: `stores check` blamed the untouched document (`data_mutation`,
  "confirm the change was intended") and `stores update` trusted its unchanged text and never
  re-extracted it, so the check stayed red. Now the model reads as `contract moved` (safe to
  run: `stores update`) and `stores update` re-extracts those documents.

## 0.1.8 - 2026-10-16 — a deleted model class no longer locks the store

- Derived-index rebuilds skip a model whose class does not import instead of raising; the
  semantic rebuild names it in `models_unresolved`, as the edge rebuild already did, and its
  documents keep their last tags. `untrack_document` (and every write that rebuilds) works
  while another registered model's class is gone.
- `sldb models remove <name> --with-documents` / `remove_model(..., untrack_documents=True)`:
  drops a model and its tracked documents without importing the class; the Markdown files stay.
- A write that raises halfway leaves no trace: `untrack_document` puts the document's shard,
  the models index and the store index back as they were; `remove_model` changes the registry
  first and deletes the model's files only once every rebuild succeeded.

## 0.1.7 - 2026-10-16 — `models remove`

- `sldb models remove <name>` / `sldb.api.remove_model(store, name)`: unregisters a model that
  tracks no documents, with its indexes and shards; the class is never imported, so a model
  whose code was deleted can go. A model that still tracks documents is refused (untrack them
  first). `stores check` already passes with such a model registered (0.1.5); its note now
  names the unimportable models with no documents as removable.

## 0.1.6 - 2026-10-16 — the graph as a state machine

- `--where` joins predicates with ` and ` (outside literals; no `or`, no parentheses), and
  `nonempty(f)` is `has(f)` that also rejects `[]` and `{}` (`has` keeps its meaning).
- `sldb.api.where_matches(expression, payload, subject=None)`: a `--where` predicate on a plain
  payload, tracked or not; `{field}` fills from `subject` (default: the payload). An unparseable
  part raises `WherePredicateError`, now exported from `sldb.api`.
- `sldb.api.edges_holding(store, node, subject, relation=None)`: the edges leaving a node whose
  condition (the edge's, else its type's) holds on the subject; `sldb edges show <node>
  --holds-for <doc>` is the same from the CLI. A self-loop is a valid edge (a terminal
  transition).

## 0.1.5 - 2026-10-16 — an unimportable model is named, not blamed on its documents

- `stores check`: when a model's class cannot be imported (a clean clone without the model's
  package, a consumer's CI with another `sldb` first on PATH), its fields cannot be
  re-extracted. Every document used to read as a `data_mutation` ("decide first", restore the
  file). Intact text now stands for intact fields, and the report names the unresolved models;
  changed text still fails. JSON: `models[].resolved`.
- CI: the structural gates pass (`legacy_contract` mapped to the `migracion` axis, unit coupling
  updated; the surface gate no longer compares the five-consumer total with a partial view),
  and `selfdoc check` passes (knowledge/ synced with the CLI, the store committed with it).

## 0.1.4 - 2026-10-16 — `fields update` leaves the store passing

- A field write (`fields update|append`, `sldb.api.save_document_payload`) rewrote the Markdown
  and the model's roster but not the document's record, so `stores check` failed with a
  `data_mutation` on the write sldb had just made. The shard cache handed out its own instance:
  the caller edited it in place and the save, comparing against the cache, saw no change and
  skipped the write. Loads now return a copy (`sldb.store.io.shards`), which also covers the
  semantic, sections and edges shards.

## 0.1.3 - 2026-10-16 — upgrading sldb no longer fails unchanged stores

Found on Governance's `pulse`, which installs sldb from git: both checks failed on a store whose
content had not changed.

- `stores check`: a model whose stored contract hash equals the formula sldb used before
  cecd97b (fields and template only) passes, with a note naming those models, instead of
  "contract moved" on every model. A class that really changed still fails. `stores update`
  re-seals the hash under the current formula. JSON: `models[].legacy_contract`.
- `edges check`: in a store that ran `edges init`, an edge sldb derives itself whose builtin
  type was added later (`composes`) is checked against the definition sldb ships and reported in
  `untracked_builtins`, not as an error. A store that never ran `edges init` still fails;
  authored edges still need a tracked type.

## 0.1.2 - 2026-10-16 — referencing documents of linked stores

- `stores add` links were recorded but no document lookup read them: `docs show
  alias:doc` answered `Unknown document target`. `docs show` (and `sections show|fields`,
  serve's document routes) now take `alias:ref` — name, `Model/name` or tracked path — and
  read only the store linked directly as `alias`. A bare ref still reads only the local store;
  a prefix that names no link leaves the ref whole, so existing refs resolve as before.
- Add `docs exists <[alias:]ref>` and `sldb.api.doc_status|doc_exists`: whether a reference
  resolves, from the indexes alone (no model import, nothing written). Exit 0 ok, 1 missing,
  2 ambiguous, 5 `link-missing` / `link-broken`, so a missing document is told apart from a
  sibling repo that is not there.
- `stores list` (and `sldb.api.store_links`) report each link's state: `ok`, `missing` or
  `not-a-store`; a broken link is reported, never raised.
- `stores add` records the link relative to the project root (it was absolute outside it), and
  refuses linking a store to itself, aliases outside `[A-Za-z0-9][A-Za-z0-9._-]*` and the
  reserved `local`. Links already written are read as before.
- `stores init` seals the root hash over the empty model layer: a new store, or one that
  only links others, passes `stores check` without a `stores update`.
- `docs show` of a linked doc reads its file from the linked project (`absolute_path` was
  built from the local root).

## 2026-10-01 — SLDB is the substrate again

- The README no longer calls this generation frozen: the v2 seed (`knowledge`) was frozen in
  turn and its evaluator moved to `pron`, so nothing supersedes this package. SLDB is the
  store every surface (`surface/`, `tools/graph_ui`, `tools/sldb-ui`) is a view over. <!-- gone -->
- New README section "Serving and surfaces": `sldb serve` routes grouped by what a UI needs,
  and where the surfaces and their design docs live.

## 2026-09-07 — v1 frozen

- The README marks this generation frozen, with `knowledge` as its successor. Earlier modularization and v0.6 removal plans are historical and do not promise further v1 releases.

## Working tree — `docs delete`

- Add `docs delete` (and `sldb.api.delete_document`): untrack a document **and** remove
  its Markdown file. `docs untrack` was the only way to drop a document, and it keeps
  the file on purpose — so "delete this document" meant untrack, then `rm` by hand, then
  remember that `runtime/cache/extracted.json` still describes the deleted path until
  some later full load rewrites it. `delete` does the three.
- Confirms before removing the file unless `--yes` is given; a non-interactive stdin
  answers no.
- Add `runtime_cache_disk.forget(store, predicate)` so cache entries can be dropped
  without a full store load.

## Working tree — self-documentation follow-up

- Add `selfdoc scan|sync|check` to derive CLI facts from argparse, preserve authored explanations, and synchronize tracked command/surface documents from the selected store root.
- Report obsolete documents without deleting them; check freshness without writing documents or indexes.
- Expose public parser help for the supported `init` and `example` commands.
- Split knowledge document definitions into one class per file, keeping public import references and resolving re-exported definitions for template editing.
- Separate follow-up work into self-documentation, store context/federation, and AST ownership/section contracts. No package version bump or publication is included.

## Historical pending changes

- Add reversible `rev,table[...]` template markers for rendering and extracting Markdown tables backed by `list[dict]` fields.
- Add generic cross-store document writes through linked store aliases and federated model namespaces for workflow tools such as `deskops`.

## 0.2.0 - 2026-05-16

- **Store write concurrency**: atomic writes + advisory `fcntl` locks on all index write paths; `--wait` flag for `stores update`
- **Rebuild auditability**: `RebuildReport` dataclass tracks missing docs, empty sections, and unparseable headings in both semantic and section rebuilds; `--verbose` flag for details
- **CLI deprecation surface**: old singular commands (`store`, `model`, `doc`, `ls`, `get`, etc.) emit deprecation warnings; v0.6 was the historical removal target (see freeze note above).
- **Read-side hot path**: `sections show` and `sections fields` prefer persisted index over full IR rebuild; `--rebuild` flag available on `find`/`sections find`
- **Marker ownership robustness**: field name from the canonical `parse_marker()` is validated against known payload paths; unknown markers log a warning

## 0.1.2 - 2026-04-24

- Reorganize the package into `core`, `models`, `runtime`, `cli`, `assets`, and `examples` subpackages while keeping compatibility re-exports
- Add explicit link recovery and transclusion composition with `recover` and `compose`
- Add structural store queries under `st` with `ls`, `get`, `glob`, and `find --where`
- Add store-local semantic indexing under `se` and explicit federated semantic navigation under `gse`
- Add model semantic metadata, canonical model registration, semantic equivalence mapping, and bundled tests for the new workflows

## 0.1.1 - 2026-04-24

- Add current-system architecture docs and diagrams under `docs/architecture/`
- Add feature proposal docs under `desk/` for future SLDB features: link/recover/compose, store tree indexing, semantic DAG indexing, canonical/global-local semantics
- Add desk workspace with task board, self-docs, and operating procedures

## 0.1.0 - 2026-04-21

- Rename the package and CLI from `nldb` to `sldb`
- Add safe-by-default Python marker execution with configurable unsafe mode
- Ship the SLDB example bundle and CLI workflows for extract, render, validate, init, and example
- Add release basics: MIT license, package metadata, and CI

FILE:instruccion
Cold-bundle de la tarea task-gd26: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_scaffold_store.py
- TMPDIR=/dev/shm pytest -q tests/store/test_stores_build.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_stores.py
- grep -rniE 'taskdoc|board|ritual|pill|atom|closeout' src/sldb/ sin nombres nuevos contra el commit base 6b80df36 (salida de ambos en esta sección)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- sldb stores scaffold --format json y sldb stores scaffold --apply sobre el store temporal del test; segunda corrida todo present
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, límite de clases por archivo; cuenta como test de los archivos tocados aunque output_scope no lo nombre)
- git fetch y rebase sobre origin/main antes de integrar (main trae SV01, SV02, SV04 en 6ba8bb20 y GO04 en d7eefdeb); en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio

