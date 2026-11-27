# sldb: principios

Estado: **borrador 5, sin aprobar**. Este documento dice qué es sldb y por qué. No dice cómo está
construido ni dónde vive cada pieza: eso es el resto del spec, y cada página del spec tiene que
poder colgarse de una proposición de aquí. La evidencia de cada proposición está aparte, en
`evidencia.md`.

## El problema

Lo que un proyecto sabe está escrito en sus archivos: documentos, código, interfaces de programa.
Esos archivos hablan unos de otros. Un documento de diseño afirma algo sobre una función; una
tarea cita una decisión; una decisión se apoya en un párrafo de otro documento.

A ese conocimiento no se le puede preguntar nada. No se puede pedir "todo lo que se apoya en esta
función", ni "las decisiones que nadie ha revisado", ni comprobar que una regla del proyecto se
cumple. Y cuando un archivo cambia, nada señala qué otras cosas hablaban de él.

La salida habitual es copiar ese conocimiento a una base de datos y trabajar ahí. Entonces hay
dos versiones, la del archivo y la de la base, y terminan diciendo cosas distintas.

## La idea

**Un archivo con estructura ya es dato. Se puede tratar como dato sin sacarlo de su archivo.**

## Qué es sldb

**sldb representa las partes de las fuentes de un proyecto para poder consultarlas, relacionarlas,
comprobarlas y modificarlas, mientras las fuentes siguen siendo archivos comunes; y hace visible
cuándo cambió aquello en que una afirmación se apoyaba.**

Para quién: para las personas y los agentes que trabajan sobre un mismo proyecto. Cada uno tiene
que poder comprobar en qué se apoya lo que el otro escribió, sin tener que creerle.

Lo que sldb no es:

- No es la base de datos donde viven los documentos. La realidad está en los archivos.
- No es una herramienta de Markdown. Markdown es una de las formas en que llega una fuente.
- No es un conversor de formatos ni un generador de documentación. Puede generar textos a
  partir de lo que sabe, pero eso es una consecuencia, no su función.
- No es un juez de la verdad. Dice si lo registrado es consistente y si su soporte cambió; no
  dice si es cierto.
- No es un control de versiones. Ese dice qué líneas de qué archivo cambiaron; sldb dice qué
  otras cosas dependían de lo que cambió.
- No es un buscador de texto. Un buscador encuentra palabras parecidas; sldb responde por
  relaciones que alguien declaró o que salen de la estructura.

## Para qué se usa

Tres usos que existen hoy sobre sldb. Ninguno es parte de sldb: cada uno es contenido que un
proyecto declara encima (proposición 8).

- **Llevar el trabajo de un proyecto.** Cada tarea es un documento con un modelo: título,
  estado, a qué decisión responde. Las reglas del equipo ("una tarea no se cierra sin pruebas")
  se declaran como dato y se comprueban al escribir. El tablero de tareas no se escribe a mano:
  se genera. sldb no sabe qué es una tarea; sabe comprobar documentos contra un modelo y contra
  reglas.
- **Describir un sistema y dibujarlo.** Los componentes de un sistema y sus conexiones se
  declaran como partes y relaciones. Una vista dice qué partes mostrar, y una notación dice con
  qué figura se dibuja cada clase de parte. sldb no dibuja: entrega la vista resuelta y otro
  programa la muestra. Agregar una norma de diagramas es declarar una notación, no programar.
- **Mantener al día lo que se dice del código.** Las funciones y clases del código se siguen
  como partes. Un documento puede apoyarse en una de ellas con un ancla, y cuando el código
  cambia se sabe qué documentos hay que revisar. Es el ejemplo de abajo.

## Palabras

- **Estructura**: lo que un programa puede leer de un archivo siempre igual, sin interpretar:
  sus secciones, sus campos, sus funciones. Un texto corrido sin divisiones casi no la tiene.
- **Fuente**: un archivo del proyecto con estructura: un documento, código, la interfaz de un
  programa.
- **Parte**: una unidad dentro de la estructura de una fuente: una sección, un párrafo, un valor,
  una función.
- **Relación**: un vínculo con tipo entre dos partes ("se apoya en", "contiene", "trata de").
- **Seguir** una parte: registrarla para poder consultarla y saber si cambia.
- **Declarar**: que una persona o un agente escriba algo que ninguna fuente dice por sí sola
  (una relación, una regla), quedando registrado quién lo escribió.
