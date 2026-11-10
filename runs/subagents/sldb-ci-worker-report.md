# main de sldb en verde: informe del worker (sci-worker, 2026-11-10)

TaskDoc: `desk/tasks/task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024.md`.
Rama `wt/main-de-sldb-en-verde`, base `55c39605` (sldb origin/main). Sin push (b1: lo pushea el coordinador).
Run de referencia: 42758984024 sobre `c1f41105`. Logs en `~/proyectos/SLDB_1/coord2-ccconfig/sci/`.

Este informe tiene cinco fallos. Tres los mostró el run: `identidad`, `ejes` (archivos sin eje y grados de unidad) y el
paso de deskops del job store. El cuarto y el quinto aparecieron en los pasos 6 y 7, que el CI no alcanzó.
Ningún arreglo usa skip ni xfail, ni relaja un gate o baja un umbral. Lo que faltaba clasificar se clasificó.

## Commits

| commit | fallo |
|---|---|
| `36d1caa5` | 1. identidad: 3 modelos sin clasificar |
| `cd1d8221` | 2a. ejes: 24 archivos sin eje |
| `65363820` | 2b. ejes: grados de unidad viejos |
| `f3f9b08c` | 4. `stores build --check`: colisión de ids de PythonSymbolDoc |
| `976519b7` | 5. `stores build`: 108 PythonSymbolDoc huérfanas en el índice versionado |
| (ninguno en sldb) | 3. job store, «Build deskops' store when it declares one»: lo arregló deskops `c66b4fad` |

## Verificación (p2): los pasos del workflow en un clon limpio, en /dev/shm

Usé un venv propio en `/dev/shm/sci/venv` con Python 3.13.18 (uv). Ahí instalé `pip install -e sldb[dev,click,code]` y `pron[mcp]`. No toqué el .venv compartido.

Los checkouts de deskops y pron salen de los clones locales, después de `git fetch origin`, en el commit que GitHub tiene como
`origin/main` y `origin/master`. El clasificador de permisos denegó clonar directamente de GitHub. Los commits son los mismos:
deskops `270f3d0f`, que incluye `c66b4fad`, y pron `7f2e308`.

| paso | resultado | commit | log |
|---|---|---|---|
| 1 `bash tools/check.sh --fast` | PASS, todas las puertas | `f3f9b08c` | `step1-check-fast-f3f9.log` |
| 2 pytest, un proceso por archivo con la guarda b7 | 166/166 archivos exit 0 | `65363820` | `pytest/summary.txt` |
| 2' re-ejecución de lo que toca `f3f9b08c` (tests/selfdoc/*, test_clean_code_rules) | 15/15 exit 0 | `f3f9b08c` | `pytest/summary-f3f9.txt` |
| 3 `python -m build` | sdist y wheel 0.1.13 | `65363820` | `step3-build.log` |
| 4 `make world` en pron | exit 0 | pron `7f2e308` | `step4-make-world.log` |
| 5 en deskops, `if [ -f .sldb/store.yaml ]; then sldb stores build; fi` | exit 0, `undeclared: 0` | deskops `270f3d0f` | `step5-deskops-build.log` |
| 6 `sldb stores build --check` | exit 0, solo alertas | `65363820` + arreglo de `f3f9b08c` | `step6-build-check-fix.log` |
| 7 `sldb stores build && sldb selfdoc check` | fallo 5, y verde en la verificación final | ídem | `step7-build-selfdoc-fix.log` |

Corrí la matriz solo con 3.13. El job test del CI también corre 3.12: este informe no lo verifica.

Nota de rendimiento: el paso 6 tardó 47:53 de reloj, con 38 % de CPU y 850 MB de RSS. En el último run verde (39464199660,
2026-10-20) el mismo paso tardó 8:27 y el paso 7 otros 7:56. La máquina estaba compartida con otro worker que corría pytest,
pero la diferencia es grande. No es un fallo de esta tarea. Lo dejo como un hallazgo para que el coordinador decida si abre una tarea.

---

## 1. identidad: tres modelos que el contrato no clasifica

