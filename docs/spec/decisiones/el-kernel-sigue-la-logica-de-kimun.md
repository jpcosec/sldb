# Decisión: la lógica del kernel de sldb es la de kimun

Clase de página: decisión. Fecha: 2026-11-26. Estado: fijado por JP; las respuestas de la tabla
dicen de quién es cada una.

## Qué fijó JP (2026-11-26)

- Todo lo que viene después va a envolver a kimun. Por eso la lógica de kernel que se escriba en
  este spec tiene que ser la misma lógica de kimun.
- kimun es solo nodos y relaciones. Los nodos son de tres clases: de anclaje, de significado y de
  proyección. Las relaciones se tipan, y ahí caen herencia, transclusión, hook y las demás.
- Un enlace del texto es una relación más.
- Los modelos de documento son consecuencia y no principio, al revés que en sldb hoy. Es una
  relajación que aprovecha que todo es Clojure: un Lisp es AST puro.

## Qué precisó JP después (2026-11-26)

- **El store es una clase de grafos**, nada más. kimun, por ser Lisp, es homoicónico: lo mismo es
  dato y es código. Precisado después por JP: no es una clase de grafos en abstracto, "al final
  es todo clojure nomas".
- **Falta definir la persistencia.** JP lo nombra como el gran problema abierto.
- **El modelo no es un objeto del spec.** Un documento nunca entra crudo, siempre como AST. Los
  nodos del AST tienen propiedades, que al final también son relaciones, y a grandes rasgos se
  separan en semánticas y estructurales. Además un nodo puede llevar un hash como propiedad (para
  un árbol de Merkle), un anclaje de referencia a un blob de git, y otras.
- **De dónde sale un modelo**: una familia de documentos que comparten en su AST las propiedades
  estructurales es un modelo como los de sldb, y ese modelo se puede declarar como un AST tipado.

## Tres correcciones de JP a la lectura del agente (2026-11-26)

- **La implementación de kimun puede no estar haciendo esto.** Donde no lo haga, se corrige más
  adelante. Este spec describe la lógica, no el estado del código de kimun.
- **A un nodo se le pueden meter cosas adentro**, y esas cosas también pueden tener relaciones.
  Eso es lo importante del modelo.
- **Los objetos y estructuras de datos de sldb no desaparecen: se absorben.** Las páginas de
  objeto se conservan; cada una dice cómo se expresa ese objeto en nodos, contenido y relaciones.

## Preguntas abiertas del spec que esta lógica contesta

Leído en `~/proyectos/kimun` (`370beaff`): `docs/v2/00-nucleo.md`, `docs/v2/14-juego-del-lenguaje.md`
§18 y §21, `docs/v2/drafts/diseno-nucleo-sldb.md`. "Dueño" es texto de JP en kimun; "concilio" y
"equipo" son inferencias registradas allá como tales; "borrador" es elección del borrador de kimun
como núcleo de sldb, sin confirmar.

| Página | Pregunta | Respuesta | Origen |
|---|---|---|---|
| nodo-documento | Qué lo identifica: nombre o ruta | Un id propio que nace al marcarlo y no cambia; la ruta es su anclaje. `Modelo:nombre` se conserva porque está escrito en las fuentes | dueño (identidad no es hash ni lugar); id opaco: concilio |
| nodo-documento | Mover es cambiar o verbo aparte | Es re-anclar y se declara con motivo. El kernel no mueve archivos ni detecta movimientos | concilio |
| nodo-documento | Borrar | Cerrar es una declaración con motivo. Que el archivo falte no lo borra: queda `missing` | concilio |
| nodo-seccion | Identidad: camino de slugs o id estable | Id estable; el camino es el anclaje | concilio (sin implementar en kimun) |
| nodo-seccion | Crear una sección que el modelo no declara | No es error ni ruido: queda en el archivo y no entra al grafo. Si importa, se especializa la clase | dueño (14 §18.2, §18.4) |
| nodo-ancla | Nodo o arista con huella | Vínculo verificable entre un conocimiento y su soporte; no es identidad | dueño (núcleo 2.3) |
| nodo-ancla | Cambiar un ancla `changed` | Releer es una observación nueva de la misma unidad; reapuntar es re-anclar y se declara | concilio |
| nodo-ancla | Reconexión al renombrar el destino | No es automática: el sensor propone y la continuidad se declara. La pérdida no se oculta | dueño (núcleo 2.4), concilio |
| nodo-ancla | Anclar sección o valor | Sí, en cada nivel: archivo, sección, campo | concilio |
| nodo-campo-de-modelo | Renombrar un campo | Una unidad `missing` más una nueva | equipo |
| nodo-campo-de-modelo | Cambiar el tipo con valores existentes | Una clase cambiada es otra clase; los documentos siguen en la original hasta reclasificarlos | dueño (núcleo 5.2) |
| arista-estructural, arista-contains-y-composes | Aristas o proyecciones | Proyecciones derivadas del modelo al leer; no se escriben. Borrar una es cambiar la fuente | borrador |
| arista-autorada | `RelationDoc` y campo de referencia: una cosa o dos | Una: son relaciones, con dos puertas | borrador |
| arista-links-to, nodo-store | Declaración contra índice | Manda la declaración; lo reconstruible no tiene autoridad | dueño (núcleo 6.3) |
| arista-semantic-parent, arista-semantic-equivalent | Dónde se guardan | En el store versionado, como relaciones; es curaduría explícita | dueño (núcleo 3.2) |
| enlace-en-el-texto | Es una arista | Sí, una relación más | JP, 2026-11-26 |

## Contestadas a medias

- Borrar algo con dependientes: kimun no borra en cascada; lo que dependía se revisa y la pérdida
  se declara. No dice si la operación se rechaza antes.
- Aplicar una transición: calcular el resultado es una función pura; escribirlo en la fuente
  depende de la pregunta de abajo.

## No contestadas por kimun

- Todo lo que es escribir la fuente (crear sobre un archivo que existe, parche por campo o
  documento entero, escribir el Python de un modelo). Es la pregunta 2 del borrador de kimun, sin
  contestar.
- Elemento de lista por posición o por clave.
- Borrar o renombrar un tipo de relación, renombrar un tag, simetría de la equivalencia.

## Consecuencias para este spec, sin hacer

- Cada página de objeto lleva una sección "Cómo se absorbe en la lógica de kimun" (lectura del
  agente, sin confirmar). Ninguna página se elimina ni se funde con otra.
- kimun separa el modelo de lectura del de generación y la ida y vuelta idéntica deja de ser
  obligación (14 §18.7, dueño). sldb usa hoy una plantilla para las dos direcciones.