- **Afirmación**: una parte que dice algo sobre otra cosa, como el párrafo del ejemplo.
- **Vista**: una selección declarada de partes y relaciones, para mostrarlas.
- **Modelo**: la estructura común de una familia de fuentes; por ejemplo, la que comparten todos
  los documentos de decisión.
- **Huella**: una marca corta calculada de lo que se observa en una parte; si lo observado
  cambia, la marca cambia.
- **Soporte**: aquello en que una afirmación se apoya.
- **Ancla**: una relación "se apoya en" que además recuerda lo que vio de su soporte.
- **Store**: lo que sldb registra de un conjunto de fuentes. Un proyecto puede tener uno o
  varios, y uno puede referirse a partes de otro.
- **Vía**: cada forma de pedirle algo a sldb (una línea de comandos, un servicio, un editor).

## El ejemplo

Un proyecto tiene una función que calcula un precio, y un documento de diseño con un párrafo que
dice: "el precio incluye el impuesto". Alguien declara que ese párrafo se apoya en esa función.

Mañana alguien cambia la función. El párrafo sigue escrito igual. ¿Sigue describiendo lo que la
función hace? Puede que sí: quizá solo la ordenaron. sldb no lo sabe y no lo decide. Lo que hace
es señalar el párrafo para que alguien lo revise, y si la función desapareció, señalar que el
párrafo perdió su soporte.

Casi todas las proposiciones se muestran sobre este ejemplo.

El diagrama muestra el ejemplo: arriba las fuentes, que son la realidad; abajo lo que sldb
registra de ellas, en sus tres clases (proposición 5). Se genera de
`diagramas/component.ejemplo.yml`; no se edita a mano.

```mermaid
---
config:
  layout: elk
  flowchart:
    curve: linear
---
%% specir: generated from docs/spec/principios/diagramas/component.ejemplo.yml; do not edit, run `sldb notations validate docs/spec/principios/diagramas/component.ejemplo.yml` and re-render
flowchart TD
    subgraph Proyecto ["Fuentes del proyecto (la realidad)"]
        subgraph Documento ["Documento de diseño"]
            Parrafo["Párrafo: el precio incluye el impuesto"]
        end
        subgraph Codigo ["Archivo de código"]
            Funcion["Función que calcula el precio"]
        end
    end
    subgraph Store ["Store (lo que sldb registra)"]
        Declarado["Declarado: el ancla «se apoya en». Responde quien la declaró"]
        Observado["Observado: la huella de la función. Sirve para comparar"]
        Calculado["Calculado: índices y resultados. Se puede borrar y rehacer"]
    end
    Parrafo -->|"se apoya en"| Funcion
    Declarado -->|"sigue"| Parrafo
    Observado -->|"lo que vio"| Funcion
    Calculado -->|"se rehace desde"| Declarado
```

## Las proposiciones

Las proposiciones 1.1, 1.2 y 1.3 comentan a la 1, y así en cada grupo. Cada una trae su **por qué**, que sirve para decidir un caso
no previsto; un caso que **rechaza**; y si **hoy** se cumple (se cumple, en parte, no se cumple).
El documento dice cómo tiene que ser; muchas no se cumplen todavía. Las marcadas **(candidato)**
vienen de un contrato del repo o de la lectura de un agente, sin confirmación del dueño.

---

### 1. Las fuentes se quedan donde están

**1.** La realidad está en las fuentes. sldb las observa y no les exige nada más que tener
estructura.

- Por qué: un proyecto tiene que poder dejar de usar sldb, o no usarlo en una parte, sin perder
  nada suyo.
- Rechaza: que para seguir el documento de diseño haya que reescribirlo o agregarle algo propio
  de sldb.
- Hoy: en parte. Seguir un documento todavía exige declararlo bajo un modelo.

**1.1.** Documentos, código e interfaces son, para sldb, lo mismo: fuentes con partes, dentro de
una sola representación.

- Por qué: lo útil es poder relacionar el párrafo con la función y consultarlos juntos. Si cada
  clase de fuente se representa distinto, esa relación une dos cosas que no se parecen.
- Rechaza: que la función cuente como representada porque se generó un documento que la
  describe.
- Hoy: no se cumple. Los documentos se representan como árbol de partes; el código, como una
  lista de hechos sueltos.

