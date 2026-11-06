## REFORMULACION

Propósito: unificar en un solo lenguaje de predicados los dos actuales (`where_parse` y `FieldCondition`), hoy incapaces de cruzar relaciones o expresar `or`/`not`/paréntesis, y evitar que `--where` re-extraiga el payload. Resultado: paquete `src/sldb/store/graph/language/` (AST, parser, evaluador, caminos, explicación) expuesto tras `GraphBackend.eval` y una API única usada por `where_matches`, `edges_holding`, `StructuredQuery` y `--where`; los lenguajes viejos quedan como shims con `DeprecationWarning`; los 52 xfail de GO02 pasan a verdes. Repo: `sldb`. Límites: fuera GO06 (RuleDoc), GO07 (anclas), GO08 (incremental), GO09 (transiciones), GO10 (retiro de shims) y la firma de `__indexed__`; no se persiste resultado de reglas y no se cierra con tests rojos o saltados.

## AMBIGUEDADES

1. «el nombre exacto del comando fijado en el TaskDoc»: el TaskDoc no fija ningún nombre; h4 menciona «sldb graph query» pero el contrato remite a un nombre inexistente. Obliga a inventar cuál comando es.
2. «booleanos completos, caminos con cuantificadores, clausura transitiva»: la gramática solo vive en `rules-language.md` (GO02), no en el input. Obliga a inventar sintaxis de `any()`/`all()`, operadores y precedencia.
3. «explicación estructurada» y «la cláusula fallida por documento»: no hay esquema ni campos. Obliga a inventar el formato de `--explain`.
4. «F__anchor_state (GO07 la produce)»: GO07 aún no la produce; obliga a inventar cómo probar el alias y su ausencia.
5. «goldens ... capturados antes de tocar código»: no se fija formato ni ubicación (`tests/fixtures/where_goldens/` solo aparece en `files`). Obliga a inventar el contrato de los goldens.
6. «un test cuenta cero llamadas a Validator.extract»: `Validator` no aparece en `files` ni se define. Obliga a inventar el punto de instrumentación.

## DRY-RUN

Lecturas: TaskDoc, `docs/architecture/rules-language.md`, `graph-backend.md`, `docs/cli-envelope.md`, spec de GO02, fixtures de goldens y módulos listados. Cambios previstos: crear `graph/language/*`; adaptar `backend/evaluate.py`, `eval.py` y `networkx_backend.py` para aceptar caminos; convertir `where_parse`/`compile_where` y `FieldCondition` en shims con aviso; enrutar API, CLI y envelope; actualizar docs y CHANGELOG; añadir tests de spec, equivalencia, warnings y CLI. Dependencias: semántica GO02, costura GO03, facet payload GO04, `F__anchor_state` de GO07 y goldens precapturados. Validaciones futuras: `pytest tests/test_rules_language_spec.py` sin xfail; equivalencia contra goldens; cero `Validator.extract`; `DeprecationWarning` en Python y entrada en `warnings` del envelope de `graph query`; `--where` sin aviso; CLI con `any()/all()` y `--explain`; `test_clean_code_rules.py` y `test_store_seams.py`; suite completa la corre el supervisor.

## FUTURO

GO07 produce `F__anchor_state`; GO06 añade RuleDoc; GO10 retira los shims. El supervisor ejecuta la suite completa una vez. La revisión en frío y la decisión humana resuelven el nombre del comando, el esquema de explicación/envelope y la integración en `main`.
