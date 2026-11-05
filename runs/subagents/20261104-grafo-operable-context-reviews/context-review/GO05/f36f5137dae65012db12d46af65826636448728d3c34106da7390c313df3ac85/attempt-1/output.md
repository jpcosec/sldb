REFORMULACION
Propósito: implementar en sldb el parser y evaluador del lenguaje fijado por GO02, sobre la facet payload de GO04 y el backend `GraphBackend` de GO03. Resultado: gramática superconjunto con and/or/not, paréntesis, comparaciones, caminos con any/all/none, clausura transitiva, sustitución `{campo}`, `incomplete` en el borde de links y explicación estructurada; API única tras `where_matches`, `edges_holding`, `StructuredQuery` y `--where`; `where_parse` y `FieldCondition` quedan como shims con `DeprecationWarning` y entrada en `warnings` del envelope; goldens previos y tests de equivalencia; tests xfail de GO02 verdes. Repo: sldb. Límites: `output_scope` declarado; no retira shims (GO10); no persiste hechos derivados; no cambia el resultado de consultas existentes.

AMBIGUEDADES
ninguna.

DRY-RUN
GO05 es un nodo delivery/code ejecutable, no un agregado. Lecturas: `rules-language.md` de GO02, protocolo `GraphBackend` de GO03, facet payload y staleness de GO04, `where_parse`, `FieldCondition`, `StructuredQuery`, `edges_holding`, `api/where`, `docs/cli-envelope.md` y tests actuales. Cambios previstos: parser/AST y evaluador en `store/graph/language/`; enrutado de `where_matches`, `edges_holding` y `--where` a la API única; shims que delegan y avisan; captura de goldens antes de tocar; tests de spec, equivalencia, CLI any/all con `--explain`, cero `Validator.extract`, warning+envelope; `docs/architecture/` y `CHANGELOG`. Dependencias: GO02/G_SEMANTICS, GO04 y GO03/G_SEAM (transitiva vía GO04). Validaciones futuras: pytest en el host indicado, sin rojos ni saltados; CLI con envelope; revisión en frío y promoción del TaskDoc.

FUTURO
GO06 consume el lenguaje para `RuleDoc`, `rules check` y `rules explain`; GO07 usa `anchor_state` sobre caminos; GO09 usa `edges_holding`; GO10 retira los shims. El desk de sldb acepta la revisión y promueve el TaskDoc con archivos y tests exactos; GO02 y GO03 resuelven G_SEMANTICS y G_SEAM; deskops valida el consumo en G_CONSUMER. Nada de esto es ambigüedad del nodo.
