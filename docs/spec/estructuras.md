# sldb: estructuras

Borrador, sin aprobar. Nivel 3: qué estructuras hacen falta para que valgan los niveles 1
(`principios/fundamentos.md`) y 2 (`principios/README.md`). Dice qué tiene que poder decirse de
cada una, no cómo se guarda ni en qué lenguaje. No habla del estado actual.

Cada estructura dice de qué principio sale (P1 a P8). Lo marcado **lectura** lo dedujo el
agente de los niveles 1 y 2 y no está confirmado.

## Lo que hay adentro

Tres cosas, y nada más: nodos, relaciones y hechos.

### Nodo

Una cosa de la que se sabe algo. (P1)

- Tiene identidad propia: estable, única dentro de su store, nunca reutilizada. No depende de su
  contenido, de su nombre ni de dónde está algo afuera. (P3)
- Puede llevar contenido, y lo que lleva adentro puede a su vez tener relaciones. (P1)
- No tiene un tipo obligatorio. Sus tipos son relaciones. (P5)

Hay tres clases de nodo, y son nodos distintos, enlazados entre sí (JP, 2026-11-27):

| Clase | Qué lleva | Cómo nace |
|---|---|---|
| de anclaje | dónde está una parte afuera y qué se vio de ella | al anclar: un anclaje crea un solo nodo, este |
| de significado | lo que se sabe: una afirmación del árbol de conocimiento | al juntar y sintetizar lo que dicen los anclajes |
| de proyección | una forma de decirlo afuera, con sus reglas | al sacar o al reconocer un texto como derivado |

El paso de anclajes a conocimiento tiene etapas:

1. **Anclar.** Cada parte marcada da un nodo de anclaje. Nada más.
2. **Juntar.** Varios anclajes que dicen lo mismo se reúnen en un "las fuentes dicen".
3. **Sintetizar.** De ahí se arma el árbol de conocimiento: los nodos de significado.

Un mismo nodo de significado puede tener muchos anclajes. Una página web, las instrucciones de
un asistente y un manual pueden traer la misma afirmación, y tiene que ser la misma. Entre esos
textos uno suele ser la fuente y los otros derivaciones de ella. Cuando hay que cambiar la
afirmación, el nodo de significado dice de inmediato en qué lugares está escrita, sin leer
todos los documentos.

### Relación

Un vínculo con tipo entre dos nodos. (P1)

- Sus dos extremos son nodos. No termina en un archivo ni en una dirección. Si hace falta
  relacionar una parte que no es nodo, primero se la marca. **Lectura.**
- Tiene tipo, y el tipo es un nodo: se puede consultar y relacionar. (P4)
- Es de estructura o de significado, y las dos clases no se mezclan. (P5)
- Tiene identidad propia, igual que un nodo: se puede decir algo sobre ella.

### Hecho

Lo que se dice de un nodo o de una relación. (P6)

Todo hecho trae:

- **quién** lo dijo: una persona, un agente o un cálculo;
- **cómo se supo**: se observó afuera, alguien lo declaró, alguien lo propuso, o se calculó;
- **cuándo**;
- **en qué se apoya**, si se apoya en algo. (P7)

Y puede traer su **papel**: si es una observación, un requisito o una decisión. (P5)

De cómo se supo depende qué se puede hacer con él:

| Cómo se supo | Vale mientras | Se puede rehacer | Se puede quitar |
|---|---|---|---|
| observado | coincida con lo de afuera | no: lo que se vio entonces ya pasó | no |
| declarado | lo sostenga quien lo declaró | no | no |
| propuesto | alguien lo declare o lo descarte | sí | sí |
| calculado | nada: no vale por sí mismo | sí | sí |

Que algo se retiró es un hecho más: "tal persona declaró, tal día, que esto ya no va". El nodo
sigue, con ese hecho encima. Una consulta lo ve, y dice que está retirado. **Lectura:** sale
de "borrar es declarar que se borró" y de que todo lo dicho tiene autor.

## Cómo se toca con el afuera

### Ancla

