# sldb: criterios

Sin aprobar. Esta página no es un nivel propio: es una herramienta. Toma los ocho principios de
`fundamentos.md` y, para cada uno, dice qué se le pregunta a una pieza de sldb o a una página
del spec, qué caso rechaza, y cómo está hoy el código frente a él. Se lee después de
`fundamentos.md` y de `README.md`.

Usa el ejemplo del whitepaper: un párrafo que dice "el precio incluye el impuesto" y se apoya
en la función que calcula el precio.

"Hoy" tiene tres valores: se cumple, en parte, no se cumple. Lo que dice sobre el código viene
de la lectura de capacidades del 2026-11-27 (`fichas/capacidades.md`, sin commitear) y de la
verificación de las páginas de objeto; no se volvió a comprobar para esta página.

## Cómo se usa

Ante una pieza, una propuesta o una página del spec:

1. ¿De qué principio cuelga? Si de ninguno, o sobra o falta un principio.
2. ¿Algún principio la rechaza?
3. ¿Es de este nivel? Si contesta cómo o dónde, es técnica, y va al resto del spec.

## 1. El valor sale de las relaciones

Se pregunta: ¿esto se puede decir como nodos y relaciones? ¿Lo que hace falta saber de la cosa
está en sus relaciones, o escondido en su nombre o en su archivo?

- Rechaza: que el enlace que el autor escribió dentro del párrafo no aparezca al preguntar por
  las relaciones del párrafo. Hoy: no se cumple; los enlaces del texto van por un camino aparte.
- Rechaza: que una relación solo pueda terminar en un documento entero y no en la función o el
  valor preciso. Hoy: en parte; casi todas terminan en documentos.
- Rechaza: dar por la misma cosa dos etiquetas de dos proyectos porque se llaman igual. Hoy: se
  cumple; la equivalencia se declara.
- Rechaza: tres vocabularios distintos para el tipo de un enlace. Hoy: no se cumple.

## 2. Entre signo y símbolo no hay un paso natural: lo fijan reglas

Se pregunta: ¿esta proyección dice con qué reglas se hace? ¿Qué promete conservar? ¿Cómo se
comprueba?

- Rechaza: tratar la ficha generada de la función como si fuera la función. Hoy: se cumple.
- Rechaza: una proyección que promete devolver el documento como estaba y cambia espacios,
  comentarios u orden. Hoy: en parte; se cumple para documentos con modelo.
- Rechaza: que el código solo se pueda leer y no proyectar de vuelta. Hoy: no se cumple.
- Rechaza: que el código y los documentos entren con reglas tan distintas que sus nodos no se
  puedan relacionar como iguales. Hoy: no se cumple; el código entra como lista de hechos sueltos
  y los documentos como árbol.

## 3. Hay un adentro y un afuera, y el afuera perturba pero no instruye

Se pregunta: ¿esto está adentro o afuera? Si toca las dos cosas, ¿por qué ancla pasa?

- Rechaza: que para seguir el documento de diseño haya que reescribirlo o agregarle algo propio
  de sldb. Hoy: en parte; seguir un documento exige declararlo bajo un modelo.
- Rechaza: que vigilar la función obligue a incorporar el archivo entero. Hoy: en parte.
- Rechaza: tratar una edición hecha con cualquier editor como un daño. Hoy: en parte; se
  detecta cuando se pide.
- Rechaza: que la continuidad de algo dependa de su posición en el archivo. Hoy: no se cumple
  para los ítems de lista, que se nombran por posición.
- Rechaza: salir a buscar a qué se renombró una función para reconectar solo. Hoy: no se
  cumple; con un único candidato se reconecta y se avisa.

## 4. El sistema actúa, también sobre sí mismo

Se pregunta: ¿esta regla, este modelo o esta acción está dicha en la red, o vive en el
programa? ¿Qué la dispara y quién queda como autor?

- Rechaza: que el paso de "propuesto" a "aprobado" dependa de una condición que solo existe
  dentro del programa. Hoy: en parte; hay transiciones sueltas que no pertenecen a ninguna
  máquina de estados declarada.
- Rechaza: una rama de programa por cada norma de diagramas. Hoy: en parte.
- Rechaza: un sistema que solo avisa y nunca puede corregir. Hoy: no se cumple; no hay hooks.
- Rechaza: que una afirmación solo pueda apoyarse en texto y no en el resultado de ejecutar
  algo. Hoy: no se cumple.

Sin definir: qué es un hook (`../abiertos/hooks.md`).

## 5. Los tipos salen de lo que entró

