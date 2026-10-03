# Bundle de diagnóstico — contexto cero

Lees esto porque te toca diagnosticar **una** función de un sistema. No conoces
el sistema y no lo necesitas: todo lo que hace falta está acá o en los archivos
de evidencia que tu tarea nombre.

---

## El sistema bajo diagnóstico

Una biblioteca que convierte documentos de texto estructurado en objetos
validados, y de vuelta a texto, sin pérdida. Tiene además un almacén que indexa
esos documentos y permite consultarlos, y una interfaz de línea de comandos.

Datos duros:

| | |
|---|---|
| archivos de código | 586 |
| líneas de código | 25.829 |
| archivo más grande | 138 líneas |
| archivos de ≤15 líneas | 90 |
| pruebas | 1.207, **todas pasan** |
| paquetes de primer nivel | 9 |
| aristas entre paquetes | 30 |
| **ciclos entre paquetes** | **5** |
| imports escritos dentro de funciones | 91 |

Lo importante de esa tabla: **el sistema funciona y está probado**. No estás
ante un sistema roto. Estás ante uno que podría no sostenerse cuando su autor
deje de mirarlo.

---

## El marco: siete funciones

Un sistema se sostiene si cumple siete funciones. Diagnosticar es recorrerlas y
encontrar cuál falta. Una función ausente produce una patología específica y
reconocible, así que el método funciona al revés: por el síntoma se llega a la
función.

| | función | qué hace | si falta |
|---|---|---|---|
| **S1** | **ejecución** | produce lo que el sistema entrega | no hay partes separables; todo depende de todo |
| **S2** | **coordinación** | evita que las partes oscilen entre sí | las partes se estorban y nadie sabe por qué |
| **S3** | **regulación** | gobierna, asigna, decide qué entra | las reglas existen pero nada las aplica |
| **S3\*** | **auditoría** | mira por una vía propia lo que el canal normal no reporta | solo se ve lo que el sistema de reportes fue diseñado para ver |
| **S4** | **anticipación** | mira afuera y adelante | el sistema reacciona, nunca prevé |
| **S5** | **clausura** | fija la identidad: qué es y qué no es este sistema | nadie puede decidir si algo pertenece |
| **A** | **corte** | interrumpe al cruzarse un umbral, sin pedir permiso | un daño en curso espera a que alguien lo discuta |

### Regla central

> **Un principio que nadie bloquea no es un principio: es una preferencia.**

De ahí se derivan tres clases, y **la clase no se declara: se deriva**.

- **bloqueable** — existe un mecanismo que recorre el conjunto completo y
  **rechaza**. No «avisa», no «hace visible»: rechaza.
- **aspiracional** — no hay tal mecanismo, o hay uno que solo produce
  visibilidad. Se enuncia igual, pero marcado.
- **decisión por caso** — exige juicio por diseño, y el mecanismo solo puede
  exigir que la decisión quede registrada.

### Cómo se deriva la clase: variedad requisita

Un mecanismo contiene un flujo de cambios solo si su variedad iguala la del
flujo. Preguntas que deciden:

1. **¿Qué flujo absorbe?** Nómbralo. Si no se puede nombrar, no hay mecanismo.
2. **¿Lo recorre completo?** Una lista escrita a mano tiene la variedad de la
   lista: exactamente los casos que alguien anticipó. Lo demás pasa sin ser
   visto.
3. **¿Rechaza o solo informa?** Visibilidad sin camino declarado a una decisión
   es el punto donde la variedad se pierde: el problema se detectó y nadie se
   enteró.
4. **¿Exige que alguien se acuerde?** Entonces es aspiracional. Lo que depende
   de la memoria de una persona se evapora cuando esa persona se va.

**Un error frecuente y grave**: declarar «bloqueable» algo que solo produce
visibilidad. Promete una garantía que no existe, y quien construye encima cree
estar protegido.

---

## Tres antipatrones que vas a encontrar

**Existencia como prueba.** Un documento, una lista o una capa existen, y su
sola existencia se toma como evidencia de que la función está cubierta. Pero
nada verifica que siga siendo cierto. Un inventario escrito a mano envejece en
silencio y conserva su autoridad mientras miente.

**Estándares sin mecanismo.** Las reglas están escritas, son correctas, y nada
las aplica. Se cumplen mientras alguien recuerda; se degradan sin que se note,
porque el documento sigue ahí diciendo lo contrario.

**Salud prestada.** El sistema parece sano porque su autor lo sostiene con
atención continua. La medición honesta pregunta: *si esta persona se va mañana,
¿qué se degrada y en cuánto tiempo?*

---

## Tu veredicto

Para la función que te toque, decides **una** de estas:

- **AUSENTE** — nadie la cumple. Nombra la patología que eso produce ya hoy.
- **PRESENTE SIN MECANISMO** — alguien la cumple a mano, o un documento la
  declara y nada la verifica. Es el caso más común y el más engañoso: parece
  cubierta.
- **PRESENTE Y BLOQUEABLE** — hay un mecanismo que recorre el conjunto y
  rechaza. Dilo solo si puedes nombrar qué rechaza y cómo.

Cada veredicto necesita **evidencia citada**: una ruta de archivo, un número de
línea, una cifra de los archivos de evidencia. Una afirmación sin cita no entra.

### Cómo se juzga tu trabajo

No se premia aprobar. Un diagnóstico que dice «todo bien» no sirve para nada:
el sistema tiene 5 ciclos entre paquetes y 91 imports escondidos dentro de
funciones, así que algo falta por fuerza.

Tampoco se premia inventar. Si la evidencia no alcanza para sostener un
veredicto, **dilo**: «no hay evidencia suficiente para decidir» es una respuesta
válida y útil.

Lo que se premia es encontrar el lugar exacto donde una función se está
cumpliendo por atención humana y nadie lo ha declarado.
