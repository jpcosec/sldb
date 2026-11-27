# sldb

Borrador, sin aprobar. Este texto explica qué es sldb y por qué es así. No describe cómo está
construido ni en qué estado está.

## El problema

Lo que un proyecto sabe está escrito en sus archivos. Hay documentos que explican decisiones,
código que las ejecuta, tareas que dicen qué falta. Y esos archivos hablan unos de otros: un
documento de diseño afirma algo sobre una función, una tarea existe por una decisión, una
decisión se apoya en un párrafo de otro documento.

Nada de eso se puede usar. No se le puede preguntar al proyecto qué depende de una función, ni
qué decisiones quedaron sin revisar, ni si todas las tareas cumplen lo que el equipo acordó. Y
cuando un archivo cambia, nada avisa a los que hablaban de él. El párrafo que describía la
función sigue ahí, escrito igual, y ya nadie sabe si describe lo que la función hace.

Además no todo lo escrito es igual. Hay documentos que siguen una forma conocida y hay texto
libre, y lo habitual es tratarlos como si fueran lo mismo: o todo son formularios, o todo es
prosa.

La salida de siempre es llevar ese conocimiento a una base de datos y trabajar ahí. Funciona un
tiempo. Después hay dos versiones de cada cosa, la del archivo y la de la base, y cada una dice
algo distinto. Quien quiere saber la verdad tiene que mirar las dos.

## La idea

Un archivo con estructura ya es dato.

Un documento tiene secciones, campos, listas. Un archivo de código tiene funciones y clases. La
interfaz de un programa tiene comandos y parámetros. Esa estructura se puede leer siempre igual,
sin interpretar nada. Entonces no hace falta copiar el conocimiento a otro lado para tratarlo
como dato: basta leerlo donde está.

sldb es eso. Lee la estructura de los archivos de un proyecto y permite trabajar sobre sus
partes como se trabaja con datos: nombrarlas, relacionarlas, consultarlas, comprobarlas,
cambiarlas. Los archivos siguen siendo archivos comunes, y siguen siendo la verdad.

Todo lo demás de este texto sale de tomarse en serio esa frase.

## El modelo

**Fuentes y partes.** Una fuente es un archivo del proyecto. Una parte es una unidad de su
estructura: una sección, un párrafo, un valor, una función. Para sldb un documento y un archivo
de código son lo mismo, un árbol de partes. Eso es lo que permite que un párrafo y una función se
relacionen: son la misma clase de cosa.

No hace falta seguir un archivo entero. Se elige qué partes importan, y el resto queda en su
archivo sin que sldb tenga nada que decir. Tampoco hace falta que la fuente se adapte: sldb mira,
no exige.

**Adentro y afuera.** Los archivos están afuera. Adentro de sldb hay solo nodos y relaciones:
objetos, vínculos y hechos. Esa es la topología propia del sistema, y solo lo que está en ella
tiene identidad. Un archivo, o un pedazo de archivo que nadie marcó, no es parte de ella.

Lo que une las dos cosas es un sensor. Cuando alguien marca una parte de una fuente, nace
adentro un nodo que la sigue: recuerda qué marcó y dónde lo encontró. sldb siente del exterior
solo lo que tiene sensor. El resto del proyecto está cubierto, archivo por archivo, por el
control de versiones, y con eso basta.

De ahí sale qué significa "la misma parte". Una parte sin marcar no tiene continuidad ni la
necesita: se nombra por su dirección, y si se mueve o se reordena, esa dirección nombra lo que
haya ahora en ese lugar. Lo que persiste es el nodo que la marcó. Si la parte cambia de lugar o
de nombre, lo que se actualiza es el "dónde" de ese nodo. El exterior puede alterar lo de
adentro, porque un sensor nota el cambio, pero no pasa a ser parte de adentro.

**Relaciones.** Entre los nodos hay relaciones, y cada relación tiene un tipo: esta sección
contiene a este párrafo, este párrafo se apoya en esta función, esta tarea responde a esta
decisión. Algunas salen de la estructura misma, como "contiene". Otras las declara alguien, una
persona o un agente, y queda escrito quién fue.

