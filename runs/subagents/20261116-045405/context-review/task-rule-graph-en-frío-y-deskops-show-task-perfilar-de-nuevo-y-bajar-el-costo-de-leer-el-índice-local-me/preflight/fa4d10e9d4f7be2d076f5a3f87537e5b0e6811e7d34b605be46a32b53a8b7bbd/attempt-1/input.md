FILE:desk/tasks/task-rule-graph-en-frío-y-deskops-show-task-perfilar-de-nuevo-y-bajar-el-costo-de-leer-el-índice-local-me.md
---
sldb:
  by: agent
  at: '2026-11-16T04:14:25Z'
  authority: generated
  via: create_document
id: task-rule-graph-en-frío-y-deskops-show-task-perfilar-de-nuevo-y-bajar-el-costo-de-leer-el-índice-local-me
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-v0-benchmark-fijo-de-velocidad-sldb-bench-y-punto-de-partida
pills: []
files:
- src/sldb/store/io/shards.py
- src/sldb/store/io/__init__.py
- src/sldb/api/rules/rule_graph.py
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-lectura-del-ndice-local-yaml-puro-y-deepcopy-dejan-rule-graph-en-1-2-s-en-fr-o.md
---

# rule_graph en frío y deskops show task: perfilar de nuevo y bajar el costo de leer el índice local (meta rule_graph < 1 s en frío)

## Rationale

_Explain why this task exists or the business driver behind it._

Residual de la tarea de rule_graph (wt/rule-graph-local bdb9b0ff, informe runs/subagents/rg-worker-report.md): rule_graph en frío tarda 1,2-2,1 s en stores grandes y deskops show task 2,8 s en el desk de deskops. La nota atribuía el costo a yaml en Python puro y a deepcopy, pero eso ya no es así: src/sldb/store/io/utils.py:26 usa CSafeLoader desde 50c2fd88 y las copias usan _fast_copy (model_validate(model_dump()), src/sldb/store/io/__init__.py:34-49). Hay que perfilar de nuevo antes de arreglar. Ojo: el .venv del repo no tiene yaml (ModuleNotFoundError); usar el intérprete de la instalación de sldb (el de `head -1 $(which sldb)`). Origen: drawer desk/drawer/tasks/task-lectura-del-ndice-local-yaml-puro-y-deepcopy-dejan-rule-graph-en-1-2-s-en-fr-o.md.

## Goal

_Describe the concrete result this task must produce._

Con un perfil nuevo (cProfile) guardado en el informe, rule_graph en frío sobre una copia en /dev/shm del store del desk de deskops tarda menos de 1 s y deskops show task menos de 2 s, con los mismos findings que antes del cambio.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) medir con sldb bench (verbo de V0, b60f0891) o con python -m cProfile sobre una copia en /dev/shm de /mnt/ssd/proyectos/SLDB_1/deskops/.sldb y desk/, en frío (sin .sldb_cache) y en caliente, y guardar las 20 funciones más caras en el informe; (2) arreglar el costo dominante si está en src/sldb/store/io/ (lectura de shards, src/sldb/store/io/shards.py:68-95, o copias de modelos) o en src/sldb/api/rules/rule_graph.py; (3) medir después y comparar findings (rules check antes y después, mismo resultado). Si el costo dominante está fuera de esos módulos, la tarea se detiene con el perfil y una propuesta en el informe. CHANGELOG.md si hubo cambio. No entra: la federación de stores enlazados (resuelta en 84eb7f75), run_view (otra tarea), cambiar el formato de los shards.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Copiar el desk de deskops a /dev/shm. 2) Perfilar rule_graph y deskops show task en frío y caliente. 3) Arreglar el punto caro. 4) Medir y comparar findings. 5) Tests de Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_rules_evaluation.py
- TMPDIR=/dev/shm pytest -q tests/api/test_transaction_rules_dirty.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rules_linked_reach.py

## Done When

_Name the observable condition that makes the task complete._

El informe tiene el perfil antes y después y los tiempos medidos bajo las metas (o el motivo por el que se detuvo); los tres comandos pasan; findings de rules check iguales antes y después; commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-rule-graph-en-frío-y-deskops-show-task-perfilar-de-nuevo-y-bajar-el-costo-de-leer-el-índice-local-me: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

