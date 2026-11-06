---
id: task-diseño-jerarquía-de-modelos-de-evidencia-family-o-herencia
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
- docs/architecture/evidence-model-family.md
- .sldb/store.yaml
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-documentar-el-patron-de-modelo-repo-local-cerrar-el-reporte-de-hash-b-y-definir-la-familia-de-modelos-de-evidencia.md
---

# Diseño: jerarquía de modelos de evidencia (__family__ o herencia)

## Rationale

_Explain why this task exists or the business driver behind it._

La nota del 2026-09-23 dejó abierta la familia de modelos de evidencia después de documentar el patrón repo-local y cerrar hash_b. El dueño pidió (2026-10-29) una tarea de diseño cuyo entregable es un documento.

## Goal

_Describe the concrete result this task must produce._

Un documento de decisión en docs/ que compare __family__ vs herencia de clases para los modelos de evidencia, con la recomendación y sus consecuencias para deskops (RunDoc, materializaciones, closeout_evidence).

## Scope

_State what is in scope and what is out of scope._

Solo documento. Sin cambios de código.

PRECISIONES AL COMPLETAR EL TASKDOC (coordinador 1, 2026-11-07, encargo del coordinador de proyecto SLDB_1):
e1 (documento): docs/architecture/evidence-model-family.md, trackeado en el store de sldb con el modelo ArchitectureNarrativeDoc (docs.models:ArchitectureNarrativeDoc, como los otros docs/architecture) y nombre arch-evidence-model-family, con sldb docs track. Un solo documento.
e2 (preguntas que responde, de la nota de origen, seccion 3 del drawer task-documentar-el-patron-de-modelo-repo-local-...): (a) base_models + herencia Python frente a __family__ (como pron con knowledge/relation) para una jerarquia de evidencia (ProofDoc: comando, exit_code, duration_ms, hash de salida, head_sha; RunDoc de deskops/models/run.py; TestDoc/StressTestDoc del analisis de setup); (b) costo en el store de un modelo base abstracto registrado con cero documentos; (c) nombres de campos de evidencia hasheada sin chocar con hash_c/hash_b del store.
e3 (consecuencias para deskops): RunDoc, materializaciones (MaterializationContractDoc), closeout_evidence y los tipos de tarea con su evidencia declarada (task.code, task.docs, task.refactor con goldens, task.aggregate con children). Incluye el hueco de la nota 8bd79409 del inbox de deskops: goldens y children se declaran pero nada los verifica (NOT_YET_VERIFIABLE_EVIDENCE en deskops/services/closeout_gates.py), asi que ninguna task.refactor ni task.aggregate puede cerrar; el documento dice como cada opcion de jerarquia permitiria representar esa evidencia (p. ej. un GoldensDoc/ChildrenDoc o un campo de ProofDoc) sin decidir la politica de cierre, que es de deskops.
e4 (marco vigente que el documento usa como dato, no reabre): herencia de modelos ya existente en sldb (base_models, model <= X en el lenguaje de reglas, rules-language.md; RuleDoc de rules.md; resolve_indexed_document / indexed_model_bases); principio del dueno 2026-11-05: invariantes de un documento como validadores pydantic del modelo, entre documentos como RuleDoc; anclas doc: con hash de contrato (anchoring.md seccion 6) como forma de evidencia que apunta a otro documento.
e5 (estructura): 1 Pregunta y contexto; 2 Opciones (herencia con base_models; __family__; hibrido si aplica), cada una con ejemplo concreto sobre ProofDoc/RunDoc/TestDoc escrito como clases pydantic de ejemplo (en el documento, no en src/); 3 Comparacion en tabla (consultas model <=, reglas por familia, registro y costo de un base vacio, migracion de RunDoc existente, validacion pydantic, closeout_evidence); 4 Consecuencias para deskops (e3); 5 Recomendacion del redactor con su razon; 6 seccion 'Decision del dueno' con el texto 'PENDIENTE: decide el dueno' y las preguntas cerradas que debe contestar (opciones marcadas). El documento NO decide.
e6 (fuera): ningun cambio de codigo ni de modelos en sldb ni en deskops; no se crea ProofDoc; no se toca la politica de cierre de deskops.

PRECISIONES (preflight, 2026-11-07):
e7 (forma del documento): ArchitectureNarrativeDoc tiene solo title y body (plantilla "# <title>" y el cuerpo); sin frontmatter. Se trackea con: sldb docs track docs/architecture/evidence-model-family.md --model ArchitectureNarrativeDoc --name arch-evidence-model-family --store .sldb (con PYTHONPATH que vea docs/models.py, como los demas docs/architecture). Los cambios que el track deja en .sldb/ (store.yaml y los indices) van en el mismo commit que el documento.
e8 (cierre): el entregable de este trabajo es el documento con 'Decision del dueno: PENDIENTE'. La tarea NO se cierra al integrar: queda abierta hasta que el dueno anote su decision en esa seccion (Done When). El ejecutor no escribe ninguna decision.
e9 (hibrido): opcional. Se incluye solo si el redactor encuentra una combinacion de herencia y __family__ que mejore a ambas en algun criterio de la tabla; si no la incluye, lo dice en una frase en la seccion 2.
e10 (hueco goldens/children): 'tratado' significa una subseccion propia de la seccion 4 que (1) resume el hueco citando deskops/services/closeout_gates.py (NOT_YET_VERIFIABLE_EVIDENCE = ("children", "goldens")) y deskops/services/closure.py (verify_task_closeout agrega closeout_evidence_not_verifiable), con la consecuencia: ninguna task.refactor ni task.aggregate puede cerrar; (2) para cada opcion de la seccion 2, esboza como se modelaria esa evidencia como documento (un modelo de ejemplo para goldens y otro para children, o campos de ProofDoc) y como la verificaria una RuleDoc o un validador pydantic segun el principio del dueno; (3) deja dicho que la politica de cierre (opciones a/b de la nota del inbox de deskops 8bd79409) es de deskops y no la decide este documento.

## Implementation Path

_Outline the expected implementation route or affected surface._

Un agente redacta la comparación; el dueño decide.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm sldb docs show arch-evidence-model-family --store .sldb renderiza el documento trackeado
- el documento tiene las seis secciones de e5 y la seccion 'Decision del dueno' dice PENDIENTE
- cada opcion tiene un ejemplo con ProofDoc, RunDoc y TestDoc y la tabla compara los seis criterios de e5
- el hueco goldens/children (nota 8bd79409 de deskops) esta tratado en consecuencias
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py sigue verde (no hay cambios en src/)

## Done When

_Name the observable condition that makes the task complete._

El documento existe, está trackeado y tiene la decisión del dueño anotada.
