# sldb: fundamentos

Borrador, sin aprobar. Este es el primero de tres niveles (JP, 2026-11-27):

1. **Fundamentos** (esta página): de dónde viene la idea y los principios que salen de ahí. Es
   lo que, si se quita, sldb deja de ser sldb.
2. **sldb como declaración de sistema**: `README.md`. Qué es el sistema, dicho desde esos
   principios.
3. **Técnicas, capacidades y estructuras de datos**: el resto del spec.

## Las fuentes

De cada una se dice qué se toma. Importa lo que la idea dice, no quién la dijo ni en qué etapa:
no se discute aquí la historia de cada autor. Están descritas de memoria, salvo el paper.

### Wittgenstein

El mundo es la totalidad de los hechos, no de las cosas. Un hecho ya está dentro del espacio
lógico: no es la cosa de afuera, es lo que se puede decir de ella. Una cosa vale por los hechos
en que entra, es decir por sus relaciones. El signo es lo que se ve o se oye; el símbolo es lo
que significa; y el paso de uno a otro no es natural: lo fija un juego con sus reglas. Hay
muchos juegos, y lo que llamamos igual se parece como se parece una familia. Y para poder dudar
de algo hay que dejar firme otra cosa.

- Se toma: hechos y relaciones como lo que hay; signo y símbolo; juegos del lenguaje con sus
  reglas; parecidos de familia; que la certeza tiene un orden.

### Zettelkasten

El fichero de Luhmann. Notas con dirección estable, enlazadas entre sí, con un registro de
pocos puntos de entrada. No se lee de corrido: se le pregunta, y contesta cosas que quien lo
armó ya no recordaba. Importa tanto el lugar de una nota como los caminos por los que se llega
a ella.

- Se toma: unidades con identidad estable; el enlace por sobre la clasificación; puntos de
  entrada; el fichero como algo que se consulta.

### Autopoiesis

De Maturana y Varela. Un sistema es una red con un borde. Lo que le pasa adentro lo determina
su propia estructura: el entorno no le da instrucciones, lo perturba, y el sistema se ajusta
según cómo está hecho. Su organización se conserva mientras su estructura cambia. Y todo lo
dicho es dicho por alguien.

- Se toma: un adentro con topología propia y un afuera; la perturbación que provoca un ajuste
  interno; la organización que se conserva; el observador. Y que el sistema actúa sobre sí
  mismo: sldb se puede usar para observar a sldb y disparar acciones, de modo que una
  perturbación del entorno termine en un ajuste hecho por el propio sistema.

### Una fuente de apoyo: sostener lo que se cree

Doyle y los sistemas que mantienen justificaciones. Cada conclusión guarda en qué se apoya;
puede tener varios apoyos; cuando uno cae se revisa lo que dependía de él, y solo eso. No es
una de las fuentes de origen: se agrega porque dice con precisión cómo opera el principio 7. De ahí sale también que dos
apoyos solo cuentan como dos si son independientes: si los dos dependen de lo mismo, caen
juntos.

### Un ejemplo, no una fuente

Zeinalipour y otros, *From Graph to Text and Back*, ACL 2026. Pasan un grafo a texto, intentan
reconstruir el grafo desde el texto y se quedan con los textos desde los que se recupera. Es un
caso de la idea de signo y símbolo: como el paso entre texto y grafo no es natural, la única
forma de saber si un texto dice lo que el grafo dice es volver.

## Los principios

**1. El valor sale de las relaciones.**
Lo que hay son hechos: nodos y relaciones en un grafo de conocimiento. Un nodo no vale por sí
mismo ni por su nombre; vale por los hechos en que entra. Que dos cosas sean la misma es
también una relación, que alguien declara.
Viene de: Wittgenstein (el mundo son hechos, no cosas) y Zettelkasten (el enlace primero).
Deja afuera: un sistema cuya unidad sea el archivo, y unir cosas porque se llaman igual.

**2. Entre signo y símbolo no hay un paso natural: lo fijan reglas.**
El texto, hablado o escrito, es signo. El grafo de conocimiento es símbolo. La correspondencia
entre los dos es arbitraria: un mismo grafo se dice con muchos textos y un texto admite más de
un grafo. Lo que los une es un juego con sus reglas. Y el grafo tampoco es "la cosa misma": es
también una proyección, como el texto, con otro conjunto de reglas. Cada proyección dice con
qué reglas se hace, y por eso se puede comprobar volviendo.
Viene de: Wittgenstein (signo y símbolo; juegos del lenguaje).
Deja afuera: tratar un texto como si fuera el conocimiento, o el grafo como si fuera la
realidad; y dar por fiel una proyección sin decir sus reglas.

**3. Hay un adentro y un afuera, y el afuera perturba pero no instruye.**
Adentro hay una red con topología propia, y solo ella tiene identidad. Afuera están los
archivos. Se tocan por puntos precisos, las anclas, que son los sensores del sistema. Lo que
pasa afuera perturba; el ajuste lo hace la red, según cómo está enlazada. Qué dice hoy un
archivo lo dice el archivo; qué se sigue de eso lo decide la red.
Viene de: autopoiesis.
Deja afuera: un sistema que es un espejo de los archivos, y uno que exige que todo pase por él.

