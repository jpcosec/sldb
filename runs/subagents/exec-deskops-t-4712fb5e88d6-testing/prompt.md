Task: task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con
Title: Los specs de docs/architecture/spec2viz se construyen con specir catalog build y se sincronizan con sldb notations sync --catalog
Status: active
Current node: ritual-testing
Task type: task.docs
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-21T06:47:23Z'
  authority: generated
  via: save_document_payload
id: task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Los specs de docs/architecture/spec2viz se construyen con specir catalog build y se sincronizan con sldb notations sync --catalog

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15 (G7 aceptada y recomendación del coordinador aceptada): el YAML del spec queda subordinado al grafo; los specs existentes se quedan como fixtures durante la paridad y dejan de depender de spec2viz para construirse.

## Goal

_Describe the concrete result this task must produce._

docs/architecture/spec2viz/vistas.yml y sus specs se construyen con specir catalog build y se sincronizan al store con sldb notations sync --catalog; ninguna instrucción ni contrato de sldb invoca spec2viz para ellos.

## Scope

_State what is in scope and what is out of scope._

Entra: la instrucción de build y sync de esos specs, contracts/identity.toml:299 y la documentación que nombra spec2viz catalog build. Sale: mover o renombrar la carpeta (se decide al archivar spec2viz).

## Implementation Path

_Outline the expected implementation route or affected surface._

Reemplazar las invocaciones de spec2viz catalog build por specir catalog build y sldb notations sync --catalog; actualizar identity.toml y la doc; comprobar con sldb notations sync --catalog --check.

## Validation

_List the checks required before this task can close._

- sldb notations sync --catalog docs/architecture/spec2viz/vistas.yml --check; bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

grep de spec2viz en las instrucciones de build de docs/architecture/spec2viz y en contracts/identity.toml sin coincidencias de invocación; sldb notations sync --catalog --check limpio.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
