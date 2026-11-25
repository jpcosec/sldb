FILE:desk/tasks/task-gd27-espacios-de-nombres-y-jerarquía-de-tags-reemplazo-de-texto-en-documentos-trackeados.md
---
id: task-gd27-espacios-de-nombres-y-jerarquía-de-tags-reemplazo-de-texto-en-documentos-trackeados
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-gd24-transacción-multi-documento-en-sldb-api-y-save-atómico-absorbe-doc-io-doctransaction
pills: []
files:
- src/sldb/api/stores/store_declaration.py
- src/sldb/api/stores/tag_namespace.py
- src/sldb/api/tags/__init__.py
- src/sldb/api/tags/tag_tree.py
- src/sldb/api/tags/tag_folder.py
- src/sldb/api/tags/tag_check.py
- src/sldb/api/semantic/__init__.py
- src/sldb/api/documents/replace_text.py
- src/sldb/api/__init__.py
- src/sldb/store/semantic_tags.py
- src/sldb/cli/parsers/tags.py
- src/sldb/cli/commands/tags.py
- src/sldb/cli/parsers/docs3.py
- src/sldb/cli/commands/docs.py
- src/sldb/cli/commands/docs_replace.py
- tests/api/test_tags.py
- tests/api/test_replace_text.py
- docs/architecture/tags.md
- docs/architecture/transactions.md
- CHANGELOG.md
- src/sldb/api/rules/builtin_tag_rules.py
- src/sldb/api/rules/rules_on_write.py
- src/sldb/api/rules/rules_check.py
- src/sldb/api/rules/rules_on_check.py
- src/sldb/api/rules/rules_explain.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/generalizar-desde-deskops/dag.yaml
---

# GD27: Espacios de nombres y jerarquía de tags; reemplazo de texto en documentos trackeados

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GD27 del plan desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PG2. Depende de: ['GD24']. Gates requeridos: G_WRITE_API: Transacción y referencias entrantes en sldb.api (satisfied).

## Goal

_Describe the concrete result this task must produce._

StoreDeclaration gana tag_namespaces ({name, hierarchical, folder_axis, anchored_by}); un store que los declara rechaza al escribir un tag de namespace no declarado y un tag jerárquico sin ancla para cada prefijo; sldb.api.tag_tree y tag_folder; sldb.api reexporta sldb.api.semantic; CLI sldb tags namespaces|tree|check; sldb.api.replace_text(store, ref, old, new, *, count=1, transaction=None) con conteo exacto, re-extracción, validación contra el modelo y re-track dentro de sldb.api.transaction; CLI sldb docs replace con envelope; docs/architecture/tags.md y sección en transactions.md.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/stores/store_declaration.py, src/sldb/api/semantic/, src/sldb/api/tags/ (nuevo), src/sldb/api/documents/replace_text.py (nuevo), src/sldb/api/__init__.py, src/sldb/store/semantic_tags.py, src/sldb/cli/parsers/tags.py y commands/tags.py (nuevos), src/sldb/cli/parsers/docs*.py y commands/docs*.py, tests, docs/architecture/tags.md, docs/architecture/transactions.md, CHANGELOG.md. Fuera: editar src/sldb/api/documents/payload_save_steps.py; nombres del caso deskops (domain, atom) en src/sldb/; migrar los tags de deskops (lo hace deskops).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3, GD27). SCOPE: (1) Tags: StoreDeclaration gana tag_namespaces: lista de {name, hierarchical: bool, folder_axis: bool, anchored_by: {model, field} opcional}. Validación al escribir un documento (paso de validación existente, sin tocar payload_save_steps.py: se registra como validador del store): un tag namespace:valor cuyo namespace no está declarado es error si el store declara tag_namespaces (sin la clave, nada cambia); con anchored_by, cada prefijo con punto del valor (la jerarquía de store/semantic_tags.py:35 _prefix_edges) debe tener un documento del modelo anchored_by.model cuyo campo anchored_by.field es ese tag; si falta, error que lista los prefijos faltantes (mecánica de deskops domain_tree.py:80 require_domain_parents, sin sus nombres). Función sldb.api.tag_tree(store, namespace) → {roots: árbol anidado {tag, document, children}, orphans: tags usados sin documento ancla, unplaced: documentos ancla sin uso}; folder_axis: sldb.api.tag_folder(tag) → ruta a/b para a.b (mecánica de atom_tags.py:120). sldb.api.semantic (dag_reads, dag_writes) se reexporta en sldb.api. CLI: sldb tags namespaces, sldb tags tree NAMESPACE, sldb tags check. (2) Reemplazo: sldb.api.replace_text(store, ref, old, new, *, count=1, transaction=None) sobre un documento trackeado o un archivo no modelado bajo la raíz: exige exactamente count apariciones de old (si no, error con el número visto y nada se escribe); en un documento trackeado reescribe los bytes, re-extrae y valida contra el modelo (si no valida, error y nada se escribe) y re-trackea con el mismo modelo y nombre; todo dentro de sldb.api.transaction. CLI sldb docs replace REF --old --new [--count N] con envelope. Doc docs/architecture/tags.md y sección en docs/architecture/transactions.md.

