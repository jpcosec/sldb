---
sldb:
  by: agent
  at: '2026-11-19T10:07:34Z'
  authority: generated
  via: create_document
id: atom-selfdoc-normaliza-el-required-de-los-posicionales-nargs-para-que-la-referencia-no-dependa-del-parche
title: selfdoc normaliza el required de los posicionales nargs=* para que la referencia
  no dependa del parche de python
five_wh_one_plus: how
tags:
- system:sldb
- topic:selfdoc
---

# selfdoc normaliza el required de los posicionales nargs=* para que la referencia no dependa del parche de python

## Answer

Entre parches de python 3.12, argparse cambió el required de un posicional nargs='*' sin default (3.12.3 lo marca True; parches más nuevos, False). selfdoc (src/sldb/selfdoc/arguments.py, _required) lo normaliza a True, que es la regla histórica y la que ya tiene la referencia commiteada. Así 'sldb selfdoc sync' genera la misma referencia en el host y en los contenedores scion, y selfdoc check da 0 en los dos. Los opcionales y los demás posicionales usan action.required tal cual.
