---
sldb:
  by: agent
  at: '2026-11-16T10:51:16Z'
  authority: generated
  via: create_document
id: atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
title: Una extensión de sldb mcp agrega reglas de dominio a la escritura registrando
  validadores de lote, sin reemplazar las herramientas de escritura
five_wh_one_plus: what
tags:
- system:sldb
- topic:mcp
provenance: src/sldb/mcp/extension.py
---

# Una extensión de sldb mcp agrega reglas de dominio a la escritura registrando validadores de lote, sin reemplazar las herramientas de escritura

## Answer

Una extensión de sldb mcp llama context.add_batch_validator(fn), con fn(changes, context) -> list[dict] y cada finding {code, level, what, subject}. WriteTools corre todos los validadores en propose_changes y en apply_changes antes de sellar o aplicar. Si algún finding es de nivel error, responde apply.rejected('domain', ...) con findings y no escribe. Las alertas viajan en domain_alerts sin bloquear. El contrato estable (Extension, BatchValidator, ServerContext.add_batch_validator) está en docs/architecture/mcp.md.
