Task: task-rules-language-md-la-cabecera-describe-la-semantica-bivaluada-incomplete-retirado
Title: rules-language.md: la cabecera describe la semántica bivaluada (incomplete retirado)
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
  at: '2026-11-21T10:34:34Z'
  authority: generated
  via: save_document_payload
id: task-rules-language-md-la-cabecera-describe-la-semantica-bivaluada-incomplete-retirado
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

# rules-language.md: la cabecera describe la semántica bivaluada (incomplete retirado)

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: la tarea 'el tercer valor del lenguaje de predicados incomplete...' agotó sus dos intentos de tester. El intento 2 (50a0cd16) arregló graph-backend.md, regeneró con selfdoc la referencia de rules explain y restauró el test on_write, pero el tester deskops-t-dd3a304c7b74-a2 encontró un último defecto de doc: docs/architecture/rules-language.md:5 sigue diciendo que el contrato fija 'la semántica trivaluada', mientras el cuerpo (§3, líneas 167-188) dice que el lenguaje es bivaluado y que incomplete se retiró. El resto del retiro está bien y todos los tests pasan.

## Goal

_Describe the concrete result this task must produce._

La cabecera de docs/architecture/rules-language.md (líneas 3-8) dice 'la semántica bivaluada' en lugar de 'la semántica trivaluada', y agrega una frase que remite a la nota de retiro de incomplete en §3. Además, git grep -n -i 'trivaluad' -- docs/ knowledge/ no devuelve ninguna afirmación vigente; las menciones históricas tienen que decir que es historia.

## Scope

_State what is in scope and what is out of scope._

Dentro: docs/architecture/rules-language.md y cualquier otro archivo de docs/ o knowledge/ que el grep muestre afirmando la semántica trivaluada como vigente. Los de knowledge/ se regeneran con 'sldb selfdoc sync', no a mano. Fuera: código y tests.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: editar la cabecera. p2: git grep -n -i 'trivaluad' -- docs/ knowledge/ y corregir lo que afirme la semántica trivaluada como vigente. p3: sldb selfdoc check sin alertas nuevas. p4: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo. La puerta 'identidad' de check.sh --fast en rojo por workbench_demo es la excepción autorizada (f055723d).

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_rules_language_spec.py

## Done When

_Name the observable condition that makes the task complete._

git grep -n -i 'trivaluad' -- docs/ knowledge/ no devuelve afirmaciones vigentes, y tests/test_rules_language_spec.py pasa.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-rules-language-md-la-cabecera-describe-la-semantica-bivaluada-incomplete-retirado"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.
