# Tester deskops-t-18a9a68f5d3b — result summary

Task: `task-read-store-distingue-un-store-inexistente-store-not-found-de-uno-sin-preparar-store-not-prepared`. Pills: ninguno. Veredicto: **PASA** (el commit y el aviso a graph_ui quedan para el closeout).

## Validation (corrida por el tester, salida completa en `validation.log`)
Todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`; `uv` funcionó sin problemas.
| Comando | Resultado |
|---|---|
| `pytest -q tests/api/test_api_stores.py` | PASA: rc=0, 14 passed |
| `pytest -q tests/test_clean_code_rules.py` | PASA: rc=0, 1206 passed |
| `bash tools/check.sh --fast` | PASA: rc=0, TODAS LAS PUERTAS PASAN |
La suite completa y `sldb stores build --check` no figuran en Validation: no se corrieron (son del integrador).

## Done When
- Los comandos de Validation pasan con los tests nuevos: **PASA**. Los dos tests nuevos están en `tests/api/test_api_stores.py`. Contra el `read_store.py` de HEAD, `test_read_store_says_not_found_when_the_store_directory_does_not_exist` FALLA (así que el test sí detecta el cambio); `..._not_prepared_when_the_store_exists_without_its_index` ya pasaba en HEAD (sirve como guarda de que el mensaje no cambió).
- CHANGELOG: **PASA**. Hay una entrada en 0.1.13 y coincide con el diff (`store_is_prepared` no cambia; la ruta es la `.sldb` resuelta).
- Commit y aviso a graph_ui: **pendientes**. El ejecutor no los hizo por decisión del coordinador y al tester no le corresponden; quedan para el closeout. No es una falla del ejecutor.

## Aclaraciones del coordinador
1. Caso de graph_ui: **PASA**. Con un proyecto inicializado al que se le borra `.sldb`, `read_store` da `store not found: <abs>/gone/.sldb`, tanto con ruta absoluta como relativa. Con `.sldb` presente pero sin `core/store_index.yaml`, da `store not prepared: run \`sldb stores update\` (<abs>/noidx/.sldb)`.
2. Callers: **PASA**. En este repo, `read_store` solo se re-exporta en `src/sldb/api/__init__.py` y se usa en los tests; nadie depende de la substring. En graph_ui (`/mnt/ssd/proyectos/SLDB_1/UIs/graph_ui`), `views_routes.py:92`, `workspace_routes.py:174` y `persistence.py:83` buscan `'store not prepared'` solo para responder 503 store_no_preparado. Ahora un store inexistente ya no entra en ese 503 y llega como error genérico, que es lo que pidió la nota del inbox. Esos comentarios y docstrings de graph_ui no mencionan el caso inexistente, así que conviene incluirlo en el aviso.
   Resolución: una ruta relativa (`.sldb` con cwd en el proyecto) da OK con la ruta absoluta. El alias `shared` registrado con `link_store` da OK y apunta al store enlazado. Un alias desconocido `ghost` da `store not found: <cwd>/ghost`, ya no 'not prepared'. Un alias cuyo store enlazado fue borrado conserva su mensaje previo `Linked store 'shared' does not exist at ...`.
3. No crea el directorio: **PASA**. Después de los casos 5, 5b, 8 (padre inexistente) y 3b, el directorio sigue sin existir. Con un HOME limpio y sin llamar al CLI, `read_store(None)` y `read_store("")` no crean nada: el árbol es idéntico antes y después. En la primera corrida se vio un `~/.sldb`, pero lo creó el `sldb stores init` del script y no `read_store`; edge2 lo descarta.

## Casos que el ejecutor no cubrió (scripts en /dev/shm/tester-rs/, sin tocar el repo)
- `.sldb` que es un archivo y no un directorio: `store not found: <ruta>`. Es razonable, porque ahí `stores update` tampoco sirve.
- Padre inexistente (`nope/deep/.sldb`): `store not found`, sin crear nada.
- Alias desconocido: ahora `store not found` (antes 'not prepared').
- Descubrimiento por defecto sin store local ni global: sigue con el mensaje de siempre, `No local .sldb store found from ... No global store exists ...`, sin prefijo `store not found`.
  **Observación menor (no es FALLA):** el docstring nuevo dice `"store not found: <path>" when no store can be found`, pero el descubrimiento sin store lanza ese otro mensaje antes de llegar a `read_store`. El Goal solo cubre "no existe el directorio del store", y ese caso cumple; el docstring es algo más amplio que el comportamiento real.

## Alcance
`git status` muestra cambios fuera de `desk/` y `runs/` solo en los 3 archivos del contrato, más `.sldb/store.yaml`, `.sldb/core/store_index.yaml`, `.sldb/core/models/RunDoc.yaml` y dos shards RunDoc nuevos. Esos son el registro de los RunDoc de esta corrida (exec-rs y test-rs), hecho por deskops y no por el ejecutor. No aparecen los cambios ajenos que lista el brief (`apply_batch.py`, `lock.py`, etc.); ya no están en el árbol.

## Regresiones vecinas
El único módulo de `src/` que cambió es `src/sldb/api/stores/read_store.py`. `grep -rlE 'read_store|store_is_prepared' tests` da solo `tests/api/test_api_stores.py`: 14 passed, sin fallas nuevas respecto de HEAD.

## Reglas de clean code
`tests/test_clean_code_rules.py` y `tools/check.sh --fast` pasan, sin violaciones en los archivos tocados.
