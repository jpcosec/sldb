## REFORMULACION
El encargo es un TaskDoc de preflight para una tarea de depuración ejecutable en el repo `/mnt/ssd/proyectos/SLDB_1`. Propósito: corregir `run_view` cuando el store no tiene índice construido (H12) y determinar si la revisión de una vista depende de cachés del proceso (H13). Resultado esperado: (H12) lanzar `SLDBStoreError` con “store index not built: run `sldb stores build`” antes de “Unknown view”, con test que borra `.sldb_cache`; (H13) un test que compare la revisión en el mismo proceso y en un subproceso nuevo, corrigiendo `view_revision` solo si difieren; además CHANGELOG, commit y aviso a deskops. Límites: no incluye H1-H8 ni rendimiento de `run_view`. No es un agregado ni paquete no ejecutable.

## AMBIGUEDADES
1. “usar la misma señal que stores check usa para store/unbuilt, src/sldb/api/stores/store_surroundings.py”: no se especifica qué señal exacta ni su semántica; obligaría a inventar el criterio técnico de detección.
2. “encontrar qué entrada de view_revision.revision viene de una caché del proceso (source_hash del índice, content_hash o shards_signature) y leerla del disco”: no indica cómo atribuir la causa ni qué API de lectura usar; obligaría a inventar el diagnóstico y la fuente canónica.
3. “el informe lo dice”: no define formato, ubicación ni destinatario del informe; obligaría a inventar el canal de entrega.
4. “la revision deja de depender de cachés en memoria”: no concreta qué cachés quedan prohibidas ni cómo demostrarlo; obligaría a inventar el alcance de la corrección.

## DRY-RUN
Lecturas previstas: `src/sldb/api/views/view_source.py`, `view_revision.py`, `stores/store_surroundings.py`, `tests/api/test_run_view_reads.py`, tests de views/view_doc y CHANGELOG. Cambios previstos: guarda en `view_source.py` antes de “Unknown view”; dos tests nuevos; posible ajuste en `view_revision.py` solo si H13 se reproduce; entrada de CHANGELOG. Dependencias: helpers existentes de stores, importabilidad de `sldb.api.run_view` en subproceso y pytest. Validaciones futuras: los tres comandos pytest indicados; informe de H13; commit y aviso.

## FUTURO
El ejecutor implementa, ejecuta los tests y reporta si H13 se reprodujo. Un revisor o humano decide aceptación, commit final y cierre; deskops recibe el aviso.
