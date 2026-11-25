FILE:desk/tasks/task-contract-signature-cubre-indexed-doc-anchors-y-contract-y-un-campo-no-puede-ser-a-la-vez-referencia.md
---
sldb:
  by: agent
  at: '2026-11-16T05:07:26Z'
  authority: generated
  via: save_document_payload
id: task-contract-signature-cubre-indexed-doc-anchors-y-contract-y-un-campo-no-puede-ser-a-la-vez-referencia
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/drawer/tasks/task-cambiar-indexed-de-un-modelo-no-marca-stale-la-proyeccion-del-payload.md
depends_on: []
pills: []
files:
- src/sldb/store/model_contract.py
- src/sldb/store/models/edge_node_record.py
- src/sldb/models/doc_anchor_value.py
- tests/store/test_payload_projection.py
- tests/api/test_doc_anchors.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo
from_drawer: desk/drawer/tasks/task-anclas-a-documentos-doc-anchors-fuera-de-la-firma-de-contrato-y-aristas-duplicadas-con-references.md
---

# contract_signature cubre __indexed__, __doc_anchors__ y __contract__, y un campo no puede ser a la vez referencia y ancla

## Rationale

_Explain why this task exists or the business driver behind it._

contract_signature (src/sldb/store/model_contract.py:89-102) firma solo los nombres de campos y __references__, __containment__ y __compositions__ (_DECLARED). Cambiar __indexed__ de un modelo no marca stale la proyección del payload (src/sldb/store/edge_index/payload_projection.py:35 usa indexed_fields), y agregar o cambiar __doc_anchors__ o __contract__ no hace que los documentos existentes ganen sus aristas de ancla (se escriben en los shards, src/sldb/store/edge_index/doc_contribution.py:63) hasta la próxima reconstrucción. Además un campo declarado en __references__ y en __doc_anchors__ produce dos aristas (declared_references.py y doc_anchor_edges.py:19) y definition_problems (src/sldb/models/doc_anchor_value.py:67) no lo rechaza. Hallazgos de GO04 (H1) y GO07 (H4, H11). Origen: drawer desk/drawer/tasks/task-anclas-a-documentos-doc-anchors-fuera-de-la-firma-de-contrato-y-aristas-duplicadas-con-references.md y desk/drawer/tasks/task-cambiar-indexed-de-un-modelo-no-marca-stale-la-proyeccion-del-payload.md.

## Goal

_Describe the concrete result this task must produce._

Cambiar __indexed__, __doc_anchors__ o __contract__ de un modelo cambia su contract_signature y deja stale los shards de sus documentos, que el rebuild reproyecta; un modelo que nombra el mismo campo en __references__ y en __doc_anchors__ es rechazado con SLDBModelError al registrarse.

## Scope

_State what is in scope and what is out of scope._

Entra: en contract_signature agregar al cuerpo firmado "indexed": sorted(__indexed__ o []), "doc_anchors": sorted(__doc_anchors__ o []) y "contract": sorted(__contract__ o []) (las tres claves siempre presentes, lista vacía si el modelo no las declara); actualizar la docstring y la descripción del campo contract_signature en src/sldb/store/models/edge_node_record.py:23; en definition_problems agregar el problema "field '<n>' is declared in both __references__ and __doc_anchors__". Tests en tests/store/test_payload_projection.py (cambiar __indexed__ marca stale y el rebuild proyecta el nuevo campo) y tests/api/test_doc_anchors.py (agregar __doc_anchors__ a un modelo con documentos ya indexados marca stale y el rebuild agrega la arista; doble declaración rechazada). Como la firma cambia para todos los modelos, todos los shards quedan stale una vez: correr sldb stores build sobre el store del repo y commitear el .sldb resultante en el mismo commit; anotarlo en CHANGELOG.md como cambio que fuerza un rebuild. No entra: cambiar cómo se proyecta el payload ni cómo se calculan las aristas de ancla.

Precisiones (preflight-1): definition_problems solo devuelve el texto del problema; quien lanza SLDBModelError es doc_anchor_fields en src/sldb/store/model_contract.py (ya hace raise SLDBModelError con los problemas), así que no hay que agregar otro punto de lanzamiento. El store del repo es .sldb en la raíz de sldb: `TMPDIR=/dev/shm sldb stores build --store .sldb` y se agregan al commit los archivos de .sldb/core que el build cambie (git add -u .sldb/core más los nuevos que liste git status bajo .sldb/core). Los avisos son dos: `deskops message send --root . --to deskops` y `--to graph_ui`, con título "sldb: contract_signature cambia, los stores se reconstruyen una vez" y como cuerpo el commit y que deben correr sldb stores build.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer model_contract.py (contract_signature, _DECLARED, doc_anchor_fields línea 53), edge_node_record.py, doc_anchor_value.py (definition_problems) y los dos archivos de test. 2) Cambiar la firma. 3) Agregar el problema de doble declaración. 4) Tests. 5) TMPDIR=/dev/shm sldb stores build --store .sldb y stores build --check.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_payload_projection.py
- TMPDIR=/dev/shm pytest -q tests/api/test_doc_anchors.py
- TMPDIR=/dev/shm sldb stores build --check --store .sldb

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan con los tests nuevos; el .sldb del repo reconstruido va en el commit; CHANGELOG avisa que fuerza un rebuild; aviso a deskops y graph_ui con deskops message send (sus stores se reconstruyen una vez).

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

