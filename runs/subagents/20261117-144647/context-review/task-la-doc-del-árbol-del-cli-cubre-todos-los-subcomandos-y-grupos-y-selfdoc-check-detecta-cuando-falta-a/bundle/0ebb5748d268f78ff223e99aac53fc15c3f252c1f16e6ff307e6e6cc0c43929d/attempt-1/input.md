FILE:desk/tasks/task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a.md
---
sldb:
  by: agent
  at: '2026-11-17T02:44:41Z'
  authority: generated
  via: create_document
id: task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- docs/architecture/current-cli-tree.md
depends_on: []
pills: []
files:
- docs/architecture/current-cli-tree.md
- src/sldb/cli/commands/selfdoc.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La doc del árbol del CLI cubre todos los subcomandos y grupos, y selfdoc check detecta cuando falta alguno

## Rationale

_Explain why this task exists or the business driver behind it._

docs/architecture/current-cli-tree.md omite unos 45 subcomandos y 11 grupos del CLI real, y sldb selfdoc check no lo detecta. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

current-cli-tree.md lista todos los grupos y subcomandos que define el parser de sldb, y selfdoc check falla nombrando cada grupo o subcomando del parser que la doc no menciona (y cada uno que la doc nombra y ya no existe).

## Scope

_State what is in scope and what is out of scope._

Entra: (1) un chequeo en selfdoc que recorre el árbol de argparse de sldb y lo compara con los comandos nombrados en current-cli-tree.md, con hallazgos accionables; (2) completar current-cli-tree.md (si es generable desde el parser, generarlo y que el chequeo compare con lo generado); (3) tests en tests/selfdoc/. CHANGELOG. No entra: reescribir las descripciones de cada comando más allá de una línea.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/cli/commands/selfdoc.py, current-cli-tree.md y cómo se arma el parser (src/sldb/cli/parsers/). 2) Implementar el chequeo y completar la doc. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_parser.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev python -m sldb selfdoc check
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; borrar una línea de current-cli-tree.md hace fallar selfdoc check nombrando el comando; CHANGELOG y commit.

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

FILE:docs/architecture/current-cli-tree.md
# Current CLI Tree

Verified from `src/sldb/cli/parsers/` on 2026-09-13. This lists public command paths; use `sldb <command> --help` for arguments and defaults.

```text
sldb
├── help [topic]
├── faq [question]
├── extract / render / validate
├── init / example
├── stores
│   └── init / add / check / update / semantic-map / semantic-export / list
├── models
│   ├── add / update / list / show / validate / create
│   ├── template show / edit
│   └── fields add / remove
├── predicates
│   └── add / list / show / validate / remove
├── docs
│   └── create / track / update / untrack / delete / show / recover / list / compose / explore
├── fields
│   └── show / query / create / update / remove / append / clean
├── sections
│   └── show / find / fields
├── find
├── ast
│   └── show / schema
├── explore / inbox / lint
├── serve
├── selfdoc
│   └── scan / sync / check
└── legacy
    └── ls / get / glob / find
```

## Command Groups

- Direct model workflows: `extract`, `render`, `validate`; no store required.
- Store workflows: `stores`, `models`, `predicates`, `docs`, `fields`, `sections`, `find`, `ast show`.
- Structural inspection: [AST/IR CLI queries](../ast_query_primitives.md).
- HTTP access: `serve --store PATH --pythonpath PATH`, default `127.0.0.1:8787`; optional `--cors`.
- Onboarding and source search: `help`, `faq`, `explore`. FAQ and explore paths are working-directory-relative, not store-anchored.
- Bootstrap and maintenance: `init`, `example`, `inbox`, `lint`.
- Code-derived CLI reference: `selfdoc scan|sync|check`; see [self-documentation](../self-documentation.md).
- Raw address queries: `legacy`; see [addressability](../addressability_model.md).

Singular aliases and old top-level address commands remain compatibility entry points. They are not the recommended surface, and there is no confirmed future removal release for this frozen checkout.

The HTTP implementation exposes `GET /health`, `/schema`, `/graph`, `/semantic-export`, and `POST /save`; it does not expose every CLI command as an HTTP route.

FILE:src/sldb/cli/commands/selfdoc.py
"""CLI orchestration for code-derived reference documents."""
from __future__ import annotations