ACCEPTANCE: En un store temporal con tag_namespaces [{name: area, hierarchical: true, anchored_by: {model: Anchor, field: tag}}]: escribir un documento con area:a.b sin Anchor de area:a falla nombrando area:a; con los dos Anchor pasa; un tag otro:x falla por namespace no declarado; un store sin tag_namespaces acepta lo mismo que antes (tests existentes verdes); tag_tree devuelve raíz a con hijo a.b, un huérfano y un unplaced del fixture; tag_folder("a.b") = "a/b"; replace_text con count 1 y dos apariciones falla sin escribir; con una aparición reescribe, re-trackea y el documento extrae igual salvo el texto; un reemplazo que rompe el modelo falla y deja el archivo igual (hash); CHANGELOG; docs; nota de cierre a deskops.

OUTPUT_SCOPE: src/sldb/api/stores/store_declaration.py, src/sldb/api/semantic/, src/sldb/api/tags/, src/sldb/api/documents/replace_text.py, src/sldb/api/__init__.py, src/sldb/store/semantic_tags.py, src/sldb/cli/parsers/tags.py, src/sldb/cli/commands/tags.py, src/sldb/cli/parsers/docs*.py, src/sldb/cli/commands/docs*.py, tests/, docs/architecture/tags.md, docs/architecture/transactions.md, CHANGELOG.md

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
q1 (gates): G_WRITE_API está satisfied (fe36893f) y GD24 cerrado (88f19ac8): sldb.api.transaction existe y replace_text la usa.
q2 (base): GO08 está cerrado en main (556408da): existen las reglas on_write (src/sldb/api/rules/rules_on_write.py, RuleDoc con moment on_write) que save_document_payload evalúa antes de escribir.
q3 (mecanismo de validación de tags, DECIDIDO por el coordinador de proyecto 2026-11-06, opción B): tag_namespaces sigue siendo dato de store.yaml (StoreDeclaration); su chequeo es una familia de reglas incorporada, no una RuleDoc de usuario, que corre dentro de la evaluación de reglas de GO08 en los tres momentos: on_write (check_on_write: un error rechaza la escritura con SLDBRuleViolationError y no se escribe nada), on_check (stores check) y sldb rules check. Condiciones: (a) rules check y rules explain muestran sus hallazgos con la misma forma que los de una RuleDoc (Finding con node, clause y seen; la regla se identifica con un id estable, p. ej. builtin:tag_namespace:<name>); (b) no se edita src/sldb/api/documents/payload_save_steps.py; (c) la familia vive en un módulo hermano nuevo, src/sldb/api/rules/builtin_tag_rules.py, y se engancha en rules_on_write.py (incluido el corte temprano de has_rules: un store sin RuleDocs pero con tag_namespaces también se chequea), rules_check.py, rules_on_check.py y rules_explain.py, agregados a files; (d) sin tag_namespaces en store.yaml nada cambia (las salidas existentes de rules check, explain y stores check son iguales). Coordinación: api/rules es área de grafo-operable (GO08 cerrado; GO10 en curso con where_parse/FieldCondition): el coordinador avisa a w1:p4 antes de despachar y el ejecutor rebasea sobre origin/main antes de entregar.
HIPÓTESIS PARA EL DUEÑO (q3): no es RuleDoc de usuario (opción C) porque el lenguaje de reglas de GO05 no tiene un predicado de prefijo ancla (para cada prefijo con punto de un tag, existe un documento de un modelo dado cuyo campo es ese prefijo); agregarlo tocaría GO05. Si el dueño lo quiere como RuleDoc, el camino es ese predicado y la familia incorporada se reemplaza por RuleDocs declaradas.
q4 (files): la lista es la mejor previsión al promover; un archivo autorizado que no se use se reporta en la entrega y el coordinador lo poda del TaskDoc; uno nuevo se pide antes.
PRECISIONES DEL PREFLIGHT (review-task-gd27-preflight-1, 2026-11-06):
q5 (anclas): con anchored_by, cada prefijo del valor INCLUIDO el valor completo necesita su ancla (a.b.c exige a, a.b y a.b.c; la regla de deskops prefixes/missing_parents). En el fixture de la aceptación los dos Anchor son area:a y area:a.b; sin el de area:a la escritura falla nombrando area:a (el mensaje lista todos los prefijos faltantes, de arriba hacia abajo). Un tag sin namespace (sin dos puntos) no es de ningún namespace y no se valida.
q6 (raíz de replace_text): ref es un documento trackeado (lo que acepta doc_status: name, Model/name, Model:name o ruta trackeada) o, si no resuelve a uno, una ruta relativa a la raíz del proyecto (StoreLocation.project_root), que debe quedar dentro de ella y existir; una ruta fuera de la raíz o inexistente es error sin escribir. Un archivo no modelado se reescribe con transaction.write_file (guarda con su sha256 leído).
q7 (tag_folder): tag_folder(tag) recibe el valor sin namespace (a.b) o con namespace (area:a.b, el namespace se descarta) y devuelve una ruta relativa posix con un segmento por parte (a/b). Un valor vacío, con segmento vacío (a..b, .a, a.) o con / en un segmento levanta ValueError nombrando el valor. Un valor sin punto devuelve un solo segmento (a).
q8 (forma de tag_tree): {namespace, roots: [{tag, document, children: [...]}], orphans: [{tag, used_by: [export_id...]}], unplaced: [{tag, document}]}; document es el export_id del documento ancla (Model:name) o null para un nodo intermedio sin ancla; tags completos con namespace (area:a.b); orden alfabético por tag en cada nivel. La CLI con --format json emite exactamente ese objeto (y en envelope, dentro de data).
q9 (conteo de replace_text): old es texto literal (no regex), no vacío; el conteo es de apariciones no solapadas de izquierda a derecha (str.count) sobre el texto decodificado como UTF-8 tal cual, sin normalizar saltos de línea ni Unicode; count >= 1. Si el conteo no es exactamente count, error con el número visto y nada se escribe; si es igual, se reemplazan esas count apariciones.
q10 (GO10 en main): GO10 (grafo-operable) entra a main ahora y no toca src/sldb/api/rules/; cambia que WherePredicateError pasa a sldb.core.exceptions (sldb.api la sigue exportando), FacetFilter usa where en vez de conditions y set_where_parser pasa a connect_where_check (notations). Importar WherePredicateError desde sldb.core.exceptions o sldb.api; rebasear sobre origin/main antes de entregar.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_tags.py
- TMPDIR=/dev/shm pytest -q tests/api/test_replace_text.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_semantic.py
- TMPDIR=/dev/shm pytest -q tests/store/test_stores_build.py
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py
- grep de genericidad: ninguna línea agregada por el diff (git diff origin/main...HEAD) en src/ o tests/ contiene taskdoc|board|ritual|pill|atom|closeout|domain_tree (regla 4)
- sldb tags tree NAMESPACE y sldb docs replace --format json sobre el store temporal del test (salida en el reporte de entrega)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, máximo 1 clase y 80 líneas efectivas por archivo)
- git fetch y rebase sobre origin/main antes de entregar; en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio
- files: del TaskDoc coincide con el diff entregado (los autorizados que no se usen se reportan y el coordinador los poda antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

En un store temporal con tag_namespaces [{name: area, hierarchical: true, anchored_by: {model: Anchor, field: tag}}]: escribir un documento con area:a.b sin Anchor de area:a falla nombrando area:a; con los dos Anchor pasa; un tag otro:x falla por namespace no declarado; un store sin tag_namespaces acepta lo mismo que antes (tests existentes verdes); tag_tree devuelve raíz a con hijo a.b, un huérfano y un unplaced del fixture; tag_folder("a.b") = "a/b"; replace_text con count 1 y dos apariciones falla sin escribir; con una aparición reescribe, re-trackea y el documento extrae igual salvo el texto; un reemplazo que rompe el modelo falla y deja el archivo igual (hash); CHANGELOG; docs; nota de cierre a deskops.

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
from pydantic import BaseModel, Field, SerializerFunctionWrapHandler, field_validator, model_serializer

from sldb.api.stores.seed import Seed

DECLARATION_FILE = "store.yaml"
SCAFFOLD_KEYS = ("folders", "seeds")
OPTIONAL_KEYS = (*SCAFFOLD_KEYS, "project_graph")


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
        """A declaration without folders, seeds or project_graph dumps as before they existed; a seed dumps only the keys it was written with."""
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

FILE:src/sldb/api/semantic/__init__.py
"""The semantic DAG as something you can write to: parents beyond the name, and equivalences."""

from sldb.api.semantic.dag_writes import add_semantic_equivalence, add_semantic_parent, remove_semantic_parent
from sldb.api.semantic.dag_reads import semantic_tag

__all__ = ["add_semantic_equivalence", "add_semantic_parent", "remove_semantic_parent", "semantic_tag"]

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
from sldb.api.documents.select_documents import select_documents
from sldb.api.documents.selector import Selector
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
from sldb.api.edges.edges_blocked import edges_blocked
from sldb.api.edges.edges_holding import edges_holding
from sldb.api.edges.project_graph import ProjectGraph, ProjectGraphConfig, project_graph
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
from sldb.api.rules import on_check_findings, refuse_unknown_family, rules_check, rules_explain, rules_on_check, transition_findings
from sldb.api.where import where_matches
from sldb.core.exceptions import AmbiguousSelectionError, ConflictError, WherePredicateError
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
from sldb.api.stores.build_store import build_store
from sldb.api.stores.scaffold_report import ScaffoldReport
from sldb.api.stores.scaffold_store import scaffold_store
from sldb.api.stores.seed import Seed
from sldb.api.stores.store_declaration import StoreDeclaration
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
    "AmbiguousSelectionError", "Selector", "select_documents",
    "DocRefStatus", "doc_exists", "doc_status", "tracked_documents", "AmbiguousDocument", "indexed_model_bases", "resolve_indexed_document", "split_doc_ref", "store_links",
    "WherePredicateError", "apply_effects", "edges_blocked", "edges_holding", "effects_of", "on_check_findings", "refuse_unknown_family", "rules_check", "rules_explain", "rules_on_check", "transition_findings", "remove_model", "where_matches", "inherit_model", "is_model_registered", "registered_models",
    "StructuredNLDoc", "UnresolvedReference", "unresolved_references",
    "BatchReport", "ConflictError", "RollbackError", "Transaction", "apply_batch", "move_document", "transaction",
    "ScaffoldReport", "Seed", "StoreDeclaration", "build_store", "scaffold_store",
    "ProjectGraph", "ProjectGraphConfig", "project_graph",
    "GlyphDoc", "LinkDoc", "NotationDoc", "PaletteDoc", "SpecDoc", "SpecNodeDoc", "ViewDoc",
    "resolve_view", "resolve_documents", "evaluate_projection_view", "list_projection_views", "save_projection_view", "sync_notation", "sync_palette",
]

