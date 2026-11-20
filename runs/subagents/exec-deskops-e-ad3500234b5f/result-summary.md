# result-summary — task-on-write-save-document-payload-devuelve-las-alertas...

run_id: exec-deskops-e-ad3500234b5f

## Hecho
- `check_on_write` devuelve las alertas (`Finding.as_dict()`, solo nivel alert); `route` las sigue recibiendo.
- `DocumentReference.alerts: list[dict[str, Any]] = Field(default_factory=list)`; `save_document_payload` lo llena (vacío sin reglas).
- `RuleGraph.with_edges(node, edges)`: reemplaza las aristas salientes `references`/`contains` del documento por las del payload nuevo (`declared_reference_edges` + `doc_anchor_edges`, vía `payload_edges` en rules_on_write.py); no muta el grafo del índice. Las demás aristas quedan.
- Tests: tests/api/test_rules.py (alerta devuelta sin listener), tests/api/test_on_write_entering.py (regla `count(depends_on: title != "") > 0`: agregar la referencia pasa, quitarla da rules/linked).
- CHANGELOG.md.

## Archivos (para `git add` uno por uno)
CHANGELOG.md, src/sldb/api/documents/document_reference.py, src/sldb/api/documents/payload_save.py, src/sldb/api/documents/payload_save_steps.py, src/sldb/api/rules/rule_graph.py, src/sldb/api/rules/rules_on_write.py, tests/api/test_rules.py, tests/api/test_on_write_entering.py

## Validación (validation.log)
- test_rules.py 14 passed; test_on_write_entering.py 8 passed; test_rules_evaluation.py 12 passed.
- `bash tools/check.sh --fast`: rc 1, solo gate `identidad`: «directorio versionado sin clasificar en la raíz: workbench_demo» (preexistente, commit 562847e2, ajeno a esta tarea).

## Para el supervisor
- NO commiteé ni ejecuté `deskops advance` porque el gate exige rc 0. Decidir clasificar workbench_demo o autorizar el commit con el gate en rojo.
- Pendiente tras el commit: `deskops message send --to deskops` (título de la tarea; cuerpo: qué cambió y el commit).

## Actualización
Coordinador autorizó commitear con `identidad` en rojo solo por workbench_demo (preexistente, 562847e2). FALLAN: solo identidad; el resto de puertas pasa. Commit hecho por nombre, con Task-Id; luego deskops advance.

## Commit
Mi código quedó en 0f91540d (Task-Id en el trailer). Ese commit también arrastró archivos que otros agentes tenían en el índice compartido (matching, notations, store_check, diagnostics y sus tests); otros commits posteriores (07450d10, eb42a49e) lo citan. Sin push; el coordinador decide si lo separa. `identidad` falla solo por workbench_demo (autorizado). `deskops advance` rc 0 (ritual-testing). Aviso a deskops: pendiente `deskops message send --to deskops` (commit 0f91540d).
