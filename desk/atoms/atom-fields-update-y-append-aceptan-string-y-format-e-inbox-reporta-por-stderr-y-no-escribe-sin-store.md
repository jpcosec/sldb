---
sldb:
  by: agent
  at: '2026-11-19T08:59:28Z'
  authority: generated
  via: create_document
id: atom-fields-update-y-append-aceptan-string-y-format-e-inbox-reporta-por-stderr-y-no-escribe-sin-store
title: fields update y append aceptan --string y --format, e inbox reporta por stderr
  y no escribe sin store
five_wh_one_plus: how
tags:
- system:sldb
- topic:cli
---

# fields update y append aceptan --string y --format, e inbox reporta por stderr y no escribe sin store

## Answer

sldb fields update y fields append aceptan --string, que toma el valor literal sin interpretarlo como YAML (un texto con ': ' ya no falla), y --format json|text|yaml para la salida; los dos flags son independientes. sldb inbox --show de una nota inexistente escribe el error por stderr y sale con 1. sldb inbox con un --store que no contiene .sldb falla con un error que lo dice, sale con 1 y no crea ningún archivo ni directorio.
