# Tareas · superficie SLDB

| # | Tarea | Estado | Dificultad |
|---|---|---|---|
| [T1](T1-ordenar-espacio.md) | Ordenar el espacio de trabajo | **hecho** | baja |
| [T2](T2-parte-A-segments.md) | Parte A: `/document/segments` en SLDB | a medias (pasos 1-4 de 6) | media |
| [T3](T3-vista-salud.md) | Vista SALUD | pendiente | baja |
| [T4](T4-vista-bandeja.md) | Vista BANDEJA | pendiente | media |
| [T5](T5-modo-oscuro.md) | Modo oscuro | pendiente | trivial |
| [T6](T6-fuga-de-estructura.md) | Fuga de estructura en compuestos | pendiente | media |
| [T7](T7-vista-lector.md) | Vista LECTOR (texto → anchors) | pendiente | alta |
| [T8](T8-identidad-seccion.md) | Identidad de sección / id semántico | pendiente | alta |
| [T9](T9-destilacion-de-modelos.md) | Destilación anchors → modelo | no existe | alta |

## Orden sugerido
T1 desbloquea T3 y T4. T5 es independiente. T6 conviene después de T2.
T7 y T9 son el mismo problema y son lo único que requiere diseño nuevo.

## Lo que ya funciona
- Superficie con 3 vistas (documento, composición, extracción)
- Round-trip byte a byte contra la KB real
- Edit-through: editar una pieza compuesta baja al documento de origen
- Procedencia por pieza en el árbol de segmentos
