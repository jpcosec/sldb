FILE:desk/tasks/task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1.md
---
sldb:
  by: agent
  at: '2026-11-11T12:47:53Z'
  authority: generated
  via: create_document
id: task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1
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
- src/sldb/api/stores/tag_namespace.py
- src/sldb/api/stores/store_declaration.py
- src/sldb/api/rules/builtin_tag_rules.py
- src/sldb/api/tags/
- src/sldb/cli/commands/tags.py
- tests/
- docs/architecture/tags.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-tag-namespaces-acotado-por-modelos-y-tag-folder-con-segmentos-vac-os-bloquea-cc35d.md
---

# GD27 para deskops: anchored_by con valor sin namespace y alcance de las reglas de tags por modelos (H1-H2); tag_folder estricto documentado (H3)

## Rationale

_Explain why this task exists or the business driver behind it._

Prioridad del coordinador: es lo que más destraba. Libera el resto de CC35d de deskops (dominios, namespaces y tag_folder por la API de sldb) y con eso el camino a CC51.

## Goal

_Describe the concrete result this task must produce._

anchored_by acepta un campo con el valor pelado (value: bare); la declaración del store acota las reglas de tags a unos modelos (tag_models); tag_folder sigue estricto y documentado.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/stores/tag_namespace.py, src/sldb/api/stores/store_declaration.py, src/sldb/api/rules/builtin_tag_rules.py, src/sldb/api/tags/, src/sldb/cli/commands/tags.py, tests/, docs/architecture/tags.md, CHANGELOG.md. Fuera: cambios en deskops (los hace CC35d resto).

## Implementation Path

_Outline the expected implementation route or affected surface._

Prioridad del coordinador (2026-11-11): libera el resto de CC35d de deskops (drawer 'CC35d resto', DO7) y con eso el camino a CC51. Drawer de origen: 6b34cd5f (GD27 para deskops, H1-H3, hallado por CC35d de deskops, wt/cc35d 568d2140, runs/subagents/cc35d-worker-report.md).

PROBLEMA (de CC35d):
- B1/H1: el anchored_by de GD27 exige que el campo del documento ancla valga el tag completo ('domain:a.b'). CrossroadDoc.path de deskops vale 'a.b'. Con el crossroad existente, la API da igual 5 hallazgos y tag_tree devuelve roots=[].
- B2/H2: declarar tag_namespaces desde desk/tag-namespaces.yaml de deskops da 115 errores nuevos (workspace 78, pill-type 29, ...), y on_write rechazaría tareas y pills. Hoy la familia builtin:tag_namespace exige que todo namespace usado en cualquier documento del store esté declarado, y deskops solo registra los namespaces de los átomos.
- H3: tag_folder da ValueError con segmentos vacíos ('a..b', 'a.'), y deskops los ignoraba.

CAUSA: src/sldb/api/stores/tag_namespace.py y src/sldb/api/rules/builtin_tag_rules.py (anchors_of compara el campo con el tag completo; las reglas de la familia corren sobre todos los documentos locales con tags).

ARREGLO (g1-g4):
g1 (H1, anchored_by con valor pelado): anchored_by admite una clave opcional 'value' con 'tag' (por defecto, el comportamiento de hoy) o 'bare' (el campo guarda el valor sin namespace, 'a.b'). anchors_of, tag_tree y las reglas comparan f'{name}:{field}' cuando es 'bare'. Las anchored_by existentes no cambian.
g2 (H2, alcance por modelos): la declaración del store admite 'tag_models: [Modelo, ...]', opcional. Si está, la familia builtin:tag_namespace (namespace no declarado, prefijos anclados, etc.) solo evalúa documentos de esos modelos o de sus descendientes (base_models del índice), y los tags de otros modelos no se chequean. Si no está, todo sigue como hoy. tag_tree y tag_check respetan el mismo alcance. Va a nivel store y no por namespace porque el problema de deskops es un namespace no declarado, que no tiene entrada propia donde decir 'no aplica'.
g3 (H3, decisión revisable del coordinador): tag_folder sigue estricto (ValueError con segmentos vacíos). Lo adapta deskops en 'CC35d resto', prohibiendo esos tags en su patrón de átomo. Este nodo solo documenta la regla en docs/architecture/tags.md.
g4 (tests): (a) un store con CrossroadDoc.path 'a.b' y anchored_by {model: CrossroadDoc, field: path, value: bare}: tag_tree da la raíz y el check no da hallazgos por los prefijos anclados; (b) un store con tag_models [AtomDoc] y tareas con tags 'workspace:x' no declarados: sin hallazgos en las tareas y con hallazgo en un átomo con un namespace no declarado; (c) sin 'value' ni 'tag_models', todo igual que hoy (tests existentes de tags y reglas en verde).

