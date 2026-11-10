## REFORMULACION

El encargo: implementar en el repo sldb la task-gd25, un nodo ejecutable (no agregado). Propósito: tipar `params` y `sections` de ViewDoc con validación y servir vistas declaradas. Resultado: `sldb.api.run_view`, CLI `sldb views run|list`, `GET /views` y `GET /views/<name>` con ETag/304, tests, `docs/architecture/views.md` y CHANGELOG. Límites: sin `register_view_provider` ni `computed`; no tocar `/views/projection*` de SV02; sin nombres deskops en `src/`; ViewDoc en `notation/view_doc.py` y `notation_models.py` sin editar (q2); reglas de `rules` comprobadas al ejecutar (q5); no inventar API de grafo-operable.

## AMBIGUEDADES

1. "Validación al escribir una ViewDoc: ... rules nombran RuleDocs existentes" frente a "En GD25 se comprueba al ejecutar la vista ... y no al escribir la ViewDoc": obliga a inventar dónde vive la comprobación; el input la llama "Hipótesis para el dueño".
2. "por edges_from/edges_to o ProjectGraph.edges_from/to de GD21": no fija qué API usar; obliga a elegir una.
3. "si hay grafo de proyecto, su firma": no define qué es la firma; obliga a inventar su cálculo.
4. "sections: {key: rows | groups}" y "agrupadas ... group_order o ... por valor": no define la forma de `groups`.
5. "GET /views (lista)": no dice qué contiene la lista.
6. "< 1 s en caliente": no define "caliente" ni el protocolo de medición.

## DRY-RUN

Un ejecutor leería `view_doc.py` y los módulos notation, los contratos de GD21/GD23, `api/__init__.py`, `cli/parsers`, `cli/dispatcher`, `serve/routes`, tests y docs; comprobaría que SV01, GD21 y GD23 están en main. Cambios previstos: tipado y validadores pydantic en `view_doc.py`; nuevos módulos `api/views` (`run_view`, secciones); registro del grupo CLI `views`; `views_routes.py` y `routes.py`; tests; docs y CHANGELOG. Dependencias: SV01 en main, GD21, GD23, GO06/GO08/GO09. Validaciones futuras: los `pytest` listados, greps de genericidad y de `register_view_provider`/`computed`, `sldb views run` contra store temporal, medición <1 s, rebase y nota a deskops. Sin ejecutar nada.

## FUTURO

El dueño decide la hipótesis q5 y aprueba o rechaza migrar `params` mapa→lista si aparece uno; el supervisor corre la suite completa y decide revisiones en frío; robocop2 aporta la medición de tiempo; el coordinador poda `files` no usados; deskops recibe la nota de cierre. SV02/DA1 mantiene `/views/projection*` y el punto de extensión.
