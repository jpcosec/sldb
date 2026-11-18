---
sldb:
  by: agent
  at: '2026-11-18T08:05:33Z'
  authority: generated
  via: create_document
id: atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un
title: stores build --check --keep DIR conserva la copia verificada y el job store
  del CI construye el store una sola vez
five_wh_one_plus: how
tags:
- system:sldb
- topic:ci
- topic:stores
---

# stores build --check --keep DIR conserva la copia verificada y el job store del CI construye el store una sola vez

## Answer

sldb stores build --check reconstruye el store en una copia scratch de las fuentes y la compara con el store local (stores check de la copia, undeclared, missing y filas only local). Con --keep DIR esa copia se construye en DIR (nuevo o vacío) y queda ahí, pase o falle, en DIR más la ruta absoluta del proyecto (el reporte la nombra en kept). Sin --check, --keep es error de uso (rc 2), y un DIR no vacío también da rc 2 sin tocarlo. El veredicto es el mismo con o sin --keep. El job store del CI corre 'sldb stores build --check --keep $RUNNER_TEMP/sldb-built' y después 'sldb selfdoc check' dentro de la copia, así que construye el store una sola vez; antes construía dos veces y el runner cortaba a las 6 h. No hay que reemplazar --check por un build en sitio más git diff: el build en sitio parte de .sldb/core/ versionado y no ve las filas only local que la copia sí detecta. Límite conocido: selfdoc con un --pythonpath relativo que apunta a un symlink fuera del proyecto no resuelve dentro de la copia; el comando del CI no lo usa.