FILE:desk/atoms/atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo.md
---
id: atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo
title: Lo que la clase declara se relee cada vez que el store firma el modelo
five_wh_one_plus: how
tags:
- system:sldb
---

# Lo que la clase declara se relee cada vez que el store firma el modelo

## Answer

Todo lo que el store copia de la clase de un modelo (contrato, familia) se relee en stamp_model_node (src/sldb/store/model_node.py), por donde pasan todas las escrituras con la clase importada: lo que se copiaba una sola vez en models add (como __family__) quedaba congelado sin que nada lo señalara. Cuando la clase no importa se conserva lo registrado.

FILE:src/sldb/store/model_contract.py
"""What the store reads from a model class and from sldb's built-in vocabulary: the one seam.

The store is a typed-document engine that sldb's document models feed. Everything it needs to
know about them (a class's document bases, its declared family, how a field is described, the
relation types sldb ships) comes through here, so the store's other modules import nothing
from `sldb.models` directly, and a store packaged on its own replaces only this module
(task: desacoplar el store dentro de sldb). Imports are lazy where the store's import time
must not pull the document models in.
"""

from __future__ import annotations

from typing import Any

from sldb.models.builtin_relation_types import BUILTIN_RELATION_TYPES, builtin_payload  # noqa: F401 - plain data


def base_names(model_type: Any) -> list[str]:
    """Names of the document-model bases above this model, nearest first (not the root class)."""
    from sldb.models.structured_doc import StructuredNLDoc

    return [b.__name__ for b in model_type.__mro__[1:] if isinstance(b, type) and issubclass(b, StructuredNLDoc) and b is not StructuredNLDoc]


def declared_family(model_type: Any) -> str | None:
    """The class's `__family__`, the root branch it belongs to; None when it declares none."""
    value = getattr(model_type, "__family__", None)
    return str(value) if value else None


def describe_field(name: str, field: Any) -> Any:
    """How one field is described for the field nodes of the edge index."""
    from sldb.models.field_schema.describe import describe_field as describe

    return describe(name, field)


def indexed_fields(model_type: Any) -> list[str] | None:
    """The class's `__indexed__` names, checked; None when it declares none.

    Raises:
        SLDBModelError: A name is not a field of the model (own or inherited), or the field's
            declared type is neither a scalar nor a list of scalars.
    """
    names = getattr(model_type, "__indexed__", None)
    if names is None:
        return None
    for name in names:
        _check_indexed(model_type, name)
    return sorted(set(names))


def doc_anchor_fields(model_type: Any) -> list[str]:
    """The class's `__doc_anchors__` names, checked; [] without a class (GO07).

    Raises:
        SLDBModelError: A name is not a field or not str / list[str], or a field ends in the
            reserved `__anchor_state` suffix (`sldb.models.doc_anchor_value.definition_problems`).
    """
    from sldb.models.doc_anchor_value import definition_problems
    from sldb.store.exceptions import SLDBModelError

    problems = [] if model_type is None else definition_problems(model_type)
    if problems:
        raise SLDBModelError(f"Model '{model_type.__name__}': {'; '.join(problems)}.")
    return [] if model_type is None else list(getattr(model_type, "__doc_anchors__", None) or [])


def doc_anchor(value: Any) -> tuple[str, str | None] | None:
    """(target export id, seen hash or None) of a document anchor value; None for anything else."""
    from sldb.models.doc_anchor_value import parse_doc_anchor

    return parse_doc_anchor(value) if isinstance(value, str) and value.strip() else None


def projected_fields(model_type: Any) -> list[str]:
    """Fields a payload filter may name: `__indexed__`, else every field whose declared type can
    hold a scalar or a list of scalars (`Any` included: known per value). [] without a class."""
    from sldb.store.edge_index.payload_types import opaque_annotation, projectable_annotation

    if model_type is None:
        return []
    indexed = indexed_fields(model_type)
    if indexed is not None:
        return indexed
    return sorted(n for n, f in model_type.model_fields.items() if projectable_annotation(f.annotation) or opaque_annotation(f.annotation))


def contract_signature(model_type: Any) -> str:
    """sha256 of the canonical JSON (sorted keys, UTF-8, no spaces) of the model's field names
    (inherited included) and its `__references__`, `__containment__`, `__compositions__` names;
    "" when the class could not be loaded."""
    import hashlib
    import json

    if model_type is None:
        return ""
    body = {"fields": sorted(model_type.model_fields), **{attr: sorted(getattr(model_type, f"__{attr}__", None) or []) for attr in _DECLARED}}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


_DECLARED = ("references", "containment", "compositions")


