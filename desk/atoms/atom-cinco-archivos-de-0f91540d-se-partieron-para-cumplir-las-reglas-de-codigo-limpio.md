---
sldb:
  by: agent
  at: '2026-11-20T14:43:07Z'
  authority: generated
  via: create_document
id: atom-cinco-archivos-de-0f91540d-se-partieron-para-cumplir-las-reglas-de-codigo-limpio
title: Cinco archivos de 0f91540d se partieron para cumplir las reglas de código limpio
five_wh_one_plus: how
tags:
- system:sldb
- topic:clean-code
---

# Cinco archivos de 0f91540d se partieron para cumplir las reglas de código limpio

## Answer

rule_graph.py, component_spec_graph.py y store_check.py bajaron a 80 líneas efectivas o menos moviendo funciones privadas a módulos hermanos en la misma carpeta; check_on_write (rules_on_write.py) y _diagnose_model (store/diagnostics.py) quedaron en 10 líneas de lógica o menos con auxiliares privadas. Mismo comportamiento: los tests de las cuatro tareas de 0f91540d no cambiaron sus asserts.
