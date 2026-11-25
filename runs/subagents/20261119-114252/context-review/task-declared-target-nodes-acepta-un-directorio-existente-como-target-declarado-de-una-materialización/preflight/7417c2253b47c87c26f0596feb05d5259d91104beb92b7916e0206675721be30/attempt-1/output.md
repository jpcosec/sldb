REFORMULACION
El nodo solicitado es un preflight solo-TaskDoc, no una implementación: debe reformular el encargo, señalar ambigüedades y describir un dry-run, sin ejecutar ni modificar nada. El encargo revisado es una tarea `code` en `/mnt/ssd/proyectos/SLDB_1/sldb`: hacer que `declared_target_nodes` acepte como target declarado un directorio existente del proyecto, produciendo un nodo de directorio (o equivalente ya existente en `project_graph`), de modo que `graph missing` no lo reporte; un directorio inexistente debe seguir missing. Incluye tests en `tests/api/test_project_graph.py` y `CHANGELOG`. Excluye expandir el directorio en nodos por archivo. El cierre exige las validaciones indicadas, commit y aviso a deskops.

AMBIGUEDADES
1. “con un nodo de kind directory o el equivalente que ya exista en project_graph”: no se define qué kind, constructor ni propiedades debe tener el nodo; obligaría a inventar la representación.
2. “y file_node.py si el nodo de archivo es la base”: contradice que `files` solo liste `declared_target_nodes.py`, tests y `CHANGELOG`; obligaría a decidir si `file_node.py` está permitido.
3. “directorio existente del proyecto”: no precisa resolución relativa, symlinks ni rutas fuera de la raíz; obligaría a inventar la política.
4. “graph missing no lo reporta”: no concreta el criterio exacto de ausencia para directorios; obligaría a inferirlo.
5. “CHANGELOG y commit”: no indica formato de entrada ni mensaje/identidad del commit; obligaría a inventarlos.
6. “aviso a deskops”: no define canal ni contenido; obligaría a inventar el aviso.

DRY-RUN
Lecturas: `declared_target_nodes.py`, `declared_file_targets.py`, `file_node.py`, `file_nodes.py`, `tests/api/test_project_graph.py`, `CHANGELOG` y la sugerencia referenciada. Cambios previstos: detectar directorio existente antes/además de `is_file()`, crear o reutilizar nodo de directorio, mantener missing para inexistentes; añadir tests; actualizar `CHANGELOG`. Dependencias: helpers de `project_graph` y contratos de materialización. Validaciones futuras: los cuatro comandos de `Validation`. Sin ejecutar.

FUTURO
El nodo ejecutor decidirá, tras leer el código, el kind/helper concreto y si toca `file_node.py`; producirá tests, `CHANGELOG` y commit. Un humano o deskops recibirá el aviso y aceptará el cierre.
