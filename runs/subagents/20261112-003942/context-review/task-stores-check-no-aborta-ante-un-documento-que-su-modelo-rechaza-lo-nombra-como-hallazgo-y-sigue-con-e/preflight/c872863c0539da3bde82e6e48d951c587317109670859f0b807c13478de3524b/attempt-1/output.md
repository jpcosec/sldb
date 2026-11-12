## REFORMULACION

Encargo: modificar `sldb` para que `stores check` no aborte ante un documento que su modelo rechaza. Propósito: diagnosticar stores heredados completos. Resultado: cada documento inválido se reporta como hallazgo por documento —código, severidad y mensaje resumido—, el resto del store se diagnostica igual y la salida texto/JSON finaliza con rc 1, sin `Unexpected`. Además, fijar con tests de regresión el comportamiento actual de H2 y H3. Repo: `sldb`; superficies: `src/sldb/store/`, `src/sldb/api/stores/`, `src/sldb/cli/commands/`, `tests/`, `docs/`, `CHANGELOG.md`, `contracts/layers.toml`. Límites: no tocar la guarda de deskops, `source_read` ni qué valida cada modelo. El documento es un TaskDoc de ejecución futura, no un agregado ejecutable.

## AMBIGUEDADES

1. «código nuevo store/doc-invalid (o el nombre que encaje con los existentes)»: obliga a inventar el identificador definitivo y su compatibilidad con los códigos existentes.
2. «CAUSA DE H1 (a confirmar)»: obliga a decidir si la causa descrita se verifica antes del arreglo o se asume.
3. «el mensaje de pydantic resumido»: obliga a inventar formato, longitud y campos del resumen.
4. «un documento inválido aparece una sola vez, no una vez por subsistema»: obliga a inventar la clave de deduplicación y el orden de hallazgos.
5. «El informe dice qué commit de sldb dejó de reproducir H2 (git bisect sobre la reproducción, o el mecanismo leído en el código)»: obliga a decidir dónde vive el informe y si basta el mecanismo leído.
6. «H2 y H3 quedan cubiertos por tests de regresión que fijan el comportamiento actual»: H2/H3 no se reproducen; obliga a definir qué comportamiento exacto fijan esos tests.

## DRY-RUN

Lecturas previstas: diagnóstico de store, CLI `stores check`, modelos y extracción, tests existentes, capítulo de stores, `contracts/layers.toml`. Cambios: capturar `ValidationError` por documento en `diagnose_store`/`_diagnose_doc`; emitir hallazgo nuevo; deduplicar rutas; tests nuevos y de regresión; docs, CHANGELOG y eje si aparece archivo nuevo. Dependencias: pydantic, API de diagnósticos, harness de tests, `wait-pytest`, reglas clean-code. Validaciones futuras: tests focalizados, suite completa por archivo desde `/dev/shm`, `test_clean_code_rules`, `tools/check.sh --fast` y los 7 pasos en clon limpio.

## FUTURO

Un humano confirma causa, nombre y severidad del hallazgo. El worker implementa, documenta el commit que resolvió H2 y entrega tests; el coordinador ejecuta los 7 pasos del workflow.
