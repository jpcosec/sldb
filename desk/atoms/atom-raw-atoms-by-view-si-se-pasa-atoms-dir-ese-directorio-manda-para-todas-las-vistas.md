---
sldb:
  by: agent
  at: '2026-11-20T15:28:06Z'
  authority: generated
  via: create_document
id: atom-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas
title: 'raw_atoms_by_view: si se pasa atoms_dir, ese directorio manda para todas las
  vistas'
five_wh_one_plus: how
tags:
- system:sldb
- topic:matching
---

# raw_atoms_by_view: si se pasa atoms_dir, ese directorio manda para todas las vistas

## Answer

En src/sldb/api/matching/atoms_by_view.py, cuando se pasa atoms_dir, raw_atoms_by_view lee los átomos de ese directorio para todas las vistas. Código en 0f91540d (el commit eb42a49e de la tarea quedó vacío porque otro ejecutor en el mismo checkout se llevó el cambio).
