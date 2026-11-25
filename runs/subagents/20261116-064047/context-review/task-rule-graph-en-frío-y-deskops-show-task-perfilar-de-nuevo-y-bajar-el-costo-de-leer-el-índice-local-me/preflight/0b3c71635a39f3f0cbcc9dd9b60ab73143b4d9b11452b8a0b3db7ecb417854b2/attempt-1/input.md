FILE:desk/tasks/task-rule-graph-en-frío-y-deskops-show-task-perfilar-de-nuevo-y-bajar-el-costo-de-leer-el-índice-local-me.md
---
sldb:
  by: agent
  at: '2026-11-16T05:44:41Z'
  authority: generated
  via: save_document_payload
id: task-rule-graph-en-frío-y-deskops-show-task-perfilar-de-nuevo-y-bajar-el-costo-de-leer-el-índice-local-me
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
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

Precisiones (preflight-1): el perfil se toma con python -m cProfile -s cumtime y las 20 primeras filas van a result-summary.md; sldb bench sirve para los tiempos, no reemplaza al perfil. La tarea de muestra para deskops show task es la primera de `deskops list tasks --root <copia>` en orden alfabético. Findings: `sldb rules check --store <copia>/.sldb --format json` antes y después, comparados como conjuntos de (code, subject, level) con jq o python.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

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

