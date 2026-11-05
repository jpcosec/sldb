REFORMULACION
Propósito: unificar el lenguaje de predicados de sldb implementando el parser y evaluador de GO02 sobre el backend de GO03 y la facet payload de GO04. Resultado: API única detrás de where_matches, edges_holding, StructuredQuery y --where, con booleanos, cuantificadores, clausura transitiva, sustitución, incomplete y explicación estructurada. Repo dueño: sldb. Límites: output_scope en src/sldb/store/query_engine/, src/sldb/store/graph/language/, src/sldb/api/where.py, CLI --where y CHANGELOG.md; depende de GO02 y GO04; requiere G_SEMANTICS y G_SEAM.

AMBIGUEDADES
1. Contradicción interna: "los parsers viejos se borran" frente a "Tests de equivalencia: cada expresión de la tabla de GO02 da el mismo resultado por el camino viejo y el nuevo". Obliga a inventar el camino viejo tras borrar sus parsers.
2. "usar un operador del vocabulario viejo emite ... una alert en el envelope de la CLI" y "un test captura ... la alert del envelope para un operador viejo": no se define forma ni ubicación; GO02 solo fija findings. Obliga a inventar el esquema.
3. La aceptación exige "CHANGELOG y docs/architecture actualizados", pero output_scope no incluye docs/architecture (solo src/sldb/store/query_engine/, src/sldb/store/graph/language/, src/sldb/api/where.py, CLI --where, CHANGELOG.md). Obliga a inventar si se puede escribir fuera del output_scope o si la aceptación es inalcanzable.

DRY-RUN
Lecturas: rules-language.md de GO02 (gramática, semántica, tabla de equivalencia, tests xfail); protocolo GraphBackend de GO03; facet payload y facet_match.py de GO04; where_parse.py, StructuredQuery/FieldCondition, where_matches, edges_holding, CLI docs find, tests de spec, CHANGELOG y docs/architecture. Cambios previstos: crear parser/evaluador en store/graph/language/; adaptar las cuatro entradas a la API única; adaptador FieldCondition→AST; borrar parsers viejos; warnings y alertas de deprecación; --explain; tests de equivalencia, xfail→verde, cero Validator.extract, captura de warning/alerta; CHANGELOG y doc. Dependencias: GO02 y GO04 terminados; G_SEMANTICS (D6) y G_SEAM (D5) confirmados. Validaciones futuras: pytest sin rojos ni saltados; CLI any()/all() con --explain; conteo cero extract; warning y alerta.

FUTURO
El dueño confirma D5 y D6 (G_SEAM, G_SEMANTICS). GO02 produce rules-language.md y los xfail; GO03 produce GraphBackend; GO04 produce la facet payload. GO06, GO07 y GO09 consumen el lenguaje, anchor_state y effects. PK02 cierra cuando GO04 y GO05 terminan. El TaskDoc fijará nombres exactos; deskops valida el consumo en G_CONSUMER.