**1.2.** Seguir es elegir. Para vigilar el cálculo del impuesto basta elegir esa parte. Lo que no
se eligió queda en su archivo.

- Por qué: casi nunca interesa un archivo entero; interesa la función o el párrafo del que algo
  depende. Y para saber si una parte cambió basta su huella: no hace falta guardar su contenido.
- Rechaza: que vigilar la función obligue a incorporar o copiar el archivo completo.
- Hoy: en parte. Se siguen valores y funciones sueltas; un documento seguido se sigue completo.
- Nota: por defecto sldb no guarda el contenido. Tendrá que poder conservar una fuente entera,
  parte por parte, cuando alguien lo pida. Eso no contradice esta proposición ni la 5: es una
  elección de quien sigue, y la copia nunca manda sobre la fuente.

**1.3.** Cuando una fuente admite edición, un cambio pedido sobre una de sus partes se escribe en
la fuente misma. Para eso sldb vuelve a leer la fuente: no edita una copia.

- Por qué: si un cambio solo se puede hacer por fuera, sldb es un espejo, y quien trabaja termina
  usando dos herramientas que no se conocen.
- Rechaza: que regenerar la documentación de la función cuente como haber editado la función.
- Hoy: en parte. Se editan documentos con modelo; el código no.
- Abierto: A3.

### 2. Las partes forman un grafo que se puede consultar

**2.** Todo lo que sldb registra se expresa con dos cosas: partes y relaciones con tipo entre
ellas. Un modelo, una regla o un ancla también son partes o relaciones. Una parte vale por sus
relaciones.

- Por qué: lo que se quiere saber de un proyecto es casi siempre qué tiene que ver con qué.
- Rechaza: tratar el documento de diseño como un registro aislado cuyos vínculos son solo texto.
- Hoy: en parte. Las relaciones existen, pero el centro del sistema es el documento con su
  modelo.

**2.1.** Una parte puede contener otras. Lo que tiene adentro, sus propiedades y los enlaces
escritos en su texto son también relaciones.

- Por qué: quien pregunta en qué se apoya el párrafo tiene que recibir todo, incluido el enlace
  que su autor escribió dentro del texto.
- Rechaza: una respuesta a "qué relaciones tiene este párrafo" que omite los enlaces de su texto.
- Hoy: no se cumple. Los enlaces del texto no aparecen junto a las demás relaciones.

**2.2.** Una relación apunta a la parte precisa de la que trata, y la sigue encontrando aunque el
archivo se mueva o cambie el orden de sus hermanas.

- Por qué: si un nombre cambia cuando se mueve un archivo o se inserta un ítem, se rompen las
  relaciones que lo usaban sin que nada haya cambiado de verdad.
- Rechaza: que el párrafo solo pueda apoyarse en "el archivo de precios" y no en la función.
  Rechaza que, al insertar un ítem en una lista, la referencia al tercero pase a nombrar otro.
- Hoy: en parte. Casi todas las relaciones terminan en documentos enteros, y los ítems de lista
  se nombran por posición.
- Abierto: A1. Esta proposición promete algo que todavía no se sabe cómo cumplir sin escribir
  nada en el archivo (proposición 1).

**2.3.** Se puede preguntar por lo que dice una parte y por lo que se desprende de varias
relaciones juntas. **(candidato)**

- Por qué: hay cosas que ningún archivo dice y que el conjunto implica. Si dos documentos se
  justifican el uno al otro en círculo, eso importa aunque ninguno lo mencione.
- Rechaza: que para saber qué depende de la función del precio haya que reconstruir las
  relaciones fuera de sldb.
- Hoy: se cumple para las relaciones registradas.

**2.4.** Ningún nombre vale en todas partes: vale en su store. Que dos nombres se escriban igual
no los hace la misma cosa; decir que lo son es una declaración que alguien hace.

- Por qué: dos proyectos usan la misma palabra para cosas distintas. Unirlas por coincidencia
  fabrica relaciones que nadie afirmó.
- Rechaza: concluir que dos proyectos hablan del mismo "precio" porque los dos usan esa palabra.
- Hoy: se cumple.

### 3. Lo que una parte dice no es cómo está escrita

**3.** El significado de una parte y su forma escrita se mantienen separados y vinculados.
**(candidato)**

- Por qué: las preguntas son sobre lo que el párrafo afirma, no sobre cómo está redactado. Sin
  esa separación, sldb sería un lector de formatos.
