## REFORMULACION
GO02 es un nodo de diseño (`delivery`, no agregado) del repo sldb. Propósito: fijar, antes de implementar, la semántica, la gramática y la firma de evaluación del lenguaje de reglas. Resultado: `docs/architecture/rules-language.md` con los apartados (a)–(f) —gramática, caminos y cuantificadores, semántica estratificada y trivaluada, explicación, hash de contrato y firma `eval`— más tests de especificación xfail; produce `G_SEMANTICS`. Límites: no implementa (eso es GO03/GO05); solo documento y ejemplos xfail; depende de GO01 y `G_BOUNDARY`; su `output_scope` se limita a ese documento y esos tests.

## AMBIGUEDADES
1. «count = incomplete si algún elemento es incomplete»: obliga a inventar el tipo de `count` cuando no es incomplete (¿entero?, ¿booleano?) y cómo participa en un predicado; sin eso no se completa la tabla trivaluada de `count` que exige la aceptación.
2. «ordenadas por nombre de campo y separadas por salto de línea»: obliga a inventar el orden canónico (bytes/Unicode) y si hay salto final; ambos cambian el sha256 y la aceptación exige «orden canónico».
3. «caminos sobre relaciones por nombre de relación o de campo»: obliga a inventar si el camino se identifica por tipo de relación, por campo del nodo o por ambos, y con qué sintaxis; los ejemplos dados solo son nombres de relación.

## DRY-RUN
Sin ejecutar: el ejecutor leería `dag.yaml` (GO02), `brief.md`, `alcance.md`, `decisiones.md`, `where_parse.py`, `FieldCondition`, `where_subject`, definiciones de modelo/`__contract__`/`field_hashes` y `docs/cli-envelope.md`; confirmaría `G_BOUNDARY` satisfecho por GO01. Crearía solo `docs/architecture/rules-language.md` y tests de spec xfail (pytest, xfail, no skipped), sin tocar `src/`. Dependencias: GO01/`G_BOUNDARY` como prerrequisito; GO03 consumirá la firma y GO05 volverá verdes los xfail. Validaciones futuras: documento existente; cada construcción de (a) y (b) con ejemplo y resultado esperado (regex inválida, clausura con ciclo); tablas de operadores y trivaluada completas; `__contract__`, orden canónico y firma `eval` definidos; pytest reporta xfail; revisión en frío aceptada.

## FUTURO
GO03 implementa `eval` sobre networkx; GO05 implementa el lenguaje y vuelve verdes los xfail; GO10 retira shims. La revisión en frío y la satisfacción de `G_SEMANTICS` las decide el desk de sldb, no GO02. La promoción fijará en el TaskDoc los nombres exactos de test. D6 ya está confirmada por el dueño el 2026-11-04.
