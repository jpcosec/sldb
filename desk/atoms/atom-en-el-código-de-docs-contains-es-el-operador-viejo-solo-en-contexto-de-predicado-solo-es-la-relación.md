---
sldb:
  by: agent
  at: '2026-11-16T09:12:45Z'
  authority: generated
  via: create_document
id: atom-en-el-código-de-docs-contains-es-el-operador-viejo-solo-en-contexto-de-predicado-solo-es-la-relación
title: En el código de docs/, contains es el operador viejo solo en contexto de predicado;
  solo, es la relación de aristas de contención
five_wh_one_plus: what
tags:
- system:sldb
- topic:rules-language
provenance: tests/store/test_where_retired.py
---

# En el código de docs/, contains es el operador viejo solo en contexto de predicado; solo, es la relación de aristas de contención

## Answer

La guarda de GO10 (tests/store/test_where_retired.py) prohíbe los operadores viejos del lenguaje de consultas en el código de docs/. contains es además el nombre de la relación de aristas de contención (__containment__, sldb edges --relation contains). Por eso contains cuenta como operador viejo solo en forma de predicado (un campo, contains y el inicio de un valor, o la clave contains:), y los otros siete operadores cuentan como palabra entera.