FILE:src/sldb/store/semantic_tags.py
from __future__ import annotations


def flatten_model_semantics(model_type: type) -> list[str]:
    """Combine base and model-local semantics.

    StructuredNLDoc supplies the representation/source defaults. A concrete
    model replaces a key such as source instead of having to repeat the
    representation declaration.
    """
    semantics = {}
    for base in reversed(model_type.__mro__):
        semantics.update(base.__dict__.get("__semantics__", {}) or {})
    tags = []
    for k, v in semantics.items():
        if isinstance(v, str): tags.append(f"{k}.{v}")
        elif isinstance(v, (list, tuple)): tags.extend([".".join([k, *[str(p) for p in v]])] if v else [])
        elif isinstance(v, dict): tags.extend([".".join([k, ck, *([str(p) for p in cv] if isinstance(cv, (list, tuple)) else [str(cv)])]) for ck, cv in v.items()])
    return sorted(set(t for t in tags if t))


def collect_document_semantic_tags(model_type: type, payload: dict) -> list[str]:
    """
    Collects both model-level and document-level semantic tags.
    """
    tags = set(flatten_model_semantics(model_type))
    for field_name in ("semantic_tags", "tags"):
        payload_tags = payload.get(field_name) or []
        if isinstance(payload_tags, list):
            for tag in payload_tags:
                if isinstance(tag, str) and tag.strip():
                    tags.add(tag.strip())
    return sorted(tags)


