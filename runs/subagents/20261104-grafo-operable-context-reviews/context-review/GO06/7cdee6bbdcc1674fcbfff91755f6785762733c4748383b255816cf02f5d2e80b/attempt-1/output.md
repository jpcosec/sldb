REFORMULACION

GO06 es un nodo de entrega (`kind: code`, no agregado) del repo sldb. Propósito: definir `RuleDoc` como documento registrado en el store, con sujeto por familia y filtro, condición, severidad, momento y mensaje de explicación. Resultado: modelo, API/CLI `rules check` y `rules explain`, findings por el canal existente y hash de regla. Límites: `output_scope` indicado; depende de GO05 y requiere G_SEMANTICS; no autentica actores ni produce hechos externos.

AMBIGUEDADES

1. «sujeto (familia de modelo vía `base_models` y un filtro en el lenguaje)». Obliga a inventar qué es `base_models`, cómo se declara y recorre la familia, cómo se compone el filtro y qué son exactamente los «hermanos».
2. «Las reglas tienen hash: cambiar una regla invalida lo derivado que depende de ella (GO08 lo usa)». Obliga a inventar qué hash (contenido, contrato, campos), su alcance y cómo se manifiesta la invalidación si los derivados no se persisten.
3. «sldb rules explain para una regla y un sujeto». La aceptación no incluye `rules explain`; obliga a inventar salida, envelope, código de salida y criterio de éxito.

DRY-RUN

Un ejecutor futuro leería brief, alcance, decisiones, contrato de GO05 (parser/evaluador), proyección de GO04, registro documental y canal de errores. Crearía `rule_doc.py`, API y CLI; registraría reglas, evaluaría las aplicables, implementaría explain y hash. Dependencias: GO05 y gate G_SEMANTICS. Validaría con pytest en store temporal: familia aplica a subtipos y no a hermanos; error/alert con cláusula y nodo; rechazo al escribir regla mal formada; documentación. Añadiría prueba de hash/invalidación o registraría hipótesis en TaskDoc. No se ejecuta nada.

FUTURO

GO05 entrega el lenguaje; GO02 y el dueño confirman D6/G_SEMANTICS; GO08 consume el hash; GO07 aporta anclas; PK03 valida el conjunto; la promoción humana/TaskDoc fija nombres exactos y tests.
