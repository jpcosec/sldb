## REFORMULACION

Encargo ejecutable (no agregado) en el repo SLDB_1: cerrar la arista de capas models→store moviendo el tokenizer/parser del lenguaje de reglas (predicate_tokens, predicate_cursor, predicate_parser, predicate_ast) desde `src/sldb/store/graph/language/` a un paquete nuevo `sldb.core.rules_language`. Resultado: los cuatro módulos viven en core; los antiguos quedan como shims de reexport con los mismos nombres; `rule_doc._parse` importa de core de forma no diferida; se eliminan de `contracts/layers.toml` la línea `[allow].upward ["models","store"]` y el bloque `[[pending]]` R6; hay una línea en CHANGELOG bajo `## 0.1.13 — not released yet`; pasa `python tools/check_layers.py` y los cinco comandos de Validation. Límites: no cambiar gramática, evaluador ni mensajes de error; no actualizar importadores (siguen por el shim); si algún módulo importa de store algo distinto de los otros tres o de core, detenerse e informar; el ejecutor no hace commit ni push (commit lo hace el coordinador).

## AMBIGUEDADES

1. «el aviso va como línea "Aviso a <repo>: ..."» y «deskops message send --to <repo>»: no se identifica qué repo; obligaría a inventar el identificador.
2. «una línea en español bajo el encabezado "## 0.1.13 — not released yet"»: no se dice qué hacer si ese encabezado no existe; obligaría a inventar si crearlo o usar otro.
3. «solo lo que ellos importen sin evaluación ni vistas»: no define "evaluación" ni "vistas"; aunque la precisión posterior lo acota a core/cuatro módulos, obligaría a interpretar casos límite.
4. «el mensaje "<título corto de la tarea>"»: no fija el texto exacto; obligaría a inventar la forma corta.

## DRY-RUN

Lecturas: `contracts/layers.toml` 80-170, `rule_doc.py` 55-70, los cuatro módulos y sus imports, `grep -rn "store.graph.language" src/ tests/`, encabezado de CHANGELOG y fixtures de los tests citados. Cambios previstos: `git mv` de los cuatro archivos a `src/sldb/core/rules_language/`; creación de los shims con `__all__`; edición del import de `rule_doc._parse`; borrado de la línea upward y del bloque pending R6; alta de la línea de CHANGELOG. Dependencias: `tools/check_layers.py`, pytest y `tools/check.sh --fast`. Validaciones futuras: los cinco comandos, `grep -n "R6" contracts/layers.toml` vacío, grep de importadores y revisión del informe. Nada ejecutado.

## FUTURO

El ejecutor produce el árbol modificado y `runs/subagents/<run-dir>/result-summary.md`; el coordinador hace `deskops closeout commit` y, si procede, envía el aviso. Un humano decide si se activa la parada por imports de store, y valida el resultado de los cinco comandos.
