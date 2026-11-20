---
sldb:
  by: agent
  at: '2026-11-20T10:14:08Z'
  authority: generated
  via: save_document_payload
id: task-merge-driver-automatico-intento-nuevo-se-instala-desde-los-comandos-cli-de-stores-no-desde-la-api-qu
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- src/sldb/api/stores/ensure_merge_driver.py
- src/sldb/api/stores/store_surroundings.py
- src/sldb/cli/commands/store_init.py
- src/sldb/cli/commands/stores_build.py
- src/sldb/cli/commands/stores_scaffold.py
- tests/api/test_gitignore_policy.py
- tests/store/test_merge_driver_auto_install.py
- tests/store/test_migrate_layout.py
- 9007f78a22569244709af77779847e14a4d57b2e
depends_on: []
pills: []
files:
- CHANGELOG.md
- src/sldb/api/stores/ensure_merge_driver.py
- src/sldb/api/stores/store_surroundings.py
- src/sldb/cli/commands/store_init.py
- src/sldb/cli/commands/stores_build.py
- src/sldb/cli/commands/stores_scaffold.py
- tests/api/test_gitignore_policy.py
- tests/store/test_merge_driver_auto_install.py
- tests/store/test_migrate_layout.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta
---

# Merge driver automático, intento nuevo: se instala desde los comandos CLI de stores, no desde la API que usan las transacciones

## Rationale

_Explain why this task exists or the business driver behind it._

Sigue a task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta, que agotó sus dos intentos. Intento 1 (68d4ee1d, revertido en 8e24da2e): instalaba el driver desde build_store/init_store/scaffold_store de la API, y rompía tests/test_transaction.py::test_split_restores_source_and_store_when_the_second_atom_create_fails de deskops, porque un build dentro de una Transaction escribe .gitattributes y git config fuera del rollback. Intento 2 (sin commit; patch en runs/subagents/exec-deskops-e-7b45b951426a-a2/intento2-sin-commit.patch): movió la instalación a los comandos CLI (bien, el test de deskops pasa), pero 3 de 9 tests de tests/api/test_gitignore_policy.py fallan porque los repos preparados con la API init_store() reciben ahora el alert merge-driver-missing y esos tests esperaban alerts vacíos.

## Goal

_Describe the concrete result this task must produce._

(1) 'sldb stores init', 'sldb stores scaffold' y 'sldb stores build' (los comandos de src/sldb/cli/commands/) instalan el merge driver cuando el store está en un repo git, con ensure_merge_driver/install_merge_driver: idempotente, sin nada fuera de git, y con aviso por stderr sin romper si git falla. Las funciones de API (init_store, scaffold_store, build_store) no lo instalan. (2) 'sldb stores check' da el alert stores/merge_driver_missing con el fix 'sldb stores merge-driver --install' cuando falta. (3) Los tests de tests/api/test_gitignore_policy.py que preparan un repo git con la API y comparan alerts esperan ahora también ese alert (es el comportamiento nuevo pedido). Si un test solo quiere aislar otra regla, que instale el driver antes o filtre por código, sin debilitar lo que verifica.

## Scope

_State what is in scope and what is out of scope._

Dentro: los tres comandos CLI, src/sldb/api/stores/ensure_merge_driver.py, store_surroundings.py, tests/store/test_merge_driver_auto_install.py, tests/api/test_gitignore_policy.py y los tests que haga falta ajustar por el alert nuevo, y CHANGELOG. Fuera: tocar init_store/scaffold_store/build_store de la API para que instalen nada.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: aplicar como punto de partida el patch del intento 2 (git apply runs/subagents/exec-deskops-e-7b45b951426a-a2/intento2-sin-commit.patch) y revisarlo contra el Goal. p2: correr tests/api/test_gitignore_policy.py y ajustar los 3 que fallan según el Goal (3). p3: correr también tests/store/test_merge_driver_auto_install.py, tests/store/test_stores_build.py, tests/api/test_scaffold_store.py, tests/api/test_api_stores.py y tests/test_clean_code_rules.py; y, si el contenedor tiene /workspace/deskops, el test de deskops 'tests/test_transaction.py -k second_atom_create_fails' con PYTHONPATH=/workspace/sldb/src. p4: bash tools/check.sh --fast: todas las puertas en verde salvo 'identidad' por workbench_demo (preexistente, excepción autorizada por el coordinador; decisión aparte). p5: COMMITEAR (git add de rutas nombradas, trailer Task-Id) y correr deskops advance. Una entrega sin commit es FALLA.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto_install.py tests/api/test_gitignore_policy.py

## Done When

_Name the observable condition that makes the task complete._

Los tests de p3 pasan; el commit existe con Task-Id; la suite completa de sldb la corre integrate y el integrador corre la de deskops.
