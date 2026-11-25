FILE:desk/tasks/task-sldb-api-notations-reexporta-lo-que-specir-importa-hoy-de-módulos-internos-estilos-paletas-errores-m.md
---
sldb:
  by: agent
  at: '2026-11-16T05:51:29Z'
  authority: generated
  via: save_document_payload
id: task-sldb-api-notations-reexporta-lo-que-specir-importa-hoy-de-módulos-internos-estilos-paletas-errores-m
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-193320-suggestion-ir-pide-exportar-desde-sldb-api-notations-los-modelos-de-spec-de-d3-y-guardar-style-y-entity-en-specdoc.md
- desk/inbox/20261115-195349-suggestion-ir-pide-exportar-desde-sldb-api-notations-resolve-style-load-palette-notationerror-anydiagram-diagramtype-y-diagramstoreenvelope.md
- desk/inbox/20261115-215007-suggestion-ir13b-pide-exportar-desde-sldb-api-notations-los-errores-de-rutas-del-cat-logo-default-notations-builtin-notations-y-resolve-catalog-path.md
depends_on: []
pills: []
files:
- src/sldb/api/notations/__init__.py
- tests/notations/test_notation_models_and_builtins.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-un-consumidor-pregunta-al-store-por-la-api-no-leyendo-sus-archivos-de-índice
---

# sldb.api.notations reexporta lo que specIR importa hoy de módulos internos (estilos, paletas, errores, modelos de spec y rutas del catálogo)

## Rationale

_Explain why this task exists or the business driver behind it._

specIR (repo IR) solo debe importar sldb.api, pero hoy toma de módulos internos de sldb una lista de nombres, con excepciones acotadas en su tests/test_imports.py. Tres notas del inbox lo piden: IR11 (modelos de spec de D3), IR12 (resolve_style, load_palette, NotationError, AnyDiagram, DiagramType, DiagramStoreEnvelope) e IR13b (errores de rutas del catálogo, DEFAULT_NOTATIONS, builtin_notations, resolve_catalog_path, split_fragment).

## Goal

_Describe the concrete result this task must produce._

Todos los nombres listados en Scope se importan desde sldb.api.notations y están en su __all__; specIR puede quitar sus excepciones de import sin cambiar comportamiento.

## Scope

_State what is in scope and what is out of scope._

Entra: agregar a src/sldb/api/notations/__init__.py (import y __all__) estos nombres, sin moverlos de donde viven: de sldb.models.notation.diagram_specs (paquete): ClassDiagram, SequenceDiagram, StateDiagram, ComponentDiagram, ActivityDiagram, DeploymentDiagram, MatrixDiagram, ReflectionDiagram (exportados por el paquete); y de sus submódulos, que el paquete no exporta hoy: BaseDiagram y DiagramType (diagram_specs/base/base_diagram.py), EnforcementArtifact (diagram_specs/reflection/enforcement_artifact.py), EnforcementFact (diagram_specs/reflection/enforcement_fact.py), AnyDiagram (diagram_specs/loader/any_diagram.py) y DiagramStoreEnvelope (diagram_specs/catalog/diagram_store_envelope.py); de sldb.notations: resolve_style (src/sldb/notations/styling.py), load_palette (src/sldb/notations/palette_files.py), NotationError (src/sldb/notations/errors/notation_error.py), AmbiguousPathError, UnknownReferenceError, UnknownNotationError (src/sldb/notations/errors/), DEFAULT_NOTATIONS (src/sldb/notations/notation_constants.py), builtin_notations (src/sldb/notations/notation_files.py); de sldb.api.notations.catalog_paths: resolve_catalog_path y split_fragment. Un test nuevo, test_api_notations_exports, en tests/notations/test_notation_models_and_builtins.py, que importa cada nombre desde sldb.api.notations y comprueba que está en __all__ y que es el mismo objeto que el original. Entrada en CHANGELOG.md. No entra: guardar entity o datos extra en SpecDoc (tarea aparte), renombrar o mover módulos, ni tocar el repo IR.

Precisiones (preflight-1): Validation tiene tres comandos (los dos pytest y tools/check.sh --fast); el python -c de Done When es una comprobación adicional. Los errores se importan de sldb.notations (que ya los exporta: AmbiguousPathError, UnknownReferenceError, UnknownNotationError, NotationError), no de sus submódulos. "Grupo" es el módulo de origen: un bloque de import por módulo de origen, y en __all__ los nombres nuevos se agregan en orden alfabético al final de la lista existente.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/notations/__init__.py (bloque de imports y __all__, líneas 49-88). 2) Confirmar con grep la ubicación de cada nombre (rutas en Scope). 3) Agregar los imports y las entradas de __all__ en orden alfabético dentro de su grupo. 4) Correr tools/check.sh --fast para el contrato de capas (api puede importar de notations y models). 5) Escribir el test de exports. 6) CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_notation_models_and_builtins.py
- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos de Validation pasan; `python -c "from sldb.api.notations import resolve_style, load_palette, NotationError, AnyDiagram, DiagramType, DiagramStoreEnvelope, ClassDiagram, EnforcementFact, AmbiguousPathError, DEFAULT_NOTATIONS, builtin_notations, resolve_catalog_path, split_fragment"` no falla; commit con los tres archivos.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-api-notations-reexporta-lo-que-specir-importa-hoy-de-módulos-internos-estilos-paletas-errores-m: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