**Reproducción.** En el clon limpio, `bash tools/check.sh --fast` falla con los mismos 3 ERROR del run:
`el modelo doc_anchor_value | rule_doc | transition_attributes existe y el contrato no lo clasifica`.

**Causa raíz.** `tools/check_identity.py` (líneas 154-158) exige que cada `src/sldb/models/*.py` esté en un grupo de
`[product.models]` de `contracts/identity.toml`. Hay tres modelos nuevos del 2026-11-06 que se agregaron sin clasificarse:
- `doc_anchor_value.py`: GO07, `4d521da8`;
- `rule_doc.py`: GO06, `622da0b5`;
- `transition_attributes.py`: GO09, `33b3c7a0`.

El último cambio del contrato es de `043ef268`, anterior a los tres.

**Arreglo** (`36d1caa5`). Ninguno de los tres nombra contenido de este repositorio, así que los tres son producto:
- `doc_anchor_value` va a `vocabulary`, porque la forma `doc:Model:name` es par de `code_ref`;
- `transition_attributes` va a `relations`, porque es la convención `sets`/`terminal` de `RelationDoc.attributes`;
- `rule_doc` va al grupo nuevo `rules`.

El coordinador aprobó la clasificación como decisión revisable.

**En verde.** `PASS: identidad — 9 paquetes de producto, 19 modelos clasificados, 0 violaciones`.

## 2a. ejes: 24 archivos sin eje

**Reproducción.** Con la misma corrida aparecen los mismos 24 `archivo sin eje: ...`: `api/rules/*` (12), `api/tags/*` (3), `api/views/*` (8)
y `core/finding_route.py`.

**Causa raíz.** `tools/check_axes.py` (el bucle «Un archivo que ningún eje reclama») exige que todo archivo de `src/sldb`
pertenezca a un `[[axis]]` de `contracts/layers.toml`. Ningún eje declaraba esas carpetas. Los archivos vienen de cuatro commits del 2026-11-06:
- `api/rules/rule_graph.py`, `rule_subjects.py`, `rule_writes.py`, `rules_check.py` y `rules_explain.py`: GO06, `622da0b5`;
- `api/rules/dirty_set.py`, `fixpoint.py`, `rule_cache.py`, `rules_on_check.py`, `rules_on_transition.py`,
  `rules_on_write.py` y `core/finding_route.py`: GO08, `3af872e7`;
- `api/rules/builtin_tag_rules.py` y `api/tags/*`: GD27, `fb733e86`;
- `api/views/*`: GD25, `05b4135f`.

**Arreglo** (`cd1d8221`). Es una decisión del coordinador, revisable (p5):
- `core/finding_route.py` va al eje `errores`, junto a `core/finding.py`: enruta los `Finding` a sus listeners.
- `api/rules` y `api/tags` van al eje nuevo `reglas`. Un espacio de etiquetas se verifica como una familia de reglas
  (`builtin_tag_rules.py`, `docs/architecture/tags.md`), y `tag_check` es `rules check` filtrado a esa familia.
- `api/views` va al eje nuevo `vistas_compuestas`.
- Los dos ejes nuevos entran en la non_unit `operacion` (fachada), y la nota de cada eje en el contrato dice por qué.

Alternativas descartadas, para que la decisión quede revisable:
- **A. `api/views` al eje existente `vistas` (unidad `notacion`).** Lo simulé: `notacion` pasaba de necesitar 4 aristas a
  necesitar 12, porque `api/views` consume grafo, índice de aristas, persistencia y errores. La unidad de vocabulario
  quedaba como consumidora neta, que es justo lo que el contrato dice de `operacion` («fachada»). Mezclaba una capacidad con
  una superficie propia y una operación compuesta.
- **C. `reglas` como unidad o non_unit propia, fuera de `operacion`.** Declarar una unidad afirma que se sostiene sola,
  con sus funciones. `reglas` necesita 7 ejes ajenos (codec, contrato, errores, grafo, índice de aristas, persistencia y
  semántica) y no la necesita ninguno. Es el mismo perfil que los ejes de operación, así que no hay evidencia de que sea
  viable. Promoverla después, si se separa, es un cambio local del contrato.

