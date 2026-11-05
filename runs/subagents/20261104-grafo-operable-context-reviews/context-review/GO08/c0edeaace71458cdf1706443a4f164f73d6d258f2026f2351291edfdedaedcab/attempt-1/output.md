REFORMULACION
GO08 (nodo `code`, `delivery`, hijo de PK04, repo sldb) encarga evaluar reglas en tres momentos: `on_write` (un error rechaza la escritura sin persistir nada; un alert pasa y se reporta), `on_transition` (`edges_holding` agrega `findings`; un error mueve la arista a `blocked`; no toca `effects`, que es de GO09) y `on_check` (`stores check` evalúa las `on_check` e invoca `check_doc_anchors` de GO07; exit 1 solo con error). Incluye caché derivada con dirty set en `.sldb_cache`, punto fijo semi-naive, validación de condiciones en `edges check`, test de integración end-to-end documentado en `rules.md` y medición antes/después. Límites: depende de GO06, GO07 y GO09; requiere G_OPS_PREREQ (pending, intencional).

AMBIGUEDADES
1. "no aparece entre las que se cumplen sino en una clave nueva blocked del resultado, con todos sus findings" y "agrega la clave findings a su resultado": no se define la forma —¿`findings` por arista o global? ¿`blocked` es lista o mapa de aristas con sus findings?—; obliga a inventar el contrato de retorno que la aceptación verifica ("mueve la arista a blocked con su finding").
2. "on_write: en los pasos de guardado de payload, antes de persistir": no fija el orden respecto del pinneado de anclas en el mismo archivo; obliga a decidir si la regla ve el valor ya pinneado (cambia `anchor_state` y el rechazo).
3. "invalidan toda la familia de esa regla": no se define qué documentos componen la familia de una regla (¿sujeto con `where`? ¿todo el modelo?); obliga a inventar el conjunto de caché que se invalida.

DRY-RUN
Lecturas: salidas de GO06, GO07 y GO09; `payload_save_steps.py`, `edges_holding.py`, `stores check`, `validation.py`, `edges.py`, `alert_sink`/`Finding`; convención de `.sldb_cache`. Cambios previstos: cablear `on_write` en guardado, `on_transition` en `edges_holding` (`findings`/`blocked`), `on_check` en `stores check`, parseo en `edges check`; caché y dirty set; `rules.md` y CHANGELOG. Dependencias: GO06, GO07, GO09 y G_OPS_PREREQ resuelto. Validaciones futuras: suite pytest en robocop2; aceptación (dos errores en el envelope, exit codes, recálculos=0, caché borrada, ciclo A→B→C→A, condición mal formada, tres pasos end-to-end) y medición de 20 escrituras.

FUTURO
G_OPS_PREREQ lo cierra el Board de sldb; GO10 retira los shims tras GO08; deskops consume en su plan (G_CONSUMER, fuera de este); el operador del desk escribe la disposición de revisión (D3); el TaskDoc fija nombres de archivos/funciones/tests al promover; el dueño indica el host de pytest.