def _prefix_edges(tag: str) -> list[tuple[str, str]]:
    """Generates parent-child edges for a dotted semantic tag."""
    parts = [part for part in tag.split(".") if part]
    edges: list[tuple[str, str]] = []
    for index in range(1, len(parts)):
        parent = ".".join(parts[:index])
        child = ".".join(parts[: index + 1])
        edges.append((parent, child))
    return edges

FILE:src/sldb/cli/parsers/docs3.py
from __future__ import annotations
from sldb.cli.output_format import add_format

def _add_docs_part3(sub):
    _select(sub)

def _select(s):
    e = s.add_parser("select", help="Which tracked documents a selector names (keys combined by conjunction).",
                     epilog="Exit codes: 0 ok; with --one, 1 when no document matches or several do (the candidates are listed).\n"
                            "Examples:\n  sldb docs select --prefix task-a --one --format json\n"
                            "  sldb docs select --model BaseDoc --path-glob 'sub/**/*.md' --where 'status = \"open\"'")
    _selector_keys(e)
    e.add_argument("--one", action="store_true", help="Expect exactly one document: error when none or several match")
    e.add_argument("--include-linked", dest="include_linked", action="store_true", help="Also read the stores linked directly to this one")
    e.add_argument("--store", help="Store path")
    add_format(e)

def _selector_keys(e):
    e.add_argument("--ref", help="Doc name, Model/DocName, Model:DocName or tracked path; 'alias:ref' reaches a directly linked store")
    e.add_argument("--prefix", help="Name prefix; with --one an exact name wins over the prefix matches")
    e.add_argument("--path-glob", dest="path_glob", help="Shell pattern over the path relative to the project root ('**' crosses directories)")
    e.add_argument("--model", help="A model name: it and every model extending it")
    e.add_argument("--where", help="A predicate of the rules language over the indexed payload")

FILE:src/sldb/cli/commands/docs.py
"""Docs CLI commands module."""
from __future__ import annotations
import json
from typing import Any
import yaml
from sldb.cli.commands.doc import DocCLI
from sldb.cli.commands.docs_exists import docs_exists
from sldb.cli.commands.docs_history import docs_history
from sldb.cli.commands.docs_select import docs_select
from sldb.cli.commands.explore import ExploreCLI
from sldb.cli.commands.links import LinkCLI
from sldb.cli.graph_ops import ast_for_target
from sldb.cli.store_context import get_store_context
from sldb.api.stores.indexed_documents import indexed_documents

