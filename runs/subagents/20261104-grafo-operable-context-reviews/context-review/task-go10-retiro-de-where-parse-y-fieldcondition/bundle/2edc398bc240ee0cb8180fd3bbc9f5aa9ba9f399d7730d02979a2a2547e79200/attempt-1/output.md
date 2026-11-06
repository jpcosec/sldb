**REFORMULACION**

Propósito: ejecutar GO10 (hijo de PK04, plan grafo-operable): retirar los lenguajes viejos que GO05 dejó como shims. Resultado: sin `where_parse`/`FieldCondition` en `src/` ni `docs/` (salvo la tabla histórica de rules-language.md), `FacetFilter` con `where: str`, cinco JSON de `contracts/queries/sldb` reescritos, docs reescritos con la tabla §7, `WherePredicateError` en capa 0, código muerto de facet_match borrado, goldens conservados como tests del lenguaje nuevo, CHANGELOG actualizado. Repo: `src/sldb/` (store, core, api, cli), `contracts/`, `docs/`, `tests/`, `CHANGELOG.md`. Límites: sin cambios de semántica del lenguaje, sin tocar `pron`, sin reparar R6, sin deudas ajenas del drawer. Nodo ejecutable, no agregado.

**AMBIGUEDADES**

1. «FacetFilter pierde conditions … y gana where: str»: no fija obligatoriedad, valor por defecto ni si `facet` permanece; obliga a inventar el esquema pydantic.
2. «los cinco JSON … se reescriben con la columna nueva de la tabla … seccion 7»: la tabla mapea operadores, no la forma del JSON; obliga a inventar clave y anidamiento.
3. «StructuredQuery con conditions rechazado con ValidationError»: exige `extra="forbid"`; el input no lo dice.
4. `graph-backend.md` dice que un campo no proyectado es `SLDBGraphArgumentError`, pero `unprojected_fields` lee `c.field`; con `where: str` hay que inventar cómo se extraen los campos del predicado.
5. «misma clase: ValueError y SLDBError»: hay dos `SLDBError` (`core/exceptions` y `store/exceptions`); obliga a inventar cuál hereda.
6. «los Markdown de docs/ en files son la lista obtenida por grep al promover»: no dice si un archivo listado sin coincidencias se toca o se descarta.
7. «La version del CHANGELOG es la cabecera vigente»: el bundle no incluye CHANGELOG.md; obliga a inventar versión y sección.
8. «los tests que hoy ejercitan los shims … se borran o se reescriben»: `test_predicate_language.py` usa `compile_where`/`FieldCondition` en `_old_where`/`_old_field_condition`; no fija si se leen goldens como dato o se eliminan filas.

**DRY-RUN**

Lecturas: TaskDoc, rituales execution/testing/closeout, los archivos listados en `files`, goldens, JSON de contracts, layers.toml, CHANGELOG. Cambios previstos: mover `WherePredicateError` a `core/exceptions/where_predicate_error.py` y reexportar; borrar `where_parse.py`, `field_condition.py`, `field_condition_translation.py`; crear `FacetFilter.where` y adaptar payload_match/facet_match (borrar `matches_filters`, `facet_matches`, `condition_matches`, `ordered_*`); repuntar imports (predicate_cursor/tokens, api, graph, cli); quitar el warning `deprecated/field-condition`; reescribir los cinco JSON y los bloques de docs; añadir `tests/store/test_where_retired.py`; adaptar test_predicate_language y test_example_queries; CHANGELOG. Dependencias: GO05–GO09 integrados; R6 y `[allow] [models, store]` quedan. Validaciones futuras: los dos greps de aceptación, rechazo pydantic, mismos ids, goldens verdes, clean-code/seams y `check_layers`, suite completa (supervisor).

**FUTURO**

El coordinador revisa los casos r9, avisa a pron por inbox, corre la suite completa y decide R6; luego revisión en frío y merge.
