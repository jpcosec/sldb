# sldb: piezas del nivel 3

Borrador, sin aprobar. Inventario de las piezas del nivel 3, ordenadas por anillos y
etiquetadas en ejes. Es el paso previo a declararlas como grafo (método aprobado por JP el
2026-11-27). No habla del estado actual.

## Anillos

Cada anillo depende solo de los de adentro.

| Anillo | Qué es |
|---|---|
| 0a | Árboles. Leer cualquier fuente como árbol de partes y volver a escribirla. No necesita grafo. |
| 0b | El grafo. Nodos, relaciones y hechos; consultarlos. Sin nombres. |
| 1 | Lo que mantiene el grafo al día con el afuera y consigo mismo. |
| 2 | El store entero y lo que lo conecta con dónde se guarda. |
| 3 | Lo que se declara encima: todo lo que tiene nombre. |
| Caras | Por dónde se le habla. No agregan nada. |

Un hecho es un hecho venga de donde venga: de algo que se ejecutó, de código, de un archivo de
datos, de texto con forma o de texto libre (JP, 2026-11-27). Por eso todas las formas de leer
una fuente están en el mismo anillo, el 0a, y pesan lo mismo.

## Ejes

Además del anillo, cada pieza lleva:

- **Quién la pone**: el núcleo; la declaración de base que viene con sldb; una librería; o una
  puerta hacia algo que no es sldb.
- **Clase**: estructura, operación, mecanismo, lenguaje o adaptador.
- **Sustrato**: sobre qué trabaja.
- **Etapa**: cuándo interviene (anclar, juntar, sintetizar, consultar, proyectar, editar,
  detectar, propagar, actuar).
- **Principio**: de cuál cuelga (P1 a P8).
- **Estado**: D, decidido por JP; L, lectura del agente; A, abierto.

## Anillo 0a: árboles

| Pieza | Qué es | Quién | Clase | Sustrato | Etapa | P | Est. |
|---|---|---|---|---|---|---|---|
| Árbol de una fuente | La forma única en que se representa una fuente leída: partes dentro de partes. | núcleo | estructura | todos | anclar | 2, 3 | D |
| Gramática de texto con forma | Lee un documento con secciones, campos y listas como árbol. | núcleo | adaptador | texto con forma | anclar | 2 | D |
| Gramática de código | Lee código como árbol. | núcleo | adaptador | código | anclar | 2 | D |
| Gramática de datos | Lee un archivo de datos como árbol. | núcleo | adaptador | datos | anclar | 2 | D |
| Gramática de texto libre | Lee texto sin forma fija: párrafos, frases. | núcleo | adaptador | texto libre | anclar | 2, 5 | L |
| Resultado de una ejecución | Lo que devuelve algo que se ejecutó, leído como una fuente más. | núcleo | adaptador | ejecución | anclar | 2, 4 | A |
| Leer | De una fuente a su árbol. | núcleo | operación | todos | anclar | 2 | D |
| Escribir por la misma estructura | Del árbol a la fuente, tal como estaba. | núcleo | operación | todos | proyectar, editar | 2 | D |
| Dirección de una parte | Cómo se nombra una parte que nadie marcó: por dónde está. | núcleo | estructura | todos | anclar | 3 | D |
| Huella | Marca corta de una parte, calculada con una regla de lectura. | núcleo | operación | todos | anclar, detectar | 3, 7 | D |

## Anillo 0b: el grafo

| Pieza | Qué es | Quién | Clase | Sustrato | Etapa | P | Est. |
|---|---|---|---|---|---|---|---|
| Nodo | Una cosa de la que se sabe algo. Sin clase. Lleva lo que haga falta. | núcleo | estructura | el grafo | todas | 1 | D |
| Relación | Vínculo con tipo entre dos nodos. | núcleo | estructura | el grafo | todas | 1 | D |
| Hecho | Lo que se dice de un nodo o una relación: quién, cómo se supo, cuándo, en qué se apoya. | núcleo | estructura | el grafo | todas | 6 | D |
| Identidad | Lo que hace que un nodo o una relación sea ese y lo siga siendo. | núcleo | estructura | el grafo | todas | 3 | D |
| Store | El contexto dentro del cual valen los nombres. | núcleo | estructura | el grafo | todas | 1 | D |
| Operaciones del grafo | Crear, leer, cambiar y declarar retirado, sobre nodos, relaciones y hechos. | núcleo | operación | el grafo | todas | 1, 7 | L |
| Lenguaje de consultas | Con qué se pregunta y con qué se filtra. Uno solo. | núcleo | lenguaje | el grafo | consultar | 8 | D |
| Condicionales | Decir "si pasa esto". | núcleo | lenguaje | el grafo | consultar, actuar | 4, 8 | A |
| Contrato de persistencia | Lo que el grafo le pide a quien lo guarde. | núcleo | estructura | el grafo | todas | 3 | A |

## Anillo 1: mantener el grafo al día

