# REFORMULACION

Encargo: corregir el diagnóstico engañoso de `docs show` sobre un store enlazado. Hoy, si el documento está en el índice pero su modelo no se pudo importar, `_resolve_model_type` (src/sldb/store/query.py:47-60) descarta la excepción y devuelve `None`, y `runtime_document` (src/sldb/api/documents/document_payload.py:23-37) lanza el genérico `_unknown_target`. Resultado esperado: mensaje `could not import model <Modelo> of store <store>: <excepción original>`, más un test que explique por qué la raíz enlazada no bastó en deskops, reproducción del choque en `sys.modules`, informe y CHANGELOG. Límite: no cambiar la estrategia de import más allá del mensaje. Repo: SLDB_1 (working dir), toca query.py, document_payload.py, tests/api/test_views_linked.py y CHANGELOG.md. Es un TaskDoc ejecutable, no un agregado.

# AMBIGUEDADES

1. "Los tres comandos pasan" — Validation solo lista dos `pytest`; "CHANGELOG y commit" no son comandos de test. Obliga a inventar cuál es el tercero.
2. "anotar en el informe si es la causa" — no se nombra ruta, formato ni destinatario del informe. Obliga a inventar su ubicación.
3. "el mensaje lo dice ("module <m> already imported from <ruta>")" — se da plantilla pero no el texto exacto ni cómo se obtiene la ruta. Obliga a inventar formato.
4. "se sabe, con un test, por qué la raíz enlazada no bastó" — condición de Goal no observable; obliga a inventar el criterio de "saber".
5. "_unknown_target (línea 61)" y rangos de líneas — pueden desviarse; obliga a reinterpretar referencias.
6. Scope "No entra: cambiar la estrategia de import" frente a reproducir el choque de `sys.modules`: no aclara si solo se detecta o se mitiga. Obliga a inventar el alcance de la mitigación.

# DRY-RUN

Lecturas: query.py 40-75, document_payload.py 20-65, tests/api/test_views_linked.py, CHANGELOG.md. Cambios previstos: `_resolve_model_type` acumula dict modelo→excepción; `document_payload.py` consulta ese dict y lanza el error nuevo; tests de modelo no importable y de choque `sys.modules`; entrada CHANGELOG. Dependencias: fixtures de stores enlazados existentes, `TMPDIR=/dev/shm`, entorno pytest. Validaciones futuras: los dos `pytest` citados (y el tercer comando, pendiente de aclarar), más commit. Sin ejecutar nada.

# FUTURO

Un ejecutor produce el informe y el commit; un humano decide si el choque de `sys.modules` es la causa real de deskops y aprueba el cierre.
