---
sldb:
  by: agent
  at: '2026-11-10T04:52:05Z'
  authority: generated
  via: create_document
id: atom-un-store-enlazado-ausente-es-alerta-en-stores-build-y-build-check
title: Un store enlazado ausente es alerta en stores build y build --check
five_wh_one_plus: what
tags:
- system:sldb
- topic:stores
---

# Un store enlazado ausente es alerta en stores build y build --check

## Answer

sldb stores build y stores build --check tratan un link declarado cuyo store no existe como alerta build/link-missing (nombre y ruta) y no como error: apply_links lo salta y build_store lo reporta en links_missing; un link al propio store o un alias inválido siguen siendo error. Así el CI de un repo no depende de tener sus repos hermanos al lado (decisión b, revisable).
