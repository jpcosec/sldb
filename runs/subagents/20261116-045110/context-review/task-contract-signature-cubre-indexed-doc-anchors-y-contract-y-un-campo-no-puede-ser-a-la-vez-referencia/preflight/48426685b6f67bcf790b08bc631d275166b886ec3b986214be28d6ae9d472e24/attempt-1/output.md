## REFORMULACION
Propósito: que `contract_signature` cubra también `__indexed__`, `__doc_anchors__` y `__contract__`, de modo que cambiarlos invalide la proyección/shards y el rebuild los reproyecte; y rechazar un campo declarado a la vez en `__references__` y `__doc_anchors__`.

Resultado: firma ampliada con las tres claves siempre presentes (`[]` si no se declaran), problema de doble declaración en `definition_problems`, tests en `tests/store/test_payload_projection.py` y `tests/api/test_doc_anchors.py`, `.sldb` reconstruido y commiteado, aviso en `CHANGELOG.md`, y aviso operativo.

Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: no cambia cómo se proyecta el payload ni cómo se calculan las aristas de ancla.

## AMBIGUEDADES
1. “un modelo que nombra el mismo campo en `__references__` y en `__doc_anchors__` es rechazado con SLDBModelError al registrarse” frente a “en definition_problems agregar el problema”: no se especifica si `definition_problems` debe lanzar `SLDBModelError` o solo devolver el problema y qué llamador lo convierte. Obliga a inventar el punto exacto de lanzamiento.
2. “correr sldb stores build sobre el store del repo y commitear el .sldb resultante en el mismo commit”: no indica ruta concreta del store ni qué artefactos `.sldb` deben versionarse. Obliga a inventar ruta y alcance del commit.
3. “aviso a deskops y graph_ui con deskops message send (sus stores se reconstruyen una vez)”: no da destinatarios, canal ni comando exacto. Obliga a inventar el mecanismo y su verificabilidad.

## DRY-RUN
Un ejecutor futuro leería `model_contract.py`, `edge_node_record.py`, `doc_anchor_value.py`, `payload_projection.py`, `doc_contribution.py`, los dos tests y `CHANGELOG.md`. Cambiaría la firma, docstrings/descripción, `definition_problems`, tests y changelog; después reconstruiría `.sldb`. Dependencias: flujo real de `SLDBModelError`, semántica de `indexed_fields` y escritura de aristas de ancla. Validaciones futuras: los dos `pytest -q` y `sldb stores build --check --store .sldb`.

## FUTURO
Un humano o nodo posterior revisa/commitea el `.sldb`, confirma el aviso a `deskops`/`graph_ui` y asume la reconstrucción única de sus stores. La CI valida el commit.
