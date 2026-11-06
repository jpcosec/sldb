---
id: task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field
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
- docs/architecture/bootstrap-model-set.md
- .sldb/store.yaml
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-atomo-y-field-convergieron-falta-un-set-bootstrap.md
---

# Diseño: set bootstrap de modelos tras la convergencia átomo/field

## Rationale

_Explain why this task exists or the business driver behind it._

La nota del 2026-10-01 muestra que AtomDoc y los fields tienen la misma forma y difieren solo en de dónde sale su identidad, y propone un set bootstrap de siete modelos (Fuente…Modelo). El dueño pidió (2026-10-29) tratarla como tarea de diseño: el entregable es un documento, no código.

## Goal

_Describe the concrete result this task must produce._

Un documento de decisión en docs/ (SpecDoc o PlanDoc trackeado) que evalúe la propuesta de siete modelos, diga qué se adopta, qué no y por qué, con ejemplos de cada modelo sobre documentos reales del store.

## Scope

_State what is in scope and what is out of scope._

Solo documento. Sin cambios de código ni de modelos existentes. Cita la nota original y los átomos relevantes.

PRECISIONES AL COMPLETAR EL TASKDOC (coordinador 1, 2026-11-07, encargo del coordinador de proyecto SLDB_1):
b1 (documento): docs/architecture/bootstrap-model-set.md, trackeado con el modelo PlanDoc (docs.models:PlanDoc: solo title y body, sin frontmatter) y nombre plan-bootstrap-model-set: sldb docs track docs/architecture/bootstrap-model-set.md --model PlanDoc --name plan-bootstrap-model-set --store .sldb (PYTHONPATH que vea docs/models.py). No se usa SpecDoc: el SpecDoc local choca con el builtin de sldb.models tras SV01 (nota del inbox 1f853301). Los cambios que el track deja en .sldb/ van en el mismo commit.
b2 (fuente): la propuesta esta en la seccion Scope del drawer desk/drawer/tasks/task-atomo-y-field-convergieron-falta-un-set-bootstrap.md (nota del 2026-10-01); la 'espiral' que cita esta en docs/surface/PROPUESTA-SUPERFICIE.md (seccion 16 o la que hable de la espiral). El documento cita ambas.
b3 (puntos a evaluar, uno por subseccion): los siete modelos propuestos (Fuente, Atomo, Relacion + TipoDeRelacion, Grupo, Composicion, Publicacion, Modelo), la regla 'un atomo nunca lleva posicion, un field nunca lleva ancla; se conectan por procedencia (H1) y por promocion' y la pregunta abierta (el resto a modelar es el dominio de cada caso o SLDB mismo). Para cada punto: que propone, que existe hoy en sldb que ya lo cubre o lo contradice (citando archivo:linea: AtomDoc de deskops, RelationDoc/RelationTypeDoc, __compositions__, base_models/herencia, anclas doc: de anchoring.md seccion 6, RuleDoc de rules.md, model_create/model_drafts de SV04, ViewDoc/notaciones de SV01), un ejemplo sobre un documento REAL del store de sldb (nombrado por su export id), la recomendacion del redactor (adoptar, adoptar con cambios, no adoptar) con su razon, y una linea 'Decision del dueno: PENDIENTE (adoptado / rechazado)'.
b4 (marco vigente que el documento usa como dato): principio del dueno 2026-11-05 (invariantes de un documento como validadores pydantic; entre documentos como RuleDoc); los atoms de desk/atoms que traten atomo/field/procedencia/contrato; G_BOUNDARY (sldb evalua reglas declaradas, los consumidores las autoran).
b5 (estructura): 1 Contexto y fuentes; 2 Resumen de la propuesta; 3 Un punto por subseccion (b3); 4 Tabla resumen (punto, recomendacion, decision del dueno: PENDIENTE); 5 Que cambiaria si se adopta todo (sin implementarlo). El documento NO decide: el dueno marca cada punto.
b6 (cierre): el entregable es el documento con todas las decisiones en PENDIENTE; la tarea no se cierra al integrar, queda abierta hasta que el dueno marque cada punto (Done When).
b7 (fuera): ningun cambio de codigo ni de modelos; no se crean los siete modelos.

PRECISIONES (preflight, 2026-11-07):
b8 (rutas de lo existente, en main de sldb salvo que se diga): AtomDoc = ../deskops/deskops/models/atom.py (y protoatom.py); RelationDoc = src/sldb/models/relation_doc.py; RelationTypeDoc = src/sldb/models/relation_type_doc.py; __compositions__ y base_models = src/sldb/store/model_contract.py y docs/architecture/model-authoring.md; anclas doc: = docs/architecture/anchoring.md seccion 6 y src/sldb/models/doc_anchor_value.py; RuleDoc = src/sldb/models/rule_doc.py y docs/architecture/rules.md; SV04 = src/sldb/api/model_create/ y src/sldb/api/model_drafts/; SV01 = src/sldb/models/notation_models.py (ViewDoc) y docs/architecture/notations-and-views.md. Se cita archivo:linea sobre el estado de main al redactar.
b9 (atoms): como minimo atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill, atom-el-dueño-de-un-field-es-la-sección-del-template-que-lo-contiene-no-la-línea-donde-quedó-renderizado, atom-el-path-guardado-de-un-modelo-es-una-pista-model-ref-es-la-identidad y atom-sldb-evaluates-declared-rules-consumers-author-them (desk/atoms/); el redactor puede sumar otros que encuentre con sldb find o grep y los nombra.
b10 (espiral): docs/surface/PROPUESTA-SUPERFICIE.md, seccion '## 16. El ciclo', subseccion '### 16.1 · La espiral'.
b11 (ejemplos reales): cada ejemplo nombra un documento trackeado en .sldb/store.yaml de sldb por su export id Model:name (p. ej. ArchitectureNarrativeDoc:arch-..., AtomDoc:atom-..., RelationTypeDoc:..., PlanDoc:...), elegido porque ilustra el punto; el redactor dice en una frase por que ese documento.
b12 (entorno y git): el trabajo va en un worktree propio de sldb en una rama wt/ que da el coordinador; Python = ~/proyectos/SLDB_1/.venv/bin/python con PYTHONPATH=<worktree>/src:<worktree> y TMPDIR=/dev/shm; un commit con el documento y los cambios de .sldb/ que produce el track; sin push (integra el coordinador de proyecto).
b13 (fuentes del marco): principio del dueno = docs/architecture/rules.md (seccion de RuleDoc y validacion al escribir) y el Scope de las tareas GO06-GO09 del plan desk/drawer/plans/grafo-operable (notas q1); G_BOUNDARY = desk/drawer/plans/grafo-operable/dag.yaml (gates.G_BOUNDARY) y el atom atom-sldb-evaluates-declared-rules-consumers-author-them.

## Implementation Path

_Outline the expected implementation route or affected surface._

Un agente redacta la propuesta; el dueño decide sobre el texto.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm sldb docs show plan-bootstrap-model-set --store .sldb renderiza el documento trackeado
- cada uno de los nueve puntos de b3 tiene su subseccion con ejemplo sobre un documento real del store (export id), recomendacion y 'Decision del dueno: PENDIENTE'
- la tabla resumen lista los nueve puntos con su recomendacion
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py sigue verde (no hay cambios en src/)

## Done When

_Name the observable condition that makes the task complete._

El documento existe, está trackeado y el dueño marcó en él cada punto como adoptado o rechazado.