**En verde.** Con este commit los 24 ERROR desaparecen. Los grados se arreglan en 2b.

`api/rules` lo toca también `wt/rule-graph-local` (p4). Este arreglo modifica solo `contracts/layers.toml` y no el código de
`api/rules`. El coordinador confirmó que no choca.

## 2b. ejes: grados de unidad distintos de los declarados

**Reproducción.** Los 5 ERROR del run son `la unidad X declara necesitar N y ser necesitada por M; el código dice ...`:
`nucleo` 4/39 → 5/39, `persistencia` 19/36 → 21/41, `grafo` 5/4 → 5/6, `notacion` 3/2 → 4/2 y `operacion` 47/9 → 53/11.

**Qué compara el gate (b6).** `check_axes.py` cuenta, para cada `[[unit]]` o `[[non_unit]]`, las aristas eje→eje distintas
que salen de la unidad (`needs`) y las que entran (`needed_by`). Las aristas salen de `coupling()`, que lee los
`from sldb.X import` de cada archivo mapeado. Después compara esas cuentas con los números del contrato. El valor
esperado es el del contrato, y el gate lo mide del código.

**Qué quedó viejo: el contrato.** Los números se midieron en `043ef268` (SV01/SV02). Los de `grafo` se midieron en GO05 (`8be66bde`).
Comparé las aristas entre unidades en `043ef268` y en `36d1caa5` y busqué con `git log -L` el commit de cada import nuevo.
Los nodos posteriores del 2026-11-06 agregaron aristas reales sin actualizar los números:

| arista nueva | dónde | commit |
|---|---|---|
| contrato → grafo | `models/rule_doc.py:62` (parser de predicados, diferido) | GO06 `622da0b5` |
| vocabulario_visual → grafo | `models/notation/view_doc_checks.py:61` | GD25 `05b4135f` |
| consulta → op_aristas | `api/where.py:14-15` | GO05 `8be66bde` |
| anclaje y op_documentos → codec e indice_de_aristas | `api/anchors/check_doc_anchors.py:19-23`, `api/documents/doc_anchor_pinning.py:15-16` | GO07 `4d521da8` |
| op_documentos → consulta, consulta → op_modelos | `api/documents/select_documents.py:18`, `store/query_engine/document_selection.py:18` | GD23 `850f8fca` |
| op_documentos → indice_de_aristas | `api/documents/transaction_state.py:13` | GD24 `0cbd307e` |
| op_almacen → runtime | `api/stores/scaffold_sources.py:48` | GD26 `96d7b823` |

Además están las aristas de los ejes `reglas` y `vistas_compuestas`, que se clasificaron en 2a. El código no está mal: cada
import es una dependencia real de la funcionalidad que se agregó. Ningún gate tiene un umbral sobre estas cifras. Solo exige
que el contrato diga lo que hay.

**Arreglo** (`65363820`). Los números son los que mide el gate después de clasificar: `nucleo` 5/43, `persistencia`
21/47, `grafo` 5/8, `notacion` 4/3 y `operacion` 66/11. Cada línea lleva un comentario con la medición, la causa y el valor anterior.

**En verde.** `PASS: ejes — 30 declarados, 739 archivos mapeados, 0 violaciones`. Con `--fast`, todas las puertas pasan.

## 3. job store, «Build deskops' store when it declares one»

**Reproducción.** El paso del run (b3, b4) es `if [ -f .sldb/store.yaml ]; then sldb stores build; fi`, en
`working-directory: deskops`. Termina con exit 1 y dice `built: ... undeclared: 7` y `undeclared: desk/lifecycle/rule-activation-task-{aggregate,code,debug,decision,docs,external,refactor}.md`.

Las líneas de SurfaceDoc y RelationDoc del log vienen del paso anterior (`make world` en pron) y no son el fallo. Lo reproduje
con deskops `6836b45f`, el main de deskops a la hora del run (04:56Z), y obtuve la misma salida y exit 1
(`step5-deskops-6836b45f-repro.log`).

