## REFORMULACION

Encargo de implementación (TaskDoc, no agregado ejecutable): corregir en el repo sldb que un mismo path nombrado por varias reglas `include` se trackee una sola vez. Propósito: que gane el modelo hijo declarado por `paths` sobre el glob del padre; sin relación de herencia, error `store/include-conflict`. Resultado esperado: t1 resolución de filas; t2 `stores declare --write` conserva el glob sin duplicar; t3 el próximo build/update destrackea la fila perdedora de forma idempotente; t4 tests en `tests/store/` con store limpio, selector sin ambigüedad y conflicto; t5 informe sobre el drawer de deskops bcf090a8. Rutas: `src/sldb/api/stores/`, `tests/store/`, `tests/api/`, `docs/`, `CHANGELOG.md`. Límites: no tocar el store.yaml de deskops ni añadir vía CLI para quitar includes.

## AMBIGUEDADES

1. «gana el modelo hijo por paths sobre el glob del padre»: no define el criterio operativo de descendencia ni qué pasa si el modelo de `paths` no desciende del de `glob`; obligaría a inventar la relación de herencia.
2. «error 'store/include-conflict' que nombra el path y los modelos»: no fija formato, código, excepción ni si lo emiten build y check por igual; obligaría a inventar el contrato de error.
3. «el próximo build o stores update destrackea la fila perdedora»: no dice cómo reconocerla sin caché ni si hay migración de datos; obligaría a inventar el algoritmo.
4. «el informe dice si el drawer de deskops bcf090a8 ... sigue haciendo falta»: no concreta formato, destinatario ni criterio de decisión.
5. «Los 7 pasos del workflow los corre el coordinador»: no delimita qué entrega el worker frente al coordinador.
6. «CHANGELOG y docs»: no concreta qué documentar ni en qué página.

## DRY-RUN

Lecturas hipotéticas: `declared_files.py`, `apply_includes`, comandos build/declare/update/check, tests de stores, `contracts/layers.toml`, CHANGELOG y docs. Cambios previstos: t1 en resolución de includes; t2 en `declare --write`; t3 en reconciliación de filas; t4 nuevos tests; t5 informe. Dependencias: modelo de herencia del store, caché y contrato de errores. Validaciones futuras: tests de `tests/store/` y `tests/api/` de stores, `test_clean_code_rules`, `tools/check.sh --fast` y los 7 pasos en clon limpio. Nada ejecutado.

## FUTURO

El worker implementa y entrega tests; el coordinador corre los 7 pasos y decide prioridad; revisión humana valida el informe t5 y el drawer bcf090a8 de deskops.
