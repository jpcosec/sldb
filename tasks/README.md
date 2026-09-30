# Tareas · superficie SLDB

| # | Tarea | Estado | Dificultad |
|---|---|---|---|
| [T1](T1-ordenar-espacio.md) | Ordenar el espacio de trabajo | **hecho** | baja |
| [T2](T2-parte-A-segments.md) | Parte A: `/document/segments` en SLDB | a medias (pasos 1-4 de 6) | media |
| [T3](T3-vista-salud.md) | Vista SALUD | **hecho** | baja |
| [T4](T4-vista-bandeja.md) | Vista BANDEJA | **hecho** (parcial, declarado) | media |
| [T5](T5-modo-oscuro.md) | Modo oscuro | **hecho** | trivial |
| [T6](T6-fuga-de-estructura.md) | Ruido estructural: bloquear al registrar | **despachado** (`pi5`) | media |
| [T7](T7-vista-lector.md) | Vista LECTOR (texto → anchors) | **hecho** (parcial, declarado) | alta |
| [T8](T8-identidad-seccion.md) | Identidad de sección / id semántico | pendiente | alta |
| [T9](T9-destilacion-de-modelos.md) | Destilación anchors → modelo | no existe | alta |

## Orden sugerido
T1 y T5 hechos. T6 pasó a ser tarea de SLDB, no de la superficie: el ruido
estructural se bloquea al registrar.
T9 es lo único que requiere diseño nuevo: anchors → regularidad → modelo.

## Lo que ya funciona
- Superficie con 6 vistas (documento, composición, extracción, salud, bandeja, lector)
- Round-trip byte a byte contra la KB real
- Edit-through: editar una pieza compuesta baja al documento de origen
- Procedencia por pieza en el árbol de segmentos
