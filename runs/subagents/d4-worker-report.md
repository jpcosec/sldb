# Informe del worker D4

Tarea: `task-emparejamiento-de-átomos-con-elementos-de-diagrama-explícito-y-difuso-en-sldb-api-matching-d4`.
Commit: el commit "D4:" en main (sha en el resumen al coordinador; `git log --grep "^D4:"`). Sin push ni closeout.

## Qué se migró, de dónde a dónde

Origen: `spec2viz/spec2viz/deskops.py`. spec2viz no se tocó (`git status` limpio en spec2viz).
Destino: `src/sldb/api/matching/`, un módulo por pieza, exportadas desde `sldb.api.matching`.

| Destino | Origen (spec2viz.deskops) |
|---|---|
| `atom_keys.py` | `label_key` (tal cual, sigue igual a `normKey`), `_normalize_key` → `normalize_key`, `_alias_candidates` → `alias_candidates` (troceada en título y etiquetas, mismo orden y sin repetidos) |
| `atom_payload.py` | `parse_atoms` (mismo JSON; los fallos van a una lista de findings opcional en vez de `print`), `SldbAtomResolver._merge_atom` → `merge_atom`, `_load_store_payload_uncached` → `atoms_from_documents` |
| `atom_tags.py` | `_tag_matches` → `tag_matches`, `filter_atoms_payload` |
| `spec_view.py` | nuevo: `SpecView` (datos planos que sustituyen a `CatalogItem`: key=anchor_id, id, specs ya cargados, source, base_dir, store, title, diagram_type, scope) |
| `spec_view_elements.py` | `_spec_elements` → `spec_view_elements`, `collect_explicit_atoms`, `collect_explicit_refs` |
| `explicit_atoms.py` | `_atom_index` → `atom_index`, `build_explicit_atoms` |
| `explicit_refs.py` | `build_explicit_refs`, `attach_atom_edges` |
| `atoms_by_view.py` | `build_atoms_by_view`, `_raw_atoms_by_view` → `raw_atoms_by_view` |
| `store_documents.py` | `SldbAtomResolver._load_store_documents` → `store_documents`, `resolve_ref`, `_ref_payload` → `ref_payload` |
| `store_edges.py` | `SldbAtomResolver.edges_of` (filtro de relaciones estructurales) → `edges_of` |
| `store_reader.py` | `StoreReader`: lo que queda de `SldbAtomResolver` sin descubrimiento (caché por store, avisos una vez) |
| `coverage.py`, `coverage_views.py`, `coverage_elements.py` | `build_coverage_by_view`, `_discover_snapshot_path`, `_project_root_from_snapshot`, `_item_source_ref`, `_empty_coverage_payload`, `_project_view_payload`, `_project_element_payload`, `_source_field_for` |
| `matching_findings.py`, `unknown_atom_error.py` | `AtomBuildWarning`/`CoverageBuildWarning` → `Finding` de sldb; `UnknownAtomError` (ahora lleva `.findings`) |
| `atom_ranking.py` | nuevo, sin matcher propio: `atom_index_items` y `rank_atoms` sobre `DocumentIndex.rank` |

Las funciones largas se trocearon en ayudantes de ≤10 líneas sin cambiar la lógica (regla de código limpio).

Quedan en spec2viz (capa visual, fuera de alcance): `render_deskops`, `build_deskops`, `split_shared_atoms`, el adaptador `CatalogItem` → `SpecView` y el JS del template (incluido `findAtomData`).

## Qué se reutilizó de sldb

- `sldb.api.matching`: `DocumentIndex.rank` sobre `Matcher`/`DifflibMatcher` para el emparejamiento difuso. Se indexa por átomo su título, sus alias y su cuerpo. No hay un segundo matcher en sldb.
- `sldb.api.notations`: `_ELEMENT_COLLECTIONS` (D1 ya lo había migrado a `spec_sync_constants`) y `pairs` (lee una colección escrita como mapa o como lista). No se reutilizó `spec_elements` de D1: ese agrega las colecciones de reflection y de paquetes de clase, los pseudonodos de actividad y las matrices, y eso cambiaría el conteo de vistas "completas". El criterio de misma salida observable no se cumplía.
- La API de store de sldb en vez de `SldbAtomResolver`: `load_runtime_documents` y `open_store` (para la raíz del proyecto) para los documentos, `edges_from`/`edges_to` para las aristas, y `sldb.core.finding.Finding` para los avisos.
- No se migró el descubrimiento del store (`_discover_store_for_item`, `_find_*`, `_store_exists`, `_is_relative_to`, `_find_repo_root`). La vista trae su `store`: lo decide el adaptador (por ejemplo con `sldb.api.notations.find_store`).
- No se migró `normalize` por `label_key`, tal como pide el TaskDoc.

