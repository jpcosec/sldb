REFORMULACION
El nodo es una tarea ejecutable, no un agregado. Propósito: implementar H4–H7 en el repo sldb. Resultado: `create_document` y `track_document_file` evalúan reglas `on_write` como `save`; `stores declare --write` conserva `tag_namespaces` y `tag_models`; los hallazgos de la familia de tags exponen evaluación estructurada en JSON de `rules check`, `rules explain` y `tags check`; y la guía de reglas/tags documenta qué documentos ve la familia. Límites: no borrar el puente de deskops, no hacer que `stores build` evalúe `on_write` y no cambiar qué reglas existen. Incluye tests, docs y CHANGELOG.

AMBIGUEDADES
1. “el dato estructurado … (namespace, tags, lo que falta)”: no define nombres de campos, tipos ni forma JSON; obliga a inventar el esquema.
2. “los 7 pasos del workflow de sldb”: no los enumera; obliga a inventar o suponer cuáles son.
3. “la suite completa de sldb de a un archivo desde /dev/shm”: no da comando ni selección exacta; obliga a inventar la invocación.
4. “se dan de baja por CLI al cierre”: no indica CLI ni sintaxis; obliga a inventar el comando.

DRY-RUN
Lecturas: `src/sldb/api/documents/`, `rules/`, `tags/`, `stores/`, `cli/commands/`, `tests/`, `docs/architecture/rules.md`, `docs/architecture/tags.md`, `CHANGELOG.md`, `contracts/layers.toml` y `tools/check.sh`. Cambios previstos, en orden: q1 conservar tags en `declare_store` y revisar otras claves autoradas; q2 llamar `check_on_write` desde creación/tracking con rechazo previo a escritura; q3 añadir dato estructurado al hallazgo y serializarlo en las tres salidas; q4 documentar alcance de la familia; q5 tests de herencia y restauración. Dependencias: comportamiento actual de `save`, `StoreDeclaration`, formato de hallazgos y CLI existente. Validaciones futuras: tests por archivo, `test_clean_code_rules`, `tools/check.sh --fast`, suite completa y workflow de 7 pasos. No se ejecuta nada.

FUTURO
El coordinador corre el workflow de 7 pasos, decide si revisa q2 y da de baja notas e ítem por CLI; el worker informa claves autoradas detectadas. La tarea de deskops elimina su puente después.
