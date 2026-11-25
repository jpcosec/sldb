## REFORMULACION

Encargo en el repo SLDB_1 (código en `src/sldb`, tests en `tests/api`): hacer que `save_document_payload` devuelva, en un campo nuevo `alerts` de `DocumentReference`, las alertas on_write generadas en esa escritura —manteniendo el envío por `finding_route`— y que una regla on_write vea las aristas salientes (`__references__`, `__doc_anchors__`) que el payload nuevo declara, sustituyendo en el grafo evaluado solo las del documento afectado. Incluye tests en `tests/api/test_rules.py` y `tests/api/test_on_write_entering.py`, `CHANGELOG.md` y commit. Límites: no toca `BatchReport.alerts` de `apply_batch` ni cambia niveles de reglas existentes.

## AMBIGUEDADES

1. «check_on_write devuelve la lista de findings de nivel alert que emitió» frente a «alerts: list[dict]»: no se define el esquema del dict ni si incluye solo nivel alert; obligaría a inventar campos (regla, mensaje, documento).
2. «construir las aristas salientes declaradas (__references__ y __doc_anchors__) del documento a partir del payload nuevo»: no se especifica formato del payload ni cómo derivar origen/destino/tipo; obligaría a inventar el mapeo.
3. «reemplazar con ellas las del documento en el grafo que evalúa la regla; las demás aristas quedan como están»: no aclara si `with_payload` muta el grafo o devuelve copia, ni si actualiza el modelo; obligaría a decidir esa semántica.
4. «opcional, lista vacía por defecto, para no romper a quien lo construye»: no fija `None` vs `[]` ni tipo exacto; obligaría a inventar contrato.
5. «una regla on_write de nivel alert» y «uno que la quita da el finding»: no fija nivel ni condición exacta del finding esperado; obligaría a inventar aserciones.
6. «sin listener instalado»: no indica cómo aislar listeners globales en test; obligaría a inventar fixture.
7. «aviso a deskops con deskops message send --to deskops»: contenido del mensaje no especificado.
8. «CHANGELOG y commit»: formato de entrada y mensaje de commit no definidos.

## DRY-RUN

Lecturas: `finding_route.py`, `rules_on_write.py`, `rule_graph.py`, `payload_save.py`, tests citados, `CHANGELOG.md`, `grep "class DocumentReference"`. Cambios previstos: retorno de findings en `check_on_write`; campo `alerts` en `DocumentReference`; reconstrucción de aristas en `with_payload`; tests nuevos; entrada de CHANGELOG. Dependencias: `finding_route`, `payload_save`, `RuleGraph`, modelo de documento. Validaciones futuras: los tres `pytest -q` listados. Sin ejecutar nada.

## FUTURO

Deciden otro nodo o un humano: redacción/aprobación del CHANGELOG y mensaje de commit, contenido del aviso a deskops y, si persisten, el esquema del dict y la semántica de copia en `with_payload`. `apply_batch` queda explícitamente para otra tarea.
