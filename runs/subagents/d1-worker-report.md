# Informe del worker D1

Tarea: migrar SpecSync de spec2viz a `sldb.api.notations`, junto a NotationSync y PaletteSync (D1, B1; cierra lo pendiente de SV02).
Commit de código: `96109856` en main, sin push ni closeout. Este informe va en un commit aparte.
spec2viz no se tocó (`git status` limpio). Su retiro lo decide el gate IR13, la tarea IR13 del desk de IR.

## Qué se migró, de dónde a dónde

Origen: `spec2viz/spec2viz/sldb_sync.py` (la parte de specs y catálogo), `spec2viz/spec2viz/catalog_paths.py` y `_ELEMENT_COLLECTIONS` de `spec2viz/spec2viz/deskops.py`.
Destino: `src/sldb/api/notations/`. La lógica es la misma. Se partió en funciones y archivos más chicos por las reglas de tamaño (funciones de 10 líneas como máximo, archivos de 80).

| spec2viz | sldb |
|---|---|
| constantes `STYLE_KEYS`, `_EDGE_COLLECTIONS`, `_MESSAGE_RELATIONS`, `_ELEMENT_COLLECTIONS(_SYNC)`, `_EDGE_LABEL_FIELDS`, `_ELEMENT_OWN_FIELDS`, `ACTIVITY_*`, `_EDGE_ATTRIBUTE_FIELDS`, la tabla deploy/manifest | `spec_sync_constants.py` |
| `spec_style_kinds`, `relation_token`, `node_ref`, `to_slash_ref`, `_plain`, `stage_id`, `edge_name`, `relation_doc_has_attributes`, `find_store` | `spec_refs.py` (`_plain` pasa a llamarse `plain`) |
| `_element` | `spec_element.py` (`element`, `pairs`) |
| `_activity_pseudonodes`, `_pseudonode`, `_activity_edges` | `spec_activity.py` |
| `_matrix_elements`, `_matrix_edges` | `spec_matrix.py` |
| `spec_elements` | `spec_elements.py` |
| `spec_edges`, `_edge_label`, `_edge_attributes` | `spec_edges.py` |
| `resolve_spec_notation`, `_store_notation`, `_looks_like_path` | `spec_notation.py` |
| `catalog_paths` (repo_root, candidates, resolve_catalog_path, split_fragment) | `catalog_paths.py` |
| `catalog_entries` | `spec_catalog.py` |
| `check_catalog` | `spec_catalog_check.py` |
| `sync_catalog` | `spec_catalog_sync.py` (más la reconciliación con `prune`) |
| `SpecSync` | `spec_sync.py` (clase + `sync_spec`); los pasos están en `spec_sync_notation.py`, `spec_sync_docs.py`, `spec_sync_edges.py` y `spec_sync_steps.py` |
| `format_report`, `format_notation_report` | `spec_sync_report.py` (más `report_findings`) |
| `spec2viz diagram sync`, `catalog sync`, `catalog validate` | `sldb notations sync --spec`, `--catalog` y `--catalog --check` (`src/sldb/cli/commands/notations_spec_sync.py`) |

Se exportan desde `sldb.api.notations`: `SpecSync`, `sync_spec`, `check_catalog`, `sync_catalog`, `catalog_entries`, `spec_elements`, `spec_edges`, `resolve_spec_notation`, `format_report`, `format_notation_report`, `report_findings`, `edge_name`, `find_store`, `node_ref`, `relation_token`, `spec_style_kinds`, `stage_id` y `to_slash_ref`.

## Qué se reutilizó (no hay copia nueva)

- `StoreWriter` (`store_writer.py`): `SpecSync` hereda de él. El actor por defecto pasa de `spec2viz` a `sldb`.
- `SyncReport` (`sync_report.py`): en spec2viz `problems` era una propiedad. Aquí es un campo, y `with_problems` lo llena con `unresolved + edge_errors` justo después de `finish`. No se puede hacer antes de `finish`, porque `finish` es el que llena `edge_errors`. `format_report` lee el campo.
- `sync_constants.py`: `MODEL_REFS` y `_MANAGED_MODELS` ya cubrían SpecDoc y SpecNodeDoc.
- `NotationSync`, para la notación del spec. `DEFAULT_NOTATIONS`, `builtin_notations`, `load_notation`, `notation_ref` y `NotationSpec` salen de `sldb.notations`. Las excepciones salen de `sldb.notations.exceptions`.
- `find_store` es un envoltorio de `sldb.store.resolver.find_local_store`.
- `load_spec` y `validate_spec` de D3. `check_catalog` los usa en vez de `spec2viz.loader` y `spec2viz.validator`. La CLI pasa `load_spec` como `validate`.
- Los modelos SpecDoc y SpecNodeDoc de `sldb.models.notation`.

