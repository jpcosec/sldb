---
id: atom-lo-que-el-código-dice-de-sí-mismo-se-publica-con-lo-que-no-se-pudo-probar-a-la-vista
title: Lo que el código dice de sí mismo se publica con lo que no se pudo probar a
  la vista
five_wh_one_plus: how
tags:
- system:sldb
---

# Lo que el código dice de sí mismo se publica con lo que no se pudo probar a la vista

## Answer

El adaptador de fuente de sldb publica con lo que encontró también lo que no pudo establecer: declaraciones sin metadata (undeclared), declaradas sin explicación (unexplained), referencias sin resolver (unresolved_references), imports bajo condición (context) o sombreados (shadowed_at) y purposes escritos a mano que difieren del docstring (purpose_conflicts). Nada de eso se adivina ni se descarta en silencio, y un escaneo fallido no reemplaza lo publicado. Spec: docs/architecture/code-docstring-indexing.spec.md.
