---
id: task-sw14-vista-de-fuente-y-anclaje-abrir-documentos-fuente-de-verdad-y-anclar-sobre-ellos-como-en-kimun
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

# SW14 · Vista de fuente y anclaje: abrir documentos fuente de verdad y anclar sobre ellos, como en kimun.

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261117-131256-suggestion-sw14-vista-de-fuente-y-anclaje-abrir-documentos-fuente-de-verdad-y-anclar-sobre-ellos-como-en-kimun.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261117-131256-suggestion-sw14-vista-de-fuente-y-anclaje-abrir-documentos-fuente-de-verdad-y-anclar-sobre-ellos-como-en-kimun.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

SW14 · Vista de fuente y anclaje: abrir documentos fuente de verdad y anclar sobre ellos, como en kimun.
Comentario de JP, textual: "La idea de esta vista es poder abrir documentos fuente y hacer el anchhoruing (revisa como funciona kimun), aca no está funcionando asi". Elemento señalado: el enlace "leer fuente ↗" de la barra superior estando en #/source (surface/src/app/WorkbenchShell.tsx:302-310, title "Abrir la FuenteDoc como prosa"). Vista: surface/src/workbench/SourceAnchoringView.tsx (715 líneas).
Qué pasa hoy: (1) la vista solo ofrece como "fuente" documentos que ya están dentro del store: los de un modelo cuyo nombre contiene fuente, acta o source, o cualquiera cuyo payload trae texto (isNamedSourceModel, isAnchorableSource, rankSources, :105-160). No abre un archivo del repositorio (un .md de docs/, un archivo de código). (2) Qué átomos pertenecen a una fuente y dónde caen en el texto lo calcula la UI: compara source / fuente_ref / provenance del átomo con el id o la ruta (atomBelongsToSource, :146) y busca la cita con indexOf sobre el texto (:249-265). Eso contradice "la UI no calcula". (3) "leer fuente ↗" saca de la vista de anclaje y abre el documento como prosa; no abre otra fuente.
Cómo funciona kimun (leído en ~/proyectos/kimun, solo lectura; kimun no se toca ni se copia): un ancla es una declaración "(anchors <afirmación> (at \"docs/spec.md\" [\"Spec\" \"Cache\"]))": apunta a un archivo y a una ruta de encabezados dentro de él. "kimun declare anchors --since COMMIT" resuelve las anclas contra lo que git dice que cambió y devuelve el estado de cada una (:anchored, :mutated); el ancla guarda lo que vio y por eso detecta mutaciones. Código: src/kimun/kernel/anchor.cljc, src/kimun/surface/declared_anchors.cljc; README, sección de declaraciones.
En sldb: la semántica de anclaje ya está fijada por JP (2026-10-19): anclar es fundar una afirmación en su fuente; changed es una alerta visible, nunca un error ni silencio; referencia rota se intenta reconectar y se informa reconnected X→Y o lost. Existen AnchorDoc, el escáner tree-sitter y write_anchor / record_reconnection en la API (commit a2d418b5).
Qué pide: que la vista permita abrir un documento fuente (del repositorio, no solo un documento del store), leerlo, seleccionar un tramo o sección y anclar; y ver el estado de las anclas existentes (anclada, cambió, perdida) según lo resuelve sldb.
Puntos a resolver primero: qué rutas de sldb serve entregan hoy la lista de fuentes anclables, el texto de un archivo y el estado resuelto de las anclas; si falta alguna, va como tarea de sldb y esta espera (los consumidores no reimplementan sldb). Qué unidad se ancla (tramo de texto, sección por encabezados, símbolo de código). Cómo se elige la fuente (ver SW10, navegador de disco: probablemente comparten selector). Qué operación con nombre escribe el ancla.
done_when sugerido: en un store real se abre un archivo fuente que no es un documento del store, se ancla un tramo con una operación de sldb firmada, y al cambiar el archivo la vista muestra la alerta de cambio que entrega sldb; ninguna pertenencia ni posición sale de cálculo en la UI.
Probablemente son dos o tres tareas (rutas de sldb, vista, estados); el coordinador decide el corte.

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