def _check_indexed(model_type: Any, name: str) -> None:
    from sldb.store.edge_index.payload_types import projectable_annotation
    from sldb.store.exceptions import SLDBModelError

    field = model_type.model_fields.get(name)
    if field is None:
        raise SLDBModelError(f"Model '{model_type.__name__}': __indexed__ names '{name}', which is not one of its fields.")
    if not projectable_annotation(field.annotation):
        raise SLDBModelError(f"Model '{model_type.__name__}': __indexed__ field '{name}' is declared {field.annotation!r}, not a scalar or a list of scalars.")

FILE:src/sldb/store/models/edge_node_record.py
"""One node of the edge index: its id, its class, and what the index knows about it."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_serializer

#: The document-only fields: left out of a dump while empty, so other nodes' shards do not grow.
PROJECTION_FIELDS = ("payload", "field_hashes", "source_hash", "contract_signature")


class EdgeNodeRecord(BaseModel):
    """A node a shard contributes to the edge index (document, section, model, field, tag...)."""

    id: str = Field(description="Absolute node id, `sldb://<kind>/<name>`; the key edges point at.")
    node_type: str = Field(description="Node class the relation types validate against: a model name for a document, else `sldb_model`, `sldb_field`, `semantic_tag`...")
    semantics: dict[str, Any] = Field(default_factory=dict, description="What the contributor knows about the node (a document's path and tags, a field's type, a relation type's payload).")
    facets: dict[str, dict[str, Any]] = Field(default_factory=dict, description="Non-semantics facet payloads (`source` provenance, `git`...); filled on read, not persisted in the shards.")
    payload: dict[str, Any] = Field(default_factory=dict, description="A document's projected payload: its top-level fields holding a scalar or a list of scalars (or exactly the model's `__indexed__`); nested values are left out. Empty on any other node.")
    field_hashes: dict[str, str] = Field(default_factory=dict, description="A document's whole field_hashes map, as its index entry records it. Empty on any other node.")
    source_hash: str = Field(default="", description="A document's source_hash (hash_c) the node was built from. Empty on any other node.")
    contract_signature: str = Field(default="", description="sha256 of the model's fields, __references__, __containment__ and __compositions__ names the node was built under; empty when the model could not be loaded, or on any other node.")

    @model_serializer(mode="wrap")
    def _drop_empty_projection(self, handler: Any) -> Any:
        data = handler(self)
        if isinstance(data, dict):
            for key in PROJECTION_FIELDS:
                if not data.get(key):
                    data.pop(key, None)
        return data

FILE:src/sldb/models/doc_anchor_value.py
"""The form of a document anchor (docs/architecture/anchoring.md §6): `doc:Model:name`, or pinned
`doc:Model:name@sha256:<64 hex>` with the contract hash it saw (rules-language.md §5).

The form is a property of one value, so it is checked by the model's own validators: the fields
a model names in `__doc_anchors__` (`StructuredNLDoc`) and the `doc:` items of `Provenance.from_`.
Whether the target exists, its hash now and the anchor's state depend on other documents: the
save pins them and `check_doc_anchors` reports them. What a model definition may declare
(`definition_problems`) is checked when the class is loaded (`store/model_contract.py`).
"""

from __future__ import annotations

import re
import types
from typing import Any, Union, get_args, get_origin

PREFIX = "doc:"
STATE_SUFFIX = "__anchor_state"
_FORM = re.compile(r"doc:([^:@\s]+):([^@\s]+)(?:@sha256:([0-9a-fA-F]{64}))?")


def parse_doc_anchor(value: str) -> tuple[str, str | None] | None:
    """(target export id `Model:name`, seen hash or None) of a well-formed anchor; else None."""
    found = _FORM.fullmatch(value.strip())
    if found is None:
        return None
    return f"{found[1]}:{found[2]}", found[3].lower() if found[3] else None


def check_doc_anchor(value: str, where: str) -> str:
    """`value` when it has the anchor form; ValueError naming `where` and the reason otherwise."""
    if parse_doc_anchor(value) is None:
        raise ValueError(f"{where}: {value!r} is not a document anchor: expected `doc:Model:name` or `doc:Model:name@sha256:<64 hex>`")
    return value


def pinned(value: str, current: str | None) -> str:
    """`value` with `@sha256:<current>` when it carries no hash and the target's hash is known."""
    parsed = parse_doc_anchor(value)
    if parsed is None or parsed[1] is not None or current is None:
        return value
    return f"{value.strip()}@sha256:{current}"


def anchor_items(value: Any) -> list[str]:
    """The non-empty strings a str or list[str] field holds."""
    raw = value if isinstance(value, list) else [value]
    return [item for item in raw if isinstance(item, str) and item.strip()]


def check_anchor_fields(doc: Any) -> Any:
    """The `model_validator` body: every value of every `__doc_anchors__` field has the form."""
    for name in getattr(type(doc), "__doc_anchors__", None) or []:
        for item in anchor_items(getattr(doc, name, None)):
            check_doc_anchor(item, f"field '{name}'")
    return doc


def check_from_items(items: list[str]) -> list[str]:
    """`Provenance.from_` validator: a `doc:` item has the anchor form; any other is left alone."""
    for item in items:
        if isinstance(item, str) and item.strip().startswith(PREFIX):
            check_doc_anchor(item, "from")
    return items


