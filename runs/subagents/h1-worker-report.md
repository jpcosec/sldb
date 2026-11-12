# h1-worker: stores check ante documentos que su modelo rechaza (nota 3895e9f7, H1-H3)

Rama `wt/h1-check`, base `origin/main` `ce27c82b`. TaskDoc:
`task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e`
(con la CORRECCIÓN del coordinador del 2026-11-12: H2 y H3 se arreglan aquí).

## 1. Causa raíz (escrita y commiteada antes del arreglo)

### H1: `stores check` sale con `Unexpected`

Confirmada sobre `ce27c82b` con el store de `tests/store/invalid_memo_store.py` (tres `Memo`,
dos editados a mano a `status: bad`, que un `field_validator` rechaza). `api.check_store` y
`sldb stores check --format json` salen con `Unexpected: 1 validation error for Memo`, sin JSON:

```
sldb/api/stores/store_check.py:26  check_store
sldb/store/diagnostics.py:123      diagnose_store
sldb/store/diagnostics.py:109      _diagnose_model
sldb/store/diagnostics.py:58       _diagnose_doc
sldb/store/diagnostics.py:67       _fields_state
sldb/store/hashing.py:58           hash_fields_with_map
sldb/store/runtime_codec.py:11     extract
sldb/runtime/validation.py:65      extract_model_data
pydantic_core.ValidationError: 1 validation error for Memo
```

Nada entre `_diagnose_doc` y `extract_model_data` atrapa el `ValidationError` de un documento:
sale de `diagnose_store` y `sldb.cli.main` lo imprime como `Unexpected`. Test que lo fija
(falla en `ce27c82b`): `tests/store/test_doc_invalid_check.py`.

Rutas de `stores check` que extraen con el modelo, por documento (disposición, punto 4):

1. `diagnostics._diagnose_doc` → `_fields_state` → `hash_fields_with_map` (los campos). Sin guarda: H1.
2. `diagnostics._diagnose_model` → `field_set_drift.document_drifted` → `hash_fields_with_map`
   (contrato movido por documento), solo si su `field_hashes` nombra un campo que el modelo ya no
   declara. Sin guarda: el mismo `ValidationError`, antes de llegar a los documentos.
3. `store_surroundings._noise` → `scan_structural_noise` → `query.load_runtime_documents`, que
   extrae cada documento (`query._extract_doc`, `codec.extract`). Sin guarda: cuando 1 y 2
   no abortan, aborta aquí.
4. `store_surroundings._rewrite_loss` y la clave `rewrite_loss` de `check_store` →
   `scan_rewrite_loss` → `load_runtime_documents` (igual que 3); `rewrite_loss` en sí ya atrapa
   un documento que no extrae.
5. `on_check_findings` → `check_doc_anchors` → `compose_edge_index` (aristas y secciones): lee
   los shards; `live_stale` solo hashea el texto. No extrae con el modelo.
6. El contrato del modelo (`contract_moved`, `legacy_contract`) es por modelo, no extrae documentos.

### H2: una escritura cae por otro documento inválido del mismo modelo

La reproducción del coordinador corrió con caché caliente y H2 no apareció. Con caché frío
(sin `.sldb_cache` ni caché de usuario, como un clon limpio del gateway) **se reproduce en
`ce27c82b` y en `84eb7f75`** (`runs/subagents/h1-worker-repro_at.sh <rev>`, sobre deskops main
`0ccf497c` en `/dev/shm/deskops-main`, solo lectura):

```
### cold: sldb docs untrack tres
  Value error, Task task-repro-dos lifecycle is inconsistent: current_node: 'ritual-execution' does not follow history 'task_hands_to_closeout'; ...
rc=1
 M .sldb/core/documents/TaskCodeDoc/task-repro-dos.yaml
 M .sldb/core/documents/TaskCodeDoc/task-repro-uno.yaml
```

Traza (`api.untrack_document` en `ce27c82b`, caché frío):

```
untrack_document.py:69   forget_document
edge_rebuild.py:36       rebuild_edges_indexes
edge_sync.py:40          process_model_edges
edge_sync.py:56          _sync_model_docs          (every=True: sin caché, los shards no son confiables)
edge_sync.py:66          _sync_one
edge_doc_contribution.py:31  sync_doc_shard
edge_rebuild.py:69       _doc_edges
edge_index/doc_contribution.py:41  build_doc_edges
edge_index/doc_contribution.py:59  _declared_edges   (lee el payload sin guarda)
edge_rebuild.py:68       read_payload -> runtime_codec.extract -> extract_model_data
pydantic_core.ValidationError: 1 validation error for TaskCodeDoc
```

Mecanismo: sin caché (`_untrusted`), el rebuild de aristas de un modelo reconstruye el shard de
**cada** documento del modelo. Para un modelo que declara referencias (`__references__`,
`__containment__`, `__compositions__`, `__doc_anchors__`), `_declared_edges` lee el payload con
`payload_of()` sin guarda, mientras la proyección del nodo (`payload_projection._read`, d7eefdeb)
sí atrapa `ValueError`. Con caché caliente solo se reconstruye el conjunto sucio, que no incluye
a los inválidos: por eso la reproducción en caliente no lo mostraba. Ningún commit lo arregló:
el modelo de prueba sin referencias (`status` solo) tampoco cae en `84eb7f75`.

