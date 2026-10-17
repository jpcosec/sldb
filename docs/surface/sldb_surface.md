Una interfaz para un proyecto que tengo. Eh, el proyecto básicamente es un sistema de proceso de documentos.

La idea es que todo texto tiene tres superficies de representación, ¿no es cierto?

Interesante. ¿Cuáles son las tres superficies que tienes en mente?

Eh, una... Ya una superficie es como lo superficial, que es sintaxis, gramática, el estilo, eh, todas esas cosas. Hay otra parte que es como, le, le puse meaning, que es como el, el, el significado. Son al final como... Las tripletas, pero abstraete un poco más de eso. Eh, digámosle que son átomos de conocimiento sobre lo que hay en el texto. Y la tercera representación es la representación de un grafo.

De estos átomos y cómo se relacionan entre ellos.

Ah, entonces tienes superficie, átomos de significado, y la topología que los conecta. Aunque me hace ruido una cosa: la tercera suena más como una vista de la segunda que como una superficie independiente. ¿Qué la hace distinta para ti?

La que, lo que necesito... lo que le hace distinta es que eh, la segunda es eh, un poco como la abstracción.

Entendido: la segunda es el contenido atómico, la tercera es la estructura relacional entre esos átomos. Son ortogonales — puedes cambiar relaciones sin tocar átomos y viceversa.

Ahora, ¿la interfaz es para que un humano edite las tres superficies, o para inspeccionar lo que el sistema infiere?

Exacto. Exacto, hay una cosa de ortogonalidad ahí. Entre la propuesta, o el, el hecho y eh, o la proposición y las relaciones que tienen. Es un poco un poco una estructura medio fractal.

Sí, es fractal: una relación entre átomos puede a su...

Si te das cuenta, eh, no sé, pues si tengo una base de conocimiento sobre perros y otra sobre gatos, puedo tirar una relación entre las dos bases de conocimiento. que va a ser eh, un poco como transitiva perdón, más que transitiva eh, por herencia se va a heredar esa relación, ¿cachai? pero eso no es el foco ahora el foco es que eh, necesito diseñar eh, desde el punto de vista más como gráfico, más visual más UX, digamos eh, algo que me permita primero mostrar desde un texto libre cuáles son los átomos que estoy creando,

Okay, para mostrar átomos emergiendo de texto libre, lo más directo es vista partida: el texto a la izquierda con resaltado, y los átomos a la derecha como tarjetas. Al pasar por una tarjeta se iluminan los tramos del texto que la originaron, y viceversa.

¿La extracción es incremental mientras escribes, o corres el texto completo y luego revisas?

Explicando el comportamiento del grafo tras publicar el documento.

Cuando el grafo cambia y el documento ya estaba publicado

El documento publicado es una instantánea, no una vista viva. Al publicar congelas qué átomos, en qué versión, llenaban cada slot. El borrador sigue vivo detrás. Cuando algo cambia en el grafo (un átomo editado, uno nuevo que calza con una consulta, uno descartado), el documento publicado no se toca: se marca como desfasado, con una insignia en el esqueleto sobre las secciones afectadas.

Al abrirlo ves un diff por slot, no por texto: "entraron 2 átomos, 1 cambió de enunciado, 1 salió". Los átomos editados muestran antes y después en la misma tarjeta. El punto delicado son los slots con prosa generada: si cambió un átomo que alimentaba un párrafo, el párrafo queda marcado como obsoleto y regenerarlo es una decisión tuya, nunca automática, porque reescribir prosa ya revisada es justo lo que no quieres que pase en silencio. Los pins apuntan a una versión específica del átomo, así que un pin cuyo átomo cambió te pregunta si sigues o te quedas con la versión vieja.

Republicar genera una versión nueva del documento, y cada frase conserva su trazabilidad a la versión del átomo que la originó.

Vista dos, el Grafo

Tres zonas. A la izquierda, el árbol de tags como panel de control: cada rama con un triángulo para plegar, un ojo para ocultar y un contador de átomos. Al centro, el canvas. A la derecha, un inspector que aparece solo cuando seleccionas algo.

En el canvas los nodos son átomos, con color según el tag de nivel más alto al que pertenecen, y los grupos de tag se dibujan como regiones de fondo tenue, tipo diagrama de Venn blando. Plegar una rama colapsa su región en un solo nodo grande, con tamaño proporcional a cuántos átomos contiene. Las aristas que cruzaban hacia adentro se fusionan en un haz con grosor según cuántas relaciones representa y un número encima. Doble clic lo despliega con una animación que expande desde el centro, para que no pierdas la orientación espacial.

El layout no puede ser force-directed puro, porque se reacomoda cada vez que pliegas y pierdes el mapa mental. Los grupos necesitan posiciones estables: el sistema propone un layout, tú puedes arrastrar regiones enteras, y eso queda fijado. Es un territorio que aprendes, no una simulación física.

Las aristas llevan el tipo de relación como etiqueta que aparece al hacer hover, no siempre visible, porque con más de unas pocas decenas se vuelve ruido. Filtrar por tipo de relación va en la barra superior, separado de los tags, porque son ejes ortogonales: tags agrupan nodos, tipos de relación filtran aristas.

Seleccionar un nodo abre el inspector: el enunciado, los tags, las relaciones entrantes y salientes listadas, y los tramos de texto que lo anclan, con salto directo a la vista uno. Seleccionar un nodo colapsado muestra los átomos que contiene como lista, sin tener que desplegarlo en el canvas.

La operación clave aquí es crear relaciones: arrastras desde el borde de un nodo a otro, eliges el tipo, listo. Si arrastras hacia un grupo colapsado, la relación se crea contra el grupo, que es tu herencia: vale para todo lo que está adentro. Visualmente esa arista se distingue con un trazo punteado o un remate distinto, para separar relaciones heredadas de las directas cuando despliegues el grupo.

Como referencia para imitar, el comportamiento de plegado se parece a los compound nodes de yEd o Cytoscape.js con la extensión expand-collapse, que además te sirve directo como base de implementación.
