REFORMULACION

El nodo encarga ejecutar en `/mnt/ssd/proyectos/SLDB_1` la tarea `task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx...`: ampliar los facts de TS, TSX, JS y JSX para publicar llamadas entre símbolos y llamadas HTTP, y handlers JSX, sin interpretar frameworks. Resultado: readers en módulos nuevos de `sldb.code`; `attrs.calls` con `{func, line, first_arg, canonical}`; `attrs.handlers` con `{element, attribute, handler}`; relación `calls` solo para nombres canónicos; fixture, tests, CHANGELOG y validaciones. Límites: no interpretar REST/frameworks, no resolver imports, no Python; no canonicalizar expresiones no canónicas; frontends reales solo lectura; partir del patch c2.

AMBIGUEDADES

1. «en los tres frontends reales del workspace (solo lectura)»: no se nombran rutas ni repositorios; obligaría a inventar cuáles son.
2. «aviso a IR»: no se define canal, formato ni destinatario; obligaría a inventar el mecanismo.
3. «status: draft» y «BLOQUEADA ... necesita OK del supervisor» frente a «Decisión del supervisor (2026-11-17, prevalece)»: no queda explícito si la tarea está operativa o aún bloqueada.
4. «cuyo valor es un identificador o una llamada»: no se especifica el texto exacto de `handler` cuando el valor es una llamada; obligaría a elegir entre conservar `()` o no.
5. «si esa ya cerró, seguir su forma exacta»: condicional sin indicar cómo proceder si no cerró; obligaría a decidir si se bloquea o se usa la forma aquí descrita.

DRY-RUN

Lecturas: `lang_ts.py`, `ts_readers.py`, `ts_fingerprints.py`, tests y fixture existentes, tarea de Python y patch `runs/subagents/20261116-exec-k4-c2/executor-diff-c3ts-c2.patch`. Cambios previstos: nuevos módulos readers en `sldb.code`; extensión de facts con `calls`, `attrs.calls` y `attrs.handlers`; fixture frontend; tests; CHANGELOG. Dependencias: forma de Python, patch c2 y decisión del supervisor. Validaciones futuras: los cinco comandos de `Validation`, más comprobación sobre los tres frontends reales y revisión de anclas TS.

FUTURO

El ejecutor producirá diff, commit, CHANGELOG y resultados de validación. Un supervisor o humano revisará y aceptará el cambio; IR consumirá los facts publicados. La canonización de nombres no canónicos queda para una tarea aparte de baja prioridad.
