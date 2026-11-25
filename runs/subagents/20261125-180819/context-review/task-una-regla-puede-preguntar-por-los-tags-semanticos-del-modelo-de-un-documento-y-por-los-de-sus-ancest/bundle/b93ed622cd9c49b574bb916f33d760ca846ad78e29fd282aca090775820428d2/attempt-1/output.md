## REFORMULACION
Propósito: que el lenguaje de reglas seleccione documentos por concepto semántico, no por nombre de modelo. Resultado: un predicado evaluable, verdadero si el modelo del documento tiene el tag consultado o uno relacionado vía el DAG semántico, más documentación en rules-language.md y tests. Repo: sldb; toca lenguaje de reglas, evaluador, docs y tests. Límites: dentro, lenguaje y evaluador; fuera, reglas concretas de specIR y cambios al DAG. Es tarea ejecutable (`task.code`), no agregado.

## AMBIGUEDADES
1. "tiene un tag dado o uno que desciende de él" frente a "casa otro cuyo modelo declara un tag hijo": no queda fijada la dirección de herencia; obligaría a inventar si el predicado sube o baja el DAG.
2. "Un tag que no existe en el DAG se informa al validar la regla": no se especifica error/warning, momento ni formato; obligaría a inventar el contrato.
3. "la relación de padre y equivalencia que el DAG ya resuelve": "equivalencia" no se define; obligaría a inventar si es alias, sinónimo o igualdad de ids.
4. "docs/architecture/rules-language.md, rules.md y tags.md": las rutas de rules.md y tags.md no se indican; obligaría a inventar ubicaciones.
5. "pills ligadas, átomos ligados" frente a `pills: []` y `atoms: []`: no hay ninguno en el bundle; obligaría a inventar qué contexto falta.
6. "revisar un estándar pide reglas por concepto" frente a "Fuera: reglas concretas de specIR": no se aclara si basta test o hace falta una RuleDoc real; obligaría a inventar el alcance de integración.

## DRY-RUN
Leer: Board, rituales, rules-language.md, rules.md, tags.md, `sldb semantic --help`, parser/evaluador y tests existentes. Cambios previstos: añadir el predicado al lenguaje y al evaluador, validarlo en RuleDoc, documentarlo con ejemplo y crear `tests/test_rules_semantic_tag_predicate.py`. Dependencias: API del DAG (padre/equivalencia) y validador de reglas. Validaciones futuras: los dos pytest citados y, si toca gates, `tools/check.sh`/`check_claims.py`.

## FUTURO
Otro nodo resuelve las ambigüedades antes de implementar; un humano decide la dirección de herencia y el contrato del tag inexistente. Después: commits, closeout y actualización del Board.
