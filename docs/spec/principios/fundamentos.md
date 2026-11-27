# sldb: fundamentos

Borrador, sin aprobar. Este es el primero de tres niveles (JP, 2026-11-27):

1. **Fundamentos** (esta página): de dónde viene la idea y los principios que salen de ahí. Es
   lo que, si se quita, sldb deja de ser sldb.
2. **sldb como declaración de sistema**: `README.md`. Qué es el sistema, dicho desde esos
   principios.
3. **Técnicas, capacidades y estructuras de datos**: el resto del spec.

## Las cuatro fuentes

De cada una se dice qué se toma y qué no. Las tres primeras están descritas de memoria, sin
releer a sus autores. La cuarta se leyó (resumen, introducción y método).

### Zettelkasten

El fichero de notas de Luhmann. Cada nota tiene una sola idea y un identificador propio que no
depende del tema. Las notas no se ordenan en categorías: se enlazan. El orden no se decide
antes; aparece con el uso. Y el fichero no se lee de corrido: se le pregunta, y contesta cosas
que quien lo armó ya no recordaba haber puesto.

- Se toma: unidades chicas con identidad propia; el enlace por sobre la clasificación; el orden
  como resultado y no como requisito; el fichero como algo que se consulta.
- No se toma: que sea de una sola persona y escrito a mano. En sldb escriben varios, personas y
  agentes, y buena parte de las notas se toma de archivos que ya existen.

### Wittgenstein

Del *Tractatus*: el mundo es la totalidad de los hechos, no de las cosas; una cosa solo tiene
sentido dentro de un hecho; el signo que se ve no es el símbolo que significa; y de lo que no
se puede hablar no se habla. De las *Investigaciones*: el significado de una palabra es su uso
dentro de una práctica; y las cosas que llamamos igual no comparten una esencia, sino parecidos
de familia que se van cruzando.

- Se toma: hechos antes que cosas; el sentido depende del contexto y no del signo; los tipos
  como parecidos de familia; decir que no se sabe cuando no se sabe.
- No se toma: ninguna de sus tesis sobre la lógica o sobre los límites del lenguaje como tales.
  Se usan como criterio de diseño, no como filosofía que sldb tenga que probar.

### Autopoiesis

De Maturana y Varela. Un sistema vivo es una red que se mantiene a sí misma y tiene un borde.
Está cerrado en su operación: lo que le pasa adentro lo determina su propia estructura. El
entorno no le da instrucciones; lo perturba, y el sistema responde según cómo está hecho. La
relación sostenida entre los dos se llama acoplamiento. Su organización, lo que lo hace ser ese
sistema, se conserva mientras su estructura cambia. Y: todo lo dicho es dicho por alguien.

- Se toma: un adentro con topología propia y un afuera; el afuera perturba y no manda dentro;
  el acoplamiento por puntos precisos; la identidad como lo que se conserva; que toda
  afirmación tiene un autor.
- No se toma, o está por verse: que el sistema se produzca a sí mismo. sldb rehace lo que
  calcula y se usa sobre sí mismo, pero no fabrica sus propios componentes. Llamarlo
  autopoiético sería decir de más.

### Del grafo al texto y de vuelta

Zeinalipour y otros, *From Graph to Text and Back: Semantic Fidelity in Automated Industrial
Knowledge Graphs*, ACL 2026, Industry Track. Un texto generado desde un grafo de conocimiento
puede inventar u omitir. Su solución: generar el texto, intentar reconstruir el grafo desde ese
texto, y quedarse solo con los textos desde los que el grafo se recupera. La ida y vuelta es la
prueba de que el texto dice lo mismo que el grafo, y da una medida que calza con el juicio de
expertos.

- Se toma: un texto es una proyección de conocimiento estructurado; una proyección es fiel si
  desde ella se puede volver; la fidelidad se comprueba y se mide, no se supone; y tiene grados.
- No se toma: que la proyección la haga un modelo de lenguaje, ni el entrenamiento con datos
  sintéticos. En sldb una proyección puede ser exacta, cuando se saca por la misma estructura
  con que entró.

## Los principios

Salen de cruzar las cuatro fuentes. Cada uno dice de cuáles viene y qué deja afuera.

**1. Lo que se sabe son hechos enlazados, no documentos.**
La unidad es chica, tiene identidad propia y vale por sus relaciones. Un documento es una forma
de juntar y mostrar hechos, no el lugar donde viven.
Viene de: Wittgenstein (hechos, no cosas) y Zettelkasten (una idea por nota, el enlace primero).
Deja afuera: un sistema cuya unidad sea el archivo.

