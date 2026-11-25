## REFORMULACION

Encargo de depuración (`task.debug`) en el repo SLDB_1, sobre `sldb.api.run_view`. Propósito: cerrar dos huecos detectados en CC34 de deskops. Resultado: (H12) cuando el índice compuesto del store está vacío o sin construir, `run_view` lanza `SLDBStoreError` con el mensaje "store index not built: run `sldb stores build`" en lugar de "Unknown view", reutilizando la señal de store/unbuilt de `store_surroundings.py`; (H13) un test decide si la revisión cambia entre el proceso que escribió el store y un subprocess nuevo, y solo si cambia se corrige la dependencia de cachés en memoria leyendo del disco. Superficie: `view_source.py`, `view_revision.py`, `tests/api/test_run_view_reads.py`, `CHANGELOG.md` (línea bajo "## 0.1.13 — not released yet"). Límites: fuera H1-H8 (task.decision aparte) y rendimiento; sin push; commit lo hace el coordinador.

## AMBIGUEDADES

1. "distinguir índice vacío o sin shards ... y lanzar el error de Goal" — no aclara si un store construido con cero vistas debe dar "store index not built" o "Unknown view"; obligaría a inventar la distinción entre "vacío legítimo" y "no construido".
2. "si difieren, encontrar qué entrada ... y leerla del disco" — no dice qué ocurre si tras leer del disco las revisiones siguen difiriendo ni cuál es entonces el criterio de cierre; obligaría a inventar el resultado esperado.
3. "en un subprocess nuevo (python -c con sldb.api.run_view) sobre el mismo store" — no fija cwd, PYTHONPATH ni cómo se pasa la ruta del store; obligaría a inventar la invocación concreta. (Lo demás queda acotado por las Precisiones: líneas orientativas, señal reutilizada, informe en `result-summary.md`.)

## DRY-RUN

Lecturas: `view_source.py` (error en :33), `view_revision.py` (:16, cuatro entradas), `store_surroundings.py` (18-28), `tests/api/test_run_view_reads.py` (fixtures/helpers), `CHANGELOG.md`. Cambios previstos: guarda antes de "Unknown view" que lanza `SLDBStoreError` usando la condición existente; test H12 que borra `.sldb_cache` y comprueba mensaje; test H13 que escribe documento, ejecuta `run_view` en proceso y en subprocess y compara revisión, con diagnóstico por entrada; corrección en `view_revision` solo si difieren (leyendo `load_document_shard`/content_hash de disco); línea de CHANGELOG. Dependencias: helpers de store de prueba, `sldb stores build` disponible en subprocess, `load_document_shard`. Validaciones futuras: los tres `pytest` de Validation y aviso a deskops.

## FUTURO

El coordinador hace `deskops closeout commit`; el ejecutor envía el aviso (o lo anota en el informe si el repo no está registrado) y redacta `result-summary.md` con el veredicto H13. La decisión sobre H1-H8 queda en su task.decision.
