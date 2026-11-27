# Concilio: Claude

Luhmann, Wittgenstein y Maturana y Varela, de memoria. Del paper, resumen y limitaciones.

## 1. Las fuentes

**Zettelkasten.** Bien descrito, con tres ajustes.
- El identificador de Luhmann no es "independiente del tema": codifica de qué nota cuelga
  (21/3d7), sobre un lugar fijo. "El orden aparece con el uso" es cierto solo a medias.
- No se usó el **registro** (pocos puntos de entrada). Ni lo más cercano: Luhmann construyó una teoría de
  sistemas sociales sobre la autopoiesis, con la **observación de segundo orden**. Une dos de las
  fuentes y explica el principio 6 mejor que Maturana solo.

**Wittgenstein.** Problema serio: son dos filosofías que se contradicen y el texto usa las dos sin
decirlo.
- El Tractatus es atomismo: hechos independientes, el sentido lo fija la forma lógica, la
  proposición es figura del hecho. Las Investigaciones lo desmienten: el sentido es uso. Los
  principios 1 y 3 viven en el primero; el 4 y el 5 en el segundo.
- "De lo que no se puede hablar, mejor callar" trata de ética y de lo místico, no de "decir que no
  se sabe". Para el principio 8 es adorno. La fuente real del "no sé" es mundo abierto contra
  mundo cerrado (Reiter) y la lógica de tres valores.
- No se usó lo mejor: **Sobre la certeza**. Hay proposiciones que se sostienen firmes para poder
  dudar de las demás, y la duda tiene un orden. Es casi el principio 7. Tampoco **seguir una
  regla** (IF §185-242): una regla no fija su propia aplicación. Explica por qué una regla de sldb
  también la declara alguien y se puede revisar.

**Autopoiesis.** El observador está bien atribuido. Falta nombrar *organización* contra
*estructura* (en sldb, modelo contra documentos); ver sección 5.

**El paper.** La fuente más débil para un fundamento.
- Un LLM verbaliza tripletas, otro paso las reconstruye, y se conservan los textos que recuperan
  el grafo para afinar un modelo. Es un método de **datos sintéticos**. Sus límites: 250 grafos de
  Wikipedia, cinco tripletas por sujeto, tripletas planas; jerarquías y logs "quedan por evaluar".
- "La ida y vuelta prueba que el texto dice lo mismo" es demasiado: prueba que **un extractor
  concreto** recuperó el grafo, y filtra a favor de textos fáciles de invertir.
- Sirve solo para la proyección con pérdida. En la exacta, la vuelta es una igualdad.
- Falta la fuente correcta: **lentes y transformaciones bidireccionales** (Foster y otros): `get`,
  `put` y dos leyes (sacar y devolver no cambia nada; cambiar y sacar da lo cambiado). Es edición
  estructural con teoría. Y los **editores proyeccionales** (Teitelbaum; MPS, Hazel).

## 2. Los ocho principios

Con la prueba "sin esto sldb deja de ser sldb":
- Pasan: 1, 2, 3 (reescrito), 6 y 7. El 7 es el más importante.
- No pasan: **4** es consecuencia de 1 y 6; su contenido operativo es "la equivalencia entre cosas
  se declara, no sale del nombre", y eso cabe en 6. **5** es decisión de producto (sin dominio),
  no fundamento. **8** pasa a medias.

**Contradicciones y fricciones.**
- **2 contra el README y contra 3.** El 2 dice "el afuera no manda adentro". El README dice "si
  difieren, manda el archivo". El 3 dice que se edita el nodo y se proyecta al archivo. No pueden
  ser todos verdad sin una regla: *sobre lo observado manda el archivo; sobre sus consecuencias,
  la red; al editar, el cambio se aplica sobre la versión que se vio*. Es lo que resuelve `put` en
  una lente o un merge de tres vías en git. Falta decirlo.
- **1 contra el README:** unidad = hecho, o "un nodo es una cosa". Elegir.
- **5 contra Wittgenstein.** "Parecido de familia" es no tener rasgo común; el 5 define modelo por
  **estructura idéntica** (inducción de conceptos, Ganter y Wille). Solo el eje "por lo que es" lo es.
- **7 junta cuatro cosas:** propagar, grados de certeza, no borrar, que se conserva la red. "No
  borrar" es historia (git); separarlo.

## 3. Lo que falta

**Sostener creencias: sistemas de mantenimiento de verdad** (Doyle 1979; de Kleer) **y revisión
de creencias** (Alchourrón, Gärdenfors, Makinson). Fuente directa del 7: cada creencia lleva su
justificación y, cuando una cae, se revisa lo que dependía de ella y solo eso. Doyle ya tiene
"dentro" y "fuera", que es "no hay" y "no miré". Aporta lo que Maturana no da.

**Qué se recalcula: sistemas de construcción** (Mokhov, Mitchell, Peyton Jones). *Corte
temprano*: si lo recalculado da lo mismo que antes, la propagación se detiene. Es "un cambio no se
lo lleva todo". Caso que decide: se reformatea la función del precio. La huella cambia, el sentido
no. ¿El párrafo queda en duda? Sin respuesta, el 7 no se puede probar.

**En qué se apoya una respuesta: procedencia** (Green y Tannen; PROV del W3C). Da forma al "en qué
se apoya" del 8 y al "quién" del 6.

