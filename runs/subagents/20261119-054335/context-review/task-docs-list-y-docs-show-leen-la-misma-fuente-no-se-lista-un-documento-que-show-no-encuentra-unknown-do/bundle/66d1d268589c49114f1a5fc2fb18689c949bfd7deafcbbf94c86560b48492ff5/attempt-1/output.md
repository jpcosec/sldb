REFORMULACION
El nodo es una tarea ejecutable `task.code`: alinear `docs list` y `docs show` para que todo nombre listado sea mostrable o quede marcado como no resoluble con su causa. Resultado: cambio en `src/sldb/cli/commands/docs.py`, test de regresión en `tests/test_cli_v2.py`, `CHANGELOG.md`, `result-summary.md`, commit y aviso a sldb-ui. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: no cambiar el formato de `docs list` salvo el marcado de no resoluble; no tocar fuera de los archivos declarados. Depende de los rituales execution/testing/closeout; no tiene pills ni átomos ligados.

AMBIGUEDADES
1. "las pills ligadas, los átomos ligados" frente a "pills: []" y "atoms: []": obliga a inventar si faltan pills/átomos o si el cold-bundle debía incluirlos.
2. "docs list lo marca como no resoluble con su causa" y "salvo el marcado de no resoluble": no define campo, forma ni texto de causa; obliga a inventar el esquema de salida.
3. "aviso a sldb-ui": no indica canal ni artefacto; obliga a inventar si es issue, mensaje o nota.
4. "un documento declarado o derivado que no está en el índice": no aclara si el test debe cubrir ambos orígenes; obliga a inventar la matriz de reproducción.

DRY-RUN
Un ejecutor futuro leería el TaskDoc, los rituales, `docs.py`, `indexed_documents`, `ast_for_target`, `tests/test_cli_v2.py`, los índices del store y la nota de inbox. Reproduciría en `tmp_path` un store cuyo listado incluya un nombre ausente de `.sldb/core/store_index.yaml`; rastrearía la divergencia list/show; unificaría la resolución o añadiría el marcado con causa; añadiría un test de regresión y actualizaría CHANGELOG. Dependencias: fixtures de modelos/store, semántica de índices y argumentos CLI. Validaciones futuras, sin ejecutar: los cuatro comandos del TaskDoc, empezando por `tests/test_cli_v2.py`.

FUTURO
Otro nodo ejecutará la implementación y las validaciones siguiendo execution/testing; deskops hará closeout y commit. El humano debe decidir el esquema exacto del marcado, el canal del aviso y si el reproducer cubre documentos declarados, derivados o ambos.