### H3: el rollback deja índices a medio escribir

Lo que deja escrito el untrack fallido de H2: `core/documents/TaskCodeDoc/task-repro-{dos,uno}.yaml`
modificados (los shards de documento de los **otros** documentos, versionados), porque
`forget_document` hace snapshot solo de `_registry_files` (el shard del documento que sale, el
índice del modelo y el del store), y el rebuild de las derivadas reescribe además los shards de
los demás antes de caer. Quién los reescribe (diff del shard de `task-repro-dos` tras el untrack
en frío): `rebuild_semantic_indexes`, que corre antes que el de aristas, le quita
`artifact:task` y `workspace:desk` de `semantic_tags`. `semantic_doc_tags._extract_tags` atrapa
el `ValidationError` del documento inválido y lo lee como payload `{}`, así que los tags que
vienen de sus campos desaparecen y el shard versionado se reescribe sin ellos. Pasa en cada
rebuild en frío, no solo cuando falla: con H2 arreglado, el untrack terminaría bien y seguiría
dañando los shards de los otros inválidos. Dentro de una transacción, esos archivos cambian sin
snapshot (`unsnapshotted_drift`) y el rollback termina en `RollbackError: Rollback incomplete`.
La transacción ya restaura lo que snapshotea y borra lo nuevo de `.sldb/` y `.sldb_cache/`
(`transaction_state.rollback`): lo que faltaba era no escribir lo que no le toca.

### Confirmación con pytest en `ce27c82b` (copia en `/dev/shm`)

- `tests/store/test_doc_invalid_check.py`: 2 failed (`ValidationError: 1 validation error for Memo`).
- `tests/store/test_doc_invalid_writes.py`: 4 failed, 4 passed. Los 4 casos en frío fallan (untrack de `a` y de `c`, escritura transaccional, transacción fallida: `ValidationError`, y sin el `RuntimeError` esperado); los 4 en caliente pasan, que es lo que vio el coordinador.

## 2. Arreglo

- **H1** (`store/doc-invalid`): `DiagnosisNote.DOC_INVALID`; `store/diagnostics_models/invalid_verdict.py`
  (`fields_state`, `invalid_message`) atrapa el `ValidationError` de `hash_fields_with_map` y arma el
  `DocumentDiagnosis` con `detail` = `invalid: <Model> rejects <path>: <N> validation error(s); first: <loc>: <msg>`
  (primera línea de hasta 3 errores, sin la URL de pydantic). El código está en `_DOC_CODES`
  (`store_findings.py`) y en `policy.ERRORS`: el nivel lo decide la política del store, no solo el
  hallazgo (una primera versión salía como alerta y rc 0). Es error, `is_valid` falso, entra en
  `damaged_documents` y en `NEEDS_DECISION`.
- **Una sola vez**: `field_set_drift` ya no re-extrae por documento (devuelve "no derivó" si el modelo
  rechaza); `scan_structural_noise` y `scan_rewrite_loss` leen con
  `load_runtime_documents(..., accepted_only=True)` (sin caché, saltan los rechazados);
  `once_per_invalid` quita cualquier otro hallazgo con sujeto `Modelo:nombre` de un documento inválido.
- **H2**: `edge_index/doc_contribution.build_doc_edges` envuelve `payload_of` con
  `payload_projection.read_payload` (la guarda de siempre, ahora pública): un documento rechazado no
  aporta aristas declaradas ni proyección y el rebuild sigue.
- **H3**: `semantic_doc_tags` conserva los tags de un documento rechazado en lugar de leerlo como `{}`;
  con eso el rebuild no reescribe los shards versionados de los inválidos, y la transacción fallida deja
  el árbol como estaba, caché incluida (el rollback ya restauraba lo snapshoteado).
- `_diagnose_doc` se partió en `_diagnose_doc` y `_compared` por el límite de 10 líneas de lógica.

## 3. Validación (desde `/dev/shm/sldb-h1`, de a un archivo, tras `wait-pytest`)

- `tests/store/test_doc_invalid_check.py`: 2 passed; `tests/store/test_doc_invalid_writes.py`: 8 passed
  (untrack de `a` y de `c`, escritura transaccional, transacción fallida; cada uno en frío y en caliente,
  en proceso nuevo).
- Suite completa: los 187 `tests/**/test_*.py` uno por uno, todos verdes salvo `test_clean_code_rules` (1
  fallo: `_diagnose_doc` con 13 líneas de lógica), que quedó en 960 passed tras partir la función. La
  partición se hizo después de la corrida completa; tras ella se repitieron `test_clean_code_rules`,
  `test_doc_invalid_*`, `test_diagnostics`, `test_unresolved_model_check` y `test_field_set_drift`.
  Los skips (anchors, machine_editor_schema, fingerprints, treesitter) son de dependencias opcionales
  y ya lo eran.
- `bash tools/check.sh --fast`: TODAS LAS PUERTAS PASAN (ejes: 748 archivos mapeados, 0 violaciones;
  sin cambio en `contracts/layers.toml`).
- Los 7 pasos del workflow en clon limpio: los corre el coordinador.
- Docs: `docs/user-manual.md` §5 (documento que su modelo rechaza). CHANGELOG: entrada en 0.1.13.