def definition_problems(model_type: Any) -> list[str]:
    """What a model class declares wrongly about anchors: a field with the reserved suffix, an
    `__doc_anchors__` name that is not a field, or a field that is not str or list[str]."""
    fields = model_type.model_fields
    reserved = [f"field '{n}' ends in the reserved suffix '{STATE_SUFFIX}'" for n in fields if n.endswith(STATE_SUFFIX)]
    named = getattr(model_type, "__doc_anchors__", None) or []
    return reserved + [problem for n in named if (problem := _field_problem(fields, n))]


def _field_problem(fields: dict[str, Any], name: str) -> str | None:
    if name not in fields:
        return f"__doc_anchors__ names '{name}', which is not one of its fields"
    if not _str_or_str_list(fields[name].annotation):
        return f"__doc_anchors__ field '{name}' is declared {fields[name].annotation!r}, not str or list[str]"
    return None


def _str_or_str_list(annotation: Any) -> bool:
    """str or list[str], optional (`| None`) or not."""
    args = [a for a in get_args(annotation) if a is not type(None)] if get_origin(annotation) in (Union, types.UnionType) else [annotation]
    if len(args) != 1:
        return False
    return args[0] is str or (get_origin(args[0]) is list and get_args(args[0]) == (str,))

FILE:tests/store/test_payload_projection.py
"""GO04: a document node carries its projected payload, field_hashes, source_hash and the model's
contract_signature; EdgeIndex.stale sees an edit from outside sldb, a moved contract and an older
shard; a StructuredQuery filters on the `payload` facet without re-extracting a document."""

from __future__ import annotations

import sys

import pytest
import yaml

from sldb import api
from sldb.api.graph import execute_query as api_execute_query
from sldb.core.exceptions import SLDBGraphArgumentError, SLDBModelError
from sldb.runtime.validation import Validator
from sldb.store import documents_hash
from sldb.store.edge_index.compose import compose_edge_index, invalidate_composed_edge_indexes
from sldb.store.edge_index.doc_contribution import build_doc_edges
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.node_ids import EDGE_INDEX_VERSION
from sldb.store.graph.executor import execute_query
from sldb.store.graph.language import FacetFilter, StructuredQuery
from sldb.store.graph.payload_match import where_holds
from sldb.store.io.shards import invalidate_shard_cache
from sldb.store.layout import edges_shard_path
from sldb.store.model_contract import contract_signature, indexed_fields, projected_fields
from sldb.store.models import DocumentEntry, EdgeNodeRecord
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_payload_projection_test_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Ticket(StructuredNLDoc):
    __references__ = {references}
    {extra}
    __template__ = """---
status: ⸢rev•status⸥
priority: ⸢rev•priority⸥
labels: ⸢rev•labels⸥
---

# ⸢rev•title⸥

```yaml
⸢rev,dict•meta⸥
```

⸢rev,table[name,state]•steps⸥
"""
    title: str = Field(description="Title.")
    status: str = Field(description="Status.")
    priority: int = Field(description="Priority.")
    labels: list[str] = Field(description="Labels.")
    meta: dict = Field(description="Free metadata, nested.")
    steps: list[dict[str, str]] = Field(description="Steps, a table.")
