## REFORMULACION

Propósito: cerrar GO08 (H2, H3): que `save_document_payload` exponga las alertas `on_write` de la escritura y que una regla `on_write` vea las aristas declaradas por el payload nuevo. Resultado: `check_on_write` devuelve los findings de nivel alert —además de enviarlos por `route`—; `DocumentReference.alerts: list[dict[str, Any]]` los recibe; `RuleGraph.with_payload` devuelve un grafo nuevo con las aristas salientes de `__references__` y `__doc_anchors__` del payload reemplazadas, usando `declared_reference_edges` y `doc_anchor_edges`; tests en `tests/api/test_rules.py` y `tests/api/test_on_write_entering.py`; línea en `CHANGELOG.md`. Repo: `/mnt/ssd/proyectos/SLDB_1` (`sldb`). Límites: no toca `BatchReport.alerts` de `apply_batch` ni cambia niveles de reglas; no hace push; el commit lo hace el coordinador con `deskops closeout commit`; el aviso va por `deskops message send --to deskops`; el informe es `runs/subagents/<run-dir>/result-summary.md`. Nodo ejecutable, no agregado.

## AMBIGUEDADES

ninguna.

## DRY-RUN

Hipotético, sin ejecutar. Lecturas: `finding_route.py`, `rules_on_write.py`, `rule_graph.py`, `payload_save.py`, `DocumentReference`, los tests nombrados, el pill y `CHANGELOG.md`. Cambios previstos: devolver alertas desde `check_on_write`; añadir `alerts` con `default_factory=list`; en `with_payload`, construir y sustituir solo las aristas salientes declaradas por el payload; añadir tests de alerta sin listener (`monkeypatch` sobre `_LISTENERS`) y de arista que aparece/desaparece con `count(...)`; entrada de changelog. Dependencias: `split`, `route`, `declared_reference_edges`, `doc_anchor_edges`, pydantic y fixtures de los tests. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/api/test_rules.py`, `TMPDIR=/dev/shm pytest -q tests/api/test_on_write_entering.py`, `TMPDIR=/dev/shm pytest -q tests/api/test_rules_evaluation.py`.

## FUTURO

El ejecutor producirá el cambio y `result-summary.md`. El coordinador hará el commit y el aviso a deskops. Un humano decide si el código contradice el pill: en ese caso se detiene y se reporta, sin ampliar alcance.
