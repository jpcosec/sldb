## REFORMULACION
Encargo ejecutable, no agregado: cerrar la arista de capas `models -> store` de R6 bajando el tokenizer/parser del lenguaje de reglas a `sldb.core.rules_language`. Resultado: cuatro módulos movidos, shims de reexport en `store.graph.language`, `rule_doc._parse` importando de core sin diferido, `contracts/layers.toml` sin excepción `upward ["models","store"]` ni `[[pending]] R6`, CHANGELOG y cinco validaciones verdes. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: no cambiar gramática, evaluador ni mensajes; no actualizar importadores; detenerse si aparece dependencia de store ajena al parseo.

## AMBIGUEDADES
1. Alcance de módulos: el TaskDoc dice “se mueven exactamente los cuatro módulos”; la pill dice “El parser importa también predicate_atoms, y este a predicate_paths y predicate_terms; predicate_paths importa predicate_reach: esos cuatro módulos se mueven junto con los cuatro”. Obliga a inventar si se mueven cuatro u ocho y qué precision manda.
2. `unquote`: la pill dice “unquote se mueve a core si es una función pura de texto, y where_literal la reimporta”, pero el TaskDoc limita a los cuatro módulos y no incluye `where_literal`. Obliga a decidir si se amplía el cambio.
3. Forma de los shims: “shims de una línea por símbolo ("from sldb.core.rules_language.predicate_parser import *" más __all__ igual)” mezcla reexport explícito por símbolo con `import *`. Obliga a inventar el contenido exacto y el origen de `__all__`.

## DRY-RUN
Lecturas: `contracts/layers.toml` 80-170, `rule_doc.py` 55-70, los cuatro módulos y sus imports, importadores por `grep -rn "store.graph.language" src/ tests/`, tests nombrados y fixtures. Cambios previstos: `git mv` de los cuatro a `sldb.core.rules_language`; imports internos a core; shims viejos; `rule_doc` importando de core a nivel de módulo; borrar R6 de `layers.toml`; entrada CHANGELOG. Dependencias: `git mv`, `check_layers`, pytest, `check.sh`. Validaciones futuras: los cinco comandos y `grep -n "R6" contracts/layers.toml` vacío. No se ejecuta nada.

## FUTURO
Un humano resuelve el conflicto TaskDoc/pill antes de ejecutar. El ejecutor produce `result-summary.md`; el coordinador hace `deskops closeout commit`, cierra la tarea y envía el aviso.
