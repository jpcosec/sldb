## REFORMULACION

PK04 es un **agregado no ejecutable**: no se promueve (regla 7 de `alcance.md`); termina cuando terminan sus hijos GO09, GO08 y GO10, en ese orden serial. Su encargo es que las reglas se evalúen cuando importan (escritura, transición, `stores check`), que la máquina de estados sea enteramente datos en las aristas, y que los lenguajes viejos desaparezcan. Repo dueño: `sldb`. Resultado sustantivo: (1) `edges_holding` devuelve `effects` resueltos por GO09 y `findings`/`blocked` por GO08 en claves separadas; (2) evaluación con rechazo ante `error`, alerta no bloqueante, incrementalidad por dirty set y punto fijo; (3) `edges check` valida condiciones; (4) el ejemplo end-to-end de GO08 pasa como test; (5) `where_parse` y `FieldCondition` ya no existen. Límites: no toca backend, no persiste derivados, no autentica actores, no migra a kimun, no escribe en deskops (D3).

## AMBIGUEDADES

ninguna. La aceptación del agregado está cubierta por la de sus hijos; la serie GO09→GO08→GO10 coincide con `depends_on`; las fronteras `effects`/`findings` están declaradas; el orden y los prerrequisitos son explícitos.

## DRY-RUN

- **GO09** (entrada: GO05, `G_SEAM`; salida: convención `attributes.sets/terminal`, `apply_effects`, `effects` en `edges_holding`, docs+CHANGELOG). Transfiere a GO08 la clave `effects` y la semántica de sustitución `{campo}`.
- **GO08** (entrada: GO06, GO07, GO09, `G_OPS_PREREQ`; salida: `on_write` reject/pass, `findings` y `blocked` en transición, `on_check` con `check_doc_anchors`, dirty set y caché por `content_hash` de reglas, semi-naive, parseo en `edges check`, test e2e y medición antes/después). Transfiere a GO10 la API de evaluación y los shims aún vivos.
- **GO10** (entrada: GO08; salida: borrado de shims, reescritura de `docs/`, suite verde, CHANGELOG).
- **Validación conjunta**: acceptance de PK04 línea por línea contra los acceptance de hijos; grep de retiro; test e2e en sus tres pasos; medición registrada; pytest verde sin saltos. `G_CONSUMER` queda fuera.

## FUTURO

`G_CONSUMER` lo produce deskops en su propio plan. La disposición de la revisión la escribe quien opera el desk de sldb (D3). El TaskDoc fijará nombres exactos de archivos/tests y la lista de `docs/` por grep. `G_SEAM`, `G_SEMANTICS` y `G_OPS_PREREQ` son gates de otros nodos.
