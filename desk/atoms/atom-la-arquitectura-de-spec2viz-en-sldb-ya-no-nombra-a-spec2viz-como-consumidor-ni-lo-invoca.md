---
sldb:
  by: agent
  at: '2026-11-21T07:27:35Z'
  authority: generated
  via: create_document
id: atom-la-arquitectura-de-spec2viz-en-sldb-ya-no-nombra-a-spec2viz-como-consumidor-ni-lo-invoca
title: La arquitectura de spec2viz en sldb ya no nombra a spec2viz como consumidor
  ni lo invoca
five_wh_one_plus: how
tags:
- system:sldb
- topic:retiro
---

# La arquitectura de spec2viz en sldb ya no nombra a spec2viz como consumidor ni lo invoca

## Answer

contracts/identity.toml deja de listar spec2viz en [surface].consumers, y docs/architecture/spec2viz/python-ast.md y code-docstring-indexing-handoff.md reemplazan las invocaciones de spec2viz por sus equivalentes de sldb (9adfdbce). notations sync --catalog --check da rc 0 y el grep no encuentra invocaciones. El tester dio FALLA solo por la puerta 'identidad' de check.sh --fast por workbench_demo: es la excepción autorizada, con la decisión f055723d pendiente.