- Rechaza: que el dato "tasa: 19 %" deje de encontrarse porque alguien lo pasó de una lista a
  una tabla.
- Hoy: en parte. Existe para documentos; para código no.

**3.1.** Leer una fuente por su estructura y comprobarla contra un modelo son dos pasos. El
modelo describe una familia de fuentes; no es requisito para observar una.

- Por qué: exigir modelo antes de leer deja fuera lo que todavía no se entiende, que es lo que
  más conviene poder mirar.
- Rechaza: que haga falta inventar un modelo para poder apoyar el párrafo en una función de un
  archivo nuevo.
- Hoy: en parte. Una función se sigue sin modelo; un documento todavía lo exige.
- Abierto: A2 y A4.

**3.2.** Desde lo que se sabe se pueden generar otras expresiones: una ficha de la función, una
vista, los datos de un diagrama. Lo generado remite a aquello de donde salió, y no se corrige ni se repite a
mano.

- Por qué: un texto generado que alguien edita a mano es una segunda versión; y uno escrito a
  mano que se pudo generar, también.
- Rechaza: dar por corregida la función porque alguien editó la ficha generada de ella. Rechaza
  mantener a mano una lista de las funciones del proyecto.
- Hoy: en parte.

### 4. Anclar es fundamentar

**4.** Un ancla une una afirmación con aquello en que se apoya, y guarda lo que vio de ese
soporte, para comprobar después si sigue diciendo lo mismo.

- Por qué: si solo se guarda el nombre de la función, mañana se la puede encontrar, pero no se
  puede saber si dice lo mismo que cuando se la citó.
- Rechaza: tratar como ancla un enlace que apunta a la función sin recordar qué decía.
- Hoy: se cumple.

**4.1.** El soporte puede ser una parte de una fuente o el resultado de ejecutar algo. El
resultado se registra como una parte más, con su huella.

- Por qué: muchas afirmaciones se apoyan en un resultado: "la prueba del precio pasa".
- Rechaza: que lo único anclable sea texto escrito.
- Hoy: en parte. Se ancla la función; no el resultado de ejecutarla.
- Abierto: A7.

**4.2.** La huella sirve para saber si lo observado cambió. No dice qué significa una parte, no
prueba que dos partes sean equivalentes y no es su nombre.

- Por qué: si una parte se nombrara por su huella, cada edición crearía una parte nueva y se
  perdería lo que se quería seguir. Y si cada cambio de espacios contara como cambio, los avisos
  dejarían de leerse.
- Rechaza: que la función pase a ser "otra" cada vez que se edita. Rechaza marcar el párrafo
  para revisión porque cambió la sangría de la función.
- Hoy: se cumple.

### 5. La fuente manda; lo que sldb calcula, no

El store no es una segunda versión de las fuentes. Tiene tres clases de cosas, y cada una
responde distinto: lo que alguien **declaró** sobre las fuentes y ninguna fuente dice (responde
quien lo declaró); lo que sldb **observó** de una parte en un momento, como su huella (sirve
para comparar); y lo que sldb **calculó** (no responde por nada: se puede rehacer).

**5.** Entre una fuente y lo que sldb calculó de ella, manda la fuente. Entre lo que alguien
declaró y el resumen que sldb hizo de eso, manda lo declarado.

- Por qué: lo calculado puede estar atrasado o mal calculado. Si manda, un error de cálculo se
  vuelve un hecho.
- Rechaza: que un índice atrasado decida que el párrafo no se apoya en nada.
- Hoy: en parte (ver 5.2).

**5.1.** Una fuente puede cambiar sin pasar por sldb, y eso es normal: es un cambio que hay que
ver, no un daño.

- Por qué: los archivos se editan con cualquier herramienta. Un sistema que solo funciona si todo
  pasa por él deja de funcionar el primer día.
- Rechaza: que editar la función con un editor cualquiera deje el párrafo sin marcar para
  revisión.
- Hoy: en parte. Los cambios de afuera se detectan cuando se pide.

**5.2.** Todo lo que se puede recalcular se puede borrar sin perder nada. Lo declarado y lo
observado no se pueden recalcular, así que no pueden vivir solo en algo que se borra.

- Por qué: es la forma de saber qué es dato y qué es cálculo. Si borrar el cálculo pierde algo,
  eso no era cálculo.
