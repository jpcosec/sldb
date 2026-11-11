## REFORMULACION
Propósito: corregir en sldb el doble trackeo cuando un documento cae en el glob de un modelo padre y en los paths de un modelo hijo; debe quedar una sola fila bajo el hijo. Resultado: resolución única (paths del hijo > glob del padre si hay herencia), error `store/include-conflict` si no hay relación o empatan reglas, corrección idempotente de stores ya duplicados, tests, docs y CHANGELOG; informe sobre el drawer de deskops bcf090a8. Repo: sldb; superficie: `src/sldb/api/stores/`, `tests/store/`, `tests/api/`, `docs/`, `CHANGELOG.md`. Límites: no tocar `store.yaml` de deskops ni añadir CLI para quitar includes. Es una tarea concreta de debug, no un agregado ni un paquete no ejecutable.

## AMBIGUEDADES
1. “La de 'paths' explícitos gana sobre la de 'glob' si su modelo es descendiente”: no dice qué pasa si paths y glob pertenecen al mismo modelo; obligaría a inventar ganador o error.
2. “el próximo build o stores update destrackea” y “corregido por build/update”: no fija si basta uno o ambos deben hacerlo; obligaría a inventar el contrato.
3. “el informe dice si el drawer de deskops bcf090a8 ... sigue haciendo falta”: no identifica informe, formato ni destino; obligaría a inventar el entregable.
4. “error 'store/include-conflict' que nombra el path y los modelos”: no fija clase, código de salida ni formato exacto; obligaría a inventar la API de error.
5. “Los 7 pasos del workflow”: no se enumeran en el input; obligaría a inventar el workflow si no está en otra fuente.

## DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout, `declared_files.py`, tests de stores/api, docs y CHANGELOG. Cambios previstos: deduplicar paths en la resolución de includes, aplicar herencia `base_names`, emitir conflicto y destrackear la fila perdedora en build/update; añadir tests en `tests/store/` y actualizar docs/CHANGELOG. Dependencias: contrato de herencia, store build/update/check y caché limpia. Validaciones futuras: tests de stores/api, `test_clean_code_rules`, `tools/check.sh --fast`, clon limpio y workflow de 7 pasos. Sin ejecutar.

## FUTURO
El worker ejecutará cambios y tests; el coordinador correrá los 7 pasos del workflow y decidirá prioridad/cierre; deskops/CI validarán el clon limpio y si el drawer bcf090a8 sigue siendo necesario.