| Pieza | Qué es | Quién | Clase | Sustrato | Etapa | P | Est. |
|---|---|---|---|---|---|---|---|
| Anclaje | Un nodo atado a una parte de afuera: dónde está, qué se vio, con qué regla se leyó. | núcleo | mecanismo | todos | anclar | 3 | D |
| Detección | Lo que un nodo anclado ejecuta para saber si lo de afuera cambió. | núcleo | mecanismo | todos | detectar | 3, 4 | L |
| Propagación | Bajar un cambio por las relaciones que lo llevan. | núcleo | mecanismo | el grafo | propagar | 7 | A |
| Certeza | Decir de un nodo o una zona si está firme, movida o suelta. | núcleo | mecanismo | el grafo | propagar, consultar | 7, 8 | L |
| Juntar | Reunir anclajes que dicen lo mismo en un "las fuentes dicen". | núcleo | mecanismo | el grafo | juntar | 1 | A |
| Sintetizar | Armar el árbol de conocimiento desde lo que las fuentes dicen. | núcleo | mecanismo | el grafo | sintetizar | 1, 5 | A |
| Proyección | Sacar lo de adentro con reglas dichas: qué conserva y cómo se comprueba. | núcleo | mecanismo | todos | proyectar | 2 | D |
| Edición | Proponer un cambio, comprobarlo, escribirlo sobre la versión vista, mostrar el choque. | núcleo | mecanismo | todos | editar | 2, 7 | D |
| Regla | Algo que tiene que cumplirse, dicho como nodo, y su comprobación. | núcleo | mecanismo | el grafo | editar, consultar | 4 | D |
| Hook | Lo que el sistema hace cuando algo ocurre. | núcleo | mecanismo | ejecución | detectar, actuar | 4 | A |
| Máquina de estados | Estados y pasos permitidos, dichos como nodos, con hooks y condicionales. | base | mecanismo | el grafo | actuar | 4 | D |
| Retirar y limpiar | Declarar que algo ya no va; y, aparte, quitar lo que quedó sin apoyo. | núcleo | mecanismo | el grafo | editar | 7 | D |

## Anillo 2: el store entero

| Pieza | Qué es | Quién | Clase | Sustrato | Etapa | P | Est. |
|---|---|---|---|---|---|---|---|
| Motor de base de datos | Quien guarda el grafo y resuelve las consultas. | puerta | adaptador | el grafo | todas | 3 | L |
| git | La historia de los archivos, y su cambio a nivel de archivo. | puerta | adaptador | todos | detectar | 3, 7 | D |
| Rehacer lo calculado | Borrar y recalcular todo lo que no es declarado ni observado. | núcleo | operación | el grafo | todas | 7 | D |
| Varios stores | Usar nodos de otro store, y decir que dos son el mismo. | núcleo | mecanismo | el grafo | todas | 1 | A |

## Anillo 3: lo que se declara encima

| Pieza | Qué es | Quién | Clase | Sustrato | Etapa | P | Est. |
|---|---|---|---|---|---|---|---|
| Declaración de base | Lo que viene ya declarado con sldb: tipos de relación de uso general, clases comunes. | base | estructura | el grafo | todas | 1, 5 | A |
| Clases de nodo | Nombres para nodos que cumplen un mismo papel. | base | estructura | el grafo | sintetizar | 5 | D |
| Modelo | La forma común de una familia de fuentes; y sus variaciones. | base | estructura | texto con forma, código, datos | anclar, proyectar | 5 | D |
| Tipo por lo que es | Nombres por significado, por papel en el texto o por función. | base | estructura | el grafo | sintetizar | 5 | D |
| Eje y cruce | Una consulta declarada; y la que junta varias. | base | estructura | el grafo | consultar | 5, 8 | D |
| Vista | Una selección declarada para mostrar. | base | estructura | el grafo | proyectar | 2 | L |
| Estructuras de documento | Formas conocidas de textos: reporte, formulario, acta. | librería | estructura | texto | juntar, sintetizar | 5 | D |
| Estructuras semánticas | Formas conocidas de significado: afirmación, requisito, decisión. | librería | estructura | el grafo | sintetizar | 5 | D |
| Patrones de código | Formas conocidas en código: componente, servicio, máquina de estados. | librería | estructura | código | sintetizar | 5 | D |
| Librería | Un paquete de declaraciones para un uso: llevar tareas, describir sistemas. | librería | estructura | el grafo | todas | 5 | D |

## Caras

| Pieza | Qué es | Quién | Clase |
|---|---|---|---|
| Línea de comandos | Hablarle desde una terminal. | puerta | adaptador |
| API | Hablarle desde un programa. | puerta | adaptador |
| MCP | Hablarle desde un agente. | puerta | adaptador |
| REPL | Hablarle en el mismo lenguaje del grafo, en vivo. | puerta | adaptador |

## Lo que muestra el inventario

- **Son 49 piezas.** 10 en el anillo 0a, 9 en el 0b, 12 en el 1, 4 en el 2, 10 en el 3 y 4 caras.
- **Casi todo lo que tiene nombre cayó en el anillo 3**, que es lo esperado con el núcleo limpio.
- **Doce piezas están abiertas.** Ocho se concentran en dos lugares: cómo pasa algo de anclaje a
  conocimiento (juntar, sintetizar), y cómo el sistema se mueve (propagación, hook,
  condicionales, resultado de una ejecución).
- **"Lectura y escritura" de la lista original son seis piezas**: leer, escribir por la misma
  estructura, y cuatro gramáticas.
- **El anclaje quedó en el anillo 1 y no en el 0.** El nodo que lleva un ancla es del 0b; atarlo
  al afuera y vigilarlo necesita además un árbol del 0a. Es una lectura: puede discutirse.

## Dudas de ubicación

1. **El lenguaje de consultas y el motor.** Si el lenguaje de consultas es el del motor de base
   de datos, el anillo 0b depende de una pieza del anillo 2. O el lenguaje es del núcleo y el
   motor lo implementa, o el motor baja al 0b.
2. **Modelo en el anillo 3, pero el anillo 0a lo usa.** Un modelo dice qué tomar al entrar. Si
   leer con modelo es del 0a, el 0a dependería del 3. Lectura: leer sin modelo es del 0a; leer
   con modelo es una operación del 3 que usa al 0a.
3. **Máquina de estados.** La puse en el anillo 1 como declaración de base. Si es solo
   declaración, va en el 3.
4. **Proyección y edición en el anillo 1.** Usan árboles y grafo. Podrían ser del 0 si se
   entienden como la vuelta de "leer".
