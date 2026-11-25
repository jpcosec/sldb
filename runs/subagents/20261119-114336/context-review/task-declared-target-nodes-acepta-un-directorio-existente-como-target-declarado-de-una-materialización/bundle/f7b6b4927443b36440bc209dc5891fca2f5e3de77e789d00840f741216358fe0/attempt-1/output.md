**REFORMULACION**

Propósito: corregir `declared_target_nodes` para que un target declarado que apunta a un directorio existente del proyecto se materialice como nodo del grafo y deje de aparecer como `missing_declared_target`. Resultado: nodo de directorio para directorios existentes; directorios inexistentes siguen siendo missing; sin expandir el directorio en nodos por archivo. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: tocar `src/sldb/api/edges/project_graph/declared_target_nodes.py`, posiblemente `file_node.py`, tests en `tests/api/test_project_graph.py` y `CHANGELOG.md`; validaciones indicadas. El nodo es `task.code` ejecutable, no un agregado.

**AMBIGUEDADES**

1. “un nodo del grafo (de directorio)” y “kind directory o el equivalente que ya exista en project_graph”: obliga a inventar el kind, id, identity, provenance y si se reutiliza `FileNode`.
2. “y file_node.py si el nodo de archivo es la base”: la condición es hipotética; obliga a decidir si se modifica `FileNode` o se crea otra representación.
3. “graph missing no lo reporta”: no se nombra dónde se construye `missing_declared_target`; obliga a inventar si hay que tocar otro módulo fuera del alcance listado.
4. “un directorio existente del proyecto”: no aclara si aplican `FileExclusions`, symlinks o rutas fuera del root; obliga a inventar la política.
5. “aviso a deskops”: no define verbo ni canal; obliga a inventar el mecanismo de notificación.

**DRY-RUN**

Lecturas hipotéticas: task, rituales execution/testing/closeout, `declared_target_nodes.py`, `declared_file_targets.py`, `file_node.py`, `file_nodes.py`, `tests/api/test_project_graph.py`, implementación de missing targets y `CHANGELOG.md`. Cambios previstos: ampliar la validación de `_declared_path` para aceptar directorios existentes; crear el nodo de directorio con kind/identity/provenance coherentes; ajustar tests con un target de directorio existente y otro inexistente; actualizar CHANGELOG. Dependencias: modelos de nodo/provenance existentes, exclusiones y API de `extract_file_nodes`. Validaciones futuras: los cuatro comandos del TaskDoc, más auditoría de closeout, commit y aviso a deskops. Nada se ejecuta aquí.

**FUTURO**

Un humano o nodo de contexto debe resolver el kind/equivalente y si `file_node.py` entra. Después, el ejecutor implementa y valida; deskops cierra, commitea y notifica.