**Causa raíz.** Está en deskops, no en sldb. deskops versiona 7 RuleDoc en `desk/lifecycle/rule-activation-*.md` y su
`.sldb/store.yaml` no las declaraba en `include`. `sldb stores build` falla si hay archivos trackeados sin declarar.

**Arreglo.** Lo hizo deskops `c66b4fad` (2026-11-10 03:30 -03, posterior al run). Ese commit declara las 7 RuleDoc en `store.yaml`
(`sldb stores declare --write`). Las alertas `build/link-missing` de spec2viz y scion ya eran alertas por `8278d2a3`, en sldb.
No hace falta ningún cambio en sldb.

**En verde.** Con deskops main `270f3d0f` el paso termina con exit 0 y dice `undeclared: 0`.

## 4. job store, `sldb stores build --check`: los símbolos de Python colisionan en el id del documento

El CI no llegaba a este paso.

**Reproducción.** Con los pasos 4 y 5 en verde, `sldb stores build --check` termina con exit 1 y dice
`Unexpected: Python symbols collide when converted to document IDs` (`step6-build-check.log`). El mismo error rompe el paso 7.

**Causa raíz.** El generador `selfdoc python-sync` (`.sldb/store.yaml`, `generate`) nombra cada documento
`python-<system>-<module>-<qualname>` y pasa el nombre a minúsculas (`src/sldb/selfdoc/python_materialize.py:42` en `65363820`).
GD24 (`0cbd307e`) definió en `src/sldb/api/documents/transaction.py` la función `transaction` (l.24) y la clase
`Transaction` (l.69). Las dos daban `python-sldb-api-documents-transaction-transaction`, y `_validate_paths` lo rechaza.

Escaneé `src/` entero: es la única colisión. Ningún documento versionado ni ningún `selfdoc check` cita ese id. `knowledge/symbols/`
es derivado y no está versionado.

**Arreglo** (`f3f9b08c`). Es la decisión B del coordinador, revisable. Solo los ids que colisionan llevan como sufijo el tipo
de nodo AST sin `Def`: `…-transaction--function` y `…-transaction--class`. Ningún otro id cambia. El cálculo vive en
`src/sldb/selfdoc/python_doc_ids.py`.

El test `tests/selfdoc/test_python_doc_ids.py` fija las dos cosas: la colisión resuelta y que los ids sin colisión no cambian.
Falla con el código anterior (`ValueError: Python symbols collide...`) y pasa con el nuevo. El arreglo también tiene entrada en el CHANGELOG.

Alternativas descartadas:
- **A. Renombrar la clase pública `Transaction`** (por ejemplo, a `TransactionOps`). Está en `sldb.api.__all__` desde GD24
  y la usan `apply_batch`, `replace_text` y `rewrite_references`. Romper la API pública para acomodar al generador de
  documentación invierte la dependencia: el defecto es que el id pierde información que Python sí distingue.
- **D. Cambiar el esquema de ids para todos** (conservar mayúsculas). Renombraría el documento de cada clase y cada método
  de clase del almacén, y cualquier referencia `PythonSymbolDoc:python-...` existente. Es mucho cambio para un caso que hoy
  aparece una sola vez, y contradice lo que `docs/architecture/code-docstring-indexing.spec.md` dice de esos ids: «not renamed silently».

**En verde.** `sldb stores build --check` termina con exit 0. Solo quedan alertas `anchors/doc_lost` de ReviewDoc cuyo TaskCodeDoc ya no existe,
que son alertas y no errores.

## 5. job store, `sldb stores build` (paso 7): 108 PythonSymbolDoc huérfanas

Este paso tampoco lo alcanzó el CI.

**Reproducción.** Con el paso 6 en verde, `sldb stores build` termina con exit 1 y dice `built: ... undeclared: 108`. Los 108 son
`knowledge/symbols/python-sldb-*.md` (`step7-build-selfdoc-fix.log`). Como `&&` corta ahí, `selfdoc check` no corre.
Corrido aparte, `selfdoc check` termina con exit 0: 34 alertas (`selfdoc/missing` 15, `selfdoc/untracked` 15, `selfdoc/changed` 4) y ningún error.

