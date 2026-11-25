REFORMULACION
Propósito: API pública `select_documents(store, selector, expect)` para ref, prefix, path_glob, model y where, expuesta en CLI y serve. Resultado: módulo nuevo y reexport, delegación de glob/find sin cambiar su salida, `docs select`, GET /docs/select, tests, doc y CHANGELOG. Repo: sldb, worktree aparte, base 6b80df36 con rebase a origin/main. Límites: no arrancar con G_GO04 pending; fuera GO05, nombres deskops, borrar resolve_selector (CC35) y superficies GD21. Es un nodo ejecutable.

AMBIGUEDADES
1. «glob_structural y find_structural … pasan a ser casos de select_documents … sin cambiar su salida» frente a «lista ordenada de {export_id, model, name, path}»: glob emite direcciones con campo (`st.{M}.doc.campo`); obliga a inventar el mapeo y el trato de patrones de campo.
2. «error de documento desconocido existente de sldb» no nombra clase ni código, y «error de ambigüedad con candidatos» solo sugiere `AmbiguousDocument`; obliga a inventar el primer tipo.
3. «exacto primero y si no hay, prefijo único; ambigüedad = error» se enuncia para expect=one; con many no dice si devuelve todos o falla; obliga a decidir.
4. No fija forma de `export_id` local ni si `path` es relativa al store o al proyecto; «orden por ruta relativa» no dice respecto a qué; obliga a inventar.
5. «también los de los stores enlazados por stores add» no aclara si sigue enlaces de enlaces; «No sigue aristas» habla de aristas de grafo; obliga a decidir transitividad.
6. «mapa (o string corto equivalente para la CLI)» contradice q6 «no hay string corto»; obliga a resolver el estado contradictorio.

DRY-RUN
Lecturas: archivos listados (`select_documents.py` no existe aún), `structural_queries.py`, `parsers/docs1-2.py`, `commands/docs.py`, `serve/docs_routes.py` y `routes.py`, tests, `api/__init__.py`, CHANGELOG. Cambios: módulo y reexport, delegación glob/find, subparser y handler `docs select` con envelope, GET /docs/select con query params, tests y goldens, doc y CHANGELOG. Dependencias: `FacetFilter(facet="payload")` de GO04, evaluador de where en main, `resolve_model_ref`, `load_runtime_documents`, `doc_status`/`split_doc_ref`, `AmbiguousDocument`. Validaciones futuras: los cuatro pytest, grep genérico, `docs select --one`, `clean_code_rules`, rebase. Sin ejecutar.

FUTURO
El supervisor marca G_GO04; GO04/GO05 fijan facet y evaluador; el coordinador despacha; el ejecutor implementa y valida; deskops recibe la nota; CC35 retira resolve_selector; el supervisor integra y corre la suite completa.