- Rechaza: que la declaración "este párrafo trata de impuestos", o la huella que el ancla
  guardó de la función, se pierdan al limpiar lo calculado.
- Hoy: en parte. Hay declaraciones de ese tipo que hoy se pierden así.

**5.3.** Quien lee tiene que poder distinguir qué declaró alguien, qué decía la fuente y qué
calculó sldb. Registrar una afirmación no la vuelve cierta. Una persona o un agente pueden
declarar, y queda escrito quién fue; un parecido encontrado por un cálculo no es una relación
hasta que alguien la declara. **(candidato en lo último)**

- Por qué: en un proyecto escriben personas, programas y modelos de lenguaje. Sin origen, lo que
  afirmó una persona y lo que supuso una máquina pesan igual.
- Rechaza: que dos cálculos de precio queden registrados como equivalentes porque una búsqueda
  por parecido los juntó.
- Hoy: en parte. Los documentos llevan su origen; otras escrituras no.

### 6. Todo cambio se ve y nada se pierde

**6.** Cuando cambia el soporte de una afirmación, sldb muestra qué quedó por revisar, y solo
eso.

- Por qué: quien depende del párrafo necesita saber que perdió soporte. Y si cada cambio obliga
  a revisar todo, nadie revisa nada.
- Rechaza: mostrar el párrafo como vigente después de que la función cambió o desapareció.
- Hoy: en parte. No todas las vías de cambio revisan lo que dependía de lo cambiado.
- Nota: "quedó por revisar" no se guarda. Se calcula cada vez, comparando la huella guardada
  con la fuente de ahora. Por eso mostrarlo no contradice la proposición 6.3.

**6.1.** Nunca se pierde un dato, salvo que se pida de forma explícita. Borrar algo de lo que
otras cosas dependen no las borra ni se rechaza: se borra lo pedido y lo que dependía queda
marcado como sin soporte.

- Por qué: borrar en cascada pierde lo que nadie pidió perder; negarse a borrar obliga a
  deshacer a mano todo lo demás. Las dos esconden la consecuencia; marcar la muestra.
- Rechaza: que borrar la función borre el párrafo. Rechaza que se impida borrar la función
  porque el párrafo existe.
- Hoy: no se cumple.

**6.2.** Nada se oculta. Que una fuente se movió respecto de lo registrado es un aviso; que algo
está roto o incumple lo declarado es un error; lo que no se sabe se dice que no se sabe.
**(candidato en lo último)**

- Por qué: quien recibe una respuesta vacía no distingue "no hay nada" de "no pude mirar".
- Rechaza: responder "nada cambió" cuando no había huellas con qué comparar. Rechaza elegir en
  silencio entre dos funciones que calzan con el nombre citado.
- Hoy: se cumple, salvo lo abierto en A5.

**6.3.** Leer no escribe. Una consulta no modifica lo registrado ni lo arregla por su cuenta.
**(candidato)**

- Por qué: si preguntar cambia la respuesta, dos que preguntan lo mismo no ven lo mismo.
- Rechaza: que preguntar qué se apoya en la función modifique lo registrado.
- Hoy: en parte.

**6.4.** Revisar es declarar. Quien revisa el párrafo confirma que sigue valiendo o lo corrige;
el ancla toma entonces la huella nueva, y queda escrito quién revisó y por qué. **(candidato)**

- Por qué: sin eso el aviso no se apaga nunca, o se apaga sin que nadie haya mirado.
- Rechaza: que un ancla vuelva a darse por vigente sin que quede quién lo decidió.
- Hoy: en parte. Se puede volver a anclar; el motivo no queda guardado.

### 7. Lo que tiene que cumplirse se declara y se comprueba

**7.** Lo que un proyecto exige de sus fuentes se declara como dato, con el mismo mecanismo que
todo lo demás: reglas, estados válidos, vistas.

- Por qué: lo declarado como dato lo pueden leer, comprobar y relacionar todos. Un
  comportamiento escondido dentro de un programa solo se conoce ejecutándolo.
- Rechaza: que el paso del párrafo de "propuesto" a "aprobado" esté permitido por una condición
  que solo existe dentro del programa y que nadie puede consultar.
- Hoy: en parte.

**7.1.** Un cambio pedido a sldb vale o no vale, sin importar por qué vía se pidió: se propone,
se comprueba, y solo si pasa se escribe. Un cambio hecho por fuera no pasa por aquí: se ve
después (5.1), y si incumple una regla aparece como error (6.2).

