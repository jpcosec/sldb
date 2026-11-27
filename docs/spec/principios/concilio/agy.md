# Crítica del concilio: fundamentos y declaración de sistema (agy)

## 1. Qué sigue mal o forzado en fuentes y principios

- **Zettelkasten:** Mezcla "dirección estable" con "identidad estable": las fichas de Luhmann tenían identidad ligada a un lugar fijo en el cajón (`21/3d7`), justo lo que `sldb` separa del archivo. Además cita "pocos puntos de entrada" (el registro) y no lo usa en ningún principio.
- **Autopoiesis:** Reduce un cierre operacional de componentes a "observarse y disparar acciones". Peor: atribuye a Maturana el principio de autoridad ("todo lo dicho es dicho por alguien"), cuando el observador explica quién distingue algo, no cómo se valida un cálculo ni quién tiene autoridad para cerrar una duda.
- **Doyle (errata y hueco):** La ficha dice que explica cómo opera "el principio 6", cuando el principio de sostener creencias es el **7**. Además Doyle exige distinguir apoyos *independientes* de apoyos derivados de la misma causa; P7 no lo dice.
- **P1:** Junta dos ideas distintas: que el valor sale de las relaciones y que "que dos cosas sean la misma es una relación declarada". La segunda pertenece a identidad/contexto (P2), no al valor relacional.
- **P3:** Sostiene que el afuera "perturba pero no instruye", pero el sistema copia contenido afuera→adentro al observar y proyecta cambios adentro→afuera al editar. Además P3 rechaza "exigir que todo pase por él", pero no explica cómo convive eso con editar desde adentro.
- **P5:** Dice que los tipos salen de lo que entró ("no se parte de una lista de tipos") y atribuye los modelos a "parecido de familia". Doble error: (a) estructura idéntica más herencia, polimorfismo y composición es clasificación clásica por rasgos comunes, lo contrario del parecido de familia; (b) prohíbe modelos previos cuando en la práctica los equipos sí declaran esquemas antes de recibir documentos.
- **P6:** Pone en el mismo plano a "una persona, un agente o un cálculo", sin distinguir observación automática, sugerencia estadística y declaración con autoridad.
- **P7:** Empaqueta cuatro reglas separadas: propagación de apoyos, grados de certeza, "dejar firme otra zona para dudar" (sin uso operativo) y "adentro no se borra". No borrar es una regla de historia y trazabilidad, no consecuencia de sostener creencias: en Doyle una creencia sin apoyo pasa a inactiva (`OUT`), no exige conservarse para siempre.
- **P8:** "Nadie ve la red entera" no implica ni "preguntar no cambia la red" ni distinguir "no hay" de "no se miró". Falta además exigir que toda respuesta muestre sus apoyos.

## 2. Contradicciones y huecos entre `fundamentos.md` (N1) y `README.md` (N2)

- **Nodos como cosas vs. hechos (P1 vs. README):** P1 dice "hechos, no cosas". El README dice: *"Un nodo es una cosa de la que se sabe algo"* y *"Lo que el párrafo dice está en su nodo"*. O el nodo es un punto relacional sin esencia propia, o es un contenedor de contenido.
- **Grafo como proyección vs. única sede de identidad (P2/P3 vs. README):** El README llama al grafo *"otra forma de decir lo mismo, con otras reglas"* (proyección) y a la vez *"lo único que tiene identidad propia"* y lo opone a "cómo se la muestra (proyección)". Si el grafo es una proyección más, no puede ser el sustrato único de identidad y significado.
- **Quién manda: el afuera o la red (P3 vs. README):** P3 afirma *"el afuera perturba pero no instruye"*. El README responde *"Cuando difieren, vale el archivo"* / *"Sobre lo que se observó manda el archivo"*. Si el archivo sobrescribe lo observado, el afuera sí instruye al adentro.
- **Tipos emergentes vs. modelos prescriptivos (P5 vs. README):** P5 dice *"No se parte de una lista de tipos"*. El README dice *"el modelo... dice qué tomar al entrar"*, *"con él se comprueba"* y *"El equipo declara qué campos tiene una tarea"*. Eso es tipado previo obligatorio.
- **Sistema activo vs. sistema pasivo (P4 vs. README):** P4 exige un sistema que actúa sobre sí mismo y corrige faltas. El README deja las acciones y hooks en *"Lo que falta decidir"* y afirma que ante un cambio *"lo ve quien revisa, y lo resuelve anclando de nuevo"*.
- **Frases del README sin principio en `fundamentos.md`:**
  1. *"sldb no trae [tipos de dominio]... Eso lo declara cada proyecto"* (l.214–216): presentado como consecuencia de P5, pero que los tipos emerjan no impide que `sldb` traiga tipos propios; falta el principio de separación entre mecanismo genérico y dominio.
  2. *"lo que sldb calculó... se puede borrar y rehacer"* (l.197–198): choca con *"adentro no se borra"* (P7) porque `fundamentos.md` no separa datos declarados/observados de cálculos descartables.
  3. *"si [una regla] es del grafo... vale lo mismo por cualquier puerta"* (l.206–207): ningún principio exige unicidad de reglas entre vías de entrada.
  4. *"si alguien tocó otra parte del archivo, eso se conserva; si tocó la misma, hay un choque"* (l.126–127): aunque editar sea nivel 2, ninguna regla en N1 prohíbe perder datos ajenos ni pisar conflictos.

## 3. Qué falta que decida un caso real

