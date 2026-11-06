REFORMULACION

Nodo ejecutable `task.code` (no agregado). Propósito: crear en sldb una API pública unificada de selección de documentos y hacer que las consultas estructurales existentes pasen por ella sin alterar su salida. Resultado: `sldb.api.select_documents(store, selector, *, expect="many"|"one")`, con `ref`, `prefix`, `path_glob`, `model`, `where` e `include_linked` combinables por conjunción, orden por ruta relativa y errores de ambigüedad con candidatos; más CLI `sldb docs select`, `GET /docs/select`, tests, `docs/architecture/selectors.md` y `CHANGELOG.md`. Repo: sldb, base `6b80df36`, worktree separado en robocop2. Límites: no implementar el lenguaje de predicados (solo consumirlo), no introducir nombres del caso deskops en `src/sldb/`, no borrar `resolve_selector` de deskops, no tocar superficies no modeladas, no cambiar salidas existentes y no inventar la API de grafo-operable.

AMBIGUEDADES

1. `"G_GO04 ... cerrado en main de sldb (pending)"` frente a `"requiere G_GO04 ... no cerrado"`: no queda claro si el ejecutor puede comenzar antes del cierre ni qué contrato usar; obligaría a inventar la condición de arranque o el esquema payload.
2. `"where (predicado del lenguaje de sldb ...)"` y `"si GO05 no cerró, where acepta el lenguaje que GO04 deja"`: no se define gramática, operadores ni forma de evaluar; obligaría a inventar sintaxis y semántica.
3. `"string corto equivalente para la CLI"`: no se especifica su formato ni cómo se mapea a las claves; obligaría a inventar una mini-sintaxis.
4. `"ruta o alias"`: no se define qué es un alias ni de dónde se resuelve; obligaría a inventar una tabla de alias.
5. `"include_linked (default false)"`: no se indica qué vínculos incluye, en qué dirección ni cómo se representan; obligaría a inventar la semántica.

DRY-RUN

Lecturas: TaskDoc, contrato GO04 disponible, `doc_status.py`, `structural_queries.py`, parsers/comandos/rutas existentes, errores actuales, fixtures y goldens. Cambios previstos: nuevo módulo API; reexportación; adaptación de `glob_structural`/`find_structural`; parser y comando CLI con envelope; ruta serve; tests nuevos/ajustados; documentación y changelog. Dependencias: facet payload de GO04, lenguaje de predicados de GO05 solo como consumo, convenciones de store/CLI/serve y commit base. Validaciones futuras: los cuatro `pytest -q` indicados, grep de genericidad, smoke de `sldb docs select`, comparación de goldens y paridad CLI/HTTP.

FUTURO

GO04 debe cerrar y fijar el payload; GO05 puede fijar el lenguaje de `where`; el supervisor decide el gate y ejecuta la suite completa; deskops recibe la nota de cierre y CC35 elimina su `resolve_selector`; el operador del desk promueve y corrige el TaskDoc.
