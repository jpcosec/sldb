REFORMULACION
El encargo es una tarea de depuración en el repo sldb: comprobar, con un test, si `sldb docs update` sobre un store A enlazado a B —cuyo modelo tipo ReviewDoc rechaza documentos al perder un valor de un Literal— reescribe archivos ajenos al documento actualizado, su shard y los índices derivados de A. Resultado: test de reproducción en `tests/store/test_doc_invalid_writes.py`, ejecución en caché caliente y fría, informe con resultado y, solo si se reproduce, arreglo en `payload_save.py`/`payload_save_steps.py`, CHANGELOG e informe. Límites: no cambiar el ReviewDoc de deskops ni tocar Chatbot_Infra; no commit/push del ejecutor. Nodo ejecutable (`task.debug`), no agregado.

AMBIGUEDADES
1. “commit; respuesta a AntonIA” (Done When) frente a “El commit lo hace el coordinador con deskops closeout commit”. Obliga a inventar si el ejecutor commitea o deja el árbol para el coordinador.
2. “`sldb docs update <doc>`” y “docs update del documento de A” no nombran la función de test; el test existente usa `api.replace_text`. Obliga a elegir CLI, API o transacción y cómo pasar `pythonpath`.
3. “snapshot de bytes de todos los archivos de A y B” frente a caché caliente/fría y al helper que excluye locks y `.sldb_cache`. Obliga a decidir si locks y caché cuentan como archivos ajenos.
4. “un Finding de nivel alert enviado por sldb.core.finding_route.route” no concreta llamada, campos ni mensaje. Obliga a inventar la alerta del arreglo.
5. “se reescribe el módulo a v2 ... y se limpia sys.modules” no fija nombre/ruta del módulo ni cómo queda registrado el modelo en B. Obliga a inventar el montaje v1/v2.

DRY-RUN
Un ejecutor leería el TaskDoc, rituales, átomo, `tests/store/test_doc_invalid_writes.py` e `invalid_memo_store`, `link_store`, `payload_save.py`, `payload_save_steps.py` y `finding_route`. Después añadiría el test con dos stores en `tmp_path`, enlace por la API pública de stores, modelo v1/v2, snapshot y `docs update` de A; compararía y solo tocaría el código si aparece un archivo ajeno modificado. Dependencias: fixtures/helpers existentes, API de stores, modelo importable y Finding. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/store/test_doc_invalid_writes.py` y `... test_doc_invalid_check.py`; informe en `result-summary.md`. Sin ejecutar.

FUTURO
El coordinador decide y ejecuta el commit/closeout y valida el árbol; el ejecutor produce el test, el informe y el aviso a AntonIA. La ejecución futura de pytest confirma caliente/frío; si no se reproduce, un humano o el coordinador acepta la guarda de regresión sin CHANGELOG.
