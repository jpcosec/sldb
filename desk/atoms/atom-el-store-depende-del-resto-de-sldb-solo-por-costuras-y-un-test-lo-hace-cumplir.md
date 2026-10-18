---
id: atom-el-store-depende-del-resto-de-sldb-solo-por-costuras-y-un-test-lo-hace-cumplir
title: El store depende del resto de sldb solo por costuras, y un test lo hace cumplir
five_wh_one_plus: how
tags:
- system:sldb
---

# El store depende del resto de sldb solo por costuras, y un test lo hace cumplir

## Answer

src/sldb/store importa sldb.core, sldb.models y sldb.runtime solo desde store/exceptions.py (errores), store/runtime_codec.py (extracción) y store/model_contract.py (lo que declara una clase de modelo y los relation types builtin), y nunca importa api, cli ni selfdoc; tests/test_store_seams.py falla si alguien importa directo. Un import nuevo hacia otra capa se agrega a la costura que corresponde, no al módulo que lo necesita: así un store empaquetado aparte reemplaza solo esas tres.
