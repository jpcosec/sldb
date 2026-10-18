---
id: atom-una-regla-de-gitignore-se-evalúa-sin-el-índice-o-un-archivo-trackeado-la-oculta
title: Una regla de .gitignore se evalúa sin el índice, o un archivo trackeado la
  oculta
five_wh_one_plus: how
tags:
- system:sldb
---

# Una regla de .gitignore se evalúa sin el índice, o un archivo trackeado la oculta

## Answer

git check-ignore sobre un archivo ya trackeado dice que no está ignorado aunque una regla lo ignore. Para saber qué dicen las reglas (por ejemplo, que .sldb/core no quede ignorado) se usa git check-ignore --no-index, como en src/sldb/api/stores/gitignore_policy.py.
