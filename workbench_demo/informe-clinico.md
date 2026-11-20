---
sldb:
  by: agent:workbench-assistant
  at: '2026-11-17T13:18:30Z'
  authority: authored
  via: save_document_payload
---

# Informe Clínico Levira

Versión: v2.4.1
Fuente: FuenteDoc:acta-comite-01

## Objetivo y Contexto Clínico

El presente informe consolida los criterios clínicos de dosificación y exclusión establecidos por el Comité Central para el ensayo Fase II de Levira.

## Criterios de Selección y Exclusión

- AtomDoc:atom-04
- AtomDoc:atom-05

## Diagrama de Decisión Renal

SpecDoc:decision-renal

## Matriz de Ajuste Basal por Cohorte

| cohorte | imc | ajuste | origen_ref |
| --- | --- | --- | --- |
| Fase II - A | < 18.5 | -25% titulación | AtomDoc:atom-07#cuerpo |
| Fase II - B | 18.5 - 24.9 | 100% dosis nominal | protocolo-std |
| Fase II - C | ≥ 25.0 | Ajuste por sup. corporal | norma-renal-03 |

## Tolerancia y Hallazgos Secundarios

Las pruebas cruzadas de interacción se mantienen bajo bandera de observación preliminar hasta recibir el panel de metabolitos plasmáticos. Los datos de telemetría se reportan con frecuencia cuatrisemanal.