class DocsCLI:
    """Plural docs surface for the redesigned CLI."""

    def __init__(self) -> None:
        self._doc = DocCLI()
        self._explore = ExploreCLI()
        self._links = LinkCLI()

    def run(self, args: Any) -> int:
        """Run appropriate docs subcommand.
        Args:
            args (Any): CLI args.
        Returns:
            int: Exit code.
        """
        cmd = args.docs_command
        if cmd in {"create", "track", "update", "untrack", "delete"}:
            args.doc_command = {"create": "add"}.get(cmd, cmd)
            return self._doc.run(args)
        return self._run_subcommand(cmd, args)

    def _run_subcommand(self, cmd: str, args: Any) -> int:
        handlers = {"list": self.list, "show": self._show, "exists": docs_exists, "history": docs_history, "select": docs_select, "recover": self._links.recover, "compose": self._links.compose, "explore": self._explore.run}
        if cmd in handlers:
            return handlers[cmd](args)
        raise SystemExit(f"Unknown docs command: {cmd}")

    def _show(self, args: Any) -> int:
        payload = ast_for_target(args.store, args.pythonpath, f"docs/{args.doc}")
        print(yaml.safe_dump(payload, sort_keys=False) if args.format == "yaml" else json.dumps(payload, indent=2))
        return 0

    def list(self, args: Any) -> int:
        """List tracked documents in the store.
        Args:
            args (Any): CLI args.
        Returns:
            int: Exit code.
        """
        sp, _root = get_store_context(args.store, mode="readonly")
        docs = indexed_documents(sp)
        return self._render_docs(args.format, {"store": str(sp), "documents": docs}, docs, sp)

    def _render_docs(self, fmt: str, payload: dict[str, Any], docs: list[dict[str, str]], sp: Any) -> int:
        if fmt == "json": print(json.dumps(payload, indent=2))
        elif fmt == "yaml": print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
        elif not docs: print(f"No tracked documents in {sp}")
        else:
            print(f"Tracked documents in {sp}:")
            [print(f"- {i['name']} ({i['model']}) -> {i['path']}") for i in docs]
        return 0

FILE:docs/architecture/transactions.md
# Transactions: several writes undone together

`sldb.api.transaction(store)` opens a `Transaction` whose operations write at once and are undone
together when the block raises. `sldb.api.apply_batch(store, changes)` applies a list of changes
in one transaction after prevalidating them all, and `POST /save` delegates to it, which made
the batch route atomic (decision DA2). This is node GD24 of the plan
`generalizar-desde-deskops`: it absorbs the `DocTransaction` deskops kept in its own `doc_io`.

## The API

```python
from sldb import api

with api.transaction(store, pythonpath) as tx:
    tx.update("login", payload, expected_source_hash=entry.source_hash)
    tx.create("TicketDoc", "signup", payload)              # path: beside the model's documents
    tx.move("faq", "docs/faq.md")                           # same name, edges rebuilt
    tx.write_file("notes/outline.txt", data, expected_sha256=digest)
    tx.record("CHANGELOG.md")                               # the caller writes it; rollback restores it
```

| Operation | Delegates to | Guard |
|---|---|---|
| `create(model, name, payload, path=None)` | `create_document` | `path` must stay inside the project root; without it, the model's default directory (`transaction_paths.default_document_path`) |
| `update(ref, payload, expected_source_hash=None, expected=None)` | `save_document_payload` | `expected_source_hash` against `DocumentEntry.source_hash` first, then `expected` (the full payload) against the current one; the first that fails raises `ConflictError` |
| `delete(ref)` | `delete_document` | |
| `move(ref, new_path)` | `move_document` (new) | destination inside the root and free, else `SLDBStoreError` before anything moves |
| `track(path, model, name=None)` | `track_document_file` | name defaults to the file stem |
| `untrack(ref)` | `untrack_document` | |
| `write_file(path, bytes, expected_sha256=None)` | plain write | current bytes must hash to `expected_sha256` (None when the file is absent) |
| `record(path)` | nothing | snapshots a file the caller writes on its own |

`ref` is a document name or its path as the store records it; every path is relative to the
project root or absolute inside it. `ConflictError(SLDBStoreError)` carries `ref`, `expected`
and `actual`. Nothing of the write path was reimplemented: every operation calls the public
function it names, with its files snapshotted first.

## Semantics

- **Writes happen at once.** What one operation writes, the next one (and any reader in the
  process) sees: an `update` inside the transaction reads back with its new value. There is
  no deferred mode (GP2 stays out of this node).
- **Nesting joins.** A `transaction()` opened over a store that already has one open in the
  process joins it (one `TransactionState` per resolved store path, counted by depth). Only
  the outermost block rolls back: an inner block that ends well commits nothing on its own,
  and an outer block that then raises reverts the inner block's writes too. An inner block
  that raises defers to the outer one.