Se pregunta: ¿esto exige un tipo antes de aceptar algo? ¿Mezcla el tipo por la forma con el
tipo por lo que algo es?

- Rechaza: que haga falta inventar un modelo para apoyar el párrafo en una función de un archivo
  nuevo. Hoy: en parte; una función se sigue sin modelo, un documento no.
- Rechaza: que una sección que el modelo no declara se pierda o se trate siempre como error.
  Entra igual; es error solo si el modelo dice que no se admite nada más. Hoy: no se cumple; se
  trata siempre como error.
- Rechaza: que sldb traiga dentro qué es una tarea o una decisión. Hoy: en parte.
- Rechaza: un solo eje de clasificación. Hoy: en parte; existen modelos y etiquetas, como
  mecanismos separados.

## 6. Todo lo dicho es dicho por alguien

Se pregunta: ¿quién lo dijo, y es una observación, una propuesta, una declaración o un cálculo?

- Rechaza: una relación registrada sin autor. Hoy: en parte; los documentos llevan su origen,
  otras escrituras no.
- Rechaza: que dos cálculos de precio queden como equivalentes porque una búsqueda por parecido
  los juntó. Hoy: se cumple; el parecido solo propone.
- Rechaza: que al volver a anclar no quede quién lo hizo ni por qué. Hoy: en parte; el motivo
  no queda guardado.

## 7. Saber algo es poder sostenerlo

Se pregunta: ¿en qué se apoya esto? Si ese apoyo se mueve, ¿qué más se mueve y qué se sostiene
por otro lado?

- Rechaza: mostrar el párrafo como firme después de que la función cambió. Hoy: en parte.
- Rechaza: tratar lo sabido como vigente o caído, sin decir si se sostiene por otro apoyo. Hoy:
  no se cumple.
- Rechaza: que borrar la función borre el párrafo, o que se impida borrarla. Adentro no se
  borra: se declara borrado y la consecuencia baja. Hoy: no se cumple.
- Rechaza: que algo que alguien declaró se pierda al limpiar lo calculado. Hoy: en parte; hay
  relaciones entre etiquetas, declaradas a mano, que hoy se pierden así.
- Rechaza: revisar todo el proyecto por un cambio en una función. Hoy: en parte.

El mínimo viable de esto está propuesto en `../mecanismos/cambio-y-certeza.md`.

## 8. Se consulta, no se contempla

Se pregunta: ¿esta respuesta dice hasta dónde miró? ¿Preguntar cambia algo?

- Rechaza: responder "nada cambió" cuando no había huellas con qué comparar. Hoy: se cumple.
- Rechaza: una lista vacía porque el índice no estaba construido. Hoy: sin comprobar.
- Rechaza: que una consulta arregle por su cuenta lo que encontró. Hoy: en parte.
- Rechaza: elegir en silencio entre dos funciones que calzan con el nombre citado. Hoy: se
  cumple.

## Del nivel 2: editar

No es un principio, pero el whitepaper lo fija y también sirve para revisar.

- Sobre lo observado manda el archivo; sobre las consecuencias manda la red.
- Un cambio se aplica sobre la versión que se vio, conserva lo que otro tocó, y muestra el
  choque si tocaron lo mismo.
- Un cambio pedido a sldb vale o no vale sin importar por qué entrada se pidió: se propone, se
  comprueba, y solo si pasa se escribe. Hoy: no se cumple; hay entradas que escriben sin correr
  las reglas.
- Todo lo que se puede hacer con sldb es una operación suya, y cada entrada solo la expone.
  Hoy: no se cumple; hay programas que leen lo que sldb guarda por dentro porque falta la
  operación.

## La distancia más grande con el sldb de hoy

El sldb de hoy nació como una herramienta para documentos con plantilla. De ahí salen sus
mayores distancias:

1. El código no entra como los documentos (principio 2).
2. Para seguir un documento hay que declararle un modelo antes (principios 3 y 5).
3. Lo sabido es vigente o caído, y borrar borra (principio 7).
4. No hay acciones (principio 4).
5. Hay entradas que escriben sin comprobar (nivel 2).

## Casos que estos criterios no deciden

- Si reformatear la función pone en duda el párrafo. La huella cambia y el sentido no.
- Si una prueba que corrió sobre la versión anterior de la función cuenta como apoyo
  independiente de esa función.
- Qué gana si el archivo cambió en el mismo lugar mientras se editaba el nodo: se muestra el
  choque, pero no está dicho cómo se resuelve.
- Las etapas de un cambio y la medida de certeza más allá del mínimo.
