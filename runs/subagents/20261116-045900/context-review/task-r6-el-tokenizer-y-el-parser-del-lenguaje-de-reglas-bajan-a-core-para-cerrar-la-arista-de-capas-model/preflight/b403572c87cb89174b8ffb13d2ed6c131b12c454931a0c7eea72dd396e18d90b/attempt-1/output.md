## REFORMULACION

Encargo: refactorizar el lenguaje de reglas para cerrar la arista de capas `models -> store`. Propósito: que `RuleDoc._parse` no importe desde `store`. Resultado: los cuatro módulos (`predicate_tokens`, `predicate_cursor`, `predicate_parser`, `predicate_ast`) viven en `sldb.core.rules_language`; `sldb.store.graph.language` los reexporta con los mismos nombres; `rule_doc` importa de core en módulo; `contracts/layers.toml` pierde la excepción `upward [models, store]` y el pending R6; `python tools/check_layers.py` pasa. Límites: no se cambia gramática, evaluador ni mensajes; los importadores actuales pueden seguir usando el reexport; si un módulo necesita algo de store que no sea parseo, se detiene y se informa. Repo: `sldb`, rutas `src/sldb/...`, `contracts/layers.toml`, `CHANGELOG.md`.

## AMBIGUEDADES

1. «solo lo que ellos importen sin evaluación ni vistas» — no define la frontera exacta; obligaría a inventar qué dependencias de store son admisibles.
2. «necesita algo de store que no es parseo» — «parseo» no está delimitado; obligaría a inventar el criterio de parada.
3. «los reexportan con los mismos nombres» — no aclara si basta reexport de símbolos o deben replicarse módulos completos; obligaría a inventar la forma del shim.
4. «los importadores actuales (api/search.py, ...)» — lista posiblemente no exhaustiva; obligaría a decidir si se grep-ea el repo o se confía en la lista.
5. «y los tests» (Implementation Path) — no identifica cuáles; obligaría a elegir entre los de Validation u otros.
6. «CHANGELOG» — no especifica entrada ni formato; obligaría a inventar el texto.
7. «commit» — no indica mensaje ni convención; obligaría a inventar ambos.

## DRY-RUN

Lecturas: `contracts/layers.toml` (80-170), `rule_doc.py` 55-70, los cuatro módulos y sus imports, importadores listados, `tools/check_layers.py`, `CHANGELOG.md`. Cambios previstos: `git mv` de los cuatro módulos a `src/sldb/core/rules_language/`; shims de reexport en `store/graph/language/`; import de módulo en `rule_doc._parse`; borrar línea upward R6 y bloque `[[pending]]` R6; entrada en CHANGELOG. Dependencias: `git mv`, `__init__` del paquete nuevo, ausencia de imports de store en core, ausencia de ciclos. Validaciones futuras: los cinco comandos de Validation, `grep -n "R6" contracts/layers.toml` vacío y commit.

## FUTURO

Un ejecutor hará las lecturas, el movimiento, los shims y las ediciones, y correrá las validaciones; si un módulo requiere store no-parseo, se detiene y reporta. Un humano decide el commit y revisa el informe de parada.
