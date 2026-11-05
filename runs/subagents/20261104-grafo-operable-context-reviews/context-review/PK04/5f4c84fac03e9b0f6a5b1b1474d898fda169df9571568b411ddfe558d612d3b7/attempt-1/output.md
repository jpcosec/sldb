## REFORMULACION

PK04 «Operación» es un agregado no ejecutable: no se promueve ni se ejecuta como tarea. Su encargo es que las reglas se evalúen en los momentos que importan y que la máquina de estados sea enteramente datos del store. Resultado sustantivo: toda escritura de payload pasa por reglas `on_write` (una `error` rechaza sin persistir y explica; una `alert` deja pasar y reporta); `edges_holding` evalúa `on_transition` y devuelve los efectos declarados en `RelationDoc.attributes`; `stores check` evalúa `on_check`; la evaluación es incremental por dirty set y a punto fijo para recursión; `edges check` rechaza condiciones mal formadas. GO09 añade la convención `sets`/`terminal` y una función que aplica efectos sin persistir, para que un consumidor no mantenga un YAML paralelo. Repo dueño: sldb. Límites: nada derivado se persiste; no autentica actores ni produce hechos externos; no toca deskops ni migra a kimun; D5/D6/D7 siguen siendo gates, no supuestos del agregado.

## AMBIGUEDADES

Ninguna. La aceptación del agregado se desglosa sin invención en GO08 y GO09; las dependencias externas están nombradas (`G_OPS_PREREQ`, `G_SEAM` vía GO05, `G_SEMANTICS` vía GO05–GO07). GO08 y GO09 no tienen arista entre sí y no se transfieren artefactos; ambos convergen en `edges_holding`, delimitado por sus `output_scope`.

## DRY-RUN

Un ejecutor futuro promovería GO08 y GO09, no PK04. Lecturas de GO08: GO06 (`RuleDoc`, hash de regla), GO07 (anclas), `payload_save_steps`, `edges_holding`, `api/stores`; cambios: evaluación en guardado, transición y check, incremental/punto fijo, validación de parseo, medición. Salida: rechazo/ explicación, alerta reportada, resultado recursivo, medición en TaskDoc. Lecturas de GO09: GO05 (lenguaje), GO03/GO04 (backend y proyección), `RelationDoc.attributes`, `edges_holding`; cambios: convención documentada, efectos devueltos, función de aplicación, doc de edges. Salida: transición aplicable con efectos y compatibilidad para aristas sin `attributes`. Sin arista entre hijos: orden indiferente o paralelo, sin handoff; posible convergencia en `edges_holding` delimitada por TaskDoc. Validación conjunta: store temporal con tres estados/transiciones; escritura con regla `error` rechazada y nada persistido; `alert` persistida y reportada; regla recursiva sobre `depends_on+` con ciclo termina; `edges_holding` devuelve efectos y aplicarlos produce el payload esperado; `edges check` falla con condición mal formada; rendimiento registrado.

## FUTURO

`G_OPS_PREREQ` (journal congelado y split `.sldb`/`.sldb_cache`) debe resolverse fuera de este plan. D5 y D6 requieren confirmación explícita del dueño. `G_CONSUMER`, producido por deskops, verifica que deskops pueda retirar `sets_status`/`terminal`. La promoción de GO08 y GO09 y el host de validación los decide el dueño; el agregado no se promueve.
