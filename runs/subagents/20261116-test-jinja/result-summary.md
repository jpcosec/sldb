# Resultado: tester deskops-t-c929c5b2583b

Tarea: `task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari`.
Cambio evaluado: el diff sin commitear de `src/sldb/core/renderer_engine/base.py`, `CHANGELOG.md` y `tests/test_list_items_round_trip.py` (ejecutor deskops-e-08683ea7876c).
Base de comparación: `git archive HEAD` (6e793686) en `/dev/shm/tj/head`, cargada con `PYTHONPATH=/dev/shm/tj/head/src` en el mismo `.venv`. No usé `git stash`.
La salida completa de todo lo que sigue está en `validation.log`.

**Veredicto: PASA**

## Validation (corrida propia, con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`; uv funcionó)

| comando | resultado |
|---|---|
| `pytest -q tests/test_cli_v2.py` | PASA: rc 0, 43 passed |
| `pytest -q tests/api/test_api_documents.py` | PASA: rc 0, 17 passed |
| `pytest -q tests/api/test_structural_noise.py` | PASA: rc 0, 10 passed |
| `pytest -q tests/test_clean_code_rules.py` (obligatorio) | PASA: rc 0, 1202 passed |
| `bash tools/check.sh --fast` (obligatorio) | PASA: rc 0 |
| `pytest -q tests/test_list_items_round_trip.py` (los tests nuevos) | PASA: rc 0, 24 passed |

La suite completa y `sldb stores build --check` no figuran en Validation y no los corrí. Si hacen falta, son del integrador.

## Done When, punto por punto

1. **Validation pasa con los tests nuevos de roundtrip: PASA.** Ver la tabla. `test_a_value_is_never_compiled_as_jinja` cubre 11 valores, cada uno en un título, un escalar y un ítem de lista.
2. **Los casos de la nota se guardan literales: PASA**, con deskops real (aclaración 1 del coordinador). Usé el código de deskops `/mnt/ssd/proyectos/SLDB_1/deskops` (e471caf8) con el sldb de HEAD y con el del cambio, y `HOME=/dev/shm/tj/home`.
   - **Desk fresco en /dev/shm** (`deskops init`, `add task`, `edit task task-t scope ...`). Con HEAD se reproduce exactamente lo que dice la nota:
     - `{{.State...}}`, `{{a`, `{{{a`, `json {{{` y `fin {{` dan rc 3 con `TemplateSyntaxError`.
     - `valor {{ 7*7 }} y {# oculto #} fin` sale con rc 0 y se guarda como `valor 49 y  fin`.
     - `{% if %}…{% raw %}…` sale con rc 0 y se guarda como ` r`.
     - Con el cambio, los 9 valores salen con rc 0 y quedan **literales** en el Markdown.
   - **Copia del store real de deskops** en `/dev/shm/tj/dk/copy-*`. Hice `edit task <TaskDocsDoc existente> scope 'docker … {{.State.Health.Status}} …; valor {{ 7*7 }} y {# oculto #} fin {% raw %}'` y después `show task --format json`:
     - Con HEAD: rc 3 con `TemplateSyntaxError`, y el documento no cambia.
     - Con el cambio: rc 0, y extract devuelve el valor idéntico (`extract scope == input: True`).
     - Un `diff -rq` contra la copia original muestra que solo cambiaron ese documento (el `.md` en la línea del scope y en la procedencia, y su shard) y los índices derivados (`TaskDocsDoc.yaml`, `store_index.yaml`, `.sldb_cache`).
     - El desk real de deskops no se tocó: el md5 de `git status` es el mismo antes y después.
   - **`message send`**: con HEAD el cuerpo `cuerpo {{ 7*7 }} {# c #} {{{x` da rc 3 con `TemplateSyntaxError`; con el cambio da rc 0 y el cuerpo queda literal en `desk/inbox`.
3. **CHANGELOG: PASA.** Hay una entrada en 0.1.13 y `check.sh --fast` pasa (incluye la puerta de afirmaciones).
4. **Commit y aviso a deskops: no lo evalúo.** No hay commit ni aviso. El ejecutor dice que, por la decisión (5) del coordinador, quedan para el coordinador o el integrador, y este brief me prohíbe commitear. Pendiente: deskops tiene que quitar el `xfail(strict=True)` de `tests/test_message_cli.py`.

## Aclaración 2: el render de los documentos existentes no cambia: PASA

Copié el repo a `/dev/shm/tj/store` y corrí `/dev/shm/tj/scripts/rt.py` con HEAD y con el cambio. El script toma `load_runtime_documents(on_invalid="skip")` sobre todos los documentos del store de sldb y, para cada uno, calcula el sha256 de `render_model_markdown` y el de `render_with_spans` (el camino con recorder, donde cambió el manejo del salto de línea final). También compara el extract del render con el extract del archivo.

