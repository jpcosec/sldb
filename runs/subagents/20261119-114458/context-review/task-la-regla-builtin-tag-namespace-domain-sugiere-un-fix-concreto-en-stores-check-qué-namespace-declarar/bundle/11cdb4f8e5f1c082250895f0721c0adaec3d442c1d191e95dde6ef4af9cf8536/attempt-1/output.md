## REFORMULACION

Encargo ejecutable (`task.code`, nodo `ritual-execution`; no es agregado ni tiene hijos). Propósito: que los hallazgos de la regla builtin `tag_namespace:domain` —hoy con `fix` vacío en `_finding` de `builtin_tag_findings.py`— emitan un texto accionable, y que las demás reglas builtin de tags con `fix` vacío también lo reciban. Resultado: `fix` no vacío, tests, CHANGELOG, commit y aviso a sldb-ui. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: no cambiar qué detecta la regla; superficie en `src/sldb/api/rules/builtin_tag_findings.py`, `builtin_tag_rules.py` si hace falta, tests y CHANGELOG.

## AMBIGUEDADES

1. «el namespace a declarar en la política del store (con el comando o la clave exacta) o los tags válidos de ese namespace»: dos alternativas de texto y ninguna fuente que defina el esquema de "política" ni el comando/clave. Obliga a inventar el formato del `fix` y el nombre de la clave o comando.
2. «revisar las demás reglas builtin de tags y llenar su fix si también está vacío»: no se enumeran; el bundle solo aporta la familia `builtin:tag_namespace:*`. Obliga a inventar el conjunto de reglas y sus archivos.
3. «tests en tests/api/test_rules_evaluation.py» frente a la validación que incluye `tests/api/test_tags.py`: el archivo del bundle no contiene tests de esta regla. Obliga a inventar dónde vive el test nuevo.
4. «(y builtin_tag_rules.py si hace falta)»: condicional y ese archivo no está en el cold-bundle. Obliga a decidir sin verlo si el cambio lo toca.
5. «aviso a sldb-ui»: no se indica mecanismo (inbox, issue, mensaje). Obliga a inventar el canal.

## DRY-RUN

Lecturas: `builtin_tag_rules.py` (ausente del bundle, dependencia a leer), `builtin_tag_findings.py`, `rules_check.explanation`, `semantic_tags.namespaced_tags`, tests de tags y esquema de política de namespaces. Cambios previstos: construir en `_finding` (o helper en `builtin_tag_rules.py`) el texto de `fix` a partir del namespace incumplido y la acción; sustituir `""`; añadir tests de `fix` no vacío; CHANGELOG. Dependencias: contrato del campo `fix` en `Finding` y sintaxis de la política. Validaciones futuras: los cuatro comandos del TaskDoc (pytest de rules_evaluation, tags, clean_code_rules y `tools/check.sh --fast`) y `stores check --format json` sobre el store de sldb-ui. Nada ejecutado.

## FUTURO

Un humano decide el texto y el esquema exactos del `fix` (ambigüedades 1 y 2); otro nodo o el cold-bundle debe aportar `builtin_tag_rules.py` y el mecanismo de aviso a sldb-ui; el closeout produce commit y retirada del Board.
