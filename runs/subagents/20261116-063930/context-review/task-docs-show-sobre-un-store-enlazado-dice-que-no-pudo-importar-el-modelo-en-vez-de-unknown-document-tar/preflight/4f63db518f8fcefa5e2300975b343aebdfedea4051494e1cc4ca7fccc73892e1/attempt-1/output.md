## REFORMULACION

Encargo ejecutable `task.debug` en el repo `/mnt/ssd/proyectos/SLDB_1` (SLDB). Propósito: corregir el diagnóstico engañoso de `docs show`/`runtime_document` cuando un documento existe en el índice de un store enlazado pero falla la importación de su modelo. Resultado: conservar el error de importación por modelo, emitir “could not import model <Modelo> of store <store>: <excepción original>”, añadir tests para modelo no importable y choque en `sys.modules`, actualizar `CHANGELOG.md` y dejar constancia en `runs/subagents/<run-dir>/result-summary.md`. Límites: no cambiar la estrategia de importación ni mitigar el choque; no hacer push; el commit corresponde al coordinador.

## AMBIGUEDADES

1. “Un aviso con deskops message send --to <repo>”: el input no identifica `<repo>`. Obliga a inventar el destinatario del aviso.
2. “CHANGELOG y commit” frente a “El commit lo hace el coordinador”: no queda claro si el ejecutor debe preparar/stagear el commit o solo dejar el archivo. Obliga a decidir la acción concreta del ejecutor y qué puede declarar completado.
3. “el caso probable de deskops” y “si es la causa”: no se especifica si basta un test sintético con dos stores y paquetes homónimos o si hay que replicar la topología real de deskops. Obliga a inventar el escenario de reproducción.

## DRY-RUN

Lecturas: `src/sldb/store/query.py` (`_resolve_model_type`), `src/sldb/api/documents/document_payload.py` (`runtime_document`, `_unknown_target`), `tests/api/test_views_linked.py`, fixtures/helpers existentes, `CHANGELOG.md` y `tests/test_cli_v2.py` para contexto. Cambios previstos: acumular errores de importación por modelo en `query.py`; consultarlos en `document_payload.py` antes del error genérico; añadir tests de modelo no importable y choque `sys.modules`; añadir línea al CHANGELOG; documentar en `result-summary.md` qué test reproduce el síntoma. Dependencias: helpers de store o `sldb.api` con `tmp_path`; localización por nombre de función, no por línea. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/api/test_views_linked.py` y `TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py`.

## FUTURO

El coordinador hará el commit y decidirá el cierre; el repo destinatario del aviso, si existe, lo recibe o se registra como línea en el informe. Nada de esto debe resolverse inventando dentro del nodo.
