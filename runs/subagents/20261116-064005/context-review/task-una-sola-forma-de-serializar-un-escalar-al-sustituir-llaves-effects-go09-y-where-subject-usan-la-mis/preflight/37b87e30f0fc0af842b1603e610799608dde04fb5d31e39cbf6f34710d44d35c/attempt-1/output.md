## REFORMULACION
Propósito: unificar en una sola función la serialización de escalares al sustituir llaves `{campo}`, para que `edge_effects._written` y `fill_braces`/`scalar_literal` produzcan el mismo texto. Resultado: `brace_text(value) -> str` en `src/sldb/store/query_engine/where_literal.py`, usada por ambos caminos, con las salidas exactas del Goal; tests parametrizados en los dos archivos indicados; entrada en `CHANGELOG.md`; informe en `runs/subagents/<run-dir>/result-summary.md`. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: no cambiar la gramática ni los literales del parser; el ejecutor no hace commit ni push; el commit lo hace el coordinador con `deskops closeout commit`.

## AMBIGUEDADES
1. “scalar_literal se queda y llama a brace_text para los escalares (sigue devolviendo None para los tipos que hoy no maneja, salvo bool…)” frente a “los cinco casos dan el mismo texto por effects y por where_subject”. No se enumera qué tipos maneja hoy `scalar_literal`; obligaría a inventar si `date`, `datetime` y `float` pasan por `brace_text` o siguen devolviendo `None`.
2. “deskops message send --to <repo>” no concreta el identificador de `<repo>`; obligaría a inventar el repo destinatario del aviso.
3. “tests parametrizados con los cinco casos … en tests/store/test_predicate_language.py y tests/api/test_edge_effects.py” no aclara si ambos archivos deben cubrir los cinco casos o si se reparten; obligaría a inventar la distribución.

## DRY-RUN
Lecturas: `edge_effects.py` 30-50, `where_literal.py` 40-60, `where_subject.py` 1-40, los tres tests y `CHANGELOG.md`. Cambios previstos: añadir `brace_text`; reemplazar la serialización de `_written`; adaptar `scalar_literal`/`fill_braces`; añadir tests de igualdad de texto por ambos caminos; actualizar CHANGELOG e informe. Dependencias: importación desde `where_literal` hacia `edge_effects` sin ciclo; fixtures/helpers existentes o `sldb.api` en `tmp_path`; `deskops message send`. Validaciones futuras: los tres `pytest -q`, `grep -n "safe_dump"` sin aparición en `_written`, comprobación de los cinco casos y revisión de CHANGELOG/commit. Nada ejecutado.

## FUTURO
El coordinador realiza el commit y decide el cierre; el ejecutor produce el informe y el aviso —o su línea de fallback—; un humano resuelve las ambigüedades si no se aclaran antes de ejecutar.
