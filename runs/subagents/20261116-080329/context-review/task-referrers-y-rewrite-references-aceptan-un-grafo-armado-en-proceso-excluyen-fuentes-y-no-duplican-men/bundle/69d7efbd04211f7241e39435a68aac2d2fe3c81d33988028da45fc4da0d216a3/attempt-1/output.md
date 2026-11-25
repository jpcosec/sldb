REFORMULACION
Propósito: que `referrers` y `rewrite_references` acepten un `ProjectGraph` armado en proceso, que `rewrite_references` pueda excluir fuentes y que `find_hits` no duplique como mención un campo del frontmatter ya devuelto como schema. Nodo ejecutable `task.code` en el repo sldb. Resultado: firmas con `graph: ProjectGraph | None = None` (keyword-only), `excluded_sources` keyword-only en rewrite, filtrado de fuentes excluidas y dedupe en `find_hits`; tests nuevos en `tests/api/test_referrers.py` y `tests/api/test_rewrite_references.py`, entrada en `CHANGELOG.md`. Límites: no declarar `project_graph` en el `store.yaml` de deskops, no cambiar el formato `Referrer`, no tocar deskops, no hacer push; commit y aviso los gestiona el coordinador.

AMBIGUEDADES
1. “Cada excluded_source se resuelve con resolve_target (el mismo que usa referrers para el target) a un documento trackeado; se compara por ruta trackeada relativa al proyecto”, pero `resolve_target` también acepta “un project node id”. Obliga a inventar si un node id es fuente válida, se rechaza con `SLDBDocumentTargetError` o cómo se compara sin ruta trackeada.
2. “se descarta solo la mención que repite, en el mismo documento y la misma línea del frontmatter, un hit schema” frente a “cuya línea cae dentro del frontmatter de ese documento”. Los hits schema no exponen línea (`location: None`). Obliga a decidir si el dedupe es por línea/campo exacto o por cualquier schema hit del documento, y cómo se asocia el hit a su línea.

DRY-RUN
Lecturas: `referrers.py`, `rewrite_references.py`, tests nombrados, `CHANGELOG.md`, `project_graph.py` y helpers de fixtures. Cambios previstos: añadir `graph` keyword-only a ambas API y pasarlo a `resolve_target`/`find_hits`; añadir `excluded_sources` a rewrite y filtrar campos y menciones por ruta resuelta; deduplicar en `find_hits`; tests H-a, H-b, H-c; changelog. Dependencias: `ProjectGraph`, `resolve_target`, `optional_graph`, `mention_hits`, `schema_hits`, `aggregate_text` y fixtures existentes. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/api/test_referrers.py` y `TMPDIR=/dev/shm pytest -q tests/api/test_rewrite_references.py`, sin ejecutar ahora.

FUTURO
El ejecutor produce `runs/subagents/<run-dir>/result-summary.md`; el coordinador hace el commit con `deskops closeout commit` y envía/registra el aviso a deskops.
