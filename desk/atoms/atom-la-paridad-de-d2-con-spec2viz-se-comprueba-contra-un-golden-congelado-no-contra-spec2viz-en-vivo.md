---
sldb:
  by: agent
  at: '2026-11-16T09:31:17Z'
  authority: generated
  via: create_document
id: atom-la-paridad-de-d2-con-spec2viz-se-comprueba-contra-un-golden-congelado-no-contra-spec2viz-en-vivo
title: La paridad de D2 con spec2viz se comprueba contra un golden congelado, no contra
  spec2viz en vivo
five_wh_one_plus: what
tags:
- system:sldb
- topic:notations
provenance: tests/notations/test_component_spec_python.py
---

# La paridad de D2 con spec2viz se comprueba contra un golden congelado, no contra spec2viz en vivo

## Answer

tests/notations/test_component_spec_python.py compara módulos, clases y aristas defines de component_spec_from_python con tests/notations/goldens/component_spec_python_spec2viz.json, generado una vez con spec2viz.generators.python_ast sobre el mismo TREE (clave _source con el commit de spec2viz). El test no importa spec2viz, así que la paridad sigue comprobándose cuando spec2viz se retire.
