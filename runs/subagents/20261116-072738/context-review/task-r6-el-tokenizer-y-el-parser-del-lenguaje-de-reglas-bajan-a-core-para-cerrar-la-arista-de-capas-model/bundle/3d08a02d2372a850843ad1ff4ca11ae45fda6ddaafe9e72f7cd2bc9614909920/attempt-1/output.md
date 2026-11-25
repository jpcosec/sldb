## REFORMULACION

**Propósito:** cerrar la arista de capas `models → store` bajando el tokenizer y el parser del lenguaje de reglas a la capa 0, para que `RuleDoc` valide sin importar del almacén.

**Resultado:** `predicate_tokens`, `predicate_cursor`, `predicate_parser` y `predicate_ast` viven en un paquete nuevo `sldb.core.rules_language`; `sldb.store.graph.language` los reexporta con los mismos nombres; `rule_doc._parse` importa de core de forma no diferida; `contracts/layers.toml` pierde la línea `["models", "store"]` de `[allow].upward` y el bloque `[[pending]] id="R6"`; `python tools/check_layers.py` pasa; entrada en `CHANGELOG.md`.

**Repo:** SLDB_1, `src/sldb/`, `contracts/layers.toml`, `CHANGELOG.md`.

**Límites:** no cambian gramática, evaluador ni mensajes; los importadores actuales no se actualizan (siguen por el shim); si un módulo necesita de `store` algo que no sea parseo, la tarea se detiene y el informe lista los imports.

## AMBIGUEDADES

1. **predicate_atoms no está listado.** Cita: *"se mueven exactamente los cuatro módulos"*, pero `predicate_parser.py` importa `sldb.store.graph.language.predicate_atoms`. Obliga a inventar si se mueve también (quinto módulo) o se deja importando de store.
2. **Imports a store contradicen la regla de parada.** Cita: *"si al moverlos alguno importa de sldb.store algo que no sea otro de los cuatro o sldb.core, la tarea se detiene"*. Pero `predicate_tokens.py` importa `sldb.store.query_engine.where_literal` y `predicate_cursor.py`/`predicate_tokens.py` importan `sldb.store.exceptions`, y el Scope admite *"solo lo que ellos importen sin evaluación ni vistas"*. Obliga a decidir entre detenerse o mover `unquote` y el error (no listados).
3. **Encabezado de CHANGELOG.** Cita: *"bajo el encabezado '## 0.1.13 — not released yet'"*. El archivo no está en el bundle; obliga a inventar el encabezado si no existe.
4. **Forma del shim.** Cita: *"shims de una línea por símbolo ('from sldb.core.rules_language.predicate_parser import *' más __all__ igual)"*. "Una línea por símbolo" e `import *` son incompatibles; obliga a elegir.

## DRY-RUN

**Lecturas:** `contracts/layers.toml` 80-170; `rule_doc.py` 55-70; los cuatro módulos más `predicate_atoms`, `where_literal` y `exceptions`; `CHANGELOG.md`; `grep -rn "store.graph.language" src/ tests/`.

**Cambios previstos:** `git mv` de los módulos a `src/sldb/core/rules_language/` (más `predicate_atoms` y dependencias si se resuelve ambigüedad 2); crear shims; editar `rule_doc`; borrar líneas de `layers.toml`; entrada CHANGELOG.

**Dependencias:** `predicate_atoms`, `unquote`, `WherePredicateError`.

**Validaciones futuras:** los cinco comandos de Validation; `grep -n "R6" contracts/layers.toml` vacío; `grep -rn "store.graph.language" src/ tests/` funcionando por shim.

## FUTURO

El commit lo hace el coordinador con `deskops closeout commit`; el aviso a `<repo>` con `deskops message send`; el informe en `runs/subagents/<run-dir>/result-summary.md` (incluido el listado de imports si la tarea se detiene).