Con partes y relaciones se arma un grafo, y sldb no tiene nada más que eso. Un modelo, una regla
o una vista también se expresan como partes y relaciones. Lo importante de una parte no es ella
misma: son sus relaciones.

**Entrar y volver a salir.** Marcar una parte la hace entrar: lo que dice pasa a ser un nodo
de adentro. Se puede marcar poco o mucho. Un documento marcado por completo vive adentro, como
los nodos que se tomaron de él.

Lo que está adentro se puede volver a mostrar de muchas formas, y cada forma es una proyección.
Una de ellas es especial: proyectar por la misma estructura que el documento tenía al entrar.
Esa proyección devuelve el documento tal como estaba. Por ahí se recupera una sección, y por
ahí se la modifica: se cambia el nodo y se proyecta de nuevo a su archivo.

Entonces hay tres cosas que conviene no mezclar: dónde estaba una parte en su fuente (su
anclaje), qué dice (su significado), y cómo se muestra (una proyección). Las preguntas se hacen
sobre lo que dice. Los cambios se detectan en donde estaba. Y lo que se muestra se genera.

**El store.** Lo que sldb registra de un proyecto se llama store. No es una copia del proyecto.
Tiene tres clases de cosas y cada una vale distinto:

- lo que alguien declaró y ningún archivo dice por sí solo: una relación, una regla. Vale lo
  que vale quien lo declaró;
- lo que sldb observó de una parte en un momento: su contenido y una huella, que es una marca
  corta que cambia si lo observado cambia. Vale mientras coincida con la fuente; si difieren,
  manda la fuente;
- lo que sldb calculó a partir de lo anterior: índices, respuestas. No vale por sí mismo; se
  puede borrar y rehacer.

## Familias de documentos

Mucho de lo que se escribe en un proyecto tiene una forma más o menos fija: un reporte, un
formulario, una decisión, una tarea. Y mucho otro no la tiene: es texto libre. Tratar todo por
igual falla para los dos lados. Si se le exige forma a todo, el texto libre queda afuera. Si no
se le reconoce forma a nada, se pierde lo que los documentos parecidos tienen en común.

sldb no parte de los tipos. Parte de los documentos y mira qué comparten.

**Por la forma.** Si varios documentos tienen exactamente la misma estructura, hay un modelo en
común: "esto es un reporte de tal clase". El modelo no se les impone; es el nombre de lo que ya
comparten. Si otros son iguales salvo por una parte de más, son una variación de ese modelo. Y
desde ahí aparece todo lo conocido: una variación hereda de su modelo, varios documentos
distintos se pueden tratar como el mismo en lo que comparten, y un modelo se puede armar
juntando otros. Herencia, clases, polimorfismo y composición no son algo que sldb agregue: son
lo que resulta de especializar documentos.

Un documento sin modelo propio no está fuera de esto. Está en la clase más general, que es ser
un árbol de partes. Lo que no calza con un modelo no se fuerza: se especializa.

**Por lo que es.** La forma no es lo único que los documentos comparten. Una parte puede
llevar además un tipo por lo que significa, por el papel que cumple en el texto o por para qué
sirve: esto es un diagnóstico, esto es una conclusión, esto es un requisito. Sobre esos tipos se
arma otra jerarquía, distinta de la de la forma: un reporte de epicrisis y un reporte de
rendimiento son los dos reportes, aunque no se parezcan por fuera.

Las dos jerarquías no coinciden, y no tienen por qué. Dos documentos pueden tener la misma forma
y ser cosas distintas, o ser lo mismo con formas distintas. Por eso sldb las lleva separadas: de
un lado las relaciones de estructura, del otro las de significado.

Esto es lo que permite tratar distinto lo que es distinto. Donde hay forma estándar se obtiene
un modelo, y con él se puede comprobar y proyectar. Donde no la hay, quedan los nodos y lo que
se diga de ellos, y eso también se puede consultar y relacionar.

## Un ejemplo, de principio a fin

Un proyecto tiene una función que calcula un precio, y un documento de diseño con un párrafo que
dice: "el precio incluye el impuesto".

