## REFORMULACION

Propósito: corregir el falso positivo de GO10 que confunde el operador viejo `contains` con el nombre de la relación de aristas de contención. Resultado: el test sigue fallando ante un operador viejo usado como predicado y deja de fallar cuando `contains` solo nombra la relación; se añaden dos tests en memoria. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: cambiar solo `tests/store/test_where_retired.py` —y, según Done When, `CHANGELOG.md`—; no tocar `docs/` ni `src/`, ni la excepción de `docs/architecture/rules-language.md`, ni el test de `where_parse/FieldCondition`. Es una tarea `task.code` ejecutable, no un agregado.

## AMBIGUEDADES

1. «cambiar solo tests/store/test_where_retired.py» frente a «el commit toca solo ese archivo y CHANGELOG.md»: no queda claro si debe editarse CHANGELOG ni con qué entrada; obliga a inventar el alcance real del commit.
2. «precedido por un nombre de campo»: no define la sintaxis del campo (¿`status`, `a.b`, identificadores entre comillas?); obliga a inventar la gramática aceptada.
3. «seguido de un valor»: no define qué cuenta como valor (¿cadena, número, identificador?); obliga a inventar el patrón.
4. «por ejemplo r"\w+\s+contains\s+\S" o r"(?<!\w)contains\s*:"»: son ejemplos; obliga a decidir el regex exacto, mayúsculas y límites de palabra.
5. «Factorizar la detección en una función pura (por ejemplo _old_operators...)»: nombre y firma no son vinculantes; obliga a decidir la API y si los tests nuevos deben llamarla.
6. «confirmar que pasa sobre docs/ actual»: no indica qué hacer si `docs/` ya contiene otros operadores viejos.
7. «comprobado revirtiendo el patrón localmente»: no define el procedimiento ni cómo dejar el árbol limpio; obliga a inventar la verificación.

## DRY-RUN

Lecturas: test completo (`OPERATORS` línea 18, `_code`, `_historic_rows`, `test_no_old_operator_in_the_code_of_docs`), nota del inbox y `docs/` en solo lectura. Cambios previstos: sacar `contains` de `OPERATORS`, añadir patrón de contexto predicado, extraer función pura y agregar dos tests. Dependencias: pytest y helpers existentes. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py`, prueba de regresión revirtiendo el patrón y `git diff` limitado a los archivos pactados. Sin ejecutar nada.

## FUTURO

El ejecutor implementará y correrá la validación. Un humano decidirá la entrada de CHANGELOG y si se restauran ejemplos en `docs/`, fuera de alcance. La aceptación de GO10 revalidará el resultado conjunto.