**2. Hay un adentro y un afuera, y el afuera no manda adentro.**
Adentro hay una red con topología propia, y solo ella tiene identidad. Afuera están los
archivos. Se tocan por puntos precisos, las anclas, que son los sensores del sistema. Lo que
pasa afuera perturba lo de adentro; qué consecuencia tiene lo decide la red, según cómo está
enlazada.
Viene de: autopoiesis (cierre, acoplamiento, perturbación).
Deja afuera: un sistema que es un espejo de los archivos, y uno que exige que todo pase por él.

**3. Un texto es una proyección de lo que se sabe, y es fiel si se puede volver.**
Lo que está adentro se saca como texto de muchas formas. Ninguna es el conocimiento: son
vistas de él. Una proyección vale por lo que permite recuperar. La que saca un documento por la
misma estructura con que entró lo recupera entero.
Viene de: el paper (ida y vuelta como prueba) y Wittgenstein (la proposición como figura de un
hecho).
Deja afuera: tratar un texto generado como fuente, y dar por fiel una proyección sin poder
volver desde ella.

**4. El sentido está en el uso y en el contexto, no en el signo.**
Un nodo significa por sus relaciones dentro de su contexto. Dos nombres iguales no son la misma
cosa. Decir que lo son es un hecho más, que alguien declara.
Viene de: Wittgenstein (signo y símbolo; significado como uso).
Deja afuera: unir cosas porque se llaman igual o porque se parecen.

**5. Los tipos son parecidos de familia: salen de lo que entró.**
No se parte de una lista de tipos. Lo que comparte forma es un modelo; lo que la comparte con
diferencias es una variación; especializar da herencia, polimorfismo y composición. Hay
parecidos por la forma y parecidos por lo que algo es, y no coinciden. Hay textos con mucha
forma y textos con casi ninguna, y no se tratan igual.
Viene de: Wittgenstein (parecidos de familia) y Zettelkasten (el orden aparece con el uso).
Deja afuera: exigir un tipo antes de aceptar algo, y un solo eje de clasificación.

**6. Todo lo dicho es dicho por alguien.**
Cada hecho tiene autor: una persona, un agente o un cálculo. No pesan igual. Registrar algo no
lo vuelve cierto, y lo que propone una máquina es una propuesta hasta que alguien lo declara.
El sistema no dice qué es verdad; dice qué se afirmó, quién, y en qué se apoya.
Viene de: autopoiesis (el observador) y el paper (no confiar en el que genera: comprobar).
Deja afuera: hechos sin origen, y un sistema que se presenta como juez.

**7. Saber algo es poder sostenerlo.**
Un hecho vale mientras se mantiene aquello en que se apoya. Cuando un apoyo se mueve, la
consecuencia baja por las relaciones, y no se lo lleva todo: algo puede sostenerse por otro
lado. Por eso la certeza tiene grados y zonas. Y por eso adentro no se borra: lo que deja de
sostenerse queda dicho, no desaparece. Lo que se conserva es la red; lo que cambia es su estado.
Viene de: autopoiesis (la organización se conserva mientras la estructura cambia) y el paper
(la fidelidad se mide y tiene grados).
Deja afuera: lo sabido como vigente o caído, y borrar como forma de corregir.

**8. Se consulta, no se contempla.**
Nadie ve la red entera. Se le pregunta, y cada respuesta dice qué se sabe, en qué se apoya y
qué tan firme está. Preguntar no la cambia. Lo que no se sabe se contesta como no sabido.
Viene de: Zettelkasten (el fichero como interlocutor) y Wittgenstein (de lo que no se puede
hablar no se habla).
Deja afuera: respuestas que no muestran su apoyo, y un vacío que puede ser "no hay" o "no miré".

## Lo que no está en este nivel

Son necesarios, pero son técnicas o decisiones del sistema, y van en los niveles 2 y 3:

- **Homoiconicidad**: que las instrucciones sean datos, es decir que una regla, un modelo o un
  hook sean nodos como cualquier otro.
- **Edición estructural**: editar el árbol y no el texto.
- **Realización superficial**: la técnica con que un árbol se vuelve texto.
- **git**: la historia de los archivos y las huellas para notar cambios.
- **Revisión de lo que se sostiene y consulta por reglas**: la forma de calcular los principios
  7 y 8.
- **Actuar**: los hooks, lo contrario del sensor. Sin definir.
- **Mecanismo genérico y plugins**: decisión de producto.

## Dudas del agente

- Tomé "las cuatro fuentes" como Zettelkasten, Wittgenstein, autopoiesis y el paper. Si la
  cuarta era otra, los principios 3 y 7 son los que más cambian.
- El principio 6 lo saqué de la frase de Maturana sobre el observador. Calza con lo que JP
  decidió sobre quién declara, pero la atribución a esa fuente es mía.
- Homoiconicidad quedó en técnicas. Si para JP es fundante, se vuelve el noveno principio: lo
  que el sistema hace está dicho en la misma red que lo que el sistema sabe.
