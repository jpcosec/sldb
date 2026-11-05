REFORMULACION
PK03 es un agregado no ejecutable de sldb. Encargo: agrupar reglas como documentos (GO06) y anclas a documentos con hash de contrato (GO07), para que un consumidor ate un recibo a su sujeto con un ancla que sldb evalúa; sldb no define modelos de recibo. Resultado conjunto: `rules check` con findings (severidad y cláusula fallida), `anchors check` con `intact/changed/lost` para `doc:`, `provenance_changed` y `anchor_state` consultable desde una regla. Repo dueño: sldb. Límites: no auth, no hechos externos, no persistir derivados, no modelos de recibo, no backend externo; el agregado no se promueve ni ejecuta.

AMBIGUEDADES
1. «un documento cualquiera con un campo de ancla doc: queda consultable desde una regla por anchor_state». Obliga a inventar si «campo de ancla» es cualquier campo con valor `doc:<Model:name>`, un campo declarado o solo `Provenance.from_`, y dónde se guarda el hash visto. La aceptación de GO07 solo concreta `from: doc:B`.

DRY-RUN
PK03 no se ejecuta: se promueven GO06 y GO07. No hay arista GO06→GO07; no se transfieren datos entre hermanos. Orden hipotético:
1. GO06, con el lenguaje de GO05 y la herencia de modelos, produce `RuleDoc`, validación al escribir, `rules check/explain`, findings, hash de regla y `docs/architecture/rules.md`. No entrega a GO07.
2. GO07, con payload/`field_hashes` de GO04, lenguaje de GO05 y hash de contrato de GO02, produce ancla `doc:`, `anchors check`, `anchor_state`, `provenance_changed` y `docs/architecture/anchoring.md`. No consume salida de GO06.
3. Validación conjunta: store temporal A→B; editar contrato, editar fuera del contrato, borrar B; verificar `changed/intact/lost` y `provenance_changed`; cargar una `RuleDoc` y comprobar finding con severidad/cláusula y consulta por `anchor_state`. Si GO07 usa una regla, el agregado debe orquestar GO06+GO07; no hay arista sibling que lo garantice. Dependencias: `G_SEMANTICS` en ambos; GO07 además GO04/GO05; D6 pendiente. Validaciones futuras: pytest, CLI con envelope, docs y CHANGELOG; sin ejecutar.

FUTURO
GO06/GO07 producen TaskDocs, código y docs; GO02/GO04/GO05 entregan hash de contrato, payload y lenguaje; el dueño confirma D5/D6/D7 y gates G_SEMANTICS/G_SEAM; deskops consume después, en su propio plan.
