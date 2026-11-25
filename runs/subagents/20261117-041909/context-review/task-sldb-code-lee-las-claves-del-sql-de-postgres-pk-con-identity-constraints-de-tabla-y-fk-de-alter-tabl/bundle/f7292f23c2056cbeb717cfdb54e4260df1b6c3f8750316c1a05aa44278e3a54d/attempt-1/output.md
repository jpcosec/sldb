REFORMULACION
Propósito: ampliar `sldb.code` para leer claves del SQL de Postgres en migraciones `sqlmigrate`: PK con `IDENTITY`, constraints de tabla y FK de `ALTER TABLE ... ADD CONSTRAINT`. Resultado: hechos `constraint` con tipo, columnas y `references`, y columnas `id` con `primary_key`, `identity` y `parse_partial`. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: fuera otras acciones de `ALTER TABLE`, `CHECK`/`EXCLUDE`, otros dialectos y estado entre migraciones. Es una tarea ejecutable (`task.code`), no un agregado.

AMBIGUEDADES
1. `"toda FK, venga de ALTER TABLE o de CREATE TABLE (constraint de tabla o REFERENCES en la columna), lleva attrs.references"` frente al docstring incluido: `"a column-level REFERENCES (no fact, no mark)"`. Obliga a inventar si una FK declarada en columna crea hecho `constraint`, cómo se nombra y si solo marca la columna.
2. `"Las constraints sin nombre se nombran por tipo (pk, fk, unique) dentro de su tabla y las repetidas llevan sufijo ~2, ~3 en orden de aparición"`. No aclara si el sufijo cuenta por tipo o entre todas las constraints sin nombre, ni qué ocurre si choca con una constraint nombrada `pk`. Obliga a inventar la política de unicidad.
3. `"el tipo leído del texto hasta el primer error"`. No define “primer error”: ¿nodo `ERROR`, token inválido, inicio de constraint de columna? Obliga a inventar el límite exacto del tipo.

DRY-RUN
Lecturas: `lang_sql.py`, `sql_readers.py`, `sql_columns.py`, `sql_keys.py`, `sql_fact.py`, `ids.py`, fixture Django y tests citados. Cambios previstos: readers de columnas/constraints, hechos y relaciones, tests de símbolos y anclas, docstring y `CHANGELOG`. Dependencias: tree-sitter-sql 0.3.13, extras `code`/`dev`, `Ids`. Validaciones futuras: los cinco comandos de Validation, empezando por `pytest` focalizado y terminando en `tools/check.sh --fast`. Sin ejecutar nada.

FUTURO
Un nodo de ejecución implementará y probará; otro de testing validará; closeout commiteará y avisará a IR. Un humano aprobará el alcance final y el merge.