- Por qué: si una vía comprueba y otra no, la regla es opcional. Y comprobar después de escribir
  deja el error adentro.
- Rechaza: que un cambio rechazado por una vía se pueda hacer por otra. Rechaza guardar una
  relación inválida y avisar después.
- Hoy: no se cumple. Hay vías de escritura que no corren las reglas.

**7.2.** Todo lo que se puede hacer con sldb es una operación suya, y cada vía de acceso solo la
expone.

- Por qué: si algo existe solo en una vía, quien usa otra tiene que imitarla o leer lo que sldb
  guarda por dentro, que cambia sin aviso.
- Rechaza: que otro programa lea directamente lo que sldb guarda porque falta la operación para
  pedirlo.
- Hoy: no se cumple.

### 8. Un mecanismo para cualquier proyecto

**8.** sldb tiene los mecanismos; cada proyecto trae su contenido. Lo que le sirve a cualquier
proyecto es de sldb. Lo que es de un dominio lo declara quien lo usa, encima.

- Por qué: un mecanismo que conoce a su primer usuario deja de servir para el segundo.
- Rechaza: que sldb traiga dentro qué es una tarea para un proyecto, una rama de programa por
  cada norma de diagramas, o nombres de carpetas del proyecto donde se desarrolla.
- Hoy: en parte. Todavía hay contenido de dominio dentro de sldb.

---

## Cómo se usa este documento para juzgar algo

Ante una pieza de sldb, una propuesta o una página del spec:

1. **¿De qué proposición cuelga?** Si de ninguna, o sobra o falta un principio.
2. **¿Alguna proposición la rechaza?** Los casos de "Rechaza" son ejemplos; el "Por qué" es lo
   que decide un caso nuevo.
3. **¿Es un qué o un por qué, o es un cómo o un dónde?** Lo primero va aquí; lo segundo, al resto
   del spec.

No son principios, aunque sean decisiones tomadas: en qué lenguaje está escrito, en qué motor se
guarda, cómo se calculan las huellas, en qué capas se ordena el código, qué comandos existen.
Tienen que poder cambiar sin que cambie nada de este documento.

## Lo que este documento no decide

Puntos donde los antecedentes dicen cosas distintas y solo el dueño puede cerrar. Mientras estén
abiertos, las proposiciones que tocan valen en lo que no dependa de ellos.

- A1. **Qué hace que una parte siga siendo la misma** (toca 2.2 y 4.2). Si se reordena una lista o
   se renombra la función, ¿qué permite afirmar que es la misma parte de antes? Se sabe que no es
   su huella ni su posición.
- A2. **Qué se puede hacer con una fuente sin modelo** (toca 3.1). Se puede observar el párrafo
   antes de darle un modelo. Al registrarlo, ¿pertenece igual a alguna clase general, o a
   ninguna?
- A3. **Qué queda igual al escribir de vuelta** (toca 1.3). Si editar una fuente tiene que dejar
   idéntico todo lo que no se tocó, y si eso vale también al generar un texto nuevo.
- A4. **Partes que el modelo no declara** (toca 1.2 y 3.1). Si un documento con modelo trae una
   sección que el modelo no conoce, ¿es un error o una parte que no se sigue?
- A5. **Reconectar un ancla** (toca 6.2 y 6.3). Si la función cambió de nombre y hay un solo
   candidato, ¿sldb reconecta y avisa, o propone y alguien confirma?
- A6. **Borrar una relación que sale de la fuente** (toca 5 y 6.1). Por ejemplo, "el documento
   contiene este párrafo". ¿Pedir borrarla se rechaza o se traduce en editar la fuente?
- A7. **Quién ejecuta** (toca 4.1). Si sldb dispara la ejecución cuyo resultado ancla, o solo ancla
   un resultado que se produjo afuera.
- A8. **Dónde se escribe lo declarado** (toca 1 y 5). Hoy una relación o una regla declarada es
   ella misma un documento del proyecto, es decir, otra fuente. Falta decir si eso es un
   principio o solo la forma actual.
- A9. **Borrar contra reglas** (toca 6.1 y 7.1). Borrar algo con dependientes no se rechaza. Pero si
   ese borrado deja incumplida una regla del proyecto, ¿se rechaza por la regla, o se borra y la
   regla queda en error a la vista?
