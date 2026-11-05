## REFORMULACION

**Propósito.** Fijar, antes de implementar, la semántica y gramática del lenguaje de reglas del plan `grafo-operable` (dag.yaml rev 9), nodo GO02, con D6 ya confirmada por el dueño.

**Resultado.** Un documento `docs/architecture/rules-language.md` con seis apartados (a)–(f) más tabla de equivalencia, y `tests/test_rules_language_spec.py` con ejemplos `xfail` (no `skipped`), uno por construcción. Sin código de producción. Produce el gate G_SEMANTICS.

**Repo.** `/home/jp/proyectos/SLDB_1/sldb`, workspace `desk`.

**Límites.** Solo esos dos ficheros; no se toca `src/`. Lecturas permitidas: `where_parse.py`, `where_subject.py`, `where_lookup.py`, `field_condition.py`, `facet_match.py`, `relation_type_doc.py`, `finding.py`, `docs/cli-envelope.md`. Reglas comunes: documentar toda capacidad nueva y registrar hipótesis en el TaskDoc ante contrato ausente.

## AMBIGUEDADES

1. `"__contract__ ... ausente = todos los campos del payload"` y `"__contract__ vacío = error"`: no define qué payload ni cómo distinguir atributo ausente de lista vacía. Obliga a inventar el criterio de detección.
2. `"model <= X"`: no define qué es `model` ni el orden de `X`. Obliga a inventar la semántica de comparación.
3. `"el dominio son los documentos de esa familia"`: "familia" no está definida. Obliga a inventar el mapeo modelo→familia.
4. `"termina ante ciclos"`: no aclara si la clausura corta en silencio o da error. Obliga a inventar el comportamiento.
5. `"seen = ... hojas de la cláusula que decidió el resultado"`: no define qué hojas en `and`/`or` con ramas no decisivas. Obliga a inventar el criterio.
6. `"revisión en frío aceptada por quien opera el desk"`: revisor, formato y evidencia no definidos. Obliga a inventar el circuito de aceptación.
7. `"pytest ... muestra N xfailed"`: `N` no fijado. Obliga a inventar el umbral.
8. `"un paso se escribe como nombre de campo (depends_on: ...)"`: los dos puntos no figuran en la gramática de caminos. Obliga a inventar si son sintaxis o glosa.
9. `"no resoluble al evaluar"` frente a `"documento inexistente"`: no define cómo distingue el ejecutor ambos casos. Obliga a inventar el mecanismo.
10. `"count(camino: predicado)"`: "camino" no se define como expresión (¿un paso o varios?). Obliga a inventar su alcance.

## DRY-RUN

Lecturas: los ocho ficheros citados más `dag.yaml`. Cambios previstos: crear `rules-language.md` con (a)–(f) y tabla de 18 operadores; crear el test de spec con un `xfail` por construcción, incluida regex inválida (`WherePredicateError`) y clausura con ciclo. Dependencias: `where_parse`/`FieldCondition` para la tabla, `finding.py` para el formato, `__contract__` para el hash. Validaciones futuras: `pytest -q`, `grep -c "^## "` ≥ 7, revisión en frío en `reviews/`.

## FUTURO

GO03 implementa `eval` según (f); GO05 convierte los `xfail` en verdes; un humano del desk acepta la revisión y marca G_SEMANTICS `satisfied` citando commit.
