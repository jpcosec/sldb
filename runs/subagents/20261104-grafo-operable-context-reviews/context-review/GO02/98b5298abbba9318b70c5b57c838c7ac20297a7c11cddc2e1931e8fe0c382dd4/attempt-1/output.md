REFORMULACION
GO02 es un nodo de diseño, no agregado, en sldb: fijar en `docs/architecture/rules-language.md` la gramática, los caminos, la semántica trivaluada, el formato de explicación, el hash `__contract__` y la firma `eval(predicado, sujeto)` del lenguaje de reglas, con tabla de equivalencia y ejemplos como tests xfail. Resultado: documento y tests de spec; sin código de producción. Límites: solo ese documento y tests; no cambia comportamiento. Produce `G_SEMANTICS`.

AMBIGUEDADES
1. "un paso se escribe como nombre de campo (depends_on: sigue las aristas references que ese campo declara)": no define qué pasa si el campo no declara aristas references o no existe; obliga a inventar si es error de parseo, conjunto vacío u omisión.
2. "una comparación con count es incomplete si algún elemento del camino es incomplete": solo cubre `count`; no define el valor de una comparación normal con operando incomplete, ni cómo evalúa el predicado sobre un elemento incomplete. Obliga a inventar la semántica.
3. "seen = mapa campo → valor leído para las hojas de la cláusula que decidió el resultado": no define el valor cuando la hoja es incomplete; obliga a inventar su representación.

DRY-RUN
Un ejecutor futuro leería `G_BOUNDARY`/GO01, `where_parse.py`, `where_subject`, `field_hashes`, `relation_type_doc.py` y las fuentes del plan; escribiría el documento con (a)–(f), tablas y ejemplos; añadiría tests xfail (no skipped). Dependencias: GO01/`G_BOUNDARY`; consumen GO03, GO05 y GO10. Validaría con pytest que los xfail fallan, cobertura de operadores, existencia del doc y revisión en frío; sin ejecutar.

FUTURO
El desk de sldb acepta la revisión y satisface `G_SEMANTICS`; GO03 implementa la firma y deja caminos en `NotImplementedError`; GO05 vuelve verdes los xfail; GO10 retira los shims. Un humano debe reconciliar que la guía llama D5–D7 pendientes y `decisiones.md` las da por confirmadas antes de cerrar el gate.