**Causa raíz.** `undeclared` (`src/sldb/api/stores/apply_declaration.py:75`) lista las filas trackeadas del índice que ningún
`include` ni `derived` cubre. Las 108 están en `.sldb/core/documents/PythonSymbolDoc/` y su archivo derivado no existe.
`git log --diff-filter=A` muestra que las 108 entraron en `9bc591c3` (2026-11-04, «sldb migra a .sldb versionado»).
Esa migración versionó un índice construido antes de `c420809c` (el mismo día, «journal retirado»), y ese commit borró los
símbolos. Por ejemplo, `_track_and_record` existe en `c420809c~1:src/sldb/api/documents/create_document.py` y no en `c420809c`.

`selfdoc python-sync` no destrackea un PythonSymbolDoc cuyo símbolo desaparece. Por eso el build in place encuentra las filas
viejas. `stores build --check` pasaba porque construye una copia desde cero.

**Arreglo** (`976519b7`). Es una excepción explícita del coordinador a «no commitear .sldb». Antes de tocar nada verifiqué que
el conjunto de PythonSymbolDoc del índice menos los ids del escaneo actual de `src/` tiene exactamente 108 ids y es igual a la lista de `undeclared`.

Después corrí `sldb docs untrack knowledge/symbols/<id>.md` una vez por id: 108 llamadas con exit 0 (`untrack.log`). Comprobé que
los archivos borrados coinciden con la lista. El commit contiene solo lo que escribió la CLI: las 108 bajas,
`.sldb/core/models/PythonSymbolDoc.yaml` (`documents_count` 2561 → 2453 y los hashes) y `store_hash`. El precedente es `e1805fc6`.

El arreglo del producto (que python-sync destrackee lo que desaparece) lo abre el coordinador como tarea aparte. No se implementa acá.

Los 108 ids:

- `python-sldb-sldb-api-documents-create_document-_track_and_record`
- `python-sldb-sldb-api-documents-payload_save-_old_payload`
- `python-sldb-sldb-api-documents-payload_save-_save_and_record`
- `python-sldb-sldb-api-documents-track_document_file-_track_and_record`
- `python-sldb-sldb-api-documents-untrack_document-_forget_and_record`
- `python-sldb-sldb-api-journal-doc_address`
- `python-sldb-sldb-api-journal-record`
- `python-sldb-sldb-api-journal-store_hash`
- `python-sldb-sldb-api-model_create-create_model-_field`
- `python-sldb-sldb-api-model_create-create_model-_forget`
- `python-sldb-sldb-api-model_create-create_model-_generate`
- `python-sldb-sldb-api-model_create-create_model-_record`
- `python-sldb-sldb-api-model_create-create_model-_resolve_base`
- `python-sldb-sldb-api-model_create-create_model-_touch_init`
- `python-sldb-sldb-api-model_create-create_model-_write_module`
- `python-sldb-sldb-api-model_create-model_source-_module_lines`
- `python-sldb-sldb-api-model_create-model_source-_quoted`
- `python-sldb-sldb-api-model_drafts-backfill-_entry`
- `python-sldb-sldb-api-model_drafts-draft_validation-_record_promote`
- `python-sldb-sldb-api-model_drafts-field_drafts-_record`
- `python-sldb-sldb-api-model_drafts-template_drafts-_record`
- `python-sldb-sldb-api-model_registry-reindex_model-_record_entry`
- `python-sldb-sldb-api-model_registry-reindex_model-_rehash_and_record`
- `python-sldb-sldb-api-search-_filtered`
- `python-sldb-sldb-api-semantic-dag_writes-_journaled`
- `python-sldb-sldb-api-stores-declare_store-_model`
- `python-sldb-sldb-cli-commands-find-findcli-_apply_filters`
- `python-sldb-sldb-cli-commands-find_format-findformatter-_print_json`
- `python-sldb-sldb-cli-commands-find_format-findformatter-_print_yaml`
- `python-sldb-sldb-cli-commands-journal-_json_safe`
- `python-sldb-sldb-cli-commands-journal-_print`
- `python-sldb-sldb-cli-commands-journal-_since`
- `python-sldb-sldb-cli-commands-journal-_text_entries`
- `python-sldb-sldb-cli-commands-journal-_text_verify`
- `python-sldb-sldb-cli-commands-journal-journalcli-_show`
- `python-sldb-sldb-cli-commands-journal-journalcli-_verify`
- `python-sldb-sldb-cli-commands-store_check-_build_diag_payload`
- `python-sldb-sldb-cli-commands-store_check-_handle_check_res`
- `python-sldb-sldb-cli-commands-store_check-_report_structural_noise`
- `python-sldb-sldb-cli-commands-store_check_content_notes-_print_noise`
- `python-sldb-sldb-cli-commands-store_check_content_notes-_print_rewrite_loss`
- `python-sldb-sldb-cli-commands-store_check_content_notes-print_content_notes`
- `python-sldb-sldb-cli-commands-store_check_notes-_print_removable`
- `python-sldb-sldb-cli-commands-store_check_notes-print_broken_links`
- `python-sldb-sldb-cli-commands-store_check_notes-print_gitignore_policy`
- `python-sldb-sldb-cli-commands-store_check_notes-print_legacy_contracts`
- `python-sldb-sldb-cli-commands-store_check_notes-print_link_notes`
- `python-sldb-sldb-cli-commands-store_check_notes-print_notes`
- `python-sldb-sldb-cli-commands-store_check_notes-print_shadowed`
- `python-sldb-sldb-cli-commands-store_check_notes-print_unresolved_models`
- `python-sldb-sldb-cli-commands-stores_build-_track`
- `python-sldb-sldb-cli-dispatcher-cli-_load_graph`
- `python-sldb-sldb-cli-serve-health-_finding_list`
- `python-sldb-sldb-cli-serve-lint_routes-_document_problems`
- `python-sldb-sldb-cli-serve-models_routes-_report`
- `python-sldb-sldb-cli-serve-models_routes-_require`
- `python-sldb-sldb-cli-serve-models_routes-_run`
- `python-sldb-sldb-cli-serve-models_routes-fields_add_payload`
- `python-sldb-sldb-cli-serve-models_routes-fields_remove_payload`
- `python-sldb-sldb-cli-serve-models_routes-promote_payload`
- `python-sldb-sldb-cli-serve-models_routes-template_edit_payload`
- `python-sldb-sldb-cli-serve-models_routes-validate_payload`
- `python-sldb-sldb-cli-serve-save_plan-delete_target`
- `python-sldb-sldb-cli-serve-save_plan-roundtrip_error`
- `python-sldb-sldb-cli-serve-save_plan-update_target`
- `python-sldb-sldb-cli-serve-save_plan-validate_payload`
- `python-sldb-sldb-cli-serve-save_routes-apply_batch`
- `python-sldb-sldb-cli-serve-save_routes-apply_change`
- `python-sldb-sldb-cli-serve-save_routes-sort_key`
- `python-sldb-sldb-models-structured_doc-structurednldoc-compose_field-_render`
- `python-sldb-sldb-store-graph-facet_match-condition_matches`
- `python-sldb-sldb-store-graph-facet_match-facet_matches`
- `python-sldb-sldb-store-graph-facet_match-matches_filters`
- `python-sldb-sldb-store-graph-facet_match-ordered_compare`
- `python-sldb-sldb-store-graph-facet_match-ordered_magnitude`
- `python-sldb-sldb-store-graph-language-field_condition-fieldcondition`
- `python-sldb-sldb-store-journal-append-_append_locked`
- `python-sldb-sldb-store-journal-append-_next_seq`
- `python-sldb-sldb-store-journal-append-_read_entry`
- `python-sldb-sldb-store-journal-append-append_entry`
- `python-sldb-sldb-store-journal-hashing-hash_entry_fields`
- `python-sldb-sldb-store-journal-layout-journal_dir`
- `python-sldb-sldb-store-journal-layout-journal_entry_path`
- `python-sldb-sldb-store-journal-layout-journal_lock_path`
- `python-sldb-sldb-store-journal-lock-journal_lock`
- `python-sldb-sldb-store-journal-read-_at_or_after`
- `python-sldb-sldb-store-journal-read-_load_newest_first`
- `python-sldb-sldb-store-journal-read-read_entries`
- `python-sldb-sldb-store-journal-verify-_load_oldest_first`
- `python-sldb-sldb-store-journal-verify-_report`
- `python-sldb-sldb-store-journal-verify-verify_chain`
- `python-sldb-sldb-store-query_engine-where_parse-_apply_op`
- `python-sldb-sldb-store-query_engine-where_parse-_build_compare`
- `python-sldb-sldb-store-query_engine-where_parse-_build_compare-check`
- `python-sldb-sldb-store-query_engine-where_parse-_build_contains`
- `python-sldb-sldb-store-query_engine-where_parse-_build_contains-check`
- `python-sldb-sldb-store-query_engine-where_parse-_build_has`
- `python-sldb-sldb-store-query_engine-where_parse-_build_has-check`
- `python-sldb-sldb-store-query_engine-where_parse-_build_model`
- `python-sldb-sldb-store-query_engine-where_parse-_build_model-check`
- `python-sldb-sldb-store-query_engine-where_parse-_build_nonempty`
- `python-sldb-sldb-store-query_engine-where_parse-_build_nonempty-check`
- `python-sldb-sldb-store-query_engine-where_parse-_build_regex`
- `python-sldb-sldb-store-query_engine-where_parse-_build_regex-check`
- `python-sldb-sldb-store-query_engine-where_parse-_compile_one`
- `python-sldb-sldb-store-query_engine-where_parse-compile_where`
- `python-sldb-sldb-store-query_engine-where_parse-wherepredicateerror`
- `python-sldb-sldb-store-query_engine-where_parse-wherepredicateerror-__init__`