## Validación previa (`validate`)

`SpecSync(..., validate=None)`: el parámetro es un callable que recibe la ruta y lanza si el spec es inválido. Sin él, solo se comprueba que el YAML sea un mapa con `id` (`check_yaml_and_id`, que lanza `ParseError`). D3 ya estaba en main, así que `sldb notations sync --spec/--catalog` pasa `load_spec`. El test portado `test_invalid_spec_touches_nothing` también pasa `validate=load_spec`. Los demás tests portados usan la validación por defecto.

## Reconciliación y avisos

- Por spec: se borran los SpecNodeDoc y RelationDoc con prefijo `<spec_id>.` que ya no salen del spec, igual que en spec2viz.
- Por catálogo (nuevo): un SpecDoc es huérfano si tiene metadatos de catálogo (category, nav o summary no vacíos) y su id no está en el vistas.yml. Con `--prune` (o `sync_catalog(..., prune=True)`) se borra el SpecDoc junto con sus nodos y aristas. Sin `--prune` queda en `unresolved` de un informe extra `catalog <vistas.yml>`, con el texto `orphan SpecDoc:<id>: ...`. Un SpecDoc sincronizado solo con `--spec`, sin catálogo, nunca es huérfano.
- Findings (`report_findings`, formato `Finding` de sldb, nivel alert):
  - `spec-sync/unresolved-ref`
  - `spec-sync/orphan-spec`
  - `spec-sync/edge-error`

  La CLI los manda a stderr con `Finding.line()` y el fix, y también por `alert_sink.report(text=False)` para el envelope. `--strict` sale con 1 si hay alguno.

## CLI

`sldb notations sync`:

- Opciones nuevas: `--spec` (repetible), `--catalog`, `--check`, `--prune`, `--strict` y `--json`. Con `--spec`, `--notation` elige la notación del spec (`none` = sin notación).
- Salida: una línea de `format_report` por spec. Con `--json`, la lista de `SyncReport.to_dict()`.
- Store: `--store` o, si no se da, el `.sldb` más cercano hacia arriba del spec o del vistas.yml.
- Combinaciones rechazadas: `--spec` con `--catalog`, `--palette` con cualquiera de los dos, y `--notation` con `--catalog`.
- Sin `--spec` ni `--catalog`, `--notation` y `--palette` siguen como antes: salida JSON. Lo fija `test_notation_view_and_routes.py::test_cli_notations`.

## Tests

Todos de a un archivo, con `flock /dev/shm/sldb1-tests.lock python -m pytest -q -p no:cacheprovider <archivo>`, `TMPDIR=/dev/shm` y `PYTHONPATH=src`. Los stores son reales, en tmp_path, sin mocks.

| Archivo | rc | Resultado |
|---|---|---|
| tests/notations/test_spec_sync.py (16 portados de test_sldb_sync) | 0 | 16 passed |
| tests/notations/test_spec_catalog_sync.py (6 portados de test_catalog_notation; uno parametrizado ×3) | 0 | 8 passed |
| tests/notations/test_notations_sync_spec_cli.py (nuevos: prune, huérfano como finding, --json, --check) | 0 | 4 passed (la primera corrida falló por un fallo del helper del test, que reiniciaba el store; corregido) |
| tests/test_clean_code_rules.py | 0 | 1132 passed |
| tests/notations/test_notation_view_and_routes.py | 0 | 9 passed |
| tests/test_cli_every_command_has_a_handler.py | 0 | 1 passed |
| tests/test_address_surface.py | 0 | 8 passed |
| tests/test_standalone.py | 0 | 29 passed |
| tests/notations/test_notations_from_graph_cli.py | 0 | 6 passed |
| tests/segments/test_field_transclusion_and_diagram_segments.py | 0 | 5 passed |

`bash tools/check.sh --fast` (bajo el lock): PASS en núcleo aislado, capas, identidad, ejes y superficie. Para que pasara la puerta de ejes, se ajustaron en `contracts/layers.toml` estas cuentas, con comentario "medido 2026-11-15 (D1)":