**Actuar.** Fuente: reglas evento-condición-acción (Widom, Ceri). Tras la corrección de la
sección 5, lo subo a candidato: es la mitad que falta del ciclo. Sigue atado a definir el hook.

## 4. Homoiconicidad

**Es fundante, con otro nombre y con un límite.**

Quítala y queda un grafo con un archivo de configuración al lado: las reglas no tendrían autor (6),
no se podrían sostener ni dudar (7), ni consultar con su apoyo (8). Los principios **valen también
para lo que el sistema hace**. Es consecuencia de ellos, pero hay que decirlo.

El nombre confunde. En Lisp es misma representación **y evaluable**. En sldb las reglas son datos
que interpreta un motor que no es un nodo: reflexión parcial. Propongo **cierre**: lo que el
sistema hace está dicho en la misma red que lo que sabe, y le aplican los mismos principios.

Límite: hay un núcleo que no se dice adentro (el motor, el metamodelo mínimo). Hay que nombrarlo;
sin él el cierre es un autohospedaje sin arranque.

Caso que decide: una regla anclada a la función que la ejecuta. Si esa función cambia, ¿la regla
queda en duda? Si no, es configuración con otro nombre.

## 5. Autopoiesis: hasta dónde

Corrección (JP, tras leer `sesion-2026-11-15.md` y `14-juego-del-lenguaje.md` de kimun): dije que
sldb no se autoproduce y que había que sacar la palabra. Vale para lo que sldb hace hoy, no para
hacia dónde va: todo en un Lisp, donde el sistema se indexa a sí mismo porque sus reglas y modelos
son datos del grafo, con acciones hacia afuera y sobre sí (un harness) y un latido que recalcula
señales. Kimun ya dice que la autopoiesis "aplica al sistema, no a la unidad". La palabra se puede
quedar, con condiciones.

**Criterio.** Hay autoproducción si se cierra un ciclo: un ancla nota un cambio, la red lo baja,
una acción escribe un archivo o un nodo, y ese archivo es fuente de los nodos que sostienen la
acción. Si reglas, modelos, vistas y hooks los escribe siempre una persona, no hay. La pregunta
observable: **¿qué parte de lo declarado la produjo una acción del propio sistema?**

**Condiciones para que no sea abuso:**
- *Un núcleo que ninguna acción edita.* Maturana separa organización (se conserva) de estructura
  (cambia). Un sistema que se reescribe sin organización fija pierde identidad. En el Lisp: el
  evaluador mínimo y el metamodelo. Hay que nombrarlos.
- *Actuar sobre sí pasa por los mismos principios:* tiene autor (6), se sostiene y puede caer (7),
  deja historia. Si no dice quién la disparó, el ciclo es una caja negra.
- *Quién dispara:* el latido y las reglas solos; la persona donde el spec lo diga. Es la pregunta
  abierta del hook, y el cierre depende de ella.

**Sigue siendo abuso** decir "perturbación" donde hay copia: al entrar se copia contenido, y por eso
en lo observado manda el archivo. Y el borde lo traza quien pone un ancla, no la red. "Autopoiético
a nivel de sistema, con borde y núcleo fijados desde afuera" es exacto; "ser vivo" no.

**Veredicto.** Dejar la palabra, atada al criterio, y subir **actuar** a candidato a principio.

## 6. Mi versión

1. **Se sabe en hechos chicos enlazados, con identidad propia.** Un documento los junta y los
   muestra; no es donde viven. (Luhmann, Tractatus.)
2. **Hay una red y hay archivos, y se tocan solo por anclas que recuerdan lo que vieron.** Sobre lo
   observado manda el archivo; sobre sus consecuencias, la red. La huella identifica lo visto; el
   nodo persiste. (Maturana como vocabulario; git.)
3. **Todo lo dicho tiene autor y origen, incluso que dos cosas sean la misma.** Una propuesta de
   máquina no es una declaración. Absorbe el 4. (Luhmann, Maturana, procedencia.)
4. **Un hecho vale por lo que lo sostiene.** Un cambio baja por los apoyos y se detiene donde algo
   más sostiene o donde el resultado no cambia. (TMS, sistemas de construcción, *Sobre la
   certeza*.)
5. **Nada se borra adentro; lo que deja de sostenerse queda dicho.** Aparte del 4: es historia,
   no cálculo. (git.)
6. **Toda respuesta trae su apoyo y su firmeza, y distingue "no hay" de "no miré".** Absorbe el 8.
   (TMS, mundo abierto, procedencia.)
7. **Un texto es una proyección y la vuelta es parte de la definición.** Toda proyección dice qué
   conserva y cómo se comprueba: exacta (igualdad) o con pérdida (medida). Editar por ella exige
   decir sobre qué versión se aplica el cambio. (Lentes; el paper, solo para la pérdida.)
8. **El sistema no trae dominio, y lo que hace, incluso actuar sobre sí, está dicho en la misma
   red que lo que sabe.** Tipos desde lo que entró; reglas, modelos y hooks son nodos y les valen 3
   a 6. Hay un núcleo que ninguna acción edita. Junta el 5 y el cierre.

Pregunta abierta: si el archivo cambió mientras se editaba el nodo, ¿quién gana? Sin respuesta, 2 y 7
se contradicen.
