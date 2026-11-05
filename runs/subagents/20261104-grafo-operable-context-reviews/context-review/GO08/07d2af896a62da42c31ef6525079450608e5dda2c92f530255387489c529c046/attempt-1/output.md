REFORMULACION

GO08 es un nodo `code` de entrega, no un agregado, en el repo `sldb`. Su propósito es que las `RuleDoc` se evalúen en tres momentos: `on_write` antes de persistir (error rechaza y alerta pasa), `on_transition` añadiendo `findings` al resultado de `edges_holding` sin tocar `effects`, y `on_check` desde `stores check`; además, caché derivada por dirty set con los `content_hash` de las reglas y evaluación a punto fijo semi-naive, validación de parseo en `edges check`, un test end-to-end y una medición. El resultado son cambios en las rutas de `output_scope`, tests, `docs/architecture/rules.md` y `CHANGELOG`. Límites: no define lenguaje, reglas ni anclas (GO05–GO07), no posee `effects` (GO09), no persiste hechos derivados, no autentica actores; `G_OPS_PREREQ` sigue pendiente.

AMBIGUEDADES

1. «Medición: 20 escrituras de un TaskDoc del store de este repo, mediana del tiempo de pared, antes y después»: no fija el punto de comparación —¿antes de GO08, antes de GO09 o estado original?—; obliga a inventar dónde se toma el baseline, que puede no existir tras GO09.
2. «una regla error rechaza la escritura con la explicación en el envelope»: no dice qué ocurre con varias reglas `error` ni con alertas simultáneas; obliga a inventar si el envelope lleva un finding o una lista y en qué orden.
3. «una alert deja pasar y reporta» / «alert: persistida y reportada»: no define canal ni forma del reporte; obliga a inventar si es `Finding`, warning o envelope.

DRY-RUN

Un ejecutor futuro leería `dag.yaml`, `brief.md`, `decisiones.md`, `payload_save_steps.py`, `edges_holding.py`, `stores check`, `validation.py` y los contratos de GO06, GO07 y GO09. Cambiaría los pasos de guardado para evaluar `on_write`, añadiría `findings` en `edges_holding`, evaluaría `on_check` en `stores check`, validaría el parseo de condiciones en `edges check`, implementaría caché derivada y punto fijo, y añadiría tests, docs y CHANGELOG. Depende de GO06 (RuleDoc y hash), GO07 (`anchor_state`), GO09 (forma de `effects`) y `G_OPS_PREREQ`. Validaría con pytest, los casos de aceptación, la medición y CHANGELOG. Nada se ejecuta aquí.

FUTURO

La promoción a TaskDoc la realiza deskops/humano con `deskops add task --from-drawer`; el Board de sldb resuelve `G_OPS_PREREQ`; GO10 retira los shims después; deskops verifica el consumo en `G_CONSUMER`. Si falta un contrato de dependencia, el nodo registra hipótesis en su TaskDoc.
