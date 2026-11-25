## REFORMULACION

Propósito: que una escritura hecha por API entregue sus alertas `on_write` y que la regla `on_write` evalúe con las aristas que el payload nuevo declara. Resultado: (1) `check_on_write` devuelve sus findings de nivel alert y `save_document_payload` los expone en un campo nuevo `DocumentReference.alerts: list[dict[str, Any]]` (vacío por defecto), sin quitar el envío por `route`; (2) `RuleGraph.with_payload` devuelve un grafo nuevo con las aristas salientes (`__references__`, `__doc_anchors__`) del documento reconstruidas desde el payload. Repo sldb; superficie: `src/sldb/api/rules/{rules_on_write,rule_graph}.py`, `src/sldb/api/documents/payload_save.py`, `DocumentReference`, `tests/api/test_rules.py`, `tests/api/test_on_write_entering.py`, `CHANGELOG.md`. Límites: fuera `BatchReport.alerts` de `apply_batch` y cambiar niveles de reglas; el commit lo hace el coordinador, sin push; las líneas citadas son orientativas y se localiza por función.

## AMBIGUEDADES

1. «condición "exists(references)" o equivalente en el lenguaje de reglas»: obliga a inventar el nombre exacto de la relación declarada y el predicado válido del lenguaje; `exists(...)` no aparece en el input como sintaxis confirmada.
2. «reemplazar con ellas las del documento en el grafo que evalúa la regla; las demás aristas quedan como están»: no aclara si las aristas salientes del documento que el payload ya no declara se borran (reemplazo) o se conservan; ambas lecturas caben.
3. «`DocumentReference.alerts: list[dict[str, Any]] = Field(default_factory=list)`»: se pide «grep -rn "class DocumentReference"», así que el bundle no muestra si es pydantic o dataclass; obliga a inventar el mecanismo de default.
4. «monkeypatch sobre la lista de listeners de finding_route»: no nombra el símbolo (`_LISTENERS`, privado); obliga a elegir cómo vaciarla.
5. Validación incluye «TMPDIR=/dev/shm pytest -q tests/api/test_rules_evaluation.py», archivo no listado en `files` ni en el Scope; obliga a decidir si requiere cambios.
6. «aviso a deskops con deskops message send --to deskops» frente a la convención «--to <repo>»: no queda claro si "deskops" es el repo destino.

## DRY-RUN

Lecturas: los cuatro módulos citados, `DocumentReference`, `declared_references.declared_reference_edges`, `doc_anchor_edges`, ambos test files y sus fixtures, `CHANGELOG.md`. Cambios previstos: retorno de `check_on_write`; campo `alerts` en `DocumentReference` y su paso desde `_save`; aristas del payload en `with_payload`; dos tests nuevos; una línea en CHANGELOG bajo «## 0.1.13 — not released yet». Dependencias: modelos pydantic del `World` de `test_rules_evaluation`; `rule_graph` cargado por índice. Validaciones futuras: los tres `pytest` y `deskops message send`.

## FUTURO

El coordinador ejecuta `deskops closeout commit` y el aviso; un humano confirma la semántica de reemplazo de aristas y si `test_rules_evaluation` cambia.
