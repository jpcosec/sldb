## REFORMULACION

Encargo de un nodo de código (`task.code`, no agregado): añadir al lenguaje de reglas y a su evaluador un predicado que consulte los tags semánticos del modelo de un documento y su relación en el DAG semántico, para poder escribir reglas por concepto en vez de por nombre de modelo. Resultado: predicado verdadero según la relación del DAG, con tests y documentación. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Dentro: lenguaje de reglas y evaluador. Fuera: reglas concretas de specIR y cambios al DAG semántico.

## AMBIGUEDADES

1. Dirección de la relación. Título: "por los tags semánticos del modelo de un documento y por los de sus ancestros en el DAG"; Goal: "tiene un tag dado o uno que desciende de él en el DAG semántico". "Ancestros" y "desciende" se contradicen; obliga a inventar si el tag consultado debe ser ancestro o descendiente del tag del modelo.
2. "El predicado usa la relación de padre y equivalencia que el DAG ya resuelve". "Equivalencia" no está definida; obliga a inventar qué equivalencia es y qué API la expone.
3. "Un tag que no existe en el DAG se informa al validar la regla". No indica error ni warning ni canal; obliga a inventar severidad y fase.
4. "Leer docs/architecture/rules-language.md, rules.md y tags.md". `rules.md` y `tags.md` sin ruta; obliga a inventar su ubicación.
5. "Un predicado del lenguaje de reglas". Sin nombre, sintaxis ni aridad; obliga a inventar token y firma.

## DRY-RUN

Lecturas: los tres documentos, `sldb semantic --help`, parser/evaluador de reglas y API de consulta del DAG. Cambios previstos: nuevo predicado en parser y evaluador, `tests/test_rules_semantic_tag_predicate.py` y sección con ejemplo en `rules-language.md`. Dependencias: resolución padre/equivalencia del DAG y CLI semántica existentes. Validaciones futuras: los dos `pytest` indicados; casos tag directo, tag relacionado y sin relación; tag inexistente reportado al validar.

## FUTURO

La implementación la realiza otro nodo. Un humano decide nombre/sintaxis, dirección de la relación y severidad del tag inexistente. Las reglas concretas de specIR y cualquier cambio al DAG semántico corresponden a otro encargo.
