---
sldb:
  by: agent
  at: '2026-11-16T11:31:46Z'
  authority: generated
  via: create_document
id: atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
title: referrers y rewrite_references trabajan sobre un grafo armado en proceso, excluyen
  fuentes y no cuentan dos veces un campo del frontmatter
five_wh_one_plus: what
tags:
- system:sldb
- topic:references
provenance: src/sldb/api/edges/referrers.py
---

# referrers y rewrite_references trabajan sobre un grafo armado en proceso, excluyen fuentes y no cuentan dos veces un campo del frontmatter

## Answer

sldb.api.referrers(store, target, *, graph=g) y rewrite_references(..., graph=g, excluded_sources=[...]) usan el ProjectGraph que se les pasa en lugar del declarado en store.yaml. excluded_sources (rutas o Model:name, resueltos con resolve_target) deja esas fuentes intactas, en campos y en menciones. find_hits no devuelve como mención una línea del frontmatter de un documento que ya es hit schema. Así un consumidor como deskops, que arma su grafo en proceso, no tiene que recomponer la reescritura.
