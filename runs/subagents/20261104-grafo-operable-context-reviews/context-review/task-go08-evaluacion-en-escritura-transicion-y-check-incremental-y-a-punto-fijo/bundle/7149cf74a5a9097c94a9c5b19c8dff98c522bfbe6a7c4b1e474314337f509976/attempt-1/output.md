REFORMULACION
Propósito: cablear la evaluación de `RuleDoc` en `on_write`, `on_transition` y `on_check`, con caché derivada incremental y punto fijo. Resultado: escritura rechazada o persistida según severidad; `edges_holding` con `findings` alert y `edges_blocked` con errores; `stores check` con `on_check` y anclas; caché en `.sldb_cache`; ejemplo end-to-end y medición. Repo: `sldb`, sobre los archivos listados. Límites: fuera GO10, GO05, GO06, GO07 y GO09 salvo el atributo `findings` de `EdgeRecord`; no persistir resultados de reglas; no agregar validadores de modelo; no tocar `effects`. Es un nodo ejecutable de implementación, no un agregado.

AMBIGUEDADES
1. “levanta un error nuevo de sldb con tipo de envelope "rules/violation" (registrado en src/sldb/cli/error_types.py, exit 1)”: no nombra la clase de excepción ni su módulo; obligaría a inventar nombre, jerarquía y mapeo exacto.
2. “la devuelve la función nueva `edges_blocked(store, node, subject)`”: no fija archivo, módulo ni exportación, y `edges_blocked` no aparece en `files`; obligaría a inventar su ubicación y superficie pública.
3. “una segunda evaluación sin cambios devuelve los mismos findings sin recalcular ningún documento (recálculos contados en el test = 0)”: no define qué se cuenta —reglas, anclas, vecinos— ni cómo instrumentarlo; obligaría a inventar el contador y su alcance.
4. “despues = el squash de GO08”: al planificar no existe ese commit; obligaría a inventar un hash o un orden de cierre.

DRY-RUN
Lecturas: TaskDoc, rituales, `EdgeRecord`, `payload_save*`, `api/rules/*`, `store_check`, `edges*`, `validation.py`, `layers.toml`, `rules.md`, CHANGELOG y tests. Cambios previstos: paso `on_write` tras el pinneado y antes de persistir; caché, dirty set y punto fijo en `api/rules`; `findings` en `EdgeRecord`, `edges_holding` y `edges_blocked`; `stores check`; validación en `edges check`; docs, CHANGELOG y tests. Dependencias: GO06 (`RuleDoc`/`Finding`), GO07 (`pin_payload`, `check_doc_anchors`), GO09 (`effects` intactos), índice de aristas y bloqueo de store. Validaciones futuras: pytest focalizados, aceptación de rechazo/alerta, incrementalidad, ciclo A→B→C→A, capas y suite completa. Sin ejecutar nada.

FUTURO
El commit o squash de cierre de GO08 lo produce el ejecutor/supervisor; la medición antes/después y su registro en Validation dependen de ese hash. El supervisor corre la suite completa al final del nodo.
