---
id: task-sw12-pie-del-panel-izquierdo-del-workbench-mostrar-el-frontmatter-del-documento-no-el-esquema-del-modelo
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

# SW12 · Pie del panel izquierdo del Workbench: mostrar el frontmatter del documento, no el esquema del modelo.

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261117-131206-suggestion-sw12-pie-del-panel-izquierdo-del-workbench-mostrar-el-frontmatter-del-documento-no-el-esquema-del-modelo.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261117-131206-suggestion-sw12-pie-del-panel-izquierdo-del-workbench-mostrar-el-frontmatter-del-documento-no-el-esquema-del-modelo.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

SW12 · Pie del panel izquierdo del Workbench: mostrar el frontmatter del documento, no el esquema del modelo.
Comentario de JP, textual: "Aca no se si importa tanto el esquema como si importa mostrar el frontmatter" (con un InboxNoteDoc abierto, store de UIs/graph_ui). Elemento señalado: el bloque al pie del árbol espacial que lista "schema: InboxNoteDoc ↗" y debajo cada campo con su tipo (kind: Literal, sender_project: Optional, created_at: str, … backlinks: list[NodeRef] (0 links)); está en surface/src/workbench/TopologyMindmap.tsx, cerca de la línea 494 (title "Abrir contrato de modelo en Esquema Studio").
Qué pasa hoy: el bloque muestra el contrato del modelo (nombre de campo y tipo), que es lo mismo que ya abre la lente Esquema y Model Studio. No muestra los valores que tiene este documento.
Qué pide: que ahí se vean los valores del frontmatter del documento abierto (kind, sender_project, status, created_at…), dejando el contrato a un clic. JP lo dijo como duda ("no sé si importa tanto"), no como decisión cerrada: el contrato de la tarea debe proponer qué queda y confirmarlo con él.
Puntos a resolver: de dónde salen los valores (GET /documents/<id> ya entrega el payload; no parsear el archivo en la UI); qué campos son frontmatter y cuáles cuerpo (lo dice el modelo, no la UI); valores largos o listas; si los campos se editan ahí mismo (si se editan, pasa por POST /save con nombre de actor, como el resto).
done_when sugerido: con un documento abierto, el pie del panel muestra cada campo de frontmatter con su valor real y el enlace al contrato sigue disponible; nada de eso sale de parseo en la UI.
Toca TopologyMindmap.tsx: en serie con SW3 y SW11.

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