- `nucleo.needed_by`: de 56 a 57, por vistas → contrato (`models/relation_doc.py`).
- unidad de persistencia, `needed_by`: de 48 a 49, por vistas → federacion (`store/resolver.py`).
- `notacion.needs`: de 6 a 8, por esas mismas dos aristas.

También se actualizó el `does` del eje `vistas`.

`deskops graph missing`: rc 0, 6 faltantes. Son los mismos 6 ajenos de D2 (task-diseño-jerarquía... y task-reglas-rule-graph...). Ninguno es nuevo.

No corrí la suite completa, `sldb stores build --check` ni selfdoc, porque así lo pidió el coordinador. Quedan para su control de entrega.

## Comparación con spec2viz, campo a campo

Script de una sola vez (no commiteado, en el scratchpad). Toma los 25 YAML de `tests/fixtures/specs` y `tests/fixtures/specs/examples` y los sincroniza en dos stores aislados en /dev/shm: uno con `spec2viz.sldb_sync.SpecSync` y otro con `sldb.api.notations.SpecSync`. Lo hace en dos rondas; en la segunda, cada spec tiene una arista menos, para ejercitar los borrados.

Resultados:

- Se compararon 50 syncs. En todas coinciden `created`, `updated`, `deleted`, `relation_types_added`, `unresolved`, `edge_errors`, `notation` y `problems`, y el texto de `format_report` es idéntico.
- Documentos en el store: 311 en cada lado, con los mismos nombres. Los payloads son iguales salvo en un campo: la `description` de los RelationTypeDoc. En spec2viz termina en " de spec2viz.". En sldb no lleva ese sufijo, igual que hace ya el NotationSync de sldb.
- Dos YAML que no son specs (`architecture-vistas.yml` y `project.yml`) se rechazan en los dos lados.

## Diferencias con spec2viz

1. Descripción de los RelationTypeDoc sin el sufijo "de spec2viz" (es la única diferencia de payload).
2. El actor por defecto es `sldb`.
3. `problems` es un campo del SyncReport, no una propiedad.
4. La validación previa es el parámetro `validate`. Por defecto solo comprueba el YAML y el `id`; la CLI pasa `load_spec`.
5. `check_catalog` valida con los modelos de sldb (D3).
6. `NotationMismatchError` y `UnknownNotationError` son las de sldb y no heredan de `ValueError`. Por eso el test portado espera `NotationMismatchError` en vez de `ValueError`.
7. En `test_refs_across_specs...`, la parte de `SldbAtomResolver.edges_of` (superficie de spec2viz, no migrada) se comprueba con `sldb_api.edges_to`.
8. La CLI pasa de click a argparse, con los cambios de nombres:

   | spec2viz | sldb |
   |---|---|
   | `diagram sync SPEC` | `--spec SPEC` |
   | `catalog sync --config` | `--catalog` |
   | `catalog validate` | `--catalog --check` |
   | `notation sync FILE` | `--notation FILE` |

   No se portó `--out`; está disponible como `SpecSync(out_dir=...)`. Si un spec falla, sldb no imprime los informes de los specs que ya se habían sincronizado antes que él; spec2viz los imprimía.
9. Lo nuevo: `--prune` y la detección de SpecDoc huérfanos del catálogo, los findings y `--json`.

## Pendientes

- El criterio de huérfano supone un catálogo por store: un SpecDoc con metadatos de otro vistas.yml en el mismo store se vería como huérfano. Sin `--prune` solo genera un aviso.
- Quedan para el coordinador la suite completa de a uno, `sldb stores build --check` y el closeout del TaskDoc. En el cierre hay que anotar que `validate` ya recibe `load_spec` (D3).
- El retiro de `spec2viz.sldb_sync` es el gate IR13, la tarea IR13 del desk de IR.

## Limpieza de /dev/shm

Borré `/dev/shm/d1-tests1.log` y `/dev/shm/d1-tests2.log`. El script de comparación borró él mismo su directorio `/dev/shm/d1cmp-*`. Mis basetemps de pytest (en `/dev/shm/pytest-of-robocop/`) ya los había rotado pytest y los que quedan son del coordinador, así que no toqué ninguno. Tampoco toqué `/dev/shm/d2-ts`.