**4. El sistema actúa, también sobre sí mismo.**
No solo siente. Una perturbación puede terminar en una acción, y esa acción puede caer sobre el
propio sistema: si falta un modelo, se detecta y se corrige; si se mide el desorden, se puede
ordenar. sldb se puede usar para observar a sldb. Para eso lo que el sistema hace tiene que
estar dicho en la misma red que lo que sabe: una regla, un modelo o una acción son nodos como
los demás. Y una acción del sistema es un hecho como cualquier otro: tiene autor, que es quien
declaró la regla que la disparó (principio 6), y se sostiene o cae como los demás (principio 7).
Viene de: autopoiesis.
Deja afuera: un sistema que solo avisa, y reglas o acciones que viven fuera de la red.

**5. Los tipos salen de lo que entró.**
Para entrar no se exige un tipo. Un modelo se puede declarar antes, como cualquier otra cosa,
pero no es la puerta. Lo que comparte estructura es un modelo; lo que la comparte
con diferencias, una variación; especializar da herencia, polimorfismo y composición. Aparte
está lo que algo es, por su significado, su papel o su función, donde las cosas se agrupan por
parecido de familia. Ahí entra también el papel de un hecho: la misma frase puede ser una
observación, un requisito o una decisión, y eso cambia qué pasa cuando deja de calzar. Los dos
ejes no coinciden. Hay textos con mucha forma y textos con casi
ninguna, y no se tratan igual.
Viene de: el principio 1 (el tipo es una relación más) y Wittgenstein (parecidos de familia,
para el eje del significado).
Deja afuera: exigir un tipo antes de aceptar algo, y un solo eje de clasificación.

**6. Todo lo dicho es dicho por alguien.**
Cada hecho tiene autor: una persona, un agente o un cálculo. Registrar algo no lo vuelve
cierto. El sistema no dice qué es verdad; dice qué se afirmó, quién, y en qué se apoya.
Viene de: autopoiesis (el observador).
Deja afuera: hechos sin origen, y un sistema que se presenta como juez.

**7. Saber algo es poder sostenerlo.**
Un hecho vale mientras se mantiene aquello en que se apoya. Cuando un apoyo se mueve, la
consecuencia baja por las relaciones y no se lo lleva todo: algo puede sostenerse por otro
lado. La certeza tiene grados y zonas, y para dudar de una zona hay que dejar firme otra.
Adentro no se borra lo que alguien declaró ni lo que se observó: lo que deja de sostenerse
queda dicho. Lo que el sistema calcula a partir de eso es otra cosa: no tiene autoridad y se
puede rehacer. Se conserva la red; cambia su estado.
Viene de: autopoiesis (la organización se conserva), Wittgenstein (el orden de la certeza), y
la fuente de apoyo (justificaciones).
Deja afuera: lo sabido como vigente o caído, y borrar como forma de corregir.

**8. Se consulta, no se contempla.**
Nadie ve la red entera. Se le pregunta. Una respuesta dice hasta dónde miró, y distingue "no
hay" de "no se miró". Preguntar no cambia la red.
Viene de: Zettelkasten.
Deja afuera: un vacío que puede querer decir dos cosas.

## Lo que no está en este nivel

Van en los niveles 2 y 3:

- **Editar.** Sobre lo observado manda el archivo; sobre las consecuencias, la red. Una edición
  se aplica sobre la versión que se vio, conserva lo ajeno y muestra el choque si lo hay. No es
  fundante (JP, 2026-11-27): lo fundante es la relación entre signo y símbolo; esto es cómo se
  la respeta al escribir. Va en la declaración de sistema.
- **Edición estructural, realización superficial y lentes**: las técnicas con que se pasa de
  árbol a texto y de vuelta, exactas o con pérdida.
- **git**: la historia de los archivos y las huellas para notar cambios.
- **Homoiconicidad**: el nombre técnico de que las instrucciones sean datos. Es lo que hace
  posible el principio 4.
- **Hooks**: la forma concreta de actuar. Sin definir.
- **Consulta por reglas** y **mecanismo genérico y plugins**.

## Discusión

Las críticas del concilio están en `concilio/`. Lo que JP resolvió sobre ellas el 2026-11-27:

- Son hechos y no "afirmaciones": un hecho, en Wittgenstein, ya está dentro del espacio lógico.
- El grafo también es una proyección, otro juego del lenguaje.
- El paper es un ejemplo de una idea, no una fuente.
- Que Wittgenstein sea "dos filosofías que se contradicen" es una lectura errada, y no importa:
  importa lo que la idea dice.
- Actuar es un principio y sale de la autopoiesis.
- Editar no es fundante.

Quedan sin respuesta dos casos que el concilio planteó y que decide el nivel 2 o 3: si
reformatear una función pone en duda lo que se apoyaba en ella; y si una prueba que corrió
sobre la versión anterior de una función cuenta como apoyo independiente de esa función.
