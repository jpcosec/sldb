REFORMULACION
Nodo ejecutable GO06 (no agregado) del plan grafo-operable, en el repo sldb. Propósito: que sldb evalúe reglas declaradas como documentos. Resultado: modelo RuleDoc validado al escribir; `api/rules` para check, explain y resolución de sujetos/reglas; CLI `sldb rules` con parser y registro en dispatcher; `docs/architecture/rules.md`, marca de reemplazo en `docs/opsys/bridge_primitives/README.md`, CHANGELOG y tests. Límites: fuera evaluación incremental y cableado `on_write`/`on_transition` (GO08), anclas `doc:` (GO07), transiciones como datos (GO09) y retiro de shims (GO10); nada se persiste del resultado de una regla.

AMBIGUEDADES
1. “severidad error|alert, momento on_write|on_transition|on_check” no fija los nombres de campo; “un test por campo (condition, where, severidad, momento, sujeto)” tampoco. Obligaría a inventar si son `severity`/`moment` o `severidad`/`momento`.
2. “rules check reporta error y alert como Finding con cláusula y nodo”, pero el Finding de core sólo tiene “level, code, subject, what, fix, document” y p2 define `what` con “<clause> (seen: ...)”. Obligaría a inventar dónde viaja `node`: campo nuevo, dentro de `what` o en otro sitio.
3. “subject sea una expresion del lenguaje de la forma model <= X (o conjuncion que la contenga)” no dice si se admiten cláusulas extra ni cómo se extrae la familia si las hay. Obligaría a inventar validación y semántica de aceptación.
4. “con prefijo <store>: si viene de un store enlazado” y “todos los documentos de su familia” no aclaran si `rules check` sin `--subject` recorre también stores enlazados. Obligaría a inventar el alcance federado.

DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout, archivos nombrados, `rules-language.md`, `graph-backend.md`, `core/finding.py`, vía de escritura/validación de documentos y registro/`base_models`. Cambios previstos: crear `RuleDoc` con validadores; `api/rules` (check, explain, subjects); comando/parser y dispatcher; exports; docs, CHANGELOG y tests de rechazo y aceptación. Dependencias: lenguaje y `GraphBackend.eval` de GO05, Finding de core, resolución de modelos/documentos y prefijos de store. Validaciones futuras: `pytest tests/api/test_rules.py`; store temporal Base/X/Y/Z; findings y exits de check; exits 0/1/2/3 de explain; rechazo por campo; `test_clean_code_rules.py` y `test_store_seams.py`; suite completa al final por el supervisor. Sin ejecutar.

FUTURO
GO08 consumirá el `content_hash` del RuleDoc y cableará `on_write`/`on_transition`; GO07 añadirá anclas `doc:`; GO09 tratará transiciones como datos; GO10 retirará shims. El supervisor correrá la suite completa y un humano aceptará la revisión en frío e integrará en main.
