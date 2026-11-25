## REFORMULACION
Propósito: que `graph_path` y `graph_paths` expliquen cada tramo de un camino, no solo devuelvan ids, para que las reglas e impacto de specIR puedan apoyarse en sldb. Resultado: una variante o parámetro `explain` que devuelva, por tramo, origen, destino, relación, dirección y procedencia; operaciones nuevas en el backend; exposición en CLI y `sldb serve`; tests, CHANGELOG y aviso a IR. Repo: `/mnt/ssd/proyectos/SLDB_1`, paquete `sldb`. Límites: no cambiar la forma sin `explain` ni los goldens; pasar por `GraphBackend`; procedencia desde metadata de la arista; `evidence` fuera; varias aristas se listan todas con orden `relation_doc > schema > structural > alias`. Es una tarea `task.code` ejecutable, no un agregado; `pills` y `atoms` están vacíos.

## AMBIGUEDADES
1. «emite {source, target, relation, direction, provenance}» frente a «steps[i].edges»: no queda claro si hay un step por par con lista de aristas o un step por arista. Obliga a inventar el esquema exacto.
2. «provenance = {origin, relation_doc o field, from_store}»: no define claves obligatorias, opcionales ni valores posibles; además «cuando una arista tiene varias, decidir y documentar» choca con la precisión posterior. Obliga a inventar el contrato de procedencia.
3. «graph_path y graph_paths ganan explain: bool = False que elige la operación»: no dice qué retorno tienen con `explain=True` ni cómo convive con `None`. Obliga a inventar la forma pública.
4. «la impresión va a un módulo nuevo» no nombra el módulo; «aviso a IR anotado en result-summary.md» no da ruta y ese archivo no figura en `files`. Obliga a inventar ubicaciones.

## DRY-RUN
Un ejecutor leería `analyze.py`, `networkx_backend.py`, parser y comandos CLI, `graph_routes.py`, tests y goldens. Crearía `path_steps.py` en `sldb.store.graph.analysis` con `explain_path(index, nodes, relations, directed)`, usando `edges_from`/`edges_to`, `relations.resolve` y `EdgeRecord.metadata`. Registraría `path_explained` y `paths_explained` en `_OPERATIONS`; añadiría `explain=False` en API; `--explain` en CLI; `?explain=1` en serve; tests y CHANGELOG. Dependencias: forma de `EdgeRecord`, índice de aristas, goldens y módulos de impresión aún sin nombre. Validaría con los seis comandos indicados y comprobaría que los goldens no cambian. Sin ejecutar nada.

## FUTURO
El nodo ejecutor producirá código, tests, CHANGELOG y commit; el cierre actualizará el Board y dejará el aviso a IR. Un humano o coordinador validará el contrato explicado y aprobará la compatibilidad antes del cierre.