Alguien declara que el párrafo se apoya en la función. Con eso nacen adentro dos nodos, uno que
sigue al párrafo y otro que sigue a la función, y una relación entre ellos. Esa relación es un
ancla: además de unirlos, recuerda lo que vio de la función en ese momento.

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
        Observado["Observado: el contenido y la huella de la función. Si difiere, manda la fuente"]
        Calculado["Calculado: índices y resultados. Se puede borrar y rehacer"]
    end
    Parrafo -->|"se apoya en"| Funcion
    Declarado -->|"sigue"| Parrafo
    Observado -->|"lo que vio"| Funcion
    Calculado -->|"se rehace desde"| Declarado
```

Desde ahí se puede preguntar. Qué dice el párrafo. En qué se apoya. Qué otras cosas del proyecto
se apoyan en esa misma función. Si hay algún documento de diseño que no se apoya en nada.

Una semana después alguien cambia la función, con el editor que quiera. sldb no estaba mirando
y no importa: la próxima vez que se le pregunte, compara la huella que guardó con la función de
ahora, ve que difieren, y muestra el párrafo como pendiente de revisión. No dice que el párrafo
esté mal. Quizá solo ordenaron el código y el impuesto sigue incluido. Eso lo decide quien
revisa; cuando lo confirma, ancla de nuevo, y queda quién lo hizo.

Si a la función le cambiaron el nombre, sldb no sale a buscar cuál es ahora. El ancla queda en
una zona movida hasta que alguien ancle de nuevo. Reconectar no es algo que el sistema persiga:
es lo que resulta de un anclaje nuevo.

Si en vez de cambiarla la borran, adentro no se borra nada. Queda declarado que la función ya no
está, y eso baja hasta el párrafo. Puede que el párrafo quede sin ningún apoyo. Puede también
que se sostenga por otro lado, porque se apoyaba además en una prueba o en otra decisión. sldb
muestra cuál de las dos es.

Y si el equipo decidió que todo documento de diseño tiene que apoyarse en algo del código, eso
no se programa: se declara como una regla, igual que se declaró el ancla, y sldb la comprueba
cada vez que alguien intenta escribir.

## Lo que se sigue de la idea

Si los archivos son el dato, varias cosas dejan de ser opcionales.

**Un cambio viaja, y no se lo lleva todo.** Lo que hay adentro se construyó desde las fuentes
y vale mientras ellas no cambien. Cuando una cambia, el sensor lo nota y queda declarado que
hubo un cambio. Esa perturbación baja por las relaciones: se sabe qué nodos tienen un camino
desde la parte que cambió. Pero que algo cambie afuera no vuelve inválido todo lo que se sabía.
Algunos nodos quedan sin ningún apoyo. Otros se sostienen por otro lado. Y la mayoría ni se
entera.

Por eso lo que se sabe no es simplemente vigente o caído. Hay zonas donde todo sigue apoyado y
zonas donde algo se movió. De ahí se puede decir cuánta certeza hay en una parte del grafo y
cuánto desorden acumuló, y es en las zonas movidas donde aparecen las contradicciones y los
errores.

**Adentro no se borra.** Borrar algo es declarar que se borró. El nodo sigue, con ese hecho
encima, y la consecuencia baja como cualquier otro cambio. Sacar de verdad los nodos que quedaron
sin apoyo es otra etapa, posterior y pedida, una limpieza; y lo que había en los archivos sigue
en el control de versiones. Afuera es distinto: ahí las cosas sí desaparecen, pero eso solo
llega adentro a través de sus anclas.

**El grafo se consulta, no se mira.** Nadie ve el grafo entero ni hace falta. Lo que importa
adentro es que toda pregunta tenga una respuesta transparente: qué se sabe, en qué se apoya y
qué tan firme está.

**Manda la fuente.** sldb puede tener el contenido de lo que sigue, y lo necesita para responder
y para generar. Pero es una observación, y una observación puede estar vieja. Por eso las fuentes
pueden cambiar por fuera de sldb sin que eso sea un daño: es un cambio que hay que ver. Y por eso
todo lo calculado se tiene que poder borrar sin perder nada. Si al borrarlo se pierde algo, eso
no era un cálculo: era algo que alguien declaró y quedó guardado en el lugar equivocado.

**Apoyarse no es apuntar.** Un enlace que solo dice "esto se refiere a aquello" sigue funcionando
aunque aquello haya cambiado por completo. Lo que hace falta saber no es si el destino existe,
sino si dice lo mismo que cuando se lo citó. Para eso el ancla guarda lo que vio. La huella sirve
para notar el cambio y para nada más: no dice qué significa una parte, ni que dos partes sean
iguales, ni es el nombre de la parte.

**Nada se oculta.** El valor de sldb está en que se pueda confiar en lo que muestra. Si una
respuesta vacía puede significar tanto "no hay nada" como "no pude mirar", esa confianza se
acaba. Lo que no se sabe se dice que no se sabe.

**Preguntar no cambia nada.** Una consulta no modifica lo registrado ni lo arregla por su
cuenta. Si lo hiciera, dos que preguntan lo mismo verían cosas distintas.

**Las mismas reglas por cualquier puerta.** Un cambio pedido a sldb se propone, se comprueba, y
solo si pasa se escribe en el archivo. Da lo mismo por dónde se pidió. Si una entrada comprueba y
otra no, la regla es un adorno.

**Lo que se genera no se escribe a mano.** Desde lo que sldb sabe se pueden generar otras
expresiones: un tablero, una ficha, los datos de un diagrama. Lo generado remite a su origen.
Editarlo a mano, o escribir a mano lo que se pudo generar, es volver a tener dos versiones.

**El sentido es local.** Un nombre vale dentro de su store. Que dos proyectos usen la palabra
"precio" no significa que hablen de lo mismo. Decir que sí es una declaración que alguien hace, no
algo que se deduce de que las letras coincidan. Lo mismo vale para un parecido que encuentra una
máquina: es una sugerencia hasta que alguien la declara.

**sldb no sabe de qué trata el proyecto.** No sabe qué es una tarea, ni una decisión, ni un
diagrama de cierta norma. Sabe de partes, relaciones, modelos, reglas y vistas. Qué es una tarea
lo declara el proyecto que las usa, con esos mismos mecanismos. Un sldb que conociera a su primer
usuario dejaría de servirle al segundo.

## Para qué se usa

Tres usos, todos declarados encima de sldb por quien lo usa:

- **Llevar el trabajo de un equipo.** Cada tarea es un documento. El equipo declara qué campos
  tiene una tarea, por qué estados pasa y qué reglas cumple. El tablero se genera.
- **Describir un sistema y dibujarlo.** Los componentes y sus conexiones se declaran como partes
  y relaciones. Una vista elige qué mostrar y una notación dice con qué figura. sldb entrega la
  vista resuelta; la dibuja otro programa.
- **Mantener al día lo que se dice del código.** Es el ejemplo de arriba.

Lo usan personas y agentes sobre un mismo proyecto. Para un agente es la forma de saber en qué se
apoya lo que otro escribió, sin tener que creerle.

## Lo que sldb no es

- No es la base de datos donde viven los documentos. Los documentos viven en sus archivos.
- No es un control de versiones. Ese dice qué líneas cambiaron; sldb dice qué dependía de ellas.
- No es un buscador. Un buscador encuentra palabras parecidas; sldb responde por relaciones.
- No es un generador de documentación. Genera, pero como consecuencia de saber, no como fin.
- No es un juez. Dice si lo registrado es consistente y si su soporte cambió, no si es cierto.

## Lo que falta decidir

Hay cosas que este texto usa y no resuelve.

1. **Las etapas de un cambio.** Detectar, declarar el cambio, bajar la consecuencia, revisar,
   limpiar. Cuántas corren solas y cuáles esperan a alguien puede variar; lo que falta fijar es
   el mínimo con que esto ya sirve.
2. **Cómo se mide la certeza.** Que hay zonas más firmes y zonas más movidas está dicho. Con qué
   se mide también puede variar; falta fijar el mínimo.
3. **Qué es un hook.** Una afirmación puede apoyarse en un resultado ("la prueba pasa"), un
   estado puede cambiar cuando algo ocurre, un cambio puede disparar una revisión. En los tres
   casos algo se ejecuta. Falta decir qué es un hook, con qué mecanismos funciona, qué
   condiciones tiene que pasar antes de correr, y cómo se mete a una persona en el medio sin que
   usarlo se vuelva una carga. Dónde y cómo corre lo define cada hook.