## Verificación final: los 7 pasos sobre `976519b7`

Clon limpio de `976519b7` con la disposición del CI (`/dev/shm/sci/{sldb,deskops,pron}`, deskops `270f3d0f`, pron `7f2e308`). Python 3.13, venv de uv en `/dev/shm`. Los logs están en `coord2-ccconfig/sci/final/`.

| paso | resultado | tiempo | log |
|---|---|---|---|
| 1 `bash tools/check.sh --fast` | rc 0 | 2 s | `1-check-fast.log` |
| 2 pytest, un proceso por archivo | 167/167 archivos con exit 0 | — | `2-pytest.txt` |
| 3 `python -m build` | rc 0 | 4 s | `3-build.log` |
| 4 `make world` en pron | rc 0 | 60 s | `4-make-world.log` |
| 5 en deskops, `if [ -f .sldb/store.yaml ]; then sldb stores build; fi` | rc 0, `tracked: 9, undeclared: 0` | 5 s | `5-deskops.log` |
| 6 `sldb stores build --check` | rc 0, solo alertas (`build/link-missing`, `anchors/doc_lost`) | 49:53 | `6-build-check.log` |
| 7 `sldb stores build && sldb selfdoc check` | rc 0, `undeclared: 0`, `selfdoc check` `"ok": true` | 26:34 | `7-build-selfdoc.log` |

El `selfdoc check` sale con exit 0 y `"ok": true`, pero deja 34 alertas: 15 `selfdoc/untracked`, 15 `selfdoc/missing` y 4 `selfdoc/changed`. Son alertas y no fallos, igual que en la corrida anterior. Ninguna cita los ids de `--class`/`--function` de `f3f9b08c`.

La corrida del paso 2 empezó con la guarda b7 (`pgrep`). Se quedó 2 h parada en el archivo 100/166 porque el worker de cc33a corría pytest sin pausa. Por orden del coordinador (presión de IO baja, avg60 0.13), los 67 archivos restantes y los pasos 3-7 se corrieron sin esa espera.

## Lo que queda fuera

- El cierre (b1): por orden del coordinador, el worker pushea `wt/main-de-sldb-en-verde`; el coordinador integra en main y corre el CI. El run de cierre va a `references`.
- Python 3.12 no se verificó localmente.
- La duración del job store (punto anterior) queda como hallazgo sin tarea, para que el coordinador decida.
