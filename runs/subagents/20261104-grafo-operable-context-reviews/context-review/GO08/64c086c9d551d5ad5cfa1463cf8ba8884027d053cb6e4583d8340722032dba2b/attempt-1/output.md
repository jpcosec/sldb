## REFORMULACION

GO08 es un nodo `code` (`delivery`) del repo sldb, hijo de PK04. Encargo: evaluar reglas en `on_write` (en los pasos de guardado de payload, antes de persistir: `error` rechaza con explicación; `alert` deja pasar y reporta), en `on_transition` (en `edges_holding`) y en `on_check` (en `stores check`); evaluación incremental por dirty set y hechos derivados a punto fijo (semi-naive) para reglas recursivas; nada derivado se persiste; `edges check` valida el parseo de condiciones de arista; medir el tiempo de escritura antes/después y registrarlo. Depende de GO06 (RuleDoc) y GO07 (anclas); requiere el gate `G_OPS_PREREQ`. Límites: `output_scope` en `src/sldb/store/` (payload_save_steps), `src/sldb/api/edges/edges_holding.py` y `src/sldb/api/stores/`.

## AMBIGUEDADES

1. «Las on_transition se evalúan en edges_holding. Las on_check en stores check» frente a una acceptance que solo cubre `on_write`, recursión, `edges check` y medición. Obliga a inventar el criterio de aceptación de `on_transition` y `on_check`: qué se reporta y cuándo se considera cumplido.
2. «edges check falla ante una condición mal formada» frente a `output_scope`, que no incluye el código de `edges check`. Obliga a decidir si se modifica fuera de alcance o se incumple la aceptación.
3. «una regla recursiva sobre depends_on+ termina y da el resultado esperado en un grafo de prueba con ciclo»: no se define el resultado esperado. Obliga a inventar el oráculo del test.
4. «Rendimiento medido en este repo (tiempo de una escritura antes y después)» no fija store, operación ni muestras. Obliga a inventar el protocolo de medición.

## DRY-RUN

Lecturas: contrato de GO06 (RuleDoc, hash, canal de findings), GO07 (`anchor_state`), `payload_save_steps`, `edges_holding`, `stores check`, índice de aristas y tests existentes. Cambios previstos: hook de evaluación antes de persistir, evaluación en `edges_holding` y `stores check`, caché derivada por dirty set con semi-naive, validación de parseo en `edges check`, medición antes/después. Dependencias: GO06 y GO07 cerrados; `G_OPS_PREREQ` resuelto. Validaciones futuras: pytest con los casos de acceptance, envelope con explicación, grafo con ciclo, condición mal formada y medición registrada.

## FUTURO

El TaskDoc fijará nombres exactos de archivos, funciones y tests. GO06 y GO07 entregan sus contratos. El Board de sldb resuelve `G_OPS_PREREQ`. D6 (Datalog estratificado) se confirma al aceptar G02; GO08 la asume. GO09 comparte PK04 pero no entrega nada a GO08.