El punto donde un nodo está atado a una parte de un archivo. Es el sensor. (P3)

- **Dónde**: cómo encontrar la parte ahora. Puede cambiar sin que cambie el nodo.
- **Qué se vio**: el contenido de la parte y su huella.
- **Con qué regla se leyó**: qué cuenta como cambio y qué no. Dos lecturas distintas de la misma
  parte dan dos huellas.
- Un nodo tiene anclas sucesivas en el tiempo. Anclar de nuevo es un hecho declarado, con autor
  y motivo.

Un ancla puede atar a algo que no es un archivo: el resultado de ejecutar algo. Sin definir
(`abiertos/hooks.md`).

**Lectura:** un nodo también puede apoyarse en otro nodo de adentro, pero eso es una relación
"se apoya en" y no un ancla: el ancla es solo hacia afuera. Lo que hace falta en los dos casos
es recordar qué se vio.

### Huella

Una marca corta calculada de lo que se observa en una parte. Sirve para una sola cosa: notar
que lo observado cambió. No identifica al nodo, no dice qué significa, y no prueba que dos
partes sean iguales.

## Cómo entra y cómo sale

### Proyección

Una forma de sacar lo de adentro. (P2)

Toda proyección dice:

- **con qué reglas** se hace;
- **qué conserva**: todo, o una parte;
- **cómo se comprueba**: si es exacta, volviendo y comparando; si pierde algo, midiendo cuánto.

Hay una proyección que cada documento trae: la de la estructura con que entró. Esa es exacta.

### Modelo

La estructura que comparte una familia de documentos, dicha una vez. (P5)

- Sirve hacia los dos lados: dice qué tomar al entrar y cómo proyectar al salir.
- Es un nodo, con sus relaciones. (P4)
- Puede ser **variación** de otro: igual, salvo diferencias que se nombran.
- No es requisito para entrar. Lo que no tiene modelo propio es un árbol de partes.
- Puede decir que no admite nada más que lo que nombra. Si no lo dice, lo que sobra entra igual.

Aparte del modelo, un nodo puede tener un **tipo por lo que es**: por su significado, por su
papel en el texto o por para qué sirve. Es otra jerarquía.

## Lo que el sistema hace

### Regla

Algo que tiene que cumplirse, dicho como nodo. (P4) Tiene autor, se apoya en algo y puede
quedar en duda, igual que cualquier hecho.

### Acción

Lo que el sistema hace cuando algo ocurre. (P4) Sin definir: `abiertos/hooks.md`.

## El borde

### Store

El contexto dentro del cual valen los nombres. (P1)

- Un nombre vale dentro de su store. Dos nombres iguales en dos stores no son la misma cosa.
- Que dos nodos de stores distintos son la misma cosa es una relación declarada.
- Un store puede usar nodos de otro. Cómo se nombra entonces un modelo ajeno: sin decidir.

## Lo que sldb trae y lo que no

sldb no trae tipos de dominio: no sabe qué es una tarea ni una decisión.

Trae los tipos de relación que sus propios principios nombran. **Lectura:**

| Relación | De dónde sale |
|---|---|
| contiene | la estructura de lo que entró (P1) |
| se apoya en | P7 |
| es variación de | P5 |
| es del tipo | P5 |
| es la misma que | P1 |
| se proyecta por | P2 |

Todo lo demás lo declara quien usa sldb.

## Sin decidir en este nivel

- Cómo se juntan los anclajes: quién dice que dos anclajes dicen lo mismo, y cuánto de eso
  puede proponer una máquina. Por el principio 1, que dos cosas son la misma se declara.
- Cómo se dice que un texto es fuente y otro derivación, y qué pasa cuando una derivación deja
  de decir lo mismo que su fuente.
- Si un nombre con partes (`a.b`) da por sí solo una relación entre `a.b` y `a`, o es solo una
  sugerencia hasta que alguien la declare.
- Cómo se nombra un modelo que declara un store y usa otro.
- Si "se apoya en" cubre solo lo anclado afuera o cualquier relación de la que algo dependa.
- Qué es una acción.
