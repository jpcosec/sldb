FILE:desk/tasks/task-v0-benchmark-fijo-de-velocidad-sldb-bench-y-punto-de-partida.md
---
sldb:
  by: agent
  at: '2026-11-16T00:33:33Z'
  authority: generated
  via: create_document
id: task-v0-benchmark-fijo-de-velocidad-sldb-bench-y-punto-de-partida
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
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# V0: benchmark fijo de velocidad (sldb bench) y punto de partida

## Rationale

_Explain why this task exists or the business driver behind it._

sldb y deskops son lentos (stores build --check ~50 min, doctor 10-14 s, status >60 s en MEPU) y ninguna mejora de V1/V2 cuenta sin una medición fija y repetible contra la que comparar.

## Goal

_Describe the concrete result this task must produce._

Agregar a sldb el verbo 'sldb bench', que copia desks a un directorio de trabajo, mide en frío y en caliente tiempo de pared, CPU y RSS máximo de stores update (sin cambios y con un documento cambiado), stores check, stores build --check, deskops doctor, deskops status y el arranque de ambos CLI, y entrega JSON más una tabla; y dejar el punto de partida medido en reports/velocidad-baseline-20261115.md.

## Scope

_State what is in scope and what is out of scope._

Solo medición: src/sldb/cli/bench/ (verbo y medición por subprocess con os.wait4), su parser y handler, tests unitarios en tests/test_bench_*.py, referencia de CLI regenerada con selfdoc sync y el informe del baseline. Fuera de alcance: cualquier arreglo de velocidad (V1/V2) y cambios en deskops o MEPU; deskops se invoca como CLI externo y MEPU solo se copia.

## Implementation Path

_Outline the expected implementation route or affected surface._

src/sldb/cli/bench/

## Validation

_List the checks required before this task can close._

- python -m pytest -q -p no:cacheprovider tests/test_bench_measure.py tests/test_bench_cli.py
- python -m pytest -q -p no:cacheprovider tests/test_clean_code_rules.py
- bash tools/check.sh --fast
- python -m sldb selfdoc check

## Done When

_Name the observable condition that makes the task complete._

sldb bench corre sobre copias en /dev/shm de los desks de sldb, deskops y MEPU, en frío y en caliente, y emite JSON y tabla; reports/velocidad-baseline-20261115.md tiene shas, máquina, tabla por desk y operación y la metodología; tests nuevos, test_clean_code_rules.py, tools/check.sh --fast y sldb selfdoc check pasan.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-v0-benchmark-fijo-de-velocidad-sldb-bench-y-punto-de-partida: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

