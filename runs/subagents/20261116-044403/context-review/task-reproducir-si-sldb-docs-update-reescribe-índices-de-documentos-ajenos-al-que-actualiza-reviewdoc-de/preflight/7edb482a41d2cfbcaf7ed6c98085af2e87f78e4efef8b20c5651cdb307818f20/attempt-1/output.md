## REFORMULACION

Encargo: determinar empíricamente si `sldb docs update <doc>` en un store A enlazado a un store B (cuyo modelo tipo ReviewDoc rechaza documentos propios) escribe archivos fuera del documento actualizado, su shard y los índices derivados. Resultado esperado: un test de reproducción en `tests/store/test_doc_invalid_writes.py` con snapshot de bytes (sha256 antes/después) de todos los archivos de A y B; si falla, corregir `payload_save.py` (`save_document_payload`, línea 15) o `payload_save_steps.py` (línea 112) para limitar escrituras y reportar los documentos inválidos de B como alerta; si no se reproduce (caché caliente y fría), dejar el test como guarda de regresión. Repo: SLDB_1. Límites: no tocar el modelo ReviewDoc de deskops ni el kit Chatbot_Infra; `CHANGELOG.md` solo si hubo arreglo; validar con `pytest` sobre `test_doc_invalid_writes.py` y `test_doc_invalid_check.py`.

## AMBIGUEDADES

1. "store B enlazado desde A" — no se indica el campo/mecanismo de enlace; obligaría a inventar la sintaxis del fixture.
2. "un Literal que pierde un valor" — no se especifica cómo mutar el modelo entre snapshot y update; obligaría a inventar el procedimiento de cambio de esquema.
3. "su shard" — no se define esquema de rutas de shards; obligaría a inventar qué rutas excluir del snapshot.
4. "los índices derivados del store (store_index.yaml y models/<Modelo>.yaml del modelo del documento)" — "modelo del documento" es ambiguo con el modelo de B; obligaría a decidir qué `models/*.yaml` son legítimos.
5. "sin .sldb_cache" — no se indica cómo deshabilitar caché; obligaría a inventar variable o borrado.
6. "se reporten como alerta" — formato/canal de alerta no definido.
7. "si ese repo no está registrado para el envío" — no se indica cómo detectarlo.

## DRY-RUN

Lecturas: el test existente y fixtures, `payload_save.py`, `payload_save_steps.py`, referencia de inbox. Cambios previstos: añadir un test con snapshot sha256; condicionalmente, filtro de escritura en `payload_save.py`/`payload_save_steps.py` y entrada en `CHANGELOG.md`. Dependencias: utilidades de enlace entre stores y creación de modelos en fixtures. Validaciones futuras: las dos invocaciones de `pytest` con `TMPDIR=/dev/shm`, en frío y caliente; commit; aviso a AntonIA. Nada se ejecuta aquí.

## FUTURO

Otro nodo/humano decide: si el fallo se reproduce y qué arreglo aceptar; si procede `CHANGELOG.md`; la disponibilidad del envío a AntonIA; y la aceptación final del informe por quien reportó.
