REFORMULACION
Propósito: cablear la evaluación de reglas en escritura, transición y check. Resultado: `on_write` rechaza o alerta antes de persistir; `edges_holding`/`edges_blocked` exponen findings por arista; `stores check` incluye `on_check` y anclas; caché derivada con dirty set y punto fijo; validación en `edges check`; test end-to-end y medición. Repo: SLDB (`src/sldb/...`, `tests/...`, `docs/architecture/...`). Límites: no toca lenguaje, RuleDoc, anclas ni effects de GO09 —solo añade `findings` a `EdgeRecord`—; no retira shims (GO10); no persiste resultados de reglas. Es una tarea `task.code` ejecutable, no un agregado.

AMBIGUEDADES
1. “después del pinneado de anclas (GO07) y antes de persistir”: no fija el punto exacto en `payload_save_steps.py`; obligaría a inventar el orden de llamada y el manejo del envelope intermedio.
2. “Caché derivada por dirty set […] cuya clave incluye los content_hash de las reglas”: no define formato físico, ubicación exacta ni bloqueo en `.sldb_cache`; obligaría a inventar esquema y concurrencia.
3. “hechos derivados a punto fijo (semi-naive)”: no especifica agenda, corte ni representación de hechos; obligaría a inventar el algoritmo concreto.
4. “el ejemplo end-to-end (el de ROOT)”: el input lo resume, pero no adjunta el caso ROOT; obligaría a inventar fixture y detalles exactos.
5. “20 escrituras de un TaskDoc del store de este repo”: no identifica el TaskDoc ni la secuencia; obligaría a inventar el corpus de medición.

DRY-RUN
Lecturas: TaskDoc, `docs/architecture/rules.md`, `anchoring.md`, `edges.md`, `contracts/layers.toml`, código de payload, edges, stores, reglas, caché y tests citados. Cambios previstos: insertar `on_write`; añadir `findings` y `edges_blocked`; integrar `on_check` y `check_doc_anchors`; implementar caché/dirty set/punto fijo; validar condiciones en `edges check`; actualizar docs, CHANGELOG y tests. Dependencias: GO06, GO07, GO09 y commits indicados. Validaciones futuras: pytest de evaluación/end-to-end, casos de rechazo/alerta, incrementalidad, ciclo, condición mal formada, `check_layers.py`, suite completa y medición antes/después. Sin ejecutar nada.

FUTURO
GO10 retirará shims; el supervisor ejecutará la suite completa; la revisión en frío y la integración en `main` quedan para humano/otro nodo.
