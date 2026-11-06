REFORMULACION
Nodo ejecutable (no agregado) del repo sldb. Propósito: retirar los shims del lenguaje viejo dejados por GO05. Resultado: sin `where_parse` ni `FieldCondition` en `src/` ni `docs/` —salvo la tabla histórica de `rules-language.md` bajo “Histórico”—; sin los ocho operadores viejos en bloques de código de docs; `WherePredicateError` reubicado y reexportado; JSON de `contracts/queries/sldb` migrados a `where: str`; goldens conservados como tests del lenguaje nuevo; CHANGELOG actualizado. Límites: no cambiar semántica del lenguaje, no tocar `pron`, no saldar otras deudas del drawer.

AMBIGUEDADES
1. “el código muerto de facet_match (drawer task-tras-go05-quedan-sin-uso-las-funciones-de-facet-match-y-el-retiro-de-los-shims)”: no nombra qué funciones son; obligaría a inventar el conjunto exacto a borrar.
2. “la lista exacta de archivos se fija por grep al promover y queda en el TaskDoc”: el input ya lista archivos; no aclara si esa lista es definitiva o solo candidata.
3. “la columna vieja queda como dato del golden (texto)”: no define formato ni estructura del golden; obligaría a inventar su esquema.
4. “se reescribe el ejemplo para no usar la palabra sin cambiar su significado”: no fija criterio de equivalencia para casos ajenos; obligaría a inventar la reescritura.
5. “Si con esto la arista models->store de R6 desaparece (RuleDoc ya no importa nada de store)”: no aporta el estado actual ni cómo comprobarlo; obligaría a inferir si `RuleDoc` importa `store`.

DRY-RUN
Lecturas: TaskDoc, archivos listados, JSON de contratos, docs, tests, `contracts/layers.toml`, CHANGELOG. Cambios previstos: borrar `where_parse.py`/`compile_where`, `field_condition*.py` y código muerto de `facet_match`; mover `WherePredicateError` a `core/exceptions` y reexportarlo; limpiar importadores residuales; reescribir cinco JSON con `where`; reescribir docs y mover tabla histórica; borrar/reescribir tests de shims; añadir `test_where_retired.py`; registrar en CHANGELOG. Dependencias: GO05-GO09 vía GO08; aviso externo a `pron`; reglas de capas. Validaciones futuras: greps de aceptación, test de rechazo pydantic, mismos ids en `test_example_queries.py`, goldens verdes, `pytest` de clean-code/seams, `check_layers.py` PASS y suite completa.

FUTURO
El coordinador avisa a `pron` por inbox; el supervisor ejecuta la suite completa al final; la revisión en frío y la integración en `main` las decide otro nodo/humano; la decisión sobre R6 y `layers.toml` depende de la comprobación de imports.
