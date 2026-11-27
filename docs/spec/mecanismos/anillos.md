# Mecanismo: los anillos

Clase de página: mecanismo. Fecha: 2026-11-27. Estado: propuesta del agente sobre los ejes y
anillos que JP fijó; el reparto eje por eje espera su confirmación.

## Regla

Cada anillo importa solo de los de adentro. Las caras llaman a la operación completa (revisar y
escribir), nunca a la escritura sola.

## Reparto

Los nombres de eje son los de `contracts/layers.toml`.

| Anillo | Qué es | Qué entra |
|---|---|---|
| 0a | Texto y árbol, sin store | texto a árbol, nodos de significado y superficie, árbol a texto, lectura de fuentes, lectura de código, errores |
| 0b | El grafo: nodos, cosas adentro, relaciones; los cuatro verbos y la navegación | modelos como declaración, persistencia, codec, identidad y hash como propiedad del nodo, derivar relaciones (índice de aristas, enlaces del texto, DAG de tags), caché, consulta con el lenguaje de predicados, operaciones de documentos, modelos y aristas |
| 1 | Lo que mantiene el grafo correcto | validar contra el modelo, reglas, máquina de estados, detección de mutaciones, anclas (a texto, a código y a un resultado ejecutado), procedencia y política, bitácora y deshacer |
| 2 | El store entero | abrir y diagnosticar, refrescar, migración, catálogo y federación |
| 3 | Lo compuesto | vistas, notaciones, composición de texto, análisis del grafo, similitud y corpus, selfdoc |
| caras | No agregan operaciones | CLI, MCP, HTTP, adaptadores; los avisos de cambio (hooks de git, daemon) |

## Lo que lo sostiene (JP, 2026-11-26 y 27)

- Un documento no necesita modelo para existir. El anillo 0 trabaja con cualquier fuente como
  árbol, Markdown o código, y puede escribirla.
- Una fuente puede cambiar sin pasar por sldb. Por eso la lógica es una sola: se ve un cambio y
  el anillo 1 lo revisa. Cuando escribe sldb, la operación es revisar lo propuesto y escribir, y
  vive en el anillo 1.
- No todo documento se sigue completo. sldb guarda lo que sigue (qué marcó, sus hashes, sus
  relaciones), no una copia de las fuentes; por eso compara hashes y no archivos enteros.

## Persistencia y motor

- El anillo 0b tiene una sola puerta de persistencia y una sola puerta de grafo. Hoy no existen
  como tales.
- Lo que la persistencia guarda es lo propio de sldb: nodos seguidos, hashes, anclajes y
  relaciones. Tiene que poder correr sobre Postgres en el corto plazo (JP).
- Para el grafo se adopta un motor externo sin esperar (JP). Cuál: abierto; la propuesta
  anterior (Cozo con sqlite) no consideraba Postgres.

## Abierto

- Qué motor de grafo, con Postgres como requisito.
- El diseño del ancla a un resultado ejecutado.