import json
from contextlib import redirect_stdout
from pathlib import Path
import sys
from sldb.cli.commands import selfdoc_python
from sldb.cli.selfdoc_context import documentation_store, load_parser
from sldb.cli.selfdoc_inspect import inspect_documents
from sldb.cli.selfdoc_write import write_documents
from sldb.selfdoc.materialize import plan_documents
from sldb.selfdoc.parser import ParserScanner
from sldb.selfdoc.python_materialize import plan_python_documents
from sldb.selfdoc.python_scanner import PythonScanner
from sldb.store.resolver import find_local_store


class SelfdocCLI:
    """Scan parser facts, synchronize tracked documents, or check freshness."""

    def run(self, args) -> int:
        """Use JSON stdout; existing lifecycle messages go to stderr."""
        if args.selfdoc_command.startswith("python-"):
            return self._python_operate(args)
        if args.selfdoc_command == "scan":
            return self._scan(args)
        store, root = documentation_store(args.store)
        output = (root / args.output).resolve()
        if not output.is_relative_to(root):
            raise ValueError("Self-documentation output must stay within the store project")
        records = self._records(args, root)
        return self._operate(args, records, store, root, output)

    def _python_operate(self, args) -> int:
        _store, root = documentation_store(args.store)
        source = (root / args.source_root).resolve()
        if not source.is_relative_to(root):
            raise ValueError("Python source root must stay within the store project")
        records = PythonScanner().scan(source, args.package)
        if args.selfdoc_command == "python-scan":
            selfdoc_python.print_python_records(source, root, records)
            return 0
        report = self._sync_python_documents(args, root, records)
        return 0 if report.ok else 1

    def _sync_python_documents(self, args, root, records):
        store, _root = documentation_store(args.store); output = selfdoc_python.documentation_output(root, args.output)
        spec = selfdoc_python.architecture_spec_path(root, args.architecture_spec)
        graph, graph_output = selfdoc_python.python_graph(args, store, root); plans = plan_python_documents(records, args.system, output, spec)
        report = selfdoc_python.python_report(plans, graph, graph_output, store, root, output, args.system)
        if args.selfdoc_command == "python-sync" and not report.metadata_errors:
            report = self._write_python(args, records, (store, root, output, spec), plans, graph, graph_output)
        _print_report(report); return report

    def _write_python(self, args, records, where, plans, graph, graph_output):
        """Write the documents and the graph, then report on what is on disk now (the plans made
        before writing still said `missing`, so a first sync always returned 1)."""
        store, root, output, spec = where
        written = selfdoc_python.write_python_plans(plans, records, args, store, root, output, spec)
        selfdoc_python.write_python_graph(graph, graph_output)
        report = selfdoc_python.python_report(plan_python_documents(records, args.system, output, spec), graph, graph_output, store, root, output, args.system)
        report.written = written.written
        return report

    def _records(self, args, root):
        return ParserScanner(args.include_hidden).scan(load_parser(args.factory, root, args.pythonpath))

    def _scan(self, args):
        local = find_local_store()
        root = documentation_store(args.store)[1] if args.store else (local.parent if local else Path.cwd())
        records = self._records(args, root)
        print(json.dumps({"factory": args.factory, "commands": [r.model_dump() for r in records]}, indent=2))
        return 0

    def _operate(self, args, records, store, root, output):
        plans = plan_documents(records, args.system, args.factory, output)
        report = inspect_documents(plans, store, root, output, args.system)
        if args.selfdoc_command == "sync":
            with redirect_stdout(sys.stderr):
                written = write_documents(plans, store, root)
            plans = plan_documents(records, args.system, args.factory, output)
            report = inspect_documents(plans, store, root, output, args.system)
            report.written = written
        _print_report(report)
        return 0 if report.ok else 1

def _print_report(report) -> None:
    """The report as JSON, its alerts in it and by every other route (`sldb.cli.alert_sink`)."""
    from sldb.cli import alert_sink
    from sldb.selfdoc.report_findings import report_findings, report_payload

    print(json.dumps(report_payload(report), indent=2))
    alert_sink.report(report_findings(report), text=False)

FILE:instruccion
Cold-bundle de la tarea task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_parser.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev python -m sldb selfdoc check
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

