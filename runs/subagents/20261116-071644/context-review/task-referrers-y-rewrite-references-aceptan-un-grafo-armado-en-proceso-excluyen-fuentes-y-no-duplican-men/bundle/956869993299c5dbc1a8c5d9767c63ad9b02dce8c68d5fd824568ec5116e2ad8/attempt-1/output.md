## REFORMULACION

Propósito: que la API pública de referencias cubra lo que deskops recompone en proceso. Resultado: `referrers(store, target, graph=g)` y `rewrite_references(..., graph=g, excluded_sources=[...])` usan el grafo recibido en vez de `optional_graph`, saltan las fuentes excluidas (campos y menciones) y `find_hits` no devuelve como mention un campo del frontmatter. Repo: sldb (`src/sldb/api/edges/referrers.py`, `rewrite_references.py`; `tests/api/test_referrers.py`, `test_rewrite_references.py`; `CHANGELOG.md`). Límites: no declarar `project_graph` en deskops, no cambiar el formato de `Referrer`, no tocar deskops; el commit y el aviso los gestiona el coordinador/ejecutor según convenciones.

## AMBIGUEDADES

1. "el desk mínimo de la nota armado en tmp_path": la nota de inbox citada en `references` no viene en el bundle; habría que inventar su contenido y la estructura de ese desk mínimo.
2. "descartar las mentions cuya ruta es la de un documento con un hit schema y cuya línea cae dentro del frontmatter de ese documento" frente al Goal "no devuelve como mention una línea del frontmatter que ya es un hit schema": ¿se descarta toda mención del frontmatter de un documento con algún hit schema, o solo la línea coincidente? Obliga a elegir criterio.
3. "con graph devuelve la mención": no se describe cómo construir un `ProjectGraph` en proceso sin declararlo en `store.yaml`; la API de construcción no está en el bundle.
4. La validación nombra solo dos archivos, mientras el ritual de testing pide "the full suite when shared behavior changed"; no se dice si ejecutar la suite completa.

## DRY-RUN

Lecturas: `referrers.py`, `rewrite_references.py`, ambos tests, `CHANGELOG.md`. Cambios previstos: parámetros keyword-only `graph` y `excluded_sources`; paso de `graph` a `find_hits`; resolución de excluidas con `resolve_target` a ruta trackeada y filtrado antes de agrupar campos y menciones; dedupe en `find_hits`; tests H-a/H-b/H-c; entrada de CHANGELOG. Dependencias: `ProjectGraph` y `resolve_target` ya importados/exportados. Validaciones futuras: pytest de los dos archivos; informe en `runs/subagents/<run-dir>/result-summary.md`; sin commit ni push.

## FUTURO

Coordinador: commit con `deskops closeout commit`. Ejecutor: aviso a deskops (o línea en el informe si no está registrado). deskops: declarar `project_graph` y retirar su módulo `references`.
