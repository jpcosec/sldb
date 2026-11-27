# sldb: criterios

Estado: sin aprobar. Esta página **no es el whitepaper**: es la lista de criterios que se
desprenden de él, para revisar una pieza de sldb o una página del spec. El whitepaper es
`README.md` y se lee primero; estos criterios no se entienden sin él y no lo reemplazan.

Cada criterio trae su por qué, un caso que rechaza, y si hoy se cumple. Usan el ejemplo del
whitepaper: un párrafo que dice "el precio incluye el impuesto" y se apoya en la función que
calcula el precio.

## La distancia con el sldb de hoy

El whitepaper dice cómo tiene que ser sldb, no cómo es. El sldb de hoy nació como una herramienta para
documentos con plantilla, y de ahí vienen sus distancias con él. Las más grandes:

- El código no entra como árbol de partes igual que los documentos. Entra por otro camino, como
  una lista de hechos.
- Para seguir un documento todavía hay que declararle un modelo antes.
- Los enlaces escritos dentro de un texto no aparecen junto a las demás relaciones.
- Hay entradas que escriben sin comprobar las reglas.
- Borrar algo no deja marcado lo que dependía de ello.

El detalle está en el "Hoy" de cada criterio.

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
se eligió queda en su archivo. Lo que sí se eligió puede llevar su contenido dentro.

- Por qué: casi nunca interesa un archivo entero; interesa la función o el párrafo del que algo
  depende. Y una parte que se sigue necesita su contenido para poder consultarla y para generar
  otras expresiones desde ella (3.2).
- Rechaza: que vigilar la función obligue a incorporar el archivo completo.
- Hoy: en parte. Se siguen valores y funciones sueltas, con su contenido; un documento seguido
  se sigue completo.
- Nota: seguir una fuente entera, parte por parte, también es una elección válida. Tener el
  contenido no cambia quién manda: si la fuente y lo guardado difieren, manda la fuente (5), y
  la huella es la forma barata de notar que difieren.

**1.3.** Cuando una fuente admite edición, un cambio pedido sobre una de sus partes se escribe en
la fuente misma. El cambio no está hecho mientras solo exista dentro de sldb.

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
quien lo declaró); lo que sldb **observó** de una parte en un momento, es decir su contenido y
su huella (sirve para consultar, para generar y para comparar; si difiere de la fuente, manda
la fuente); y lo que sldb **calculó** (no responde por nada: se puede rehacer).

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