'''


def _payload(title: str, status: str) -> dict:
    return {"title": title, "status": status, "priority": 2, "labels": ["x", "y"], "meta": {"k": "v"}, "steps": [{"name": "s1", "state": "done"}]}


def _write_models(tmp_path, references: str = '["title"]', extra: str = "") -> None:
    (tmp_path / f"{MODULE}.py").write_text(_MODELS.format(references=references, extra=extra), encoding="utf-8")
    sys.modules.pop(MODULE, None)
    invalidate_runtime_cache()


def _fresh_read() -> None:
    invalidate_composed_edge_indexes()
    invalidate_shard_cache()


@pytest.fixture
def world(tmp_path):
    py = str(tmp_path)
    _write_models(tmp_path)
    sys.path.insert(0, py)
    try:
        root = tmp_path / "world"
        root.mkdir()
        sp = api.init_store(root).store_path
        api.add_model(sp, f"{MODULE}:Ticket", py)
        api.create_document(sp, "Ticket", root / "a.md", _payload("a", "open"), "a", py)
        api.create_document(sp, "Ticket", root / "b.md", _payload("b", "closed"), "b", py)
        yield tmp_path, root, sp, py
    finally:
        sys.path.remove(py)
        sys.modules.pop(MODULE, None)


def _status_is(value: str) -> StructuredQuery:
    return StructuredQuery(filters=[FacetFilter(facet="payload", where=f'status = "{value}"')])


def test_the_index_version_is_5():
    assert EDGE_INDEX_VERSION == "5"


def test_a_written_document_node_exposes_its_projection_and_omits_nested_fields(world):
    _, _, sp, _ = world
    node = api.edge_node(sp, "Ticket:a")
    assert node.payload == {"labels": ["x", "y"], "priority": 2, "status": "open", "title": "a"}
    entry = next(e for e in documents_hash.entries_of(sp, "Ticket") if e.name == "a")
    assert node.field_hashes == entry.field_hashes and set(node.field_hashes) >= {"meta", "steps"}
    assert node.source_hash == entry.source_hash != ""
    assert node.contract_signature == contract_signature(sys.modules[MODULE].Ticket) != ""
    sections = [n for n in api.edge_nodes_of_type(sp, "sldb_section") if n.semantics["document_id"] == "Ticket:a"]
    assert sections and all(n.payload == {} and n.source_hash == "" and n.contract_signature == "" for n in sections)


def test_the_shard_persists_the_four_fields_only_on_the_document_node(world):
    _, _, sp, _ = world
    shard = yaml.safe_load(edges_shard_path(sp, "Ticket", "a").read_text(encoding="utf-8"))
    doc = next(n for n in shard["nodes"] if n["id"] == "sldb://document/Ticket:a")
    assert {"payload", "field_hashes", "source_hash", "contract_signature"} <= set(doc)
    others = [n for n in shard["nodes"] if n["id"] != doc["id"]]
    assert others and not any({"payload", "field_hashes", "source_hash", "contract_signature"} & set(n) for n in others)


def test_status_closed_is_answered_with_zero_extractions(world, monkeypatch):
    _, _, sp, _ = world
    calls = []
    original = Validator.extract
    monkeypatch.setattr(Validator, "extract", lambda self, md: calls.append(1) or original(self, md))
    _fresh_read()
    invalidate_runtime_cache()
    nodes = api_execute_query(sp, _status_is("closed"))
    assert [n.id for n in nodes] == ["sldb://document/Ticket:b"]
    assert calls == []


def test_existing_facets_answer_as_before_and_nodes_show_no_new_keys(world):
    _, _, sp, _ = world
    query = StructuredQuery(filters=[FacetFilter(facet="identity", where='node_type = "Ticket"')])
    nodes = api_execute_query(sp, query)
    assert [n.id for n in nodes] == ["sldb://document/Ticket:a", "sldb://document/Ticket:b"]
    assert "payload" not in nodes[0].model_dump()


def test_a_filter_on_a_field_not_projected_is_a_query_error_naming_it(world):
    _, _, sp, _ = world
    for field in ("meta", "steps", "nonexistent"):
        query = StructuredQuery(filters=[FacetFilter(facet="payload", where=f"has({field})")])
        with pytest.raises(SLDBGraphArgumentError, match=repr(field)):
            api_execute_query(sp, query)


def _doc(id_: str, payload: dict) -> EdgeNodeRecord:
    return EdgeNodeRecord(id=f"sldb://document/M:{id_}", node_type="M", payload=payload)


def test_a_projectable_field_absent_from_every_payload_gives_the_empty_set():
    index = EdgeIndex(nodes={n.id: n for n in [_doc("a", {"s": "x"}), _doc("b", {})]}, payload_fields={"M": ["s", "owner"]})
    query = StructuredQuery(filters=[FacetFilter(facet="payload", where='owner = "z"')])
    assert execute_query(index, query) == []


def test_only_document_nodes_match_a_payload_filter():
    tag = EdgeNodeRecord(id="sldb://semantic_tag/t", node_type="semantic_tag")
    index = EdgeIndex(nodes={n.id: n for n in [_doc("a", {"s": "x"}), _doc("b", {}), tag]}, payload_fields={"M": ["s"]})
    query = StructuredQuery(filters=[FacetFilter(facet="payload", where="not has(s)")])
    assert [n.id for n in execute_query(index, query)] == ["sldb://document/M:b"]


@pytest.mark.parametrize(("value", "where", "expected"), [
    (None, "not has(f)", True), (None, "has(f)", False),
    (None, 'f != "x"', False), (None, '"x" in f', False), (None, "f > 1", False), (None, 'f ~ "^x"', False),
    (["a", "b"], '"a" in f', True), (["a", "b"], '"c" in f', False), (["a", "b"], 'f = ["a", "b"]', True),
    (["a", "b"], 'f = "a"', False), (["a", "b"], 'f != "a"', True), (["a"], "f > 0", False), (["a"], "f < 9", False),
    (["a"], 'f ~ "^a"', False), (["a"], "not has(f)", False), (["a"], "has(f)", True),
    ([], "f = []", True), (1, "f = 1.0", True), (True, "f = 1", True), ("b", 'f > "a"', True), ("b", "f > 1", False),
    ("abc", 'f ~ "^ab"', True), (3, "f < 5", True),
])
def test_payload_operators_follow_the_contract(value, where, expected):
    payload = {} if value is None else {"f": value}
    assert where_holds(where, payload) is expected


def test_an_edit_from_outside_sldb_is_stale_and_the_rebuild_updates_the_projection(world):
    _, root, sp, py = world
    path = root / "a.md"
    path.write_text(path.read_text(encoding="utf-8").replace("status: open", "status: closed"), encoding="utf-8")
    assert "Ticket:a" in api.load_edge_index(sp).stale
    api.update_store_indexes(sp, py)
    assert api.edge_node(sp, "Ticket:a").payload["status"] == "closed"
    assert api.load_edge_index(sp).stale == []


def test_a_new_references_entry_is_stale_and_the_rebuild_takes_it(world):
    tmp_path, _, sp, py = world
    assert api.load_edge_index(sp).stale == []
    _write_models(tmp_path, references='["title", "status"]')
    assert sorted(api.load_edge_index(sp).stale) == ["Ticket:a", "Ticket:b"]
    api.rebuild_edges(sp, py)
    assert api.load_edge_index(sp).stale == []
    assert api.edge_node(sp, "Ticket:a").contract_signature == contract_signature(sys.modules[MODULE].Ticket)


def test_a_version_4_shard_is_stale_on_open_and_rebuilt_on_the_next_write(world):
    _, root, sp, py = world
    path = edges_shard_path(sp, "Ticket", "a")
    shard = yaml.safe_load(path.read_text(encoding="utf-8"))
    shard["edges_version"] = shard["edges_version"].replace("5|", "4|", 1)
    for node in shard["nodes"]:
        for key in ("payload", "field_hashes", "source_hash", "contract_signature"):
            node.pop(key, None)
    path.write_text(yaml.safe_dump(shard, sort_keys=False, allow_unicode=True), encoding="utf-8")
    _fresh_read()
    assert api.load_edge_index(sp).stale == ["Ticket:a"]
    api.create_document(sp, "Ticket", root / "c.md", _payload("c", "open"), "c", py)
    _fresh_read()
    assert yaml.safe_load(path.read_text(encoding="utf-8"))["edges_version"].startswith("5|")
    assert api.edge_node(sp, "Ticket:a").payload["status"] == "open"
    assert api.load_edge_index(sp).stale == []


def test_indexed_restricts_the_projection(world):
    tmp_path, root, sp, py = world
    _write_models(tmp_path, extra='__indexed__ = ["status", "labels"]')
    api.create_document(sp, "Ticket", root / "c.md", _payload("c", "closed"), "c", py)
    assert api.edge_node(sp, "Ticket:c").payload == {"labels": ["x", "y"], "status": "closed"}
    query = StructuredQuery(filters=[FacetFilter(facet="payload", where="priority = 2")])
    with pytest.raises(SLDBGraphArgumentError, match="'priority'"):
        api_execute_query(sp, query)


@pytest.mark.parametrize(("indexed", "field"), [('["meta"]', "meta"), ('["steps"]', "steps"), ('["ghost"]', "ghost")])
def test_an_indexed_name_that_cannot_be_projected_fails_when_the_model_loads(tmp_path, indexed, field):
    _write_models(tmp_path, extra=f"__indexed__ = {indexed}")
    sys.path.insert(0, str(tmp_path))
    try:
        with pytest.raises(SLDBModelError, match=f"Ticket.*'{field}'"):
            api.resolve_model_ref(f"{MODULE}:Ticket", str(tmp_path))
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def test_projected_fields_and_the_signature_follow_the_class(tmp_path):
    _write_models(tmp_path)
    sys.path.insert(0, str(tmp_path))
    try:
        ticket = api.resolve_model_ref(f"{MODULE}:Ticket", str(tmp_path))
        assert indexed_fields(ticket) is None
        assert projected_fields(ticket) == ["labels", "priority", "status", "title"]
        before = contract_signature(ticket)
        ticket.__containment__ = {"steps": ["Ticket"]}
        assert contract_signature(ticket) != before
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def test_a_model_that_cannot_be_loaded_projects_nothing_and_signs_empty(world):
    _, _, sp, _ = world
    doc = DocumentEntry(name="a", path="a.md", hash_c="h", field_hashes={"title": "t"})
    shard = build_doc_edges("Ticket", doc, [], lambda: None, None)
    node = next(n for n in shard.nodes if n.id == "sldb://document/Ticket:a")
    assert (node.payload, node.contract_signature, node.source_hash, node.field_hashes) == ({}, "", "h", {"title": "t"})
    _fresh_read()
    assert sorted(compose_edge_index(sp, model_type_of=lambda ref, root: None).stale) == ["Ticket:a", "Ticket:b"]

FILE:tests/api/test_doc_anchors.py
"""GO07: document anchors pinned with the target's contract hash (docs/architecture/anchoring.md §6).

A Review's `subject` (in `__doc_anchors__`) anchors a TaskDoc whose `__contract__` is title and
status; `notes` is outside it. The save pins, the composed index derives `subject__anchor_state`
(never written to a shard), `anchors check` reports what moved as alerts, and the rules
language reads it through `^subject`. A malformed form or model definition is refused.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from pydantic import Field, ValidationError

from sldb import StructuredNLDoc, api
from sldb.api.rules.rule_graph import rule_graph
from sldb.cli import main
from sldb.core.exceptions import SLDBModelError
from sldb.models.provenance import Provenance
from sldb.models.provenance_block import attach_block, read_block
from sldb.store.edge_index.doc_anchor_states import field_states
from sldb.store.edge_index.node_ids import EDGE_INDEX_VERSION
from sldb.store.graph.language.contract_hash import contract_hash
from sldb.store.layout import edges_shard_path

MODULE = "sldb_go07_doc_anchor_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class TaskDoc(StructuredNLDoc):
    __contract__ = ["title", "status"]
    __template__ = "---\\nstatus: ⸢rev•status⸥\\nnotes: ⸢rev•notes⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(default="", description="Status.")
    notes: str = Field(default="", description="Free notes, outside the contract.")


class Review(StructuredNLDoc):
    __doc_anchors__ = ["subject"]
    __template__ = "---\\nsubject: ⸢rev•subject⸥\\nverdict: ⸢rev•verdict⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    subject: str = Field(default="", description="The reviewed document.")
    verdict: str = Field(default="", description="accepted or rejected.")


class Bundle(StructuredNLDoc):
    __doc_anchors__ = ["subjects"]
    __template__ = "---\\nsubjects: ⸢rev•subjects⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    subjects: list[str] = Field(default_factory=list, description="Anchored documents.")


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''
ACCEPTED = 'any(^subject: anchor_state = "intact" and verdict = "accepted")'
TASK = {"title": "b", "status": "open", "notes": ""}


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("TaskDoc", "Review", "Bundle", "Note"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.create_document(self.store, "TaskDoc", self.root / "b.md", TASK, "b", self.py)

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def save(self, model: str, name: str, payload: dict) -> None:
        api.save_document_payload(self.store, model, name, payload, self.py)

    def payload(self, export_id: str) -> dict:
        return api.edge_node(self.store, export_id).payload

    def b_hash(self) -> str:
        return contract_hash(sys.modules[MODULE].TaskDoc, api.edge_node(self.store, "TaskDoc:b").field_hashes)

    def review(self, name: str = "a", subject: str = "doc:TaskDoc:b", verdict: str = "accepted") -> None:
        payload = {"title": name, "subject": subject, "verdict": verdict}
        self.create("Review", name, payload)
        self.save("Review", name, payload)

    def codes(self) -> list[tuple[str, str, str]]:
        return [(f.level, f.code, f.subject) for f in api.check_doc_anchors(self.store, self.py)]

    def holds(self, predicate: str = ACCEPTED, node: str = "TaskDoc:b") -> str:
        return rule_graph(self.store).holds(predicate, node)["holds"]


@pytest.fixture
def world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def test_a_saved_anchor_is_pinned_with_the_target_contract_hash(world: World) -> None:
    world.review()
    assert world.payload("Review:a")["subject"] == f"doc:TaskDoc:b@sha256:{world.b_hash()}"
    assert world.payload("Review:a")["subject__anchor_state"] == "intact"
    assert world.codes() == []


def test_the_anchor_follows_the_target_contract_and_anchors_check_alerts(world: World, capsys) -> None:
    world.review()
    world.save("TaskDoc", "b", {**TASK, "notes": "outside the contract"})
    assert world.payload("Review:a")["subject__anchor_state"] == "intact"
    world.save("TaskDoc", "b", {**TASK, "status": "closed"})
    assert world.payload("Review:a")["subject__anchor_state"] == "changed"
    assert world.codes() == [("alert", "anchors/doc_changed", "Review:a")]
    found = api.check_doc_anchors(world.store, world.py)[0]
    assert found.document == "a.md" and "subject" in found.what and "TaskDoc:b" in found.what and "changed" in found.what and found.fix == ""
    assert main(["--envelope", "anchors", "check", "--store", str(world.store), "--pythonpath", world.py, "--format", "json"]) == 0
    envelope = json.loads(capsys.readouterr().out)
    assert [w["code"] for w in envelope["warnings"]] == ["anchors/doc_changed"]
    api.delete_document(world.store, "b", world.py)
    assert world.payload("Review:a")["subject__anchor_state"] == "lost"
    assert world.codes() == [("alert", "anchors/doc_lost", "Review:a")]


def test_an_anchor_to_a_missing_target_is_saved_without_hash_and_pinned_by_a_later_write(world: World) -> None:
    world.review(subject="doc:TaskDoc:later")
    assert world.payload("Review:a")["subject"] == "doc:TaskDoc:later"
    world.create("TaskDoc", "later", {**TASK, "title": "later"})
    assert world.payload("Review:a")["subject__anchor_state"] == "lost"
    world.save("Review", "a", {"title": "a", "subject": "doc:TaskDoc:later", "verdict": "accepted"})
    assert world.payload("Review:a")["subject"].startswith("doc:TaskDoc:later@sha256:")
    assert world.payload("Review:a")["subject__anchor_state"] == "intact"


def test_the_subject_anchor_is_an_edge_and_the_derived_state_never_reaches_the_shard(world: World) -> None:
    world.review()
    edges = api.edges_from(world.store, "Review:a", "references")
    assert [(e.target, e.metadata["field"]) for e in edges] == [("sldb://document/TaskDoc:b", "subject")]
    shard = edges_shard_path(world.store, "Review", "a").read_text(encoding="utf-8")
    assert "__anchor_state" not in shard and EDGE_INDEX_VERSION == "5"


def test_the_rule_reads_anchor_state_through_the_inverse_subject(world: World) -> None:
    assert world.holds() == "false"
    world.review("r1", verdict="rejected")
    assert world.holds() == "false"
    world.review("r2", verdict="accepted")
    assert world.holds() == "true"
    world.save("TaskDoc", "b", {**TASK, "status": "closed"})
    assert world.holds() == "false"


def test_a_list_field_has_one_state_and_one_edge_per_anchor(world: World) -> None:
    payload = {"title": "set", "subjects": ["doc:TaskDoc:b", "doc:TaskDoc:ghost"]}
    world.create("Bundle", "set", payload)
    world.save("Bundle", "set", payload)
    assert world.payload("Bundle:set")["subjects__anchor_state"] == ["intact", "lost"]
    assert [e.target for e in api.edges_from(world.store, "Bundle:set", "references")] == ["sldb://document/TaskDoc:b"]
    assert world.codes() == [("alert", "anchors/doc_lost", "Bundle:set")]
    assert field_states(["doc:A:x", "", "  "], lambda _: (True, None)) == ["lost", None, None]


def test_a_provenance_from_anchor_is_pinned_and_alerts_when_the_target_contract_moves(world: World) -> None:
    world.create("Note", "c", {"title": "c"})
    path = world.root / "c.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(attach_block(text, {**(read_block(text) or {}), "from": ["code:src/x.py::f", "doc:TaskDoc:b"]}), encoding="utf-8")
    world.save("Note", "c", {"title": "c"})
    assert read_block(path.read_text(encoding="utf-8"))["from"] == ["code:src/x.py::f", f"doc:TaskDoc:b@sha256:{world.b_hash()}"]
    assert world.codes() == []
    world.save("TaskDoc", "b", {**TASK, "status": "closed"})
    assert world.codes() == [("alert", "anchors/provenance_changed", "Note:c")]
    api.delete_document(world.store, "b", world.py)
    assert world.codes() == [("alert", "anchors/provenance_lost", "Note:c")]


def test_a_value_that_is_not_an_anchor_is_refused_when_written(world: World) -> None:
    with pytest.raises(Exception, match="subject.*not a document anchor"):
        world.create("Review", "bad", {"title": "bad", "subject": "TaskDoc:b", "verdict": ""})
    world.review()
    with pytest.raises(Exception, match="subject.*not a document anchor"):
        world.save("Review", "a", {"title": "a", "subject": "see TaskDoc:b", "verdict": ""})


@pytest.mark.parametrize("value", ["TaskDoc:b", "doc:TaskDoc", "doc:TaskDoc:b@sha256:", "doc:TaskDoc:b@sha256:abc", "doc:TaskDoc:b@sha256:" + "g" * 64, "doc:TaskDoc:b@md5:" + "a" * 64])
def test_a_malformed_anchor_form_is_rejected_in_a_field_and_in_from(world: World, value: str) -> None:
    review = sys.modules[MODULE].Review
    with pytest.raises(ValidationError, match="subject"):
        review(title="x", subject=value)
    if value.startswith("doc:"):
        with pytest.raises(ValidationError, match="from"):
            Provenance(from_=[value])


def test_the_accepted_forms_and_from_items_that_are_not_doc_anchors(world: World) -> None:
    review = sys.modules[MODULE].Review
    assert review(title="x", subject="").subject == ""
    assert review(title="x", subject="doc:TaskDoc:b@sha256:" + "a" * 64).subject.endswith("a" * 64)
    assert Provenance(from_=["code:src/x.py::f", "whatever"]).from_ == ["code:src/x.py::f", "whatever"]


@pytest.mark.parametrize(
    ("body", "reason"),
    [
        ('__doc_anchors__ = ["count"]\n    count: int = Field(default=0, description="A number.")', "count"),
        ('__doc_anchors__ = ["ghost"]\n    title: str = Field(description="Title.")', "ghost"),
        ('__doc_anchors__ = ["meta"]\n    meta: dict = Field(default_factory=dict, description="Nested.")', "meta"),
        ('subject__anchor_state: str = Field(default="", description="Reserved.")', "reserved suffix"),
    ],
)
def test_an_invalid_model_definition_is_refused_when_loaded(tmp_path: Path, body: str, reason: str) -> None:
    module = "sldb_go07_bad_definition"
    (tmp_path / f"{module}.py").write_text(f"from pydantic import Field\nfrom sldb import StructuredNLDoc\n\n\nclass Bad(StructuredNLDoc):\n    {body}\n", encoding="utf-8")
    try:
        with pytest.raises(SLDBModelError, match=f"Bad.*{reason}"):
            api.resolve_model_ref(f"{module}:Bad", str(tmp_path))
    finally:
        sys.modules.pop(module, None)


def test_optional_str_and_list_fields_are_valid_anchor_fields() -> None:
    class Fine(StructuredNLDoc):
        __doc_anchors__ = ["one", "many"]
        one: str | None = Field(default=None, description="One.")
        many: list[str] = Field(default_factory=list, description="Many.")

    from sldb.store.model_contract import doc_anchor_fields

    assert doc_anchor_fields(Fine) == ["one", "many"]

FILE:instruccion
Cold-bundle de la tarea task-contract-signature-cubre-indexed-doc-anchors-y-contract-y-un-campo-no-puede-ser-a-la-vez-referencia: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/store/test_payload_projection.py
- TMPDIR=/dev/shm pytest -q tests/api/test_doc_anchors.py
- TMPDIR=/dev/shm sldb stores build --check --store .sldb

