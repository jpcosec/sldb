## REFORMULACION
Nodo ejecutable `task.code` (no agregado) en el repo `/mnt/ssd/proyectos/SLDB_1/sldb`. Propósito: que los hallazgos de la regla builtin `tag_namespace:domain` —y de otras reglas builtin de tags con `fix` vacío— incluyan un `fix` accionable en `stores check --format json`. Resultado: texto de `fix` que indique el namespace a declarar y la acción/comando/clave, o los tags válidos; tests y CHANGELOG actualizados. Límites: trabajar sobre `src/sldb/api/rules/builtin_tag_findings.py` (y `builtin_tag_rules.py` si hace falta), tests de reglas, sin cambiar qué detecta la regla.

## AMBIGUEDADES
1. “el namespace a declarar en la política del store (con el comando o la clave exacta) o los tags válidos de ese namespace”: no fija formato ni cuándo usar una alternativa u otra; obligaría a inventar plantilla y criterio.
2. “revisar las demás reglas builtin de tags y llenar su fix si también está vacío”: no enumera cuáles ni define “demás”; obligaría a inventar el inventario y el alcance.
3. “nombrando el namespace y la acción”: no indica de dónde obtener el namespace esperado para cada hallazgo; obligaría a inventar el mapeo.
4. “CHANGELOG y commit; aviso a sldb-ui”: no precisa mensaje de commit, canal ni formato del aviso; obligaría a inventarlos.

## DRY-RUN
Lecturas hipotéticas: TaskDoc, inbox referenciada, `builtin_tag_rules.py`, `builtin_tag_findings.py`, `tests/api/test_rules_evaluation.py`, `tests/api/test_tags.py`, `CHANGELOG.md` y utilidades de test. Cambios previstos: completar textos `fix` y añadir/ajustar tests; actualizar CHANGELOG. Dependencias: entorno `uv`, extras `code`/`dev`, fixtures y helpers existentes. Validaciones futuras, sin ejecutar: los cuatro comandos de `Validation`, incluido `tools/check.sh --fast`.

## FUTURO
Un ejecutor implementará y ejecutará validaciones; un revisor humano o nodo de revisión aceptará el commit y decidirá el aviso final a `sldb-ui`.
