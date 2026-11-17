# Ejecutor deskops-e-a7eadfe52463-a2 — task-contract-signature-cubre-indexed-doc-anchors-y-contract-y-un-campo-no-puede-ser-a-la-vez-referencia (intento 2)

## Punto de partida
`git apply --exclude=CHANGELOG.md runs/subagents/20261116-exec-contract-signature/executor-diff-paused.patch` aplicó limpio sobre HEAD 502ef641. La línea del CHANGELOG se copió tal cual del parche como primera entrada bajo `## 0.1.13 — not released yet (no tag, not on PyPI)`. El hunk de CHANGELOG no aplicaba porque j02 y B2-SQL agregaron entradas encima.

## Cambios (archivo y función)
- `src/sldb/store/model_contract.py`: `_DECLARED` suma `indexed`, `doc_anchors` y `contract`. Así `contract_signature` firma las tres claves siempre, con `[]` si el modelo no las declara. La docstring está actualizada.
- `src/sldb/store/models/edge_node_record.py`: actualizada la descripción del campo `EdgeNodeRecord.contract_signature`.
- `src/sldb/models/doc_anchor_value.py`: `definition_problems` suma el problema `field '<n>' is declared in both __references__ and __doc_anchors__`. Lo lanza como `SLDBModelError` la función `doc_anchor_fields`, que ya existía; no se agregó otro punto de lanzamiento.
- `tests/store/test_payload_projection.py`: test nuevo `test_a_new_indexed_is_stale_and_the_rebuild_projects_the_new_field`. Además, `test_projected_fields_and_the_signature_follow_the_class` comprueba ahora que cada uno de `__containment__`, `__indexed__`, `__doc_anchors__` y `__contract__` cambia la firma.
- `tests/api/test_doc_anchors.py`: test nuevo `test_doc_anchors_added_to_a_model_with_indexed_documents_is_stale_and_the_rebuild_adds_the_edge` y un caso más (doble declaración) en `test_an_invalid_model_definition_is_refused_when_loaded`.
- `CHANGELOG.md`: entrada "**Fuerza un rebuild**" en 0.1.13.

## Revisión del diff contra el HEAD actual (lote 2, B2, B3, j02)
- Los consumidores de `contract_signature` no cambiaron de forma: `edge_sync.py`, `payload_projection.py`, `live_stale.py`, `edge_doc_contribution.py` y `composed_disk.py`. No hubo que ajustar el diff.
- `stores rebuild-index` (j02) no usa `contract_signature`, así que no le afecta.
- Nota sin cambio: `src/sldb/store/edge_index/composed_disk.py:97` concatena `contract_signature(c)` con `__doc_anchors__` y `__contract__` sueltos. Ahora es redundante pero inocuo, y el archivo está fuera del alcance. Queda para el drawer si se quiere simplificar.

## Done When
- Los tests nuevos pasan: test_payload_projection 41 passed (rc=0) y test_doc_anchors 24 passed (rc=0).
- CHANGELOG avisa que fuerza un rebuild: sí.
- `sldb stores build --check --store .sldb`: **delegado al integrador** (brief y punto 2 del coordinador). No se corrió.
- `.sldb` del repo reconstruido: **no hecho**. Intenté `flock -w 900 /dev/shm/sldb1-tests.lock ... sldb stores build --store .sldb` y el clasificador de permisos de Claude Code lo denegó (Destructive or Unwanted Actions); no llegó a correr. El coordinador o el integrador tienen que correrlo antes del closeout y agregar `.sldb/core`. Ojo: hoy `.sldb/` tiene cambios del coordinador sin commitear.
- Avisos a deskops y graph_ui: no enviados (punto 4 del coordinador). Quedan para el coordinador en el closeout.

## Comandos (salida completa en validation.log)
| comando | rc |
|---|---|
| pytest -q tests/store/test_payload_projection.py | 0 (41 passed) |
| pytest -q tests/api/test_doc_anchors.py | 0 (24 passed) |
| pytest -q tests/test_clean_code_rules.py | 0 (1190 passed) |
| bash tools/check.sh --fast | 1 |
| sldb stores build --check --store .sldb | delegado al integrador |

`check.sh --fast` rc=1 solo por la puerta «identidad»: `ERROR archivo versionado sin clasificar en la raíz: AGENTS.md`. Ese archivo entró en 7dbb6bc9 (j02) y no lo toca esta tarea. El resto de las puertas dan PASS: núcleo, capas, ejes y superficie. No hay ninguna violación en archivos tocados. Hay que clasificar AGENTS.md en el contrato de identidad: queda como tarea aparte para el coordinador.

## Archivos tocados
- CHANGELOG.md
- src/sldb/models/doc_anchor_value.py
- src/sldb/store/model_contract.py
- src/sldb/store/models/edge_node_record.py
- tests/api/test_doc_anchors.py
- tests/store/test_payload_projection.py
- runs/subagents/20261116-exec-contract-signature-i2/{validation.log,result-summary.md}

Sin commit, sin stage y sin avisos.