## Avisos (findings)

Todos usan nivel `warning`, y `error` con `strict`. `raise_if_strict` lanza `UnknownAtomError` con los findings de nivel error. La lógica ya no imprime nada.
Códigos: `matching/unknown-atom` (subject `vista#nodo`, fix "crear el átomo o corregir el id"), `matching/unknown-ref`, `matching/no-store`, `matching/coverage-snapshot-missing`, `matching/coverage-snapshot-unreadable` y `matching/atom-parse-failed`.
**Dos códigos agregados que el TaskDoc no lista** cubren avisos que spec2viz ya emitía: `matching/store-unreadable` ("Failed to load documents through SLDB") y `matching/edges-unavailable` (store sin índice de aristas, se avisa una vez).

## Decisión sobre test_refs.py (matriz IR07, SV-I03)

**Sí corresponde.** Prueba la resolución de `refs:` y las aristas de los átomos (`collect_explicit_refs`, `build_explicit_refs`, `edges_of`, `attach_atom_edges`, la lectura de documentos del store), que son parte de esta pieza. Se portaron 9 de sus 14 casos a `tests/matching/test_matching_refs.py`. Donde spec2viz falseaba el store con monkeypatch, aquí hay un store sldb real en el tmp de la prueba (en /dev/shm), sin mocks.
No se portan: `test_models_accept_refs`, `test_refs_without_model_part_are_rejected` y `test_state_model_and_schema_expose_refs`, que son de modelos y schema (tarea de modelos de spec, D3 e IR12). Tampoco `test_store_discovery_uses_a_real_store`, porque el descubrimiento no se migra, ni `test_no_internal_sldb_imports`, que no aplica dentro de sldb.
También se portaron de `tests/test_deskops.py` (SV-I04): `test_parse_atoms_handles_missing_dir`, `test_parse_atoms_builds_index_and_skips_bad_files`, `test_build_coverage_by_view_projects_snapshot_payload` y `test_build_atoms_by_view_uses_store_scoped_payload` (este último con store real).
El TaskDoc se actualizó con `deskops edit task … validation … --root .`, que agrega un ítem con estos tests.

## Tests

Comando: `flock /dev/shm/sldb1-tests.lock python -m pytest -q -p no:cacheprovider …`, con TMPDIR=/dev/shm.

| Archivo | Resultado |
|---|---|
| tests/matching/test_matching_explicit.py | 11 (los 6 del TaskDoc, 2 de parse_atoms, alias, label_key/normKey) |
| tests/matching/test_matching_refs.py | 10 (9 de test_refs y el de build_atoms_by_view) |
| tests/matching/test_matching_coverage.py | 3 (el portado, descubrimiento hacia arriba, snapshot faltante o ilegible) |
| tests/matching/test_matching_fuzzy.py | 3 (nuevo: emparejamiento difuso con alias vía DocumentIndex.rank) |
| tests/matching/ (junto, -n 4) | 26 passed, rc 0 |
| tests/test_clean_code_rules.py + tests/matching/ (-n 4) | 1175 passed, rc 0 |
| `bash tools/check.sh --fast` | rc 0: núcleo aislado, capas (0 violaciones), identidad, ejes y superficie en PASS |

Ejes: la primera corrida falló con 4 cuentas medidas de unidades. Sobre una copia de HEAD pasaba, así que las 4 son de D4. Se ajustaron en `contracts/layers.toml` con el comentario "medido (D4)": `nucleo` needed_by 57→58, `recuperacion` needs 4→9, `notacion` needed_by 3→4 y `operacion` needed_by 12→15. **Para revisión:** `recuperacion` mantiene `extractable_today = true`, pero ahora depende de 9 unidades (lee stores, aristas y notations por sldb.api). Si se quiere conservar `api/matching` como puerto puro y extraíble, el emparejamiento de átomos podría vivir en su propio eje o subpaquete. Lo decide el coordinador.

