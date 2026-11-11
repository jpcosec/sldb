## REFORMULACION

El nodo es una tarea ejecutable (`task.debug`), no un agregado ni paquete no ejecutable; no tiene hijos que recorrer. Propósito: corregir el fallo de seguridad de `live_stale` al cargar el índice de aristas, que hoy abre y hashea archivos trackeados siguiendo symlinks fuera de la raíz. Resultado: cargar el índice no abre archivos fuera de la raíz, no sigue symlinks y no lee contenido de archivos sin cambios desde el build; con tests de regresión para symlink saliente y archivo protegido. Repo: sldb, superficies `src/sldb/store/edge_index/live_stale.py`, `compose.py`, `models/doc_edges.py`, `src/sldb/store/`, `tests/store/`, `tests/api/`, `docs/`, `CHANGELOG.md`. Límites: fuera de alcance el rebuild y la stale global (hueco a2); no se ejecuta nada en esta revisión.

## AMBIGUEDADES

1. «queda nombrado en un hallazgo (store/path-outside-root o similar), sin error»: el nombre y la forma del hallazgo no están fijados; obligaría a inventar un código y un canal de publicación.
2. «su documento sale stale con motivo» / «stale con su motivo»: `stale` es `list[str]` de ids; no se define dónde ni cómo se representa el motivo sin cambiar el contrato; obligaría a inventar estructura.
3. «La decisión es revisable: si rompe un caso real de sldb, el worker lo escribe y propone»: no se define si debe detenerse, aplicar fallback o solo documentar; obligaría a inventar el criterio de parada.
4. «si cambia el contrato de DocEdges se migra como en GO04»: GO04 no está en el input; obligaría a inventar el procedimiento de migración.
5. «el caso del archivo protegido de graph_ui»: no se define qué archivo ni qué protección; obligaría a inventar el fixture.

## DRY-RUN

Lecturas: los tres módulos citados, `tests/store/`, `tests/api/`, `docs/`, `CHANGELOG.md`, historial de GO04 `d7eefdeb`, workflow de sldb. Cambios previstos: s1 comprobar `resolve()` dentro de `project_root`; s2 usar `lstat` y marcar symlink stale; s3 guardar stat del build en `DocEdges` y hashear solo si cambió; s4 tests con audit hook de `open`; s5 informe sobre `sldb serve`. Dependencias: `project_root`, `documents_hash`, `compose_edge_index`, contrato y migración de `DocEdges`, helpers de test. Validaciones futuras: tests de `tests/store/` y `tests/api/` tocados, `test_stale_shard_hashes.py`, los 7 pasos del workflow en clon limpio.

## FUTURO

El coordinador ejecuta los 7 pasos del workflow en clon limpio. Un humano o el overlord decide si s2 rompe un caso real. El hueco a2 queda en la nota del inbox de sldb. La integración de graph_ui (`test_mindmap_workspace_reader`) se desbloquea al cerrar.