- **Rollback restores bytes, entries and shards.** Before each operation the transaction
  snapshots the bytes (or the absence) of every file that operation may move
  (`transaction_paths.document_files`): the document's Markdown, its entry shard under
  `.sldb/core/documents/<Model>/`, its semantic, sections and edges shards under
  `.sldb_cache/`, the model's index and edges shard, the store index, the store's own edges
  shard, the semantic DAG and the declaration `store.yaml`. The first snapshot of a path is
  the state the rollback goes back to, however many later operations touch it. This is
  `store/io/rollback.py`'s `rollback_on_error` spread over the whole transaction: it now
  exposes `snapshot` and `restore_all`, and the one-operation context manager is built on them.
- **A file moved without a snapshot is not silently left behind.** On entry the outermost
  transaction records the (mtime, size) signature of every file under `.sldb/` and
  `.sldb_cache/` (lock files aside). On rollback, a file that appeared without a snapshot is
  deleted; one that changed or disappeared without a snapshot cannot be restored and is reported.
- **Caches are forgotten after the restore** with the functions that already existed:
  `forget_store_caches(store, model)` for every model touched, `invalidate_index_cache()`,
  `invalidate_shard_cache()` and `invalidate_composed_edge_indexes()`. The runtime document
  cache keys on the files' signatures, so a restored file is re-read on its own.
- **A failure during the rollback is not swallowed.** `RollbackError(SLDBStoreError)` is
  raised chained to the original exception (`raise ... from original`), with `unrestored`: the
  paths still not as they were, relative to the project root, in the order their restore was
  tried. It lives in `sldb.store.io.rollback` and is re-exported by `sldb.api`.

## `apply_batch`

`apply_batch(store, changes, pythonpath=None) -> BatchReport` takes the same change dicts
`POST /save` takes: `id` (the document name, unique in the batch), `action` (`create`,
`update`, `move`, `delete`, `track`, `untrack`), and by action `model`, `payload`, `path`,
`expected_source_hash` and `expected`. It prevalidates every change before writing anything
(`batch_prevalidate`): shape, model registered, payload rendered and read back under the model
(G4), guards, document present or absent as the action needs, target path inside the project
and free. Then it applies them in one transaction: creates and tracks, then updates, then
moves, then untracks and deletes, request order within each group. `BatchReport.saved` lists
the ids in that order; a failure while applying rolls the whole batch back and re-raises.

## `POST /save` (contract change, DA2)

Request and successful response are unchanged (`{"ok": true, "saved": [...]}`), as are the
409 for a stale `expected` or a taken name or file and the 422 for a payload the model
rejects. What changed: a failure halfway through a batch no longer leaves the earlier changes
saved and reports `completed`; it is a 500 `{"ok": false, "error": ..., "rolled_back": true}`
with the store exactly as before. The route also accepts `expected_source_hash` as the guard
of an update, delete, move or untrack (a stale one is the same 409), and the actions `move`
(`path`), `track` (`model`, `path`) and `untrack`. `write_file` is not exposed over HTTP.
`cli/serve/save_plan.py` keeps the HTTP-shaped checks and their messages; the model checks are
`apply_batch`'s, mapped to 409 (`ConflictError`, `SLDBStoreError`) and 422 (`SLDBValidationError`).

## Every write path validates against the model (G4)

`sldb fields update`, `sldb docs update`, `POST /save`, `apply_batch` and `transaction` all
render the payload under the model and read it back before writing, so a `model_validator`
that rejects a value rejects it on every path, with the file, the entry and the indexes left
as they were. `tests/api/test_write_paths_validate.py` proves it with one test per path. No
route had to be fixed: the rendering itself instantiates the model.

## Out of this node

- An `on_write` rule (`RuleDoc`, GO08) raising inside a batch: GO08 was not closed when GD24
  was dispatched, so that part is not implemented nor tested here (TaskDoc q10).
- Deferred writes (GP2) and exposing `write_file` over HTTP.

## Measurement

Wall time of one `POST /save` with 20 updates on a 20-document store, served with
`build_handler` as `tests/test_serve.py` does (script outside the repo; "before" is the route
of commit `baacd852`, "after" this node), 2026-11-06 on a machine shared with other workers:

| | round 1 | round 2 | round 3 | pooled median (9 samples) |
|---|---|---|---|---|
| before (median of 3) | 1.861 s | 1.923 s | 1.943 s | 1.923 s |
| after (median of 3) | 2.203 s | 1.864 s | 3.914 s | 2.203 s |

The transaction adds, per update, the snapshot of the document's files (eleven small reads)
and, per batch, one signature walk of the store; the spread between runs (1.4 s to 4.6 s) is
the machine's, larger than that cost.