1. **Separar lo declarado/observado de lo calculado (de Doyle / Luhmann):** Todo cálculo es descartable y sin autoridad; lo declarado a mano nunca puede vivir solo en un índice reconstruible. *Caso que decide:* rechaza guardar relaciones de equivalencia curadas dentro de una caché que se regenera desde cero.
2. **Fuerza ilocucionaria / rol epistémico del hecho (Wittgenstein, *Investigaciones* §23):** Un mismo texto ("el precio incluye el impuesto") funciona distinto si es **observación**, **requisito normativo** o **decisión aceptada**. P6 solo dice quién lo dijo. *Caso que decide:* si el código no incluye el impuesto, decide si el párrafo desactualizado queda en duda (observación) o si el código falla una regla (requisito).
3. **Mecanismo genérico sin dominio propio:** `sldb` no conoce qué es una tarea ni una norma de diagramas. *Caso que decide:* rechaza incrustar lógica o rutas del flujo propio de un equipo dentro del motor genérico.
4. **No perder datos ni pisar lo ajeno (preservación):** Complementa P7 ("adentro no se borra") hacia afuera y hacia la edición. *Caso que decide:* rechaza que una operación borre trabajo concurrente en otra parte del archivo o aplaste una edición en conflicto sin mostrarla.

## 4. Prueba concreta por principio

- **P1 (valor relacional):** Decide unificar "función del precio" y "párrafo" en una red consultable de dependencias en vez de guardar metadatos aislados por archivo; su segunda frase ("equivalencia declarada") rechaza fusionar dos nodos llamados "precio" en carpetas distintas (pero eso pertenece a P2).
- **P2 (reglas entre signo y símbolo):** Decide rechazar cualquier extracción o vista sin reglas explícitas que digan qué toma y qué conserva, evitando igualar coincidencia de nombres con identidad.
- **P3 (adentro/afuera):** Decide aceptar archivos editados por fuera con herramientas comunes y no exigir que el proyecto meta sus fuentes en un formato propietario de `sldb`.
- **P4 (actuar y cierre):** La segunda mitad (reglas/modelos como nodos) decide que una regla anclada a una función que cambió quede en duda igual que cualquier afirmación. La primera mitad ("el sistema actúa") **no decide ningún caso concreto de diseño por sí sola** sin definir qué es un hook, qué puede tocar y quién autoriza cambios.
- **P5 (tipos desde lo que entró):** Decide aceptar un documento libre sin esquema previo y separar la clasificación por forma (secciones) de la clasificación por significado (rol en el texto).
- **P6 (observador/autor):** Decide rechazar una relación inferida por similitud automática como si fuera una declaración humana vigente y obliga a registrar quién o qué la produjo.
- **P7 (sostener creencias):** Decide no tumbar una afirmación cuando cae solo uno de dos apoyos independientes, y conservar el nodo como movido/sin apoyo en lugar de borrarlo en cascada al desaparecer su fuente.
- **P8 (consulta):** Decide prohibir que una lectura modifique la red y obligar a distinguir "0 resultados verificados" de "no pude mirar esa zona".

## 5. Ataque en serio a P2 y P4

### Contra P2 ("El texto es signo. El grafo es símbolo... Y el grafo tampoco es 'la cosa misma': es también una proyección")
- **Incoherencia interna:** En tres líneas P2 dice que el grafo *es el símbolo* y luego que el grafo *es también una proyección como el texto*. Si ambos son proyecciones con sus reglas, falta decir qué es aquello común que ambos proyectan: hoy P2 deja el símbolo vacío y el README termina dando "identidad propia" al grafo, contradiciendo que sea solo una proyección más.
- **Simetría falsa entre origen y vista:** Decir que texto y grafo son dos proyecciones paralelas borra la diferencia entre una *fuente autorada afuera* (que nació como texto libre sin reglas del grafo, y manda sobre lo observado) y una *vista generada desde el grafo* (donde sí cabe exigir "comprobar volviendo"). Exigir que toda proyección "vuelva" al otro lado confunde extraer de una fuente con round-trip de vistas.
- **Límite del ejemplo del paper:** Volver desde el texto al grafo bajo un extractor solo prueba que ese extractor recupera esas tripletas; no prueba equivalencia semántica ni detecta omisiones o inventos fuera de las reglas del extractor.

### Contra P4 ("El sistema actúa, también sobre sí mismo")
- **No pasa la prueba de fundamento:** Si `sldb` solo siente perturbaciones, calcula consecuencias y expone qué quedó en duda para que otro actor o herramienta actúe, sigue siendo `sldb`. Hacer obligatorio que "dispare acciones" lo convierte en ejecutor/agente antes de haber definido siquiera qué es un hook (que el propio README deja abierto).
- **Confunde cierre representacional con auto-modificación:** Representar reglas, modelos y vistas como nodos dentro de la misma red (para que apliquen P1, P6, P7 y P8) es necesario y legítimo; pero que el sistema *actúe modificándose a sí mismo* ("si falta un modelo, se detecta y se corrige; si se mide el desorden, se puede ordenar") rompe P6 y P3: ¿con qué autoridad crea modelos o reordena nodos sin una persona que declare el criterio, y qué impide que reescriba su propia organización?
- **Choca con P5:** Si los tipos emergen de lo que entró y no hay modelos previos obligatorios, no tiene sentido detectar "falta un modelo" como defecto que el sistema deba corregir automáticamente.
