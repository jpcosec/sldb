# result-summary — tester deskops-t-5021a6084fb0

Tarea: task-ci-el-test-de-graph-path-explicado-sobre-datos-reales-pasa-en-un-clon-limpio-sin-sldb-cache-ni-archi
Veredicto global: **PASA**. Toda la salida está en `validation.log`.

## Validation (corrida por mí en el checkout de trabajo)
| Comando | Resultado |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py` | PASA: 10 passed, rc=0 |
| `... pytest -q tests/test_clean_code_rules.py` | PASA: 1177 passed, rc=0 |
| `... bash tools/check.sh --fast` | PASA: "TODAS LAS PUERTAS PASAN", rc=0 |

`uv` funcionó; no hizo falta el fallback a uvx. La suite completa y `sldb stores build --check` no están en Validation; quedan delegados al integrador.

## Done When, punto por punto
- **Los comandos de Validation pasan**: PASA (tabla de arriba).
- **El test pasa en un clon limpio sin .sldb_cache y con XDG_CACHE_HOME vacío (aclaración 1)**: PASA. Pasos: `git clone` del checkout a /dev/shm/ci1t-clon (HEAD 34b26a50), copia encima del test sin commitear y comprobación de que no existen `.sldb_cache` ni `knowledge/symbols` y de que `/dev/shm/ci1t-xdg` tiene 0 entradas. Luego `XDG_CACHE_HOME=/dev/shm/ci1t-xdg TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q -p no:cacheprovider tests/api/test_api_graph_analysis.py` → 10 passed, rc=0.
  - Control en el mismo clon con el test de HEAD: `FAILED ...::test_explain_over_the_repo_own_index_names_origin_and_relation_doc`, 1 failed / 9 passed, rc=1. Así se reproduce el fallo de CI y se confirma que el cambio lo arregla.
  - El clon y el directorio XDG se borraron al terminar (verificado).
- **El result-summary del ejecutor trae la salida en el clon limpio con rc 0**: PASA (sección "Salida en el clon limpio").
- **commit**: pendiente. El ejecutor no commiteó por la aclaración 5; le toca al coordinador.

## Aclaración 2: ¿cubre lo que cubría el test viejo?
PASA. El test viejo solo exigía que cada arista trajera `origin` y además `relation_doc` o `field`; en la práctica, con los datos reales, solo ejercía `relation_doc`. El nuevo conserva literalmente esa aserción y añade dos más:
- los orígenes son exactamente `{"schema", "relation_doc"}`;
- `edges[0].provenance == {"origin": "schema", "field": "about"}`, es decir, una arista con `field`;
- `edges[1:] == [_refines("s3-s2"), _refines("s2-s1")]`, donde `_refines` fija `{"origin": "relation_doc", "relation_doc": ...}`.

Cubre los dos tipos de arista y es más estricto que el viejo. Lo que pierde es el uso de datos reales del desk (las aristas entre RitualDoc); el Scope lo pide así.

## Aclaración 3: mutación de path_steps
Hice cada mutación en una copia en /dev/shm de `src/sldb/store/graph/analysis/path_steps.py` y corrí solo el test nuevo (`-k over_a_store_built_in_tmp`):
| Mutante | Resultado |
|---|---|
| M1: `_provenance` devuelve `{}` | FALLA el test (KeyError 'origin'): mutante muerto |
| M2: sin `relation_doc`/`field` (solo origin) | FALLA (AssertionError `{'origin':'schema'}` != `{..., 'field':'about'}`): muerto |
| M3: sin `origin` (solo detalle) | FALLA (KeyError 'origin'): muerto |
| M4: `_item` sin clave `provenance` | FALLA (KeyError 'provenance'): muerto |

Las 4 mutantes mueren.

## Caso extra que no cubrió el ejecutor (punto 4)
Script `test_ci1t_extra.py` en el clon de /dev/shm, que ya está borrado; su contenido completo está en el log. Resultado: 3 passed.
- Camino inverso `Spec:s1 → Card:c1`: la arista schema sale con `direction: backward` y conserva `field: about`, y las refines salen backward con su relation_doc.
- Con `relations=["refines"]` no hay camino (None): la arista `references` es la que une.
- Con las relaciones por defecto el camino es `None`. Confirma la nota del ejecutor de que `references` no es authored por defecto, y por eso el test pasa `relations` explícito. No es un fallo, solo una observación para el coordinador.

## Alcance y regresiones vecinas
- Fuera de `.sldb/`, `desk/`, `runs/` y `.herdr-coordination.md` (ajenos), solo cambia `tests/api/test_api_graph_analysis.py`, el único archivo del contrato.
- No hay módulos de `src/` cambiados, así que no hay tests vecinos que correr. Los cambios ajenos que listaba el brief (apply_batch.py, lock.py, test_apply_batch_lock.py, uv.lock) no aparecen modificados en el árbol en este momento.
- Clean code: 1177 passed y check.sh --fast en verde, con el archivo tocado incluido.

## Observación
Al primer intento, `git diff --name-only` quedó vacío en el log por un fallo de captura mío. Lo repetí y la salida correcta está más abajo en el log.
