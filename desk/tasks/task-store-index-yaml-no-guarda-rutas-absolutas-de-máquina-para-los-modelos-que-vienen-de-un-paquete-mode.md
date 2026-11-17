---
sldb:
  by: agent
  at: '2026-11-17T02:13:59Z'
  authority: generated
  via: create_document
id: task-store-index-yaml-no-guarda-rutas-absolutas-de-máquina-para-los-modelos-que-vienen-de-un-paquete-mode
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-224143-unclear-store-index-yaml-versionado-guarda-path-absolutos-de-modelos-de-paquete-de-sldb-home-jp-mnt-ssd-herramientas.md
depends_on: []
pills: []
files:
- src/sldb/api/stores/apply_declaration.py
- tests/api/test_declare_store_authored.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# store_index.yaml no guarda rutas absolutas de máquina para los modelos que vienen de un paquete (model_ref)

## Rationale

_Explain why this task exists or the business driver behind it._

En pron (store versionado) y en el propio sldb, .sldb/core/store_index.yaml guarda path absolutos para modelos de paquete de sldb (RelationTypeDoc -> /home/jp/..., RuleDoc -> /mnt/ssd/herramientas/...), aunque store.yaml solo declara model_ref; un clon en otra máquina o en el CI hereda rutas inexistentes. Pregunta si ese path se lee. Origen: desk/inbox/20261116-224143-unclear-store-index-yaml-versionado-guarda-path-absolutos-de-modelos-de-paquete-de-sldb-home-jp-mnt-ssd-herramientas.md.

## Goal

_Describe the concrete result this task must produce._

Para un modelo declarado por model_ref de un paquete importable, store_index.yaml no guarda una ruta absoluta de la máquina (la omite o guarda una relativa a la raíz del proyecto si está dentro de él), y cargar el store en otra máquina funciona igual.

## Scope

_State what is in scope and what is out of scope._

Entra: averiguar dónde se escribe y dónde se lee ese path (src/sldb/api/stores/apply_declaration.py e index_refresh.py, y quién lo lee); si solo es informativo, dejar de escribir rutas fuera del proyecto; si se lee, resolverlo desde model_ref y no desde la ruta guardada; un store existente con rutas absolutas se sigue leyendo; test en tests/api/test_declare_store_authored.py. CHANGELOG. Responder la pregunta de pron (se lee o no) en result-summary.md. No entra: regenerar los stores de otros repos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Buscar escritores y lectores del path de modelos en store_index. 2) Implementar. 3) Test. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_declare_store_authored.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_stores_build.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con el test nuevo; result-summary.md responde si el path se lee; CHANGELOG y commit; aviso a pron.
