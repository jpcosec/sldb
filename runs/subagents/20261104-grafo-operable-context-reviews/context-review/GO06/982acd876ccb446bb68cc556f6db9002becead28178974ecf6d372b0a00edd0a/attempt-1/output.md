## REFORMULACION
GO06 encarga en sldb definir el modelo `RuleDoc` (sujeto por familia de modelo con filtro opcional, condición, severidad, momento y mensaje), registrarlo como documento y añadir `sldb rules check [--subject DOC]` y `sldb rules explain RULE SUBJECT`. Resultado: findings con cláusula y nodo, exits 0/1/2, rechazo de reglas mal formadas y `docs/architecture/rules.md`. Repo dueño: sldb. Límites: no define el lenguaje (GO05), no implementa evaluación `on_write`/`on_transition`/`on_check` ni caché (GO08), no define anclas `doc:` (GO07), no define modelos de recibo ni autenticación.

## AMBIGUEDADES
1. «sldb rules check [--subject DOC] que evalúa las reglas aplicables»: no dice qué evaluar si se omite `--subject` (¿todas las reglas?, ¿todos los documentos?, ¿error?). Obliga a inventar el alcance del comando.
2. «Hermanos = modelos con el mismo base que no son X ni subtipos de X.»: introduce “hermanos” pero no indica si afecta al sujeto, al filtro, a los findings o a nada. Obliga a inventar su función.
3. «Reemplaza al Constraint de docs/opsys que nunca tuvo código.»: `output_scope` no incluye `docs/opsys`; no dice si hay que editar o eliminar ese documento. Obliga a inventar un cambio fuera del alcance declarado.
4. «emite Finding por el canal existente»: no identifica el canal ni el esquema de `Finding`; la aceptación solo exige cláusula y nodo. Obliga a inventar formato y destino.

## DRY-RUN
Lecturas: brief, alcance, decisiones, dag y contrato de GO05; evidencia de G_SEMANTICS. Cambios previstos: `rule_doc.py`, `api/rules/`, `cli/commands/rules.py`, `docs/architecture/rules.md` y pruebas. Dependencias: parser/evaluador y error de parser de GO05; G_SEMANTICS pendiente. Validaciones futuras: store temporal con Base, X<Base, Y<X, Z<Base; sujeto `model <= X` aplica a X e Y, no a Z; `rules check` reporta error y alert con cláusula y nodo; `rules explain` cubre los tres exits; regla mal formada rechazada al escribir; documentación. Sin ejecutar.

## FUTURO
GO08 consumirá el `content_hash` como clave de caché y decidirá los momentos de evaluación. GO05 entregará lenguaje, parser y formato de error. El dueño confirmará G_SEMANTICS/D6. Un humano promoverá el nodo y fijará el TaskDoc. PK03 validará el conjunto con GO07.
