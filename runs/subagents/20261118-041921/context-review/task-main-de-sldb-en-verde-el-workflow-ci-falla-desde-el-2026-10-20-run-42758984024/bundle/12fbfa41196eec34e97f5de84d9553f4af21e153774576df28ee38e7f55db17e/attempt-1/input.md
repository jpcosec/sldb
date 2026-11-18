FILE:desk/tasks/task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024.md
---
sldb:
  by: agent
  at: '2026-11-18T04:17:27Z'
  authority: generated
  via: save_document_payload
id: task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-231010-suggestion-el-job-store-del-ci-de-sldb-no-termina-stores-build-check-regenera-knowledge-symbols-y-supera-las-6-h-del-runner.md
- desk/inbox/20261117-232608-suggestion-ci-store-build-check-pasa-en-ci-lo-que-corta-las-6-h-es-el-segundo-stores-build-del-paso-de-referencia-cli.md
- .github/workflows/ci.yml
depends_on: []
pills: []
files:
- .github/workflows/ci.yml
- src/
- tests/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# main de sldb en verde: el workflow CI falla desde el 2026-10-20 (run 42758984024)

## Rationale

_Explain why this task exists or the business driver behind it._

El CI de main de sldb no tiene una corrida verde desde el 2026-10-20 (39464199660). Los nodos de grafo-operable y generalizar-desde-deskops se integraron con tests dirigidos. Regla del dueño: un fallo conocido sin tarea no existe.

## Goal

_Describe the concrete result this task must produce._

El workflow CI de sldb (jobs test 3.12/3.13 y store) termina en success sobre main.

## Scope

_State what is in scope and what is out of scope._

Estado al 2026-11-18 (sldb origin/main d764b9fd): los fallos de la versión anterior de esta tarea ya están resueltos. Los jobs test 3.12 y 3.13 están en verde desde ca73071d (testpaths). En el job store pasan 'Build deskops' store', 'Prepare pron's store' (make world; pron a0c4100 enlaza ../deskops/.sldb) y 'Rebuild sldb's store from its sources' (sldb stores build --check). El run 44169114744 (6d87f126) se canceló a las 6 h en 'Check generated CLI reference', que corre 'sldb stores build && sldb selfdoc check'. La causa: stores build --check reconstruye una copia scratch y no escribe nada, así que el paso siguiente construye el store completo otra vez. En robocop2, sin knowledge/symbols (gitignored, se regenera), un build tarda 110 min con un núcleo al 100 %; con symbols presente, unos 55 min. El runner es varias veces más lento. En alcance: que el job store construya el store una sola vez y termine con holgura dentro del límite de 6 h del runner, sin perder ninguna comprobación (lo que verifica --check y el selfdoc check siguen verificándose). Fuera de alcance: optimizar la generación de símbolos más allá de lo necesario, y cambios en deskops o pron.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1 (causa): el integrador la diagnosticó con evidencia de CI (run 44169114744, job 134343092734: 'Rebuild sldb's store from its sources' en success, 'Check generated CLI reference' cancelado a las 6 h) y con la ayuda de la CLI ('--check: Rebuild a scratch copy of the sources and compare, writing nothing here'). Es una hipótesis fuerte, no un hecho cerrado: el ejecutor la confirma en el código (archivo y línea de stores build --check y del paso del workflow) antes de cambiar nada, y si no se confirma, para y reporta. Nada de skip, xfail ni subir timeouts como arreglo. p2 (opciones, en orden de preferencia; el ejecutor elige con evidencia y lo justifica en el informe): (a) un solo build en el job: que el paso de referencia CLI reuse el store que deja el paso anterior. Por ejemplo, el paso 'Rebuild' corre sldb stores build (escribe) y después comprueba que el árbol versionado no cambió (git diff --exit-code sobre lo que --check compara), seguido de sldb selfdoc check. Antes de reemplazar --check hay que mostrar con el código qué compara --check y que la sustitución verifica lo mismo; si no es equivalente, (b). (b) una opción de sldb stores build que verifique y deje el store escrito (p. ej. --check que conserve el resultado o --write), con test. (c) aparte de (a) o (b), opcional: cachear knowledge/symbols con actions/cache, con clave en el hash de las fuentes que lo generan. p3 (reproducción local y criterio medible): clones en /dev/shm/sci/{sldb,deskops,pron}. deskops desde GitHub main y pron desde GitHub master. sldb se clona de GitHub y después se trae el commit local del ejecutor con: git -C /dev/shm/sci/sldb fetch /mnt/ssd/proyectos/SLDB_1/sldb <sha> && git -C /dev/shm/sci/sldb checkout --detach <sha> (el commit no está pusheado; se trae del checkout local). Sin knowledge/symbols, con el venv /mnt/ssd/proyectos/SLDB_1/.venv. Perímetro del cronómetro: solo los pasos del job store que van después de 'Install sldb and pron', es decir desde el inicio de 'Build deskops' store when it declares one' hasta el final del último paso del job (hoy 'Check generated CLI reference'). Cada paso se corre con /usr/bin/time -f '%e s' y en el orden de ci.yml. El total es la suma de esos tiempos. Se mide dos veces: con el ci.yml de origin/main (antes) y con el del commit del ejecutor (después). Build de referencia: un sldb stores build sin --check de ese mismo sldb (el commit del ejecutor), en la misma máquina, en la misma sesión y sin knowledge/symbols. Criterio de holgura: después hay exactamente un build completo, y el total del después no supera 1,2 veces ese build de referencia. p4 (dónde trabaja y cómo se cierra): el ejecutor commitea en el checkout /mnt/ssd/proyectos/SLDB_1/sldb, rama main local, con rutas nombradas (nunca git add -A ni -u sobre todo el árbol; hay trabajo ajeno sin commitear en sldb/surface/ y un stash que no se tocan) y sin push. Los cambios de .github/workflows/ci.yml no se pueden pushear sin el scope workflow; el integrador (wA:p1) corre la suite completa en copia limpia y pushea con jpcosec. El run de cierre es el de CI cuyo headSha es el commit integrado: gh run list --repo jpcosec/sldb --commit <sha> --json status,conclusion,url. p5: informe en el run dir que fija el despacho (runs/subagents/exec-<nombre del agente scion>/result-summary.md; el brief del ejecutor trae la ruta exacta) con la causa confirmada, la opción elegida y por qué, los tiempos y el número de builds antes y después y los comandos de la reproducción. p6: si --check y la sustitución discrepan en lo que verifican, o si hace falta una decisión de diseño, el ejecutor para y reporta con las opciones.

