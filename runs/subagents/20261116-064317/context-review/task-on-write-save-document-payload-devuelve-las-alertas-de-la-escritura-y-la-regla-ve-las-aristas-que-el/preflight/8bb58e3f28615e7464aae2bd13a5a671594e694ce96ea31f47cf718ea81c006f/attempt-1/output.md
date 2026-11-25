## REFORMULACION
Propósito: corregir en el repo SLDB_1 (`/mnt/ssd/proyectos/SLDB_1`) dos hallazgos GO08: que `save_document_payload` devuelva las alertas `on_write` de la escritura y que una regla `on_write` vea las aristas declaradas por el payload nuevo. Resultado: `check_on_write` devuelve los findings de nivel alert; `DocumentReference.alerts: list[dict[str, Any]]` con `default_factory=list`; `save_document_payload` los adjunta y sigue enviándolos por `route`; `RuleGraph.with_payload` devuelve un grafo nuevo con las aristas salientes `__references__` y `__doc_anchors__` del documento reemplazadas por las del payload; tests en `tests/api/test_rules.py` y `tests/api/test_on_write_entering.py`; línea en `CHANGELOG.md`. Límites: no incluye `BatchReport.alerts` de `apply_batch` ni cambiar niveles de reglas existentes.

## AMBIGUEDADES
1. Destinatario del aviso: «aviso a deskops con deskops message send --to deskops» frente a «deskops message send --to <repo>» y «si el comando responde que el repo no está registrado». Obliga a decidir si `<repo>` es literalmente `deskops`, otro repo, y si aplica el fallback al informe.
2. Condición exacta del test de aristas: «“exists(references)” o equivalente en el lenguaje de reglas». Obliga a inventar la sintaxis o semántica concreta si el lenguaje no tiene un equivalente inequívoco.

## DRY-RUN
Sin ejecutar: leería `finding_route.py`, `rules_on_write.py`, `rule_graph.py`, `payload_save.py`, la clase `DocumentReference`, los tests nombrados, el lenguaje de reglas y las funciones `declared_reference_edges`/`doc_anchor_edges`. Cambios previstos: retorno de findings alert desde `check_on_write`; campo `alerts` en `DocumentReference`; asignación en `save_document_payload`; construcción de aristas del payload y sustitución de salientes en un `RuleGraph` nuevo; tests y CHANGELOG. Dependencias: firma de las funciones de aristas, API de evaluación de reglas, versión de Pydantic y fixtures existentes. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/api/test_rules.py`, `tests/api/test_on_write_entering.py` y `tests/api/test_rules_evaluation.py`.

## FUTURO
El coordinador hará el commit con `deskops closeout commit`, sin push, y decidirá el envío o fallback del aviso. El ejecutor dejará el informe en `runs/subagents/<run-dir>/result-summary.md`. Un humano resolverá las ambigüedades si el código no las despeja.
