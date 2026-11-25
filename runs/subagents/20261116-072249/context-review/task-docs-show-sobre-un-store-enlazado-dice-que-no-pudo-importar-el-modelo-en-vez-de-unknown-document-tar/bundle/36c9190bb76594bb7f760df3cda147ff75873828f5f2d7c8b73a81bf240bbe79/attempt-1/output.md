## REFORMULACION

**Propósito:** que `sldb docs show` sobre un store enlazado cuyo modelo no importa reporte el fallo de import con su excepción original, en lugar del genérico "Unknown document target"; y determinar con test qué caso reproduce el síntoma de deskops (modelo que no importa o choque en `sys.modules`).

**Resultado:** cambios en `src/sldb/store/query.py` (guardar error de import por modelo), `src/sldb/api/documents/document_payload.py` (mensaje nuevo), tests en `tests/api/test_views_linked.py`, línea en `CHANGELOG.md` y `runs/subagents/<run-dir>/result-summary.md`.

**Repo:** SLDB_1 (`sldb`). **Límites:** no cambia la estrategia de import; solo detecta/reporta; dos comandos de Validation; el commit lo hace el coordinador vía `deskops closeout commit`; el ejecutor no hace push.

## AMBIGUEDADES

1. "Guardar en `_resolve_model_type` el error de import por modelo (dict modelo -> excepción) ... y en `document_payload.py` ... lanzar el error". No especifica cómo viaja ese dict desde `_resolve_model_type`/`_load_one` hasta `runtime_document` (firma, retorno, caché). Obliga a inventar el mecanismo de propagación.
2. "could not import model <Modelo> of store <store>: <excepción original>". `<store>` no se define (¿alias, nombre o ruta?). Obliga a inventar el formato.
3. "un choque de nombres en `sys.modules` (dos stores con un paquete del mismo nombre, el caso probable de deskops)". No indica cómo montarlo con las fixtures existentes (el fixture actual usa un `MODULE` único). Obliga a inventar la construcción del test.
4. "el test del modelo que no importa ve el mensaje nuevo". No fija la aserción exacta (substring vs. igualdad). Obliga a inventar el criterio.

## DRY-RUN

**Lecturas:** `query.py` 40–75 y `document_payload.py` 20–65 (por nombre de función, no por línea); `tests/api/test_views_linked.py` para fixtures/helpers; `CHANGELOG.md` (encabezado 0.1.13).

**Cambios previstos:** acumular errores de import por modelo; propagarlos; en `runtime_document`, si el ref nombra un documento de modelo fallido, lanzar el mensaje nuevo; test del modelo no importable; test del choque en `sys.modules`; línea de CHANGELOG; informe con qué test reproduce deskops.

**Dependencias:** `sldb.api` (init_store, add_model, create_document), fixtures del archivo de test, tmp_path.

**Validaciones futuras (no ejecutadas):** `TMPDIR=/dev/shm pytest -q tests/api/test_views_linked.py` y `TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py`.

## FUTURO

El coordinador ejecuta `deskops closeout commit` (sin push). Otro nodo o un humano decide, leyendo `result-summary.md`, si el choque en `sys.modules` es la causa de deskops. El aviso a `deskops` (o la línea "Aviso a …" en el informe si el repo no está registrado) lo resuelve quien tenga el repo registrado.
