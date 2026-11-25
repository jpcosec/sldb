## REFORMULACION

Propósito: que `sldb.code` exponga como hechos las claves del SQL de Postgres generado por `sqlmigrate` de Django (PK con IDENTITY, constraints de tabla y FK de `ALTER TABLE ADD CONSTRAINT`). Resultado: la columna `id` con tipo, `primary_key`, `parse_partial` e `identity`; un hecho `constraint` por clave con tipo, columnas y, en FK, `references`. Repo: `/mnt/ssd/proyectos/SLDB_1`, paquete `sldb.code`. Límites: sin estado acumulado entre migraciones ni otros dialectos; CHECK, EXCLUDE y demás acciones de ALTER quedan fuera y documentados.

## AMBIGUEDADES

1. "un hecho por cada clave (primaria, foránea y única)" frente a "UNIQUE o PRIMARY KEY escritos en la propia columna no crean un hecho constraint": obliga a decidir si el Goal incluye UNIQUE de columna.
2. "para PRIMARY KEY, FOREIGN KEY y UNIQUE de tabla" no aclara si UNIQUE de columna genera hecho; inventar alcance.
3. "el tipo leído del texto hasta el primer error": no define si incluye el texto del nodo ERROR ni el recorte; inventar la frontera.
4. "attrs.identity true además de attrs.primary_key si corresponde": "si corresponde" carece de criterio.
5. "columns vacía cuando la FK no lista columnas referenciadas": ¿`attrs.columns` o `attrs.references.columns`?
6. "o <tabla>.pk, <tabla>.fk~N si no tiene nombre": no cubre UNIQUE sin nombre; inventar convención.
7. "con la misma función de ids.py": no identifica la función; exige inspección no listada.
8. `files` lista `sql_readers.py`, pero Implementation Path añade `sql_fingerprints.py`: ¿entra modificarlo?
9. "partir en módulos si pasa de 80 líneas": métrica indefinida (líneas añadidas, fichero, función).
10. "relación references hacia el hecho de la tabla referenciada si está en el mismo archivo": tipo y dirección del edge no especificados.
11. "aviso a IR": canal y formato no definidos.
12. "commit": mensaje y autoridad no definidos.

## DRY-RUN

Lecturas: `lang_sql.py`, `sql_readers.py`, `sql_fingerprints.py`, fixture Django, `ids.py`, tests citados y `CHANGELOG.md`. Cambios previstos: parser de `column_definition` con ERROR, nodo `constraint`, soporte `ALTER TABLE ADD CONSTRAINT`, docstring, fixture, tests y CHANGELOG. Dependencias: tree-sitter-sql 0.3.13, `ids.py` y el fixture. Validaciones futuras: los cinco comandos de Validation y comprobar que los hechos de `.py` y TS no cambian.

## FUTURO

La salida concreta del árbol tree-sitter y el contenido del fixture los produce el ejecutor/parser; IR recibe el aviso y valida el resultado; un humano decide commit, merge y redacción final del CHANGELOG.
