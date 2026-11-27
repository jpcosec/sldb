# Abierto: lo que los niveles 1 y 2 no deciden

Clase de página: abierto. Fecha: 2026-11-27. Salió de releer las 17 páginas de objeto contra
`principios/fundamentos.md` y `principios/README.md` (tres subagentes, cada uno con seis
páginas) y de la crítica de agy (`principios/concilio/agy.md`). Varias dudas las repitieron los
tres por separado.

## Del modelo (niveles 1 y 2)

1. **De qué son proyección el texto y el grafo.** El principio 2 dice que el grafo es símbolo y
   también una proyección, como el texto. No dice de qué. Y el whitepaper le da al grafo
   identidad propia, lo que no calza con que sea una proyección más.
2. **Cómo queda dicho que algo se quitó.** "Borrar es declarar que se borró" no dice si eso es
   una relación nueva, un estado del nodo o un hecho encima, ni qué ve una consulta sobre lo
   quitado. Lo preguntaron los tres.
3. **Cuándo una parte pasa a ser nodo.** Un valor o una sección sin marcar se nombran por su
   dirección. No está dicho si "el documento contiene esta sección" es una relación sobre algo
   que no es nodo, o solo una dirección dentro del documento.
4. **Relaciones que salen de la estructura.** Si alguien quita afuera el valor del que salía una
   relación ("contiene", "compone"), no está dicho si la relación se retira sola o queda dicha
   con otro estado. Depende de si esas relaciones son observadas o calculadas.
5. **Qué trae sldb de fábrica.** El whitepaper dice que sldb no trae tipos. Pero "contiene" y
   "se apoya en" son tipos de relación del propio sistema. Falta decir cuáles son suyos.
6. **Un nombre con puntos.** Hoy `a.b` da por padre a `a`. No está dicho si eso es una relación
   que sale de la estructura del nombre o una sugerencia hasta que alguien la declare.
7. **Anclar un nodo a otro nodo.** El whitepaper solo describe anclas hacia partes de archivos.
8. **Dónde viven las declaraciones del propio store** (qué sigue, sus reglas de entrada). Si su
   archivo de declaración es una proyección de lo de adentro o una puerta de entrada.
9. **Varios stores.** Cómo se nombra un modelo que declara un store y usa otro, y si el enlace
   entre stores es una relación de adentro.
10. **El papel de un hecho.** Una misma frase puede ser observación, requisito o decisión. El
    principio 5 ya lo nombra; falta decir cómo se declara y qué cambia en cada caso.

## Del nivel 3

- Cuál de los tres vocabularios de tipo de enlace queda.
- Qué es un alias: ancla, relación o nombre. Hoy "ancla" nombra tres cosas.
- Si renombrar un campo, mover un documento y cambiar el contrato de un modelo son operaciones
  propias o un cambio de "dónde".
- El mínimo de procedencia de una relación declarada: quién y cuándo.
- Si "apoyo" cubre solo anclas o también otras relaciones.
- Cómo se dicen en la red el modelo, el tipo de relación y las reglas que hoy están en código.

## Casos sin respuesta

- Reformatear una función: la huella cambia y el sentido no.
- Una prueba que corrió sobre la versión anterior de la función que respalda.
- El archivo cambió en el mismo lugar mientras se editaba el nodo.
