## REFORMULACION

GO05 implementa en sldb el lenguaje de predicados de `rules-language.md` sobre `GraphBackend.eval` y la proyección payload, unificando `where_matches`, `edges_holding`, `StructuredQuery` y `--where`; `where_parse` y `FieldCondition` quedan como shims con `DeprecationWarning` y los 52 xfail pasan a verdes. Repo: sldb (`/dev/shm/sldb-desk`). Límites: fuera RuleDoc/`rules check` (GO06), `F__anchor_state` (GO07), evaluación incremental (GO08), transiciones (GO09) y retiro de shims (GO10). Es un nodo ejecutable de código, no un agregado.

## AMBIGUEDADES

1. "Los tests de especificación llaman a un módulo `sldb.store.query_engine.rules`" (H1) frente a "src/sldb/store/graph/language/". Obliga a decidir si `rules` es módulo nuevo, fachada o adaptador, y su firma real con `grafo`.
2. "El objeto real es el índice compuesto / `GraphBackend`" (H2). Obliga a inventar el adaptador del dict de fixtures al backend.
3. `test_model_less_or_equal_family` evalúa `model <= BaseDoc` con `"model": "ChildDoc"`, pero el fixture no trae `base_models`: obliga a inventar de dónde sale la familia.
4. "una proyeccion sintetica cargada en el backend (`load(indice, proyeccion)`) cuya facet de origen trae la entrada `F__anchor_state`" (p4): `load` recibe `{export_id: payload}`, no facets. Obliga a inventar formato y derivación del alias.
5. "el resultado de find (los documentos que cumplen) no cambia" (p3) no dice si `incomplete` cuenta como cumplir, ni si `--where` con caminos aplica a records de `field`/`section` que `find` también devuelve. Obliga a inventar filtro y alcance.
6. `_query` imprime JSON directo; no se fija cómo el comando inyecta `warnings` en `sldb --envelope graph query` (p1). Obliga a inventar el canal.
7. p5: "la expresion vieja" de `FieldCondition` es un dict, no una expresión; el formato del golden no está fijado.

## DRY-RUN

Lecturas: `rules-language.md` §1-3,6-7; `graph-backend.md`; ficheros listados. Cambios previstos: paquete `language/` (AST, parser, evaluador, caminos, explain), `eval` sin `NotImplementedError`, shims, enrutado de API/CLI, `--explain`, docs y CHANGELOG. Dependencias: `load`/`eval` de GO03, proyección de GO04, `where_lookup` y `fill_braces`. Validaciones futuras: spec sin xfail, equivalencia contra goldens, cero `Validator.extract`, `DeprecationWarning` y envelope, CLI con envelope, `test_clean_code_rules`/`test_store_seams`, suite completa.

## FUTURO

GO06 fija la clave de explain y RuleDoc; GO07 produce `F__anchor_state`; GO10 retira shims; el supervisor corre la suite completa y un humano acepta la revisión en frío.
