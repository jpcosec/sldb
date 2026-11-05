REFORMULACION
GO07 es un nodo `code`/`delivery` del repo sldb, hijo de PK03. Debe entregar anclas documentales `doc:Model:name@sha256:<hash>` en campos `__doc_anchors__` y en `Provenance.from_`; pinneado al guardar; estados intact/changed/lost; `check_doc_anchors(store)` y comando `anchors check`; alertas `provenance_changed`; documentación y CHANGELOG. Límites: no cablea `stores check` (GO08), no define reconnected, no autentica actores, no persiste estados ni define modelos de recibo.

AMBIGUEDADES
1. Cita: “GO07 expone check_doc_anchors(store) → list[Finding] y el comando anchors check la usa”; “anchors check lo reporta como alertas”. El `output_scope` no incluye ningún área CLI. Obliga a inventar dónde vive el comando o si se toca fuera del alcance.
2. Cita: “anchor_state es un campo derivado consultable desde el lenguaje de GO05...”. El `output_scope` no incluye lenguaje ni evaluador. Obliga a inventar el mecanismo de exposición —hook, faceta derivada o cambio en GO05— y si excede el alcance.
3. Cita: “lista de nombres de campos de str o de list[str]”. La aceptación solo usa un campo escalar `subject`; no define cómo se reporta `anchor_state` con varias anclas. Obliga a inventar si el estado es por elemento, agregado (any/all) o una lista de findings.

DRY-RUN
Un ejecutor leería el contrato de hash de GO02/G_SEMANTICS, la proyección de GO04, el lenguaje de GO05, `Provenance`, el modelo base, `payload_save_steps.py` y el canal de alertas/CLI. Cambiaría: atributo `__doc_anchors__`, parseo y pinneado de `doc:`/`from:`, estados y `check_doc_anchors`, comando `anchors check`, alerta `provenance_changed`, docs y CHANGELOG. Depende de GO04 y GO05; G_SEMANTICS está pending. Validaría con pytest: pinneado, changed/intact/lost, borrado, regla con `anchor_state`, `provenance_changed`, envelope de alertas y docs/CHANGELOG. No se ejecuta.

FUTURO
GO02/G_SEMANTICS fija el hash de contrato; GO05 aporta el lenguaje; GO04 la proyección; GO08 cablea `stores check`; el desk de sldb acepta la revisión y el dueño indica el host de pytest. GO09 conserva `effects`. Nada de esto es ambigüedad del nodo.
