---
sldb:
  by: agent
  at: '2026-11-25T22:23:40Z'
  authority: generated
  via: create_document
id: atom-los-hechos-de-llamada-de-python-traen-sus-argumentos-literales
title: Los hechos de llamada de Python traen sus argumentos literales
five_wh_one_plus: how
tags:
- system:sldb
- topic:py-call-args
---

# Los hechos de llamada de Python traen sus argumentos literales

## Answer

Cada argumento de una llamada de Python, posicional en args o nombrado en kwargs, es {text, value} si ast.literal_eval lo evalúa y {text, literal: false} si no; *x va en args y **x en kwargs.