VALIDACIÓN: el worker corre los tests que toca, los de tests/ sobre tags y reglas (grep tag_namespace, anchored_by, tag_tree, tag_check), tests/test_clean_code_rules.py (80 líneas efectivas por archivo, 10 de lógica por función; no se suben límites) y tools/check.sh --fast. Un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml. Los 7 pasos del workflow los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test anchored_by value bare con CrossroadDoc.path a.b: tag_tree con raíz y check sin hallazgos
- Test tag_models [AtomDoc]: tareas con namespaces no declarados sin hallazgos; átomo sí
- Sin value ni tag_models, tests existentes de tags y reglas en verde
- test_clean_code_rules y check.sh --fast
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

g1-g4 hechos con tests verdes; docs/architecture/tags.md y CHANGELOG.

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

FILE:src/sldb/api/stores/tag_namespace.py
"""One entry of `tag_namespaces` in `.sldb/store.yaml` (GD27, docs/architecture/tags.md).

A tag `name:value` belongs to the namespace `name` (the text before its first colon). The
namespace says whether the value's dots form a hierarchy (`hierarchical`), whether the value
places the document in a folder (`folder_axis`, read by `tag_folder`) and which documents
anchor its values (`anchored_by: {model, field}`: a local document of `model` whose `field`
is the tag). The checks run as the rule family `builtin:tag_namespace:<name>`.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, SerializerFunctionWrapHandler, field_validator, model_serializer

from sldb.store.semantic_tags import split_namespace, tag_prefixes

ANCHOR_KEYS = ("model", "field")


class TagNamespace(BaseModel):
    """What a store declares of one tag namespace."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="The namespace: what precedes the first colon of its tags; no colon, no blank.")
    hierarchical: bool = Field(default=True, description="Whether `a.b.c` is a path whose prefixes `a` and `a.b` are tags too; false means the value is one piece, without prefixes.")
    folder_axis: bool = Field(default=False, description="Declarative: the value of a tag of this namespace is the document's folder (`tag_folder`).")
    anchored_by: dict[str, str] | None = Field(default=None, description="`{model, field}`: every tag the namespace requires must be the `field` of a local document of `model`.")

    @field_validator("name")
    @classmethod
    def _is_a_namespace(cls, value: str) -> str:
        if not value.strip() or ":" in value or value != value.strip():
            raise ValueError(f"tag namespace name {value!r} must be non-blank, without colons or surrounding spaces")
        return value

    @field_validator("anchored_by")
    @classmethod
    def _names_model_and_field(cls, value: dict[str, str] | None) -> dict[str, str] | None:
        if value is not None and (set(value) != set(ANCHOR_KEYS) or not all(str(value[k]).strip() for k in ANCHOR_KEYS)):
            raise ValueError(f"anchored_by must be {{model, field}} with non-blank values, not {value!r}")
        return value

    @model_serializer(mode="wrap")
    def _without_absent_anchor(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        """A namespace without `anchored_by` dumps without the key (as `store.yaml` is written)."""
        return {key: value for key, value in handler(self).items() if value is not None}

    def required(self, tag: str) -> list[str]:
        """The tags an anchor must exist for so `tag` is placed: its value's prefixes (the
        value included) when hierarchical, else the value alone; each with the namespace."""
        value = split_namespace(tag)[1]
        values = tag_prefixes(value) if self.hierarchical else [value]
        return [f"{self.name}:{v}" for v in values]


def unique_namespaces(value: list[TagNamespace]) -> list[TagNamespace]:
    """`tag_namespaces` as declared, once no name repeats (a `ValueError` naming the repeated ones)."""
    names = [namespace.name for namespace in value]
    if len(names) != len(set(names)):
        raise ValueError(f"tag_namespaces declares a name twice: {sorted(n for n in set(names) if names.count(n) > 1)}")
    return value

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
OPTIONAL_KEYS = (*SCAFFOLD_KEYS, "project_graph", "tag_namespaces")


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
        """A declaration without folders, seeds, project_graph or tag_namespaces dumps as before they existed; a seed dumps only the keys it was written with (a namespace does the same on its own)."""
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

FILE:src/sldb/api/rules/builtin_tag_rules.py
"""The built-in rule family `builtin:tag_namespace:<name>` (GD27, docs/architecture/tags.md):
the `tag_namespaces` of `store.yaml`, checked where the RuleDocs are (`on_write`, `on_check`,
`rules check`, `rules explain`) and reported as their findings (code `rules/<id>`).

On a document, the rule of namespace `<name>` holds when every tag `<name>:value` it carries
names a declared namespace and, with `anchored_by`, every tag the namespace requires for the
value (`TagNamespace.required`) is the `field` of a local document of `model`, the document
being written included. Without `tag_namespaces` the family reads nothing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.rules.rule_graph import RuleGraph, rule_graph
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_declaration import declaration_path, load_declaration
from sldb.api.stores.tag_namespace import TagNamespace
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.core.finding import Finding
from sldb.store.semantic_tags import namespaced_tags, split_namespace

PREFIX = "builtin:tag_namespace:"


def tag_rules(store_path: Path) -> dict[str, TagNamespace]:
    """The declared namespaces by name; empty without a declaration or without the key."""
    if not declaration_path(store_path).is_file():
        return {}
    return {namespace.name: namespace for namespace in load_declaration(store_path).tag_namespaces}


def store_findings(store: str | Path | None) -> list[Finding]:
    """The family over every local document; a store without namespaces is not read."""
    store_path = open_store(store, mode="readonly").store_path
    return family_findings(rule_graph(store_path, None), None) if tag_rules(store_path) else []


def family_findings(graph: RuleGraph, nodes: list[str] | None) -> list[Finding]:
    """The findings on `nodes` (every local document when None), by document then namespace."""
    rules = tag_rules(graph.store_path)
    found = [(node, name) for node in (sorted(graph.local) if nodes is None else nodes) for name in _names(graph, node)] if rules else []
    results = [(name, evaluate(graph, rules, name, node)) for node, name in found]
    return [_finding(graph, name, result) for name, result in results if result["holds"] != "true"]


def explain(graph: RuleGraph, rule: str, node: str) -> dict[str, Any]:
    """`rules explain` of a built-in rule: its eval finding on `node`; no namespaces, no rule."""
    rules = tag_rules(graph.store_path)
    if not rules:
        raise SLDBDocumentTargetError(f"Unknown document target: {rule}")
    return {"rule": rule, "subject": node, "finding": evaluate(graph, rules, rule.removeprefix(PREFIX), node)}


def evaluate(graph: RuleGraph, rules: dict[str, TagNamespace], name: str, node: str) -> dict[str, Any]:
    """The eval finding (node, holds, clause, seen) of `builtin:tag_namespace:<name>` on `node`."""
    tags = [tag for namespace, tag in namespaced_tags(payload_of(graph, node)) if namespace == name]
    if name not in rules:
        return _found(node, not tags, "namespace declared", {"namespace": name, "tags": tags, "declared": sorted(rules)})
    if rules[name].anchored_by is None:
        return _found(node, True, "namespace declared", {"namespace": name, "tags": tags})
    missing = _missing(rules[name], tags, anchors_of(graph, rules[name]))
    clause = f"each prefix anchored by {rules[name].anchored_by['model']}.{rules[name].anchored_by['field']}"
    return _found(node, not missing, clause, {"namespace": name, "tags": tags, "missing": missing})


def anchors_of(graph: RuleGraph, namespace: TagNamespace) -> dict[str, str]:
    """Anchor tag -> export id of the local document of `anchored_by.model` whose `field` is
    that tag, as `graph` reads it (a payload being written included)."""
    model, field = namespace.anchored_by["model"], namespace.anchored_by["field"]
    found: dict[str, str] = {}
    for node in sorted(graph.local | ({graph.override[0]} if graph.override else set())):
        item = graph.located(node)[1]
        value = item["payload"].get(field) if model in (item["model"], *item["base_models"]) else None
        if isinstance(value, str) and split_namespace(value)[0] == namespace.name:
            found.setdefault(value, node)
    return found


def payload_of(graph: RuleGraph, node: str) -> dict[str, Any]:
    """The payload `graph` reads for `node` (its projection, or the payload overriding it)."""
    return graph.located(node)[1]["payload"]


def _names(graph: RuleGraph, node: str) -> list[str]:
    return sorted({namespace for namespace, _ in namespaced_tags(payload_of(graph, node))})


def _missing(namespace: TagNamespace, tags: list[str], anchors: dict[str, str]) -> list[str]:
    """The required tags without an anchor, top-down, once each."""
    missing: list[str] = []
    for tag in tags:
        missing += [t for t in namespace.required(tag) if t not in anchors and t not in missing]
    return missing


def _found(node: str, holds: bool, clause: str, seen: dict[str, Any]) -> dict[str, Any]:
    return {"node": node, "holds": "true" if holds else "false", "clause": clause, "seen": seen}


def _finding(graph: RuleGraph, name: str, found: dict[str, Any]) -> Finding:
    from sldb.api.rules.rules_check import explanation

    what = explanation({"name": PREFIX + name}, found)
    return Finding("error", f"rules/{PREFIX}{name}", found["node"], what, "", graph.semantics(found["node"]).get("path"))

FILE:src/sldb/cli/commands/tags.py
"""`sldb tags namespaces|tree|check`: thin printing wrappers over `sldb.api.tags`.

`check` reports its findings exactly as `sldb rules check` does (`{"findings": [...]}` in JSON,
one line each in text, the tally at the end) and exits 1 only when one is an error.
"""

from __future__ import annotations

from typing import Any

from sldb.api.tags import tag_check, tag_namespaces, tag_tree
from sldb.cli import alert_sink
from sldb.cli.output_format import emit
from sldb.core.exceptions import SLDBError


class TagsCLI:
    """The tag namespaces of a store through the CLI."""

    def run(self, args: Any) -> int:
        commands = {"namespaces": self.namespaces, "tree": self.tree, "check": self.check}
        if args.tags_command not in commands:
            raise SLDBError(f"Unknown command: {args.tags_command}")
        return commands[args.tags_command](args)

    def namespaces(self, args: Any) -> int:
        found = tag_namespaces(args.store)
        emit({"namespaces": found}, args.format, "\n".join(_namespace_line(n) for n in found) or "No tag namespaces declared")
        return 0

    def tree(self, args: Any) -> int:
        tree = tag_tree(args.store, args.namespace)
        lines = [line for root in tree["roots"] for line in _tree_lines(root, 0)]
        lines += [f"orphan: {o['tag']} used by {', '.join(o['used_by'])}" for o in tree["orphans"]]
        lines += [f"unplaced: {u['tag']} ({u['document']})" for u in tree["unplaced"]]
        emit(tree, args.format, "\n".join(lines) or f"No tags in namespace {tree['namespace']}")
        return 0

    def check(self, args: Any) -> int:
        findings = tag_check(args.store)
        text = args.format == "text"
        if not text:
            emit({"findings": [f.as_dict() for f in findings]}, args.format, "")
        alert_sink.report(findings, text=text)
        if text:
            print(f"tags check: {alert_sink.tally(findings) or 'sin hallazgos'}")
        return 1 if any(f.level == "error" for f in findings) else 0


def _namespace_line(namespace: dict[str, Any]) -> str:
    anchored = namespace.get("anchored_by")
    flags = [k for k in ("hierarchical", "folder_axis") if namespace.get(k)]
    return f"{namespace['name']}: {', '.join(flags) or 'flat'}" + (f"; anchored by {anchored['model']}.{anchored['field']}" if anchored else "")


def _tree_lines(node: dict[str, Any], depth: int) -> list[str]:
    line = "  " * depth + node["tag"] + (f" ({node['document']})" if node["document"] else "")
    return [line] + [l for child in node["children"] for l in _tree_lines(child, depth + 1)]

FILE:docs/architecture/tags.md
# Tag namespaces: declared in `store.yaml`, checked as a rule family, read as a tree

Node GD27 of the plan `generalizar-desde-deskops`. A document's tags (`tags` or
`semantic_tags`) may carry a namespace: `area:a.b` belongs to `area`, the text before the
first colon; what follows is the value (it may hold colons). A tag without a colon belongs to
no namespace and is never checked. The store declares its namespaces in `.sldb/store.yaml`,
beside `models` and `include`:

```yaml
tag_namespaces:
- name: area                 # what precedes the first colon
  hierarchical: true         # a.b.c is a path: a, a.b and a.b.c are tags too (default)
  folder_axis: true          # declarative: the value is the document's folder (tag_folder)
  anchored_by:               # optional: every required tag must be the `tag` of an Anchor
    model: Anchor
    field: tag
- name: kind
  hierarchical: false        # the value is one piece: no prefixes
```

`sldb.api.TagNamespace` (`src/sldb/api/stores/tag_namespace.py`) is one entry; its invariants
are its validators: a name without colon or blanks, `anchored_by` exactly `{model, field}`,
no other key; `StoreDeclaration.tag_namespaces` refuses a repeated name. A declaration without
the key reads and writes as before it existed. `sldb tags namespaces` lists what is declared.

## What the family checks

The checks are the built-in rule family `builtin:tag_namespace:<name>`
(`src/sldb/api/rules/builtin_tag_rules.py`), one rule per namespace a document names, not a
RuleDoc of the user (q3: the rules language has no anchor predicate). On a document, the rule
of namespace `<name>` holds when:

1. `<name>` is declared (`clause: namespace declared`; `seen: {namespace, tags, declared}`);
2. with `anchored_by`, every tag the namespace **requires** for each of its values is the
   `field` of a local document of `model` (`clause: each prefix anchored by Model.field`;
   `seen: {namespace, tags, missing}`, `missing` top-down, once each). A hierarchical
   namespace requires every prefix of the value, the whole value included (`area:a.b.c`
   requires `area:a`, `area:a.b` and `area:a.b.c`); a non-hierarchical one requires the value
   alone. The document being written counts as an anchor of the tag it carries in that field.

Without `anchored_by`, declaring the namespace is all a tag needs. Every finding is an
`error` with code `rules/builtin:tag_namespace:<name>`, the subject is the document's export
id and `what` is `<clause> (seen: <seen>)`, the form of a RuleDoc's finding (rules.md §4).

The family runs where the RuleDocs run (rules.md §9), also in a store that registers no
`RuleDoc` but declares `tag_namespaces`:

| Moment | Where | Effect |
|---|---|---|
| `on_write` | `save_document_payload` (so `fields update`, `docs update`, `transaction.update`, `apply_batch`, `POST /save`) and `replace_text` | an error is `SLDBRuleViolationError` (`rules/violation`, exit 1) and nothing is written |
| `on_check` | `stores check`, `on_check_findings` | the findings follow the `on_check` RuleDocs' (not cached) |
| `rules check [--subject]` | `rules_check` | the findings follow the RuleDocs', on the same documents |
| `rules explain builtin:tag_namespace:<name> DOC` | `rules_explain` | `{"rule", "subject", "finding": {node, holds, clause, seen}}`, also when it holds; without `tag_namespaces` the rule is an unknown target |
| `tags check` | `tag_check` | the same evaluation as `rules check` filtered to the family; exit 1 on an error |

`create_document` and `track_document_file` evaluate no `on_write` rule (a GO08 gap, q18):
a document created without its anchor is reported by `tags check`, `rules check` and
`stores check`.

## `tag_tree`, `tag_folder`

`sldb.api.tag_tree(store, namespace)` (`sldb tags tree NAMESPACE --format json` emits the same
object, in the envelope's `data`):

```json
{"namespace": "area",
 "roots": [{"tag": "area:a", "document": "Anchor:a",
            "children": [{"tag": "area:a.b", "document": "Anchor:ab", "children": []}]}],
 "orphans": [{"tag": "area:c", "used_by": ["Note:n2"]}],
 "unplaced": [{"tag": "area:a.x", "document": "Anchor:ax"}]}
```

- Everything is limited to the namespace asked; tags are complete (`area:a.b`); each level
  is alphabetical by tag; an undeclared namespace is `SLDBStoreError`.
- With `anchored_by`, `roots` is the anchors' tree: every prefix of an anchored value is a
  node, `document` its anchor's export id or `null` for a prefix without one; `orphans` are
  the tags local documents use that no anchor declares (`used_by`: their export ids);
  `unplaced` are the anchors no local document uses, directly or, when hierarchical, through
  a tag under them (an anchor of `area:a` is placed by a document tagged `area:a.b`).
- Without `anchored_by`, `roots` nests the tags local documents use (`document: null`) and
  both lists are empty. A non-hierarchical namespace has roots without children.

`sldb.api.tag_folder(tag)` is a pure function of the text: `a.b` or `area:a.b` -> `a/b`, one
segment per part (`a` -> `a`); it never reads the store (`folder_axis` is the declaration that
tells a consumer to use it). A blank value, an empty segment (`a..b`, `.a`, `a.`) or a slash
inside a segment is a `ValueError` naming the value.

## API and CLI

- `sldb.api.tag_namespaces(store) -> list[dict]`, `tag_tree(store, namespace) -> dict`,
  `tag_folder(tag) -> str`, `tag_check(store) -> list[Finding]` (also in `sldb.api.tags`);
  `sldb.api.TagNamespace`.
- `sldb.api` re-exports `sldb.api.semantic`: `add_semantic_parent`, `remove_semantic_parent`,
  `add_semantic_equivalence`, `semantic_tag`.
- `sldb tags namespaces | tree NAMESPACE | check` (`--store`, `--pythonpath`, `--format`,
  with envelope). `tags check` prints as `rules check` does (`{"findings": [...]}` in JSON).
- Helpers of the store layer (`src/sldb/store/semantic_tags.py`): `payload_tags`,
  `split_namespace`, `namespaced_tags`, `tag_prefixes`.

## Hypotheses

- The anchors are read from the local store only (linked stores do not anchor).
- `anchors_of` reads every local document per evaluation: a sweep over a store of N
  documents is O(N²) dictionary reads. Enough for the stores seen so far; a cache keyed by the
  rule graph is the next step if it is not.
- `tags check` and `stores check` recompute the family every time (no `.sldb_cache/rules`
  entry): the family has no `content_hash` to key it by.

FILE:instruccion
Cold-bundle de la tarea task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Test anchored_by value bare con CrossroadDoc.path a.b: tag_tree con raíz y check sin hallazgos
- Test tag_models [AtomDoc]: tareas con namespaces no declarados sin hallazgos; átomo sí
- Sin value ni tag_models, tests existentes de tags y reglas en verde
- test_clean_code_rules y check.sh --fast
- 7 pasos del workflow de sldb en clon limpio