FILE:src/sldb/api/rules/rules_on_write.py
"""`on_write` (GO08, rules.md §9): the rules a write must pass before anything is persisted.

A step of `save_document_payload`, right after the document anchors are pinned (GO07): the rule
reads the pinned payload, with the anchors' states (`<field>__anchor_state`) as the index would
compose them; paths follow the index as it is before the write. An `error` finding refuses the
write (`SLDBRuleViolationError`, nothing written); alerts are routed (`sldb.core.finding_route`)
whether the write passes or not. The document and its neighbours enter the dirty set.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import model_type_of
from sldb.api.rules.dirty_set import mark_dirty
from sldb.api.rules.rule_graph import rule_graph
from sldb.api.rules.rules_on_transition import has_rules, payload_findings
from sldb.core.exceptions import SLDBRuleViolationError
from sldb.core.finding import split
from sldb.core.finding_route import route
from sldb.store.edge_index.doc_anchor_states import SUFFIX, field_states, store_current
from sldb.store.model_contract import doc_anchor_fields


def check_on_write(store_path: Path, model_type: type, node: str, payload: dict[str, Any]) -> None:
    """Evaluate the `on_write` rules on `node` (`Model:name`) as `payload`; raise on an error."""
    if not has_rules(store_path):
        return
    graph = rule_graph(store_path)
    errors, alerts = split(payload_findings(graph, "on_write", node, anchored(store_path, model_type, payload)))
    mark_dirty(store_path, graph.index, node)
    route(alerts)
    if errors:
        raise SLDBRuleViolationError(errors)


def anchored(store_path: Path, model_type: type, payload: dict[str, Any]) -> dict[str, Any]:
    """`payload` with the state of each of its `__doc_anchors__` fields, as the index adds it."""
    names = [name for name in doc_anchor_fields(model_type) if payload.get(name)]
    if not names:
        return payload
    current = store_current(store_path, model_type_of)
    return {**payload, **{name + SUFFIX: field_states(payload[name], current) for name in names}}

FILE:src/sldb/api/rules/rules_check.py
"""`sldb rules check`: the local rules evaluated, each failure a core `Finding` (GO06).

With a subject, every rule that applies to that document, of any moment; without one, the
`on_check` rules over every local document they apply to. Only `false` and `incomplete` become
findings: `false` at the rule's severity with code `rules/<name>`, `incomplete` always an alert
with code `rules/<name>/incomplete`. Nothing of the result is stored.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sldb.api.rules.fixpoint import witness
from sldb.api.rules.rule_graph import RuleGraph, rule_graph
from sldb.api.rules.rule_subjects import applies, resolve_subject, rules_of
from sldb.core.finding import Finding


def rules_check(store: str | Path | None, subject: str | None = None, pythonpath: str | None = None) -> list[Finding]:
    """The findings of the store's rules (see the module); `subject` is a document reference
    (`Model:name`, `store:Model:name` or a path). An unknown subject is `SLDBDocumentTargetError`."""
    graph = rule_graph(store)
    rules = rules_of(graph)
    if subject is not None:
        node = resolve_subject(graph, subject, pythonpath)
        pairs = [(rule, node) for rule in rules if applies(graph, rule, node) is None]
    else:
        pairs = [(r, n) for r in rules if r.get("moment") == "on_check" for n in graph.domain(r["subject"]) if applies(graph, r, n) is None]
    return [f for f in (rule_finding(graph, rule, node) for rule, node in pairs) if f is not None]


def rule_finding(graph: RuleGraph, rule: dict[str, Any], node: str) -> Finding | None:
    """The finding of `rule` on `node` (None when its condition holds)."""
    found = graph.holds(rule["condition"], node)
    if found["holds"] == "true":
        return None
    incomplete = found["holds"] == "incomplete"
    level = "alert" if incomplete else rule.get("severity", "error")
    code = f"rules/{rule['name']}" + ("/incomplete" if incomplete else "")
    named = witness(graph, rule["condition"], found)
    return Finding(level, code, node, explanation(rule, found, named), "", graph.semantics(node).get("path"))


def explanation(rule: dict[str, Any], found: dict[str, Any], named: tuple[str, dict] | None = None) -> str:
    """`<clause> (seen: <seen as compact JSON>)`, after `<message> | ` when the rule has one,
    then ` (witness: <Model:name> <its seen>)` when a quantifier decided it (GO08, `fixpoint.witness`)."""
    seen = _compact(found["seen"])
    text = f"{found['clause']} (seen: {seen})" + (f" (witness: {named[0]} {_compact(named[1])})" if named else "")
    return f"{rule['message']} | {text}" if rule.get("message") else text


