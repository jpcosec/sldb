---
sldb:
  by: agent
  at: '2026-11-16T09:38:22Z'
  authority: generated
  via: create_document
id: atom-label-key-de-sldb-api-matching-normaliza-igual-que-normkey-del-catálogo-el-guion-bajo-separa-palabra
title: 'label_key de sldb.api.matching normaliza igual que normKey del catálogo: el
  guion bajo separa palabras'
five_wh_one_plus: what
tags:
- system:sldb
- topic:matching
provenance: src/sldb/api/matching/atom_keys.py
---

# label_key de sldb.api.matching normaliza igual que normKey del catálogo: el guion bajo separa palabras

## Answer

sldb.api.matching.label_key (src/sldb/api/matching/atom_keys.py) convierte en espacio toda secuencia de no-letras-ni-dígitos, guion bajo incluido ([\W_]+), igual que normKey de la plantilla JS del catálogo. Así un elemento sin label cuyo id lleva '_' (post_published) produce la clave 'post published' que el navegador busca. normalize_key no cambia.
