REFORMULACION
GO02 es un nodo de diseño (delivery, no agregado) del repo sldb. Busca fijar, antes de implementar, la semántica, la gramática y la firma `eval` del lenguaje de reglas, produciendo G_SEMANTICS. Resultado: `docs/architecture/rules-language.md` con los apartados (a)-(f), tablas de equivalencia y trivaluada, y `tests/test_rules_language_spec.py` con un xfail por construcción. Límites: solo esos archivos, sin tocar `src/` ni escribir código de producción; depende de GO01 y G_BOUNDARY; cierra con revisión en frío aceptada.

AMBIGUEDADES
1. "la tabla cubre has, nonempty, in, ~, model <=, = != < <= > >=, eq, ne, gt, lt, contains, starts_with, is_null, is_not_null" frente a "los 18 operadores listados en la aceptacion". Si se cuentan los seis comparadores por separado, la lista enumerada tiene 19; el ejecutor debe decidir si omite uno o si el "18" excluye `model <=`, que la aceptación igual exige.
2. "seen = mapa campo → valor leído para las hojas de la cláusula que decidió el resultado". No define qué hojas entran cuando hay varios testigos posibles (dos conjuntos falsos, dos disyuntos verdaderos, cuantificadores anidados) ni si `not` incluye la hoja negada; obliga a inventar la regla de selección.
3. "salvo que el predicado sea una conjunción de nivel superior que contenga model <= X, en cuyo caso el dominio son los documentos de esa familia". Con dos `model <=` no se dice si "esa familia" es la intersección, la unión o la primera; tampoco si un `model <= X` solo cuenta como conjunción.

DRY-RUN
Un ejecutor futuro leería los archivos indicados (where_parse, where_subject, where_lookup, field_condition, facet_match, relation_type_doc, finding, cli-envelope), redactaría el documento y los tests xfail, sin tocar `src/`. GO01/G_BOUNDARY ya están satisfechos. Validaría con `pytest tests/test_rules_language_spec.py -q` (xfailed, 0 skipped), el grep de >=7 secciones y la revisión en frío; nada se ejecuta aquí.

FUTURO
GO03 implementará `eval`; GO05 volverá verdes los xfail; GO06/GO07 consumirán el contrato; el desk acepta la revisión y marca G_SEMANTICS en dag.yaml.
