# Tester deskops-t-2fcaf5e3932d: task-contract-signature-… (intento 2)

**Veredicto: PASA.** Lo que falta para cerrar (el `.sldb` reconstruido, `build --check` y los avisos) le toca al coordinador y al integrador, según la aclaración del coordinador. La salida completa está en `validation.log`.

## Validation
| comando | resultado |
|---|---|
| pytest -q tests/store/test_payload_projection.py | PASA: 41 passed, rc=0 |
| pytest -q tests/api/test_doc_anchors.py | PASA: 24 passed, rc=0 |
| sldb stores build --check --store .sldb | delegado al integrador; no lo corrí |
| pytest -q tests/test_clean_code_rules.py | PASA: 1190 passed, rc=0 |
| bash tools/check.sh --fast | rc=1, solo en la puerta identidad (`AGENTS.md` sin clasificar). Núcleo, capas, ejes y superficie dan PASS. |

**Sobre check.sh y HEAD.** La puerta identidad lee `git ls-files`. Por eso una copia de HEAD sacada con `git archive` y sin `.git` la pasa sin comprobar nada. Hice `git init` y `git add` en `/dev/shm/t2fc-head` y la corrí ahí: HEAD da el mismo `ERROR archivo versionado sin clasificar en la raíz: AGENTS.md`, con rc=1. Ese fallo ya estaba (entró con j02, en 7dbb6bc9), y `AGENTS.md` no tiene cambios respecto de HEAD. Ninguna violación cae en un archivo tocado.

## Done When
- **Los tests nuevos pasan: PASA.** Están `test_a_new_indexed_is_stale_and_the_rebuild_projects_the_new_field`, `test_projected_fields_and_the_signature_follow_the_class` (que ahora prueba containment, indexed, doc_anchors y contract), `test_doc_anchors_added_to_a_model_with_indexed_documents_is_stale_and_the_rebuild_adds_the_edge` y el caso de doble declaración en `test_an_invalid_model_definition_is_refused_when_loaded`.
- **La firma: PASA.** `_DECLARED` suma `indexed`, `doc_anchors` y `contract`. Las tres claves van siempre en la firma, con `[]` cuando el modelo no las declara. La docstring de `contract_signature` y la descripción de `EdgeNodeRecord.contract_signature` están actualizadas.
- **La doble declaración: PASA.** `definition_problems` devuelve `field '<n>' is declared in both __references__ and __doc_anchors__` y `doc_anchor_fields` lanza `SLDBModelError`. Lo comprobé también a través de `api.add_model`.
- **CHANGELOG avisa que fuerza un rebuild: PASA.** Es una sola línea bajo `## 0.1.13 — not released yet`.
- **El `.sldb` del repo reconstruido en el commit: no hecho.** Le toca al coordinador o al integrador (aclaración 2). Los cambios de `.sldb/` que hay hoy en el árbol son del coordinador.
- **Avisos a deskops y graph_ui: no enviados.** Le tocan al coordinador en el closeout.

## Aclaración 3: copia de un store en /dev/shm
Lo hice con el script `/dev/shm/t2fc-edge/edge_check.py`, que pasó 16 de 16 comprobaciones:
- Armé un store con documentos indexados (Target y dos Pointer) y lo copié entero con `copytree`. Antes del cambio, ni el original ni la copia estaban stale.
- **`__indexed__` nuevo.** En la copia quedan stale `Pointer:p` y `Pointer:q`, y Target no. Después de `rebuild_edges` no queda nada stale y el payload pasa a ser `{'status': 'open'}`.
- **`__doc_anchors__` nuevo.** Los mismos dos documentos quedan stale. Después del rebuild no queda nada stale y aparece la arista `references` de `Pointer:p` a `sldb://document/Target:t`, con field `about`.
- **`__contract__` nuevo.** Quedan stale y el rebuild lo resuelve.
- El store original, que no se reconstruyó, sigue stale frente al modelo nuevo. Así que el rebuild de la copia no lo tocó.

## Casos que el ejecutor no cubrió (mismo script)
- La doble declaración **heredada** también se rechaza: `__references__` en la clase base y `__doc_anchors__` en la hija dan `SLDBModelError` en Child.
- Un campo de referencia y otro de ancla **distintos** se aceptan.
- `api.add_model` rechaza la doble declaración con `SLDBModelError`.
- El orden de `__indexed__` no cambia la firma, porque se ordena.
- **Hallazgo (no es FALLA: el contrato lo pide así).** Pasar `__indexed__` de *ausente* a `[]` deja la misma firma, por el "o []" del Scope. Pero la proyección cambia: sin la clave se proyectan todos los campos y con `[]` no se proyecta ninguno. Lo probé de punta a punta en `/dev/shm/t2fc-edge/indexed_empty.py`. Después del cambio no queda nada stale, y el rebuild deja el payload `{'status','title'}`, cuando un store creado ya con `[]` proyecta `{}`. Con `__contract__` pasa lo mismo: ausente quiere decir todos los campos y `[]` quiere decir hash None (H11), y los dos dan la misma firma. Esto queda para el drawer. Arreglarlo es tan simple como distinguir `None` de `[]` en el cuerpo firmado, por ejemplo `getattr(...)` sin el `or []`.

## Alcance
- Fuera de `.sldb/` y `desk/` (que son del coordinador) y de lo ajeno que lista el brief, el diff solo toca los 6 archivos del contrato.
- `uv run --frozen` anduvo bien.

## Regresiones vecinas
Los módulos cambiados son `sldb.store.model_contract`, `sldb.store.models.edge_node_record` y `sldb.models.doc_anchor_value`. Busqué con grep los archivos de `tests/` que los importan: son 11, y los corrí uno por uno.
- 10 pasan: test_api_graph_analysis, test_doc_anchors, test_unresolved_references, test_contract_in_model_node, test_graph_analysis, test_graph_executor, test_graph_neighborhood, test_payload_projection, test_predicate_language y test_upgrade_compat.
- `tests/test_store_seams.py` da 1 failed (`io/derived_guard.py: sldb.core.exceptions`). **En HEAD falla igual** (lo corrí en `/dev/shm/t2fc-head`): ya venía de j02 y no es una regresión de esta tarea.

## Prohibido, respetado
No usé stash, add ni commit, y no edité `desk/` ni `.sldb/`. No corrí la suite completa ni `build --check`.
