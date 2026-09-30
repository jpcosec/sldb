# Tareas · superficie SLDB

| # | Tarea | Estado | Dificultad |
|---|---|---|---|
| [T1](T1-ordenar-espacio.md) | Ordenar el espacio de trabajo | **hecho** | baja |
| [T2](T2-parte-A-segments.md) | Parte A: `/document/segments` en SLDB | **hecho** | media |
| [T3](T3-vista-salud.md) | Vista SALUD | **hecho** | baja |
| [T4](T4-vista-bandeja.md) | Vista BANDEJA | **hecho** (parcial, declarado) | media |
| [T5](T5-modo-oscuro.md) | Modo oscuro | **hecho** | trivial |
| [T6](T6-fuga-de-estructura.md) | Ruido estructural: bloquear al registrar | **hecho** | media |
| [T7](T7-vista-lector.md) | Vista LECTOR (texto → anchors) | **hecho** (parcial, declarado) | alta |
| [T8](T8-identidad-seccion.md) | Identidad de sección / id semántico | pendiente | alta |
| [T9](T9-destilacion-de-modelos.md) | Destilación anchors → modelo | **hecho** (parcial, declarado) | alta |
| [T10](T10-delete-deja-archivo.md) | `delete` deja el archivo en disco | **hecho** (falta integrar a `tools/sldb`) | — |

## Orden sugerido
T1, T2, T5, T6 y T9 hechos. T6 pasó a ser tarea de SLDB, no de la superficie: el ruido
estructural se bloquea al registrar.
Queda T8 (identidad de sección / id semántico).

## Lo que ya funciona
- Superficie con 7 vistas (documento, composición, extracción, salud, bandeja, lector, destilación)
- Round-trip byte a byte contra la KB real
- Edit-through: editar una pieza compuesta baja al documento de origen
- Procedencia por pieza en el árbol de segmentos
