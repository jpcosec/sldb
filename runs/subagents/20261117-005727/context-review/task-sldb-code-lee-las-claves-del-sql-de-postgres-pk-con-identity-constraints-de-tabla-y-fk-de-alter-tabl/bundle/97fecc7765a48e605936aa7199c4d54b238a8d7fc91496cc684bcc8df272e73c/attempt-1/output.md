REFORMULACION
Nodo ejecutable `task.code`, no agregado. Propósito: ampliar `sldb.code` para que, sobre SQL de Postgres y migraciones de `sqlmigrate`, publique la columna `id` aunque la gramática falle en `GENERATED ... AS IDENTITY`, y un hecho `constraint` por PK, FK y UNIQUE de tabla y por cada `ALTER TABLE ... ADD CONSTRAINT`. Resultado: columnas con `attrs.primary_key`, `attrs.unique`, `attrs.identity` y `attrs.parse_partial`; constraints con `constraint_type`, `columns`, `references {table, columns}` y relación `references` si la tabla referenciada está en el archivo. Repo: `src/sldb/code/lang_sql.py`, `sql_readers.py`, fixture Django, tests de símbolos/anclas, CHANGELOG. Límites: sin estado acumulado entre migraciones ni otros dialectos; otras acciones de `ALTER TABLE` quedan fuera.

AMBIGUEDADES
1. «partir en módulos si pasa de 80 líneas»: no dice si son líneas nuevas, del archivo resultante o de una función; obliga a inventar unidad, umbral y criterio de división.
2. «attrs.constraint_type»: no fija los valores observables; podría ser `primary_key`/`foreign_key`/`unique` o `pk`/`fk`/`unique`; obliga a inventar vocabulario y tests.
3. «un kind nuevo constraint, hijo de su tabla» junto a «ALTER TABLE ... ADD CONSTRAINT»: no aclara qué hacer si la tabla alterada no tiene hecho en el mismo archivo; obliga a inventar si se omite, se crea una tabla implícita o queda un constraint huérfano.

DRY-RUN
Un ejecutor futuro leería el TaskDoc, rituales, `lang_sql.py`, `sql_readers.py`, `sql_fingerprints.py`, el fixture Django y los tests citados; inspeccionaría cómo tree-sitter-sql representa `ALTER TABLE ADD CONSTRAINT` y las constraints de tabla. Cambiaría `sql_readers.py` para lectura tolerante de columnas y constraints, y `lang_sql.py` para emitir hechos `constraint`, attrs y relación `references`; actualizaría fixture, tests, docstring y CHANGELOG. Dependencias: tree-sitter-sql 0.3.13, `Ids`, `fact`/`rels`, escaneo y anclas existentes. Validaciones futuras: los cinco comandos de Validation, sin ejecutarlos ahora.

FUTURO
Otro nodo ejecutará implementación y validaciones; closeout verificará git, árbol limpio y commit; IR recibirá el aviso y consumirá los hechos publicados.
