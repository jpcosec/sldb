## REFORMULACION
Nodo ejecutable `task.code`, no agregado. Propósito: ampliar el lector SQL de Postgres de SLDB para que IR08 disponga de claves en migraciones Django generadas con `sqlmigrate`. Resultado esperado: publicar la columna `id` con tipo, `attrs.primary_key` y `attrs.parse_partial`; emitir hechos `constraint` para PK, FK y UNIQUE de tabla y para cada `ALTER TABLE ... ADD CONSTRAINT`, con `constraint_type`, columnas y, en FK, `references {table, columns}` y relación `references` si la tabla está en el archivo. Repo: `src/sldb/code/lang_sql.py`, `src/sldb/code/sql_readers.py`, fixtures y tests indicados, `CHANGELOG.md`. Límites: fuera estado acumulado entre migraciones, otros dialectos y otras acciones de `ALTER TABLE`.

## AMBIGUEDADES
1. «PK con IDENTITY» y «marca de clave primaria»: no se especifica si IDENTITY debe exponerse como atributo propio; obligaría a inventar un `attrs.identity` o similar.
2. «si el texto contiene PRIMARY KEY»: no delimita comentarios, literales ni mayúsculas; obligaría a inventar reglas de detección textual.
3. «PRIMARY KEY, FOREIGN KEY y UNIQUE de tabla»: no aclara si `UNIQUE` declarado en columna también genera `constraint`; obligaría a decidir alcance no escrito.
4. «<tabla>.fk~N»: no define numeración ni unicidad de `N`; obligaría a inventar el criterio de asignación.
5. «el primer hijo es un identificador»: depende del árbol real de tree-sitter-sql; obligaría a inventar el manejo si el error aparece antes o el hijo no es identificador.

## DRY-RUN
Lecturas futuras: `lang_sql.py`, `sql_readers.py`, `sql_fingerprints.py`, fixture Django y tests citados. Inspección hipotética del parseo de `ALTER TABLE ADD CONSTRAINT` y constraints de tabla con tree-sitter-sql. Cambios previstos: captura parcial de `column_definition`; nuevo `kind constraint`; extracción de nombre, tipo, columnas y referencias; relación `references`; actualización de fixture, tests de símbolos y anclas; docstring y CHANGELOG. Dependencias: gramática tree-sitter-sql instalada, esquema de hechos existente y fixture disponible. Validaciones futuras, sin ejecutar: los cinco comandos `pytest`/`check.sh --fast` listados en Validation, y comprobación de que los hechos `.py` y TS no cambian.

## FUTURO
Corresponde al ejecutor implementar y ejecutar las validaciones; a revisión humana aceptar el alcance de atributos IDENTITY/UNIQUE; a IR confirmar que los hechos publicados cubren IR08; al nodo de cierre registrar CHANGELOG, commit y aviso a IR.
