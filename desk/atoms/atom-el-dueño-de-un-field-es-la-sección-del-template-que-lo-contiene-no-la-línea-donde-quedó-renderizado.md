---
id: atom-el-dueño-de-un-field-es-la-sección-del-template-que-lo-contiene-no-la-línea-donde-quedó-renderizado
title: El dueño de un field es la sección del template que lo contiene, no la línea
  donde quedó renderizado
five_wh_one_plus: how
tags:
- system:sldb
- topic:ast
- topic:sections
provenance: tests/test_field_ownership.py
---

# El dueño de un field es la sección del template que lo contiene, no la línea donde quedó renderizado

## Answer

Para saber a qué sección pertenece un field, sldb no compara números de línea entre el template y el documento renderizado: una lista expandida, un frontmatter o un valor de varias líneas corren todas las líneas siguientes y hacen que el field caiga en la sección de al lado. La identidad se mapea por estructura: cada heading del template se empareja, en orden, con el heading renderizado en la misma posición, y el field queda dueño de esa sección. Si el template tiene más de una sección y el documento tiene más headings que el template (un valor con markdown adentro inyectó headings), el mapeo se rechaza entero en vez de adivinar: no mapear es mejor que atribuir mal en silencio. Con una sola sección el dueño es único y los headings extra no lo desplazan. La sección cubre su cuerpo hasta el siguiente heading de igual o mayor nivel, y los títulos repetidos reciben rutas deterministas (same, same-2), iguales antes y después de reconstruir el índice.
