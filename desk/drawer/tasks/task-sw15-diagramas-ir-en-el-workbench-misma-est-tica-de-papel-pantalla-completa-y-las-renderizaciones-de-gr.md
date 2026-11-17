---
id: task-sw15-diagramas-ir-en-el-workbench-misma-est-tica-de-papel-pantalla-completa-y-las-renderizaciones-de-gr
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW15 · Diagramas IR en el Workbench: misma estética de papel, pantalla completa, y las renderizaciones de gr

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261117-131320-suggestion-sw15-diagramas-ir-en-el-workbench-misma-est-tica-de-papel-pantalla-completa-y-las-renderizaciones-de-gr.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261117-131320-suggestion-sw15-diagramas-ir-en-el-workbench-misma-est-tica-de-papel-pantalla-completa-y-las-renderizaciones-de-gr.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

SW15 · Diagramas IR en el Workbench: misma estética de papel, pantalla completa, y las renderizaciones de graph_ui ahí mismo.
Comentario de JP, textual (por chat, mirando #/diagram): "Distintos archivos se van a renderizar distinto. lo que aca se llama SPEC2viz … y que en el SLDB_1 actual se llama IR deberia renderizarse en esa estetica, deberiamos poder ponerlo en pantalla completa. La idea es que una \"renderizacion\" graphui deberia poder hacerse ahi mismo".
Qué pasa hoy: la vista de diagramas es surface/src/workbench/Spec2VizInspectorView.tsx (rótulos "SPEC2VIZ DIAGRAM CANVAS", "engine: spec2viz-renderer") con NotationSvgCanvas.tsx, que dibuja lo que entrega GET /notations/view con solo cuatro tipos de nodo (initial, terminal, decision, step) y una disposición por niveles propia. No hay pantalla completa (no aparece fullscreen ni requestFullscreen en src/app ni src/workbench). El nombre vigente del proyecto de diagramas es IR (SLDB_1/IR), no spec2viz.
Qué pide, en tres partes: (a) que cada tipo de documento tenga su forma de renderizarse y que los diagramas IR se dibujen con la estética de papel del Workbench; (b) poder poner el diagrama en pantalla completa; (c) que lo que hoy se ve como renderización en graph_ui (vista Specs: UIs/graph_ui/frontends/mindmap/views/specs/notation/, con notation-layout, notation-deployment, notation-swimlanes, notation-style) se pueda ver dentro del Workbench.
Puntos a resolver: quién calcula la disposición (hoy la calcula la UI en NotationSvgCanvas; con "la UI no calcula" debería venir de IR o de sldb, y si falta la ruta es tarea de ese desk); qué notaciones entran primero; cómo se elige el renderizador por tipo de documento (registro por modelo, no ifs en el shell); renombrar los rótulos spec2viz a IR; no copiar código de graph_ui entre repos: o se comparte por un paquete o se rehace sobre los datos de sldb.
Defecto encontrado de paso, tarea chica aparte: el router conserva parámetros de la vista anterior al cambiar de vista. La URL que pegó JP mezclaba doc=reltype-sends_async (store de graph_ui), node=SpecNodeDoc:decision-renal.ingreso (demo Levira) y model=FuenteDoc. Ver surface/src/app/workbench-router.ts.
done_when sugerido: un diagrama IR de un store real se ve en la vista de diagramas con los tokens --wb-*, se abre y se cierra en pantalla completa con teclado, y al menos una notación de graph_ui (swimlanes o deployment) se dibuja ahí; cambiar de vista deja en la URL solo los parámetros de esa vista.
Son varias tareas (router, pantalla completa, estética, notaciones); el coordinador decide el corte. Requiere consulta al desk IR.

Origen: comentario que JP dejó sobre la propia interfaz al recorrer el Workbench de sldb/surface (2026-11-17, vía la sesión supervisora local). Instrucción de JP: cada comentario se registra como tarea, no se resuelve en el momento. Base de código: df3903db en origin/main de sldb. Contexto de producto: el Workbench es LA UI de SLDB, general y autónoma; principios firmes: papel con fierros ocultables, toda escritura tiene nombre, la UI no calcula. Va en la cola después de la serie SW1-SW9, salvo que JP diga otra cosa. La evidencia viene de lectura del código; confirmar cada punto antes de escribir el TaskDoc.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