## Validation

_List the checks required before this task can close._

- bash tools/check.sh --fast
- pytest -q -n 4 -p no:cacheprovider (suite completa; la corre el integrador en copia limpia)
- reproducción local del job store (p3): rc 0 en todos los pasos, exactamente un build completo y tiempo total <= 1,2 x un build, con los tiempos en el informe
- gh run list --repo jpcosec/sldb --commit <sha integrado> --json status,conclusion,url: success en test 3.12, test 3.13 y store

## Done When

_Name the observable condition that makes the task complete._

El run de CI sobre el commit integrado en main termina en success (test 3.12, test 3.13 y store) y su URL queda en references. El job store construye el store una sola vez.

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

FILE:.github/workflows/ci.yml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install package and test deps
        run: |
          python -m pip install --upgrade pip
          python -m pip install -e ".[dev,code,mcp]"
      - name: Structural gates
        run: bash tools/check.sh --fast
      - name: Run tests
        run: pytest
      - name: Build distribution
        run: python -m build

  store:
    # The store is derived (docs/architecture/derived-store-boundary.md): rebuild it from the
    # sources, with the stores it links checked out as siblings at the same relative paths.
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          path: sldb
      - uses: actions/checkout@v4
        with:
          repository: jpcosec/opsys
          path: deskops
      - uses: actions/checkout@v4
        with:
          repository: jpcosec/pron
          ref: master
          path: pron
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - name: Install sldb and pron
        run: |
          python -m pip install -e "sldb[dev,click,code,mcp]"
          python -m pip install -e "pron[mcp]"
      - name: Build deskops' store when it declares one
        # deskops still versions its .sldb/core/; once it moves to .sldb/store.yaml, build it.
        # Runs before pron's world: pron links deskops as ../deskops/.sldb.
        working-directory: deskops
        run: if [ -f .sldb/store.yaml ]; then sldb stores build; fi
      - name: Prepare pron's store
        # pron keeps .sldb/ out of git and builds it with its own CLI; a store.yaml generator
        # runs only sldb subcommands, by design.
        working-directory: pron
        run: make world
      - name: Rebuild sldb's store from its sources
        working-directory: sldb
        run: sldb stores build --check
      - name: Check generated CLI reference
        # needs the store built: the reference documents are tracked in it
        working-directory: sldb
        run: sldb stores build && sldb selfdoc check

FILE:instruccion
Cold-bundle de la tarea task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- bash tools/check.sh --fast
- pytest -q -n 4 -p no:cacheprovider (suite completa; la corre el integrador en copia limpia)
- reproducción local del job store (p3): rc 0 en todos los pasos, exactamente un build completo y tiempo total <= 1,2 x un build, con los tiempos en el informe
- gh run list --repo jpcosec/sldb --commit <sha integrado> --json status,conclusion,url: success en test 3.12, test 3.13 y store