def _compact(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

FILE:src/sldb/api/rules/rules_on_check.py
"""`on_check` (GO08, rules.md §9): every `on_check` rule of the store, recomputed only where
something changed, and the document anchors (GO07) beside them; `stores check` reports both.

`recompute` is the one evaluation of a rule on a document that does not come from the cache
(p8): the rest are read from `rule_cache`, unless the document is dirty (`dirty_set`), has no
entry, or its stamp moved. The set is emptied once every rule ran, under the store lock.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.anchors.check_doc_anchors import check_doc_anchors
from sldb.api.rules.dirty_set import read_dirty, stamps_of, wide, write_dirty
from sldb.api.rules.rule_cache import prune, read_results, rule_hash, write_results
from sldb.api.rules.rule_graph import RuleGraph, rule_graph
from sldb.api.rules.rule_subjects import applies, rules_of
from sldb.api.rules.rules_check import rule_finding
from sldb.api.rules.rules_on_transition import has_rules
from sldb.api.stores.open_store import open_store
from sldb.core.finding import Finding
from sldb.store.io import store_lock


def on_check_findings(store: str | Path | None, pythonpath: str | None = None) -> list[Finding]:
    """The findings `stores check` adds: the `on_check` rules', then `check_doc_anchors`'."""
    store_path = open_store(store, mode="readonly").store_path
    rules = rules_on_check(store_path) if has_rules(store_path) else []
    return rules + check_doc_anchors(store_path, pythonpath)


def rules_on_check(store: str | Path | None) -> list[Finding]:
    """The findings of every `on_check` rule over its family, by rule export id then document."""
    graph = rule_graph(store)
    rules = [rule for rule in rules_of(graph) if rule.get("moment") == "on_check"]
    with store_lock(graph.store_path, wait=True):
        dirty = read_dirty(graph.store_path)
        found = [finding for rule in rules for finding in _rule_findings(graph, rule, dirty)]
        write_dirty(graph.store_path, set())
        prune(graph.store_path, {rule_hash(graph.store_path, rule) for rule in rules})
    return found


def recompute(graph: RuleGraph, rule: dict[str, Any], node: str) -> dict[str, Any] | None:
    """One recalculation: the finding of `rule` on `node` as a dict, None when it holds or does not apply."""
    if applies(graph, rule, node) is not None:
        return None
    found = rule_finding(graph, rule, node)
    return found.as_dict() if found is not None else None


def _rule_findings(graph: RuleGraph, rule: dict[str, Any], dirty: set[str] | None) -> list[Finding]:
    key = rule_hash(graph.store_path, rule)
    results, stamps = read_results(graph.store_path, key)
    now = stamps_of(graph, rule, sorted(graph.domain(rule["subject"])))
    stale = dirty is None or (bool(dirty) and wide(rule))
    fresh = {n: results[n] if _kept(n, results, stamps, now, stale or n in (dirty or set())) else recompute(graph, rule, n) for n in now}
    write_results(graph.store_path, key, fresh, now)
    return [Finding(**value) for _, value in sorted(fresh.items()) if value]


def _kept(node: str, results: dict, stamps: dict, now: dict, dirty: bool) -> bool:
    return not dirty and node in results and stamps.get(node) == now[node]

FILE:src/sldb/api/rules/rules_explain.py
"""`sldb rules explain RULE SUBJECT`: the eval finding of one rule on one document (GO06).

The answer is `{"rule", "subject", "finding"}` with the finding exactly as `GraphBackend.eval`
returns it (node, holds, clause, seen), also when it holds. When the rule does not apply to the
document it is `{"rule", "subject", "applies": false, "reason", "detail"}` and has no finding.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.rules.rule_graph import rule_graph
from sldb.api.rules.rule_subjects import applies, resolve_rule, resolve_subject

EXITS = {"true": 0, "false": 1, "incomplete": 2}
NOT_APPLIED_EXIT = 3


def rules_explain(store: str | Path | None, rule: str, subject: str, pythonpath: str | None = None) -> dict[str, Any]:
    """The explanation of `rule` (`RuleDoc:name`, `name` or path) on `subject` (`Model:name`,
    `store:Model:name` or path); an unknown reference is `SLDBDocumentTargetError`."""
    graph = rule_graph(store)
    found, node = resolve_rule(graph, rule), resolve_subject(graph, subject, pythonpath)
    answer = {"rule": found["id"], "subject": node}
    missing = applies(graph, found, node)
    if missing is not None:
        return {**answer, "applies": False, "reason": missing[0], "detail": missing[1]}
    return {**answer, "finding": graph.holds(found["condition"], node)}


def explain_exit(answer: dict[str, Any]) -> int:
    """0 true, 1 false, 2 incomplete, 3 when the rule does not apply; severity never counts."""
    return EXITS[answer["finding"]["holds"]] if "finding" in answer else NOT_APPLIED_EXIT

FILE:instruccion
Cold-bundle de la tarea task-gd27: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_tags.py
- TMPDIR=/dev/shm pytest -q tests/api/test_replace_text.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_semantic.py
- TMPDIR=/dev/shm pytest -q tests/store/test_stores_build.py
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py
- grep de genericidad: ninguna línea agregada por el diff (git diff origin/main...HEAD) en src/ o tests/ contiene taskdoc|board|ritual|pill|atom|closeout|domain_tree (regla 4)
- sldb tags tree NAMESPACE y sldb docs replace --format json sobre el store temporal del test (salida en el reporte de entrega)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, máximo 1 clase y 80 líneas efectivas por archivo)
- git fetch y rebase sobre origin/main antes de entregar; en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio
- files: del TaskDoc coincide con el diff entregado (los autorizados que no se usen se reportan y el coordinador los poda antes de entregar)