## Diferencias con spec2viz

1. Las funciones reciben `SpecView` en vez de `CatalogItem`. Los specs ya vienen cargados, y el store es un campo de la vista en vez de descubrirse.
2. Los avisos son `Finding` y la lógica ya no imprime. `UnknownAtomError` lleva `.findings`. `parse_atoms(dir, findings=None)` conserva su salida JSON.
3. `build_explicit_refs(views, reader=None, strict=False)` usa `StoreReader` en vez de `SldbAtomResolver` (sin `pythonpath` en el constructor de la vista: va en `StoreReader(pythonpath)`).
4. `source_ref` en la cobertura usa `view.source` (lo arma el adaptador) en vez de `item.src`. El descubrimiento del snapshot parte de `view.base_dir` (o de la carpeta de `source`).
5. Las vistas que comparten store ya no comparten el mismo objeto de payload: cada vista recibe su propio dict.
6. El emparejamiento difuso del navegador (`findAtomData`) no tiene equivalente uno a uno. En sldb es `rank_atoms`, un ranking con puntaje sobre DocumentIndex (difflib sin red o embedder), no las reglas de frase y tokens del template. El JS sigue en spec2viz (SV-G08).

## Anotaciones del catálogo con autoguardado: `sldb serve` alcanza

Prueba real contra `sldb serve --store <tmp>/.sldb --pythonpath <tmp>` (puerto 18764, en /dev/shm, con `timeout 90`), sobre un store con AtomDoc:atom-y:
- `GET /document?id=atom-y` → 200, con `id`, `model_name`, `path`, `payload`, `semantic_tags` e `ir`.
- `POST /save` con `{"changes":[{"id":"atom-y","action":"update","model":"AtomDoc","payload":<nuevo>,"expected":<payload leído>}]}` → 200 `{"ok":true,"saved":["atom-y"]}`. La relectura devuelve el cambio.
- El mismo `POST /save` con `expected` viejo → 409 ("atom-y cambió en SLDB. Recarga…").
- `POST /save` con `expected_source_hash` viejo → 409.

Las tres cosas funcionan, así que alcanza y no se envió nota al inbox. Rutas a usar: `GET /document?id=` para leer y `POST /save` con `changes[].expected` = el payload leído como guarda optimista.
Observación, no bloqueante: `GET /document` no devuelve `source_hash` ni `version`. Por eso la guarda práctica es `expected` (igualdad de payload) y no `expected_source_hash`. Si IR13b quisiera guardar por hash, haría falta exponerlo en la lectura.

## Limpieza de /dev/shm

Se borraron `/dev/shm/d4-serve` (store y log del serve), `/dev/shm/d4-validation.json`, `/dev/shm/d4-probe`, `/dev/shm/d4-head` (copia de HEAD para medir ejes) y `/dev/shm/d4-check.log`. Los basetemps de pytest (`/dev/shm/pytest-of-robocop/…`) ya no existían al revisar. El proceso serve terminó solo por `timeout` (health ya no responde). No se tocó `/dev/shm/sldb1-tests.lock` ni los archivos de otros.

## Pendientes

1. No se corrió `sldb stores build --check`, selfdoc ni la suite completa de a uno (el encargo los prohíbe). Tampoco `deskops graph missing`.
2. `deskops edit task` también reescribió el índice del store: el yaml del documento TaskCodeDoc, `TaskCodeDoc.yaml` y el store_hash. Esos cambios entraron en el commit de closeout de D2 (7f58222c), hecho mientras D4 trabajaba. El commit de D4 lleva solo el `.md` del TaskDoc. `.sldb/store.yaml` y `InboxNoteDoc.yaml` traían cambios ajenos de notas de inbox de IR y no se tocaron.
3. El adaptador `CatalogItem` → `SpecView` en spec2viz/specIR (IR13b) no es de esta tarea.
4. `uv.lock` modificado de antes, no se toca.
