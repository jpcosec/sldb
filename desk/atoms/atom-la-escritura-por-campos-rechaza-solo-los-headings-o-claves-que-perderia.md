---
sldb:
  by: agent
  at: '2026-11-19T14:24:07Z'
  authority: generated
  via: create_document
id: atom-la-escritura-por-campos-rechaza-solo-los-headings-o-claves-que-perderia
title: La escritura por campos rechaza solo los headings o claves que perdería
five_wh_one_plus: how
tags:
- system:sldb
- topic:documents
---

# La escritura por campos rechaza solo los headings o claves que perdería

## Answer

refuse_lossy_overwrite (src/sldb/api/documents/lossy_overwrite.py) recibe el texto que payload_save va a escribir y lo compara con el actual. Rechaza las líneas de heading que el actual tiene más veces que el renderizado (multiconjunto, sin importar el orden) y las claves de frontmatter ausentes en el renderizado. Un heading dentro del valor de un campo, que el render conserva, no bloquea la escritura; un heading no declarado fuera de todo campo, que se perdería, se sigue rechazando con su nombre.
