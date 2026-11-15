---
sldb:
  by: agent
  at: '2026-11-15T22:37:14Z'
  authority: generated
  via: save_document_payload
id: task-emparejamiento-de-átomos-con-elementos-de-diagrama-explícito-y-difuso-en-sldb-api-matching-d4
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Emparejamiento de átomos con elementos de diagrama (explícito y difuso) en sldb.api.matching (D4)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: el emparejamiento de átomos con elementos de un spec es genérico y debe usar sldb.api.matching, no un matcher propio de cada consumidor.

## Goal

_Describe the concrete result this task must produce._

sldb.api.matching empareja átomos con elementos de diagrama por vínculo explícito (atoms: en el elemento) y por similitud difusa.

## Scope

_State what is in scope and what is out of scope._

SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE. Entra en sldb.api.matching: la resolución explícita por id (atoms: en el elemento) y por refs, las claves y alias por título y etiquetas, el filtro por tags, la cobertura por vista y los avisos con el formato de findings de sldb. El emparejamiento difuso se reutiliza de sldb.api.matching (DocumentIndex.rank sobre Matcher y DifflibMatcher); no se migra ningún matcher. Se reutiliza también la API de store de sldb en vez de SldbAtomResolver. Criterio de reutilizar: misma entrada y misma salida observable en los tests portados. Sale: la inyección de átomos en el HTML del catálogo, split_shared_atoms, el adaptador CatalogItem y el JS del template (quedan en spec2viz), los modelos con atoms (tarea de modelos de spec) y cualquier cambio en el código de sldb serve. Sobre sldb serve: si ya sirve lectura y escritura de un documento por id con su guarda de hash, alcanza y solo se registra; si no, se envía una nota al inbox de sldb con deskops message send --to sldb y la tarea no lo implementa. spec2viz NO se retira y conserva su código (incluido su emparejamiento en el template); el gate IR13 es la tarea IR13 del desk de IR, que decide el retiro; aquí solo se nombra. Paridad: los tests de spec2viz de la pieza se portan con el mínimo cambio.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Comparación previa con lo que ya tiene sldb (leída al preparar la tarea; repetir y registrar en el cierre). Origen en spec2viz (repo hermano, existe): módulo spec2viz.deskops (969 líneas). Hallazgo: el emparejamiento difuso de spec2viz NO está en Python, vive en el template HTML (findAtomData, que normaliza con normKey); el Python de deskops hace la parte explícita (id de átomo en el elemento, refs), el índice por alias, la cobertura y los avisos. sldb.api.matching (src/sldb/api/matching/: DifflibMatcher, Matcher, DocumentIndex con rank, Embedder, cosine) cubre la similitud difusa: dado un texto de consulta devuelve claves ordenadas por similitud con umbral, con difflib sin red o con un embedder. Criterio reutilizar o migrar: si sldb ya tiene una función con la misma entrada y la misma salida observable en los tests portados, se reutiliza; si no, se migra el código de spec2viz.
2. Reutilizar (no se migra nada de esto): el emparejamiento difuso entra por DocumentIndex.rank sobre Matcher/DifflibMatcher, indexando por átomo su título, sus alias y su cuerpo; el descubrimiento y carga del store (SldbAtomResolver._find_store*, _load_store_*, _store_exists, _is_relative_to, _find_repo_root) se sustituye por la API de sldb (sldb.api.stores.open_store y la lectura de documentos y del edge index de sldb.api), y resolve_ref y edges_of por las funciones de lectura de documentos y aristas de sldb.api. Qué cuenta como "falta": todo lo que sldb.api.matching no hace hoy, que es lo siguiente.
3. Migrar a sldb.api.matching, como módulos nuevos bajo src/sldb/api/matching/ (uno para claves y alias, uno para resolución explícita y refs, uno para cobertura; cada módulo bajo el límite de líneas del repo), con la misma lógica y sin CatalogItem: label_key (se migra tal cual, NO se sustituye por normalize de sldb, que además quita acentos y no la puntuación: label_key debe seguir coincidiendo con normKey del template), _normalize_key, _alias_candidates, parse_atoms, filter_atoms_payload, _tag_matches, _spec_elements y _ELEMENT_COLLECTIONS, collect_explicit_atoms, build_explicit_atoms, collect_explicit_refs, build_explicit_refs, _atom_index, _ref_payload, attach_atom_edges, build_coverage_by_view y sus ayudantes (_project_view_payload, _project_element_payload, _empty_coverage_payload, _source_field_for, _item_source_ref, _discover_snapshot_path, _project_root_from_snapshot) y UnknownAtomError. Las funciones que reciben CatalogItem pasan a recibir datos planos: una lista de vistas, cada una con su clave (anchor_id), su id, sus specs ya cargados como dict y la ruta de origen; el adaptador que arma eso desde CatalogItem se queda en spec2viz.
4. Semántica de "alias por título y etiquetas" (se migra _alias_candidates tal cual): alias = el título normalizado, cada palabra de 3 o más letras, cada par de palabras contiguas, y por cada etiqueta "namespace:valor" el valor normalizado (guiones y guiones bajos a espacios) y sus palabras de 3 o más letras, sin repetidos y en ese orden.
5. Avisos: dejan de ser AtomBuildWarning y CoverageBuildWarning (scope, message) y pasan al formato de los findings de sldb (level, code, subject, what, fix; src/sldb/core/finding.py). Códigos: matching/unknown-atom (el id no existe entre los cargados; subject la vista y el nodo; fix "crear el átomo o corregir el id"), matching/unknown-ref, matching/no-store (la vista no tiene store), matching/coverage-snapshot-missing, matching/coverage-snapshot-unreadable y matching/atom-parse-failed. Nivel warning, y con strict nivel error; UnknownAtomError se conserva y se lanza con los avisos de nivel error. Ya no se imprime a stderr desde la lógica: lo imprime quien llama.
6. Se queda en spec2viz (capa visual, no se migra): la inyección de átomos en el HTML del catálogo (render_deskops, build_deskops), split_shared_atoms, el adaptador CatalogItem y el JS del template.
7. Anotaciones del catálogo con autoguardado ("si alcanza"): alcanza si "sldb serve" ya sirve lectura y escritura de un documento por id con su guarda de hash. Comprobar con una prueba real contra "sldb serve" en un store temporal: leer un documento por id (GET /document?id=), escribirlo con POST /save (cambio update) y recibir conflicto cuando el expected o el expected_source_hash está viejo. Si las tres cosas funcionan, alcanza: la tarea no implementa nada de serve y registra en el cierre qué rutas usar. Si falta alguna (por ejemplo la lectura no devuelve el hash que la escritura exige), no alcanza: se envía una nota al inbox de sldb con "deskops message send --to sldb" que diga qué ruta falta, y la tarea NO lo implementa. La nota sigue el formato de los findings (level, code, subject, what, fix) con code serve/annotation-autosave-gap.
8. Tests a portar con el mínimo cambio (los que no dependen del HTML ni de node): de test_atoms_matching, test_filter_atoms_payload_by_full_tag_or_value (con su fixture _two_atoms y parse_atoms); de test_explicit_atoms, test_build_exposes_explicit_map_by_label_and_id, test_unknown_atom_is_warning_unless_strict, test_fully_explicit_view_embeds_no_fuzzy_payload (como: la vista queda en el conjunto de completas), test_partially_explicit_view_keeps_fuzzy_payload (como: no queda en el conjunto) y test_atoms_linked_from_explicit_are_embedded_one_level (como: el mapa de enlazados). Se reescriben contra las funciones puras sin CatalogItem. No se portan: los de modelos con atoms (test_models_accept_atoms, test_state_model_and_schema_expose_atoms, test_spec_with_atoms_validates: son de la tarea de modelos de spec), los que ejecutan el template con node (test_atoms_matching parametrizados por template y test_tabs_follow_the_target_atom), test_split_shared_atoms_emits_repeated_payload_once y test_catalog_build_embeds_atoms_once_and_honors_atoms_tag (HTML del catálogo). Se agrega un test nuevo de sldb que empareja difusamente un título con un átomo vía DocumentIndex.rank y alias, y otro de cobertura.
9. spec2viz conserva su código: su deskops y su matcher en el template no se tocan ni se borran. "Sin matcher duplicado" se refiere a sldb: dentro de sldb existe un solo emparejador (el de sldb.api.matching) y el resto de las piezas nuevas lo llaman. El gate IR13 es la tarea IR13 del desk de IR, que decide el retiro de spec2viz; aquí solo se nombra.

