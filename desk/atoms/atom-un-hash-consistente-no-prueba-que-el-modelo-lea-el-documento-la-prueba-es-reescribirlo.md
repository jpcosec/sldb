---
id: atom-un-hash-consistente-no-prueba-que-el-modelo-lea-el-documento-la-prueba-es-reescribirlo
title: 'Un hash consistente no prueba que el modelo lea el documento: la prueba es
  reescribirlo'
five_wh_one_plus: how
tags:
- system:sldb
---

# Un hash consistente no prueba que el modelo lea el documento: la prueba es reescribirlo

## Answer

Los hashes de sldb firman lo que la extracción devolvió; si el modelo no lee un bloque, el hash queda consistente sobre la extracción pobre y todo pasa. La única prueba de que nada se pierde es comparar el documento con render(extract(texto)): cada bloque que no sobrevive es lo que una reescritura borraría (src/sldb/api/documents/rewrite_loss.py). Las secciones que el template llena solo con render/py se regeneran y no cuentan.
