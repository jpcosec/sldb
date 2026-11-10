---
id: task-project-graph-para-deskops-nodos-para-archivos-declarados-que-no-son-documento-y-declaraci-n-con-closed-document-como-dato-desv-os-de-cc33c
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

# project_graph para deskops: nodos para archivos declarados que no son documento y declaración con closed_document como dato (desvíos de CC33c)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-project-graph-para-deskops-nodos-para-archivos-declarados-que-no-son-documento-y-declaración-con-clo.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-project-graph-para-deskops-nodos-para-archivos-declarados-que-no-son-documento-y-declaración-con-clo.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallado por CC33c de deskops el 2026-11-10 (wt/cc33c 0571d23d; log coord2-ccconfig/cc33c/oracle-compare-ba982a45.log). La paridad con el oráculo v1 está bien: 618 nodos, 296 triples, 0 diferencias, missing 0=0. Quedan dos desvíos que dependen de sldb.

H1 (b14). El grafo de proyecto no crea nodo para archivos declarados como target que no son documento del store, como desk/drawer/plans/deskops-como-config/dag.yaml y tests/fixtures/model_contract_hashes.json (estos vienen del arreglo de main-en-verde-2). Por eso deskops conserva declared_target_is_a_file en deskops/graph/checks.py. Propuesta: project_graph crea un nodo de archivo para el target declarado que existe en disco, o 'missing' de GD21 no cuenta como faltante un archivo que existe.

H2 (b17). sldb.api.project_graph(store) falla con SLDBStoreError 'store.yaml declares no project_graph' porque deskops no declara project_graph en .sldb/store.yaml. Además su closed_document (issues cerrados) es un callable y la declaración no puede expresarlo. Por eso deskops usa ProjectGraph(root, desk_graph_config()) de sldb.api.edges.project_graph, igual que desk_graph.py y closeout. Propuesta: la declaración de project_graph admite el criterio de documento cerrado como dato (por ejemplo, campo y valores de status), y así deskops lo declara vía deskops desk update.

Cuando H1 y H2 estén en sldb main, deskops borra declared_target_is_a_file y declara project_graph (lo decidido en DO8, en decisiones.md de deskops-como-config).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
