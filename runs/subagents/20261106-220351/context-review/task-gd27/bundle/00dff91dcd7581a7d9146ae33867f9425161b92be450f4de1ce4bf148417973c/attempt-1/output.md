## REFORMULACION

Encargo ejecutable (no agregado): nodo GD27 de `generalizar-desde-deskops`, hijo de PG2, depende de GD24 (cerrado). Propósito: dar a `StoreDeclaration` el campo `tag_namespaces` con validación de namespaces y anclas jerárquicas como familia de reglas incorporada (decisión q3), exponer `sldb.api.tag_tree`, `tag_folder` y reexportar `sldb.api.semantic`, añadir `sldb.api.replace_text` transaccional con recuento exacto, re-extracción y re-track, la CLI `sldb tags`/`sldb docs replace`, tests, docs y CHANGELOG. Resultado: la aceptación de `Done When` verde. Repo: `sldb`, en worktree de robocop2. Límites: no tocar `payload_save_steps.py`; sin nombres deskops en `src/`/tests fuera de fixtures; sin migrar tags de deskops; sin rutas de `serve`.

## AMBIGUEDADES

1. "un tag namespace:valor cuyo namespace no está declarado": no define qué es el namespace si el valor tiene más de dos puntos (`a:b:c`); obliga a inventar la regla de corte.
2. "CLI sldb tags namespaces|tree|check" y `tag_check.py`: la semántica de `tags check` no se describe (¿findings de la familia sobre todos los documentos?), solo su nombre y archivo.
3. "hierarchical: bool, folder_axis: bool": no dice qué cambia con `false`; obliga a inventar si una declaración no jerárquica admite prefijos o anclas.
4. "re-extrae y valida contra el modelo": no aclara si el reemplazo vuelve a pasar `on_write`, reglas de usuario y la familia `tag_namespaces`; obliga a inventar el alcance de la validación.
5. "transaction=None": no define si `None` abre transacción propia o escribe sin ella.
6. "orphans: tags usados sin documento ancla" / "unplaced: documentos ancla sin uso": no acota si se limitan al `namespace` pedido o abarcan todo el store.

## DRY-RUN

Un ejecutor futuro leería los archivos listados y `store_declaration.py` para añadir el campo; crearía `api/tags/`, `builtin_tag_rules.py`, `replace_text.py` y parsers/commands; engancharía la familia en los cuatro módulos de `rules/`; añadiría reexports y tests. Dependencias: GD24 (`transaction`), GO08 (`check_on_write`) y GO10 en main (rebase, `WherePredicateError`). Validaciones futuras: los `pytest` del TaskDoc, grep de genericidad, CLI sobre store temporal, clean-code y rebase.

## FUTURO

El dueño decide q3 (familia incorporada vs RuleDoc con predicado de prefijo); el coordinador poda `files` no usados y avisa a w1:p4; el supervisor ejecuta la suite completa; deskops recibe la nota de cierre y migra sus tags.
