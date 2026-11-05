REFORMULACION  
GO06 es un nodo `code` de entrega, repo dueño `sldb`. Propósito: definir `RuleDoc` como documento registrado, con sujeto por familia de modelo, `where` opcional, condición, severidad y momento; validarlo al escribir; y exponer `sldb rules check` y `sldb rules explain` emitiendo `Finding` por el canal existente. Resultado: modelo, API/CLI, validación, exits 0/1/2/3 y documentación. Límites: solo `output_scope`; no implementa el lenguaje (GO05), anclas (GO07) ni integración/caché en escritura, transición o check (GO08); no auth ni motor externo. Depende de GO05 y del gate `G_SEMANTICS`. La aceptación es comprobable con store temporal y los casos enumerados.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Lecturas: nodo GO06 y dag, brief/alcance/decisiones, API y parser de GO05, `core/finding.py`, registro de modelos/`base_models` y `RelationTypeDoc`, CLI/envelope y puntos de validación de escritura. Cambios previstos: crear `rule_doc.py`, `api/rules/`, `cli/commands/rules.py`, `docs/architecture/rules.md`; actualizar `bridge_primitives/README.md` y CHANGELOG. Implementar validación de `condition`, `where`, severidad, momento y sujeto; `rules check`; `rules explain`; mapeo de `false`/`incomplete` a `Finding`; exits. Dependencias: GO05 entrega parser/evaluador y explicación; `G_SEMANTICS` debe estar resuelto; GO08 consumirá el `content_hash` de la regla. Validaciones futuras: pytest de aceptación —herencia X/Y/Z, exits, rutas, incomplete, reglas mal formadas—, docs y CHANGELOG. Sin ejecución.

FUTURO  
El gate `G_SEMANTICS` lo resuelve la revisión en frío de GO02 y la disposición del desk de sldb. El TaskDoc fijará nombres exactos de archivos/tests. GO05 produce el lenguaje; GO08 integra caché y evaluación en escritura/transición/check. Un humano o el desk promueve el nodo y corre pytest en el host indicado.
