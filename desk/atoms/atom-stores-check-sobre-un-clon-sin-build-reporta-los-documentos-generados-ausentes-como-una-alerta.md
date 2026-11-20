---
sldb:
  by: agent
  at: '2026-11-20T16:28:14Z'
  authority: generated
  via: create_document
id: atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta
title: stores check sobre un clon sin build reporta los documentos generados ausentes
  como una alerta
five_wh_one_plus: how
tags:
- system:sldb
- topic:stores
---

# stores check sobre un clon sin build reporta los documentos generados ausentes como una alerta

## Answer

En un clon sin build, los documentos generados que todavía no existen son una alerta de stores check y no un error (store_check.py, store_findings.py, store/diagnostics.py). Código en 0f91540d y CHANGELOG en 07450d10.
