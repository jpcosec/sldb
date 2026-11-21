---
sldb:
  by: agent
  at: '2026-11-21T02:47:24Z'
  authority: generated
  via: create_document
id: atom-el-generador-del-golden-de-d2-se-retiro-de-runs-porque-importaba-spec2viz
title: El generador del golden de D2 se retiró de runs/ porque importaba spec2viz
five_wh_one_plus: how
tags:
- system:sldb
- topic:notations
---

# El generador del golden de D2 se retiró de runs/ porque importaba spec2viz

## Answer

runs/subagents/20261116-exec-oraculo-d2/gen_golden.py se borró (cfa6477b): importaba spec2viz y era la única dependencia de sldb que contaba specir retirement check. Un README en esa carpeta dice que generó el golden de D2 de ce0bd384 a partir de spec2viz y que se retiró por el retiro de spec2viz; el golden y tests/notations/test_component_spec_python.py siguen igual. Se avisó a IR.
