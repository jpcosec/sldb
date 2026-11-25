## REFORMULACION

Encargo: determinar, con un test reproducible, si `sldb docs update <doc>` en un store A enlazado a un store B (cuyo modelo rechaza documentos propios) escribe archivos ajenos al documento actualizado, a su shard y a los índices derivados de A. Resultado: test en `tests/store/test_doc_invalid_writes.py` con snapshot sha256 antes/después, ejecutado con caché caliente y fría; arreglo en `payload_save.py`/`payload_save_steps.py` solo si se reproduce; `CHANGELOG.md` solo si hubo arreglo; informe en `runs/subagents/<run-dir>/result-summary.md`. Repo: SLDB_1 (`/mnt/ssd/proyectos/SLDB_1`). Límites: no tocar el modelo ReviewDoc de deskops ni el kit Chatbot_Infra; sin push; commit por el coordinador.

## AMBIGUEDADES

1. "con caché caliente ni con caché fría (sin .sldb_cache)" — define fría, no caliente. Obliga a inventar cómo calentar caché sin contaminar el snapshot inicial (¿dos updates? ¿snapshot tras el primero?).
2. "los documentos inválidos de B se reporten como alerta" — no dice cuántos Findings, con qué mensaje ni si aplica también cuando el test no reproduce. Obliga a inventar contenido y cardinalidad.
3. Convenciones: "El commit lo hace el coordinador"; Done When: "commit". Obliga a decidir quién commitea.
4. "la función que usa `sldb stores add`, en src/sldb/api/stores/link_store.py" — el nombre exacto de la función no se cita. Obliga a inventarlo o buscarlo.
5. Validation exige `tests/store/test_doc_invalid_check.py`, ausente en `files`. Obliga a asumir que existe.

## DRY-RUN

Lecturas: el archivo de test nombrado, `payload_save.py` (save_document_payload), `payload_save_steps.py` (~línea 112), `link_store.py`, `tests/api/test_api_stores.py`, `finding_route`. Cambios previstos: nuevo test con dos stores en `tmp_path`, modelo v1→v2 vía reescritura de módulo y purga de `sys.modules`, snapshot sha256, `docs update`, comparación contra el conjunto legítimo; posible parche en reconstrucción de índices. Dependencias: API pública de stores, `sldb.api` (init/add_model/create_document), pytest. Validaciones futuras: `pytest -q` de ambos archivos; ambas corridas de caché; entrada de CHANGELOG si hay arreglo.

## FUTURO

El coordinador ejecuta `deskops closeout commit` con el título corto. El envío a AntonIA (`deskops message send --to AntonIA`) decide su resultado; si el repo no está registrado, el aviso pasa al informe. El humano/coordinador valida si el arreglo de índices es aceptable.