- 2682 documentos, ninguno inválido y ningún error con ninguna de las dos versiones.
- **0 documentos con bytes distintos** entre HEAD y el cambio, en los dos caminos (con y sin recorder).
- Con las dos versiones, el roundtrip del extract coincide en 2682 de 2682.

## Aclaración 3: otros caminos que compilan texto del usuario con Jinja: PASA

Busqué `from_string|Template\(|Environment\(|get_template|jinja2` en `src/sldb`:

- Hay un único `from_string`, en `base.py:33`, que es justo el que se cambió.
- `Environment(autoescape=False)` aparece solo en `core/renderer.py:19`, y el resto de los renderers (`ListRenderer`, `TableRenderer`, `YamlRenderer`) usan ese mismo env.
- No hay `Template(` ni `get_template` (el único resultado es `_get_template_assign_node`, que es un AST de Python).
- Los marcadores `py` evalúan expresiones de la plantilla, no valores.

## Casos que el ejecutor no cubrió (`/dev/shm/tj/edge/test_edge_jinja.py`, fuera del repo): PASA

Con el cambio pasan 14 de 14. Con HEAD fallan 13 de 14.

- Celdas de una tabla (`⸢rev,table[name,status]•tasks⸥`) con `{{ 7*7 }}`, `{{{`, `{% raw %}` y `{{` al final: quedan literales y el roundtrip del extract es exacto. Con HEAD dan `TemplateSyntaxError` o `49`.
- Valores multilínea (con `{% endif %}` en otra línea) en un campo intermedio y en el último campo `optrev`, presente y ausente: roundtrip exacto.
- `render_with_spans`: el texto es igual al del render normal, y cada span (`a` y `b`, este último cerrando el documento) cubre exactamente el valor literal. Es decir, los offsets del recorder no se corren por la nueva referencia `{{ _sldb_marker_values[i] }}`.
- Un valor con el texto `{{ _sldb_marker_values }}` queda literal. HEAD lo evalúa y deja la línea vacía.
- Un valor final que termina en `\n` no agrega líneas en blanco extra.

Un campo de datos llamado `_sldb_marker_values` taparía el contexto interno, como avisa el ejecutor. En la práctica no puede pasar: pydantic no acepta campos con guion bajo inicial como campos públicos.

## Regresiones vecinas: PASA

El único módulo de `src/` que cambió es `sldb/core/renderer_engine/base.py`. Ningún archivo de `tests/` importa `renderer_engine` por nombre (el grep sale vacío). Amplié la búsqueda a los consumidores directos (`render_model_markdown`, `sldb.core.renderer`, `BaseRenderer`) y salen 22 archivos. Corrí cada uno por separado:

- `tests/api/test_model_metadata_drafts.py`, `test_on_write_entering.py`, `test_select_documents.py`
- `tests/notations/test_notation_models_and_builtins.py`
- `tests/segments/test_field_transclusion_and_diagram_segments.py`
- `tests/selfdoc/test_python_scanner.py`, `test_sync.py`
- `tests/store/test_contract_in_model_node.py`, `test_optional_field_hash_neutral.py`, `test_unresolved_model_check.py`, `test_upgrade_compat.py`
- `tests/test_composition.py`, `test_document_segments.py`, `test_extraction_segments.py`, `test_last_section_kept.py`, `test_literal_paragraph_anchor.py`, `test_relation_models.py`, `test_segment_structure.py`, `test_standalone.py`, `test_store_readme_doc.py`
- `tests/api/test_api_documents.py` y `tests/test_list_items_round_trip.py`, que ya estaban en Validation.

Todos dan rc 0. `tests/api/conftest.py` no es un test. No hubo fallas, así que no hizo falta comparar con HEAD.

## Alcance: PASA

El ejecutor tocó tres archivos:

- `src/sldb/core/renderer_engine/base.py` y `CHANGELOG.md`, que son los del contrato.
- `tests/test_list_items_round_trip.py`, que no está en `files` pero que el Scope autoriza: "tests de roundtrip … en un archivo de tests del renderer existente".

El resto del diff no es del ejecutor:

- `.sldb/store.yaml`, `.sldb/core/models/{ReviewDoc,RunDoc}.yaml` y `store_index.yaml` registran las reviews y los runs del desk (incluido este run).
- Durante mi corrida aparecieron cambios de otro agente en `desk/tasks/task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-…md`, en su shard `TaskCodeDoc` y en `.sldb/core/models/TaskCodeDoc.yaml`.

`base.py` está en 80 líneas efectivas, justo en el límite, y las reglas de clean code pasan.

## Archivos ajenos

No toqué, no stageé y no revisé `apply_batch.py`, `lock.py`, `test_apply_batch_lock.py`, `uv.lock`, `desk/runtimes/` ni `runs/subagents/2026110*`. Ningún test falló por ellos.