## Validation

_List the checks required before this task can close._

- Tests de origen en spec2viz: de test_atoms_matching, test_filter_atoms_payload_by_full_tag_or_value; de test_explicit_atoms, test_build_exposes_explicit_map_by_label_and_id, test_unknown_atom_is_warning_unless_strict, test_fully_explicit_view_embeds_no_fuzzy_payload, test_partially_explicit_view_keeps_fuzzy_payload y test_atoms_linked_from_explicit_are_embedded_one_level.
- Tests de origen agregados por la matriz de cobertura de IR07 (SV-I03, SV-I04): de test_refs, test_collect_explicit_refs_indexes_by_label_and_id, test_build_resolves_refs_with_title_path_and_summary, test_unknown_ref_is_warning_unless_strict, test_view_without_store_warns_per_ref, test_edges_of_keeps_declared_edges_both_ways_and_drops_structural, test_edges_of_without_edge_index_warns_once_and_is_empty, test_edges_of_against_a_real_store, test_build_attaches_edges_to_explicit_atoms y test_store_documents_come_from_sldb_api, contra un store sldb real en vez de monkeypatch; de test_deskops, test_parse_atoms_handles_missing_dir, test_parse_atoms_builds_index_and_skips_bad_files, test_build_coverage_by_view_projects_snapshot_payload y test_build_atoms_by_view_uses_store_scoped_payload. De test_refs no se portan los de modelos y schema (tarea de modelos de spec), test_store_discovery_uses_a_real_store (la vista trae su store) ni test_no_internal_sldb_imports (no aplica dentro de sldb).
- Destino previsto: un archivo de tests de resolución explícita y alias junto a los de matching de sldb, uno de cobertura y uno de emparejamiento difuso con alias (test nuevo sobre DocumentIndex.rank).
- Prueba real de sldb serve en un store temporal (lectura por id, escritura con guarda, conflicto con hash viejo) y su resultado, alcanza o nota enviada, registrado en el cierre.
- Informe de comparación con sldb.api.matching escrito en el cierre.
- TMPDIR=/dev/shm pytest -q de cada archivo tocado, uno a la vez; antes de entregar, todos los tests/*.py de a uno.
- tools/check.sh
- sldb stores build --check
- deskops graph missing sin faltantes nuevos.

## Done When

_Name the observable condition that makes the task complete._

1. sldb.api.matching exporta la resolución explícita (atoms y refs), los alias, el filtro por tags, la cobertura y UnknownAtomError; el emparejamiento difuso usa DocumentIndex.rank y no hay un segundo matcher dentro de sldb.
2. Los 6 tests portados pasan sin HTML ni node, el test nuevo de emparejamiento difuso con alias y el de cobertura también.
3. Los avisos salen con el formato de findings de sldb (level, code, subject, what, fix) con los códigos matching/*; con strict se lanza UnknownAtomError.
4. Decisión sobre sldb serve registrada en el cierre: alcanza (con las rutas usadas y la prueba real hecha) o nota enviada al inbox de sldb con deskops message send --to sldb, sin tocar el código de serve.
5. Informe de comparación con sldb.api.matching escrito en el cierre (qué se reutilizó y qué se migró y por qué).
6. spec2viz sin cambios, conserva su deskops y su matcher del template (retiro = gate IR13, tarea IR13 del desk de IR).
7. Suite de a un archivo, tools/check.sh y sldb stores build --check en verde; deskops graph missing sin faltantes nuevos.
