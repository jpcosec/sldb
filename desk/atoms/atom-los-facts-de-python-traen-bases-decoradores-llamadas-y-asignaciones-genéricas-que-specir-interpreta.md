---
sldb:
  by: agent
  at: '2026-11-17T08:26:43Z'
  authority: generated
  via: create_document
id: atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta
title: Los facts de Python traen bases, decoradores, llamadas y asignaciones genéricas
  que specIR interpreta
five_wh_one_plus: what
tags:
- system:sldb
- topic:code
provenance: tarea C3 de IR (nota 211648), corrección 2; ejecutor deskops-e-fc2bbe7745a8,
  tester PASA en runs/subagents/20261116-test-k3-c2
---

# Los facts de Python traen bases, decoradores, llamadas y asignaciones genéricas que specIR interpreta

## Answer

sldb.code publica para Python, sin conocer ningún framework: relación extends y attrs.bases en cada clase; attrs.decorators {name, args, kwargs}; relación calls y attrs.calls {name, line} en cada función o método; kind assignment para asignaciones de módulo o de clase (incluida Meta), con attrs.call {func, args, kwargs}, attrs.items o attrs.value, y attrs.op para las aumentadas (+=); kind call para sentencias que son solo una llamada (router.register). Los facts nuevos toman su id en una segunda pasada, así los facts existentes conservan su id. Todo sale por sldb.api.code.code_facts; specIR reconstruye rutas, campos y serializers de Django/DRF sobre estos hechos.
