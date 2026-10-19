---
id: atom-un-log-no-puede-reducirse-a-una-vista-si-el-árbol-que-mira-no-guarda-el-pasado
title: Un log no puede reducirse a una vista si el árbol que mira no guarda el pasado
five_wh_one_plus: why
tags:
- system:sldb
- topic:hashing
- topic:merkle-tree
provenance: docs/architecture/journal-authority.md
---

# Un log no puede reducirse a una vista si el árbol que mira no guarda el pasado

## Answer

El journal de sldb guarda los valores antes y después de cada escritura y los mismos hashes que el árbol Merkle ya calcula: es una segunda fuente de verdad. La salida natural es que el árbol sea la autoridad y el journal una lista de punteros entre raíces, con el diff calculado comparando dos árboles, como git log y git diff sobre el object database. Pero eso solo funciona si el árbol tiene memoria: hoy guarda únicamente los hashes del estado actual, así que los valores del journal son lo único que dice qué cambió. Antes de adelgazar un log hay que decidir dónde vive el pasado (snapshots contenido-direccionados propios, la historia de git, o ninguno); sacarle los valores sin eso borra la historia en vez de moverla.
