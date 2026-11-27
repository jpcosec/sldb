# Metodología para destilar los principios fundantes de sldb

Clase de página: mecanismo del spec. Aprobada por JP el 2026-11-27. Las fichas de los pasos 1 a 3 están en `fichas/`.

## Contexto

El spec de sldb se estuvo escribiendo sin un núcleo conceptual, y por eso salió mal: se partió de
los comandos hacia adentro y se llegó a definir sldb como "un grafo de documentos Markdown". JP
pidió destilar los principios fundantes para evaluar con ellos el resto del spec. El método tiene
que leer kimun, leer este repo (Markdown, specs viejos, contratos), entender las capacidades, y
sacar **el cómo tiene que ser** separado del **cómo es**.

Resultado esperado: una página corta de principios (el "core conceptual" o whitepaper), cada uno
con su origen y su evidencia, que sirva para aceptar o rechazar lo que diga el spec.

## Qué cuenta como principio

Una afirmación es principio solo si pasa las cuatro pruebas:

1. **Si cambia, sldb deja de ser sldb.** Es el criterio con que kimun escribió su núcleo.
2. **No depende de la implementación.** Sobrevive a pasar de Python a Clojure y de archivos a
   Postgres. Si no sobrevive, es un mecanismo, no un principio.
3. **Permite rechazar algo.** Tiene que decidir al menos un caso real. Es el criterio del
   contrato de identidad del repo ("en términos que permitan rechazar").
4. **JP lo dijo o lo confirma.** Lo que solo infiere un agente queda como candidato.

## Fuentes, por orden de autoridad

Una fuente de más abajo no puede contradecir a una de más arriba; si lo hace, es un conflicto
que se lista, no se resuelve solo.

| Orden | Fuente | Dónde |
|---|---|---|
| 1 | Palabras de JP, textuales y con fecha | `sala/2026-11-25-planificacion/sldb.md`; citas entre «» en kimun (`docs/v2/drafts/sesion-*.md`, `fuentes-identidad.md`) |
| 2 | Núcleo de kimun | `~/proyectos/kimun/docs/v2/00-nucleo.md`, `14-juego-del-lenguaje.md`, `01-orden-filosofico.md` |
| 3 | Contratos declarados de sldb | `contracts/identity.toml`, `contracts/layers.toml`, `AGENTS.md` del repo y del workspace |
| 4 | Decisiones aceptadas | ADR con estado aceptado en `docs/architecture/`; lo fijado en `docs/spec/decisiones/` |
| 5 | Propuestas, specs viejos y borradores | `propuesta/` (16 documentos), `docs/*.spec.yaml`, `docs/target_architecture.md`, `desk/drawer/plans/`, resto de `docs/` (125 documentos) |
| 6 | Átomos del desk | `desk/atoms/` (123) |
| 7 | Código y tests | `src/sldb`, `tests/` |

El código dice cómo es, nunca cómo tiene que ser. Un documento viejo no tiene autoridad por
existir: vale solo si cita a JP, si es una decisión aceptada, o si se comprueba contra el código.

Fuera del alcance salvo que algo de arriba lo cite: `kimun/docs/archive/` (809 documentos) y
`kimun/runs/research/` (148).

## Pasos

### 1. Inventario de fuentes

Una tabla con cada documento: fecha, quién lo escribió, estado (vigente, reemplazado, sin
verificar) y a qué orden de autoridad pertenece. Aquí se marca lo que es documentación vieja o
relleno, antes de leerla como si valiera.

### 2. Extraer afirmaciones, sin interpretar

De cada fuente se sacan fichas. Una ficha tiene: la afirmación, la cita con archivo y línea,
quién la dice (JP, concilio, agente), la fecha, y de qué tipo es (principio candidato, decisión,
mecanismo, hecho de implementación). Se buscan definiciones ("sldb es…"), obligaciones ("nunca",
"siempre", "debe") y razones ("porque", "para que"). Las razones valen más que las reglas: un
principio suele estar en el porqué de una decisión.

### 3. Leer las capacidades desde el código

Lista de lo que el sistema sabe hacer, partiendo de lo que ya existe: los 32 ejes de
`contracts/layers.toml` con su campo `does`, y lo que mide `tools/check_axes.py`. Para cada
capacidad, una pregunta: ¿qué principio la justifica?

De ahí salen dos listas que son lo más útil del método:

- **Capacidad sin principio**: está implementada y nada dice por qué. O es un accidente, o falta
  nombrar un principio.
- **Principio sin capacidad**: está dicho y no existe. Ejemplo conocido: el ancla a un resultado
  ejecutado.

### 4. Separar el "es" del "tiene que ser"

Cada candidato pasa por las cuatro pruebas de arriba. Lo que no pasa la segunda baja a
mecanismo. Lo que no pasa la tercera se corta. Lo que no pasa la cuarta queda como candidato
para JP.

### 5. Cruzar con kimun

Cada principio se marca como: igual a una proposición del núcleo de kimun (con su número),
propio de sldb, o en conflicto con kimun. La regla ya fijada es que la lógica del kernel es la de
kimun, así que un conflicto se lleva a JP, no se decide.

### 6. Contradicciones y huecos

Lista de lo que las fuentes dicen distinto entre sí y de lo que ninguna dice. De aquí salen las
preguntas a JP: solo las reales, de a una.

### 7. Redactar

Una página, en proposiciones numeradas como el núcleo de kimun, donde cada número decimal comenta
al anterior. Cada proposición lleva su origen. Aparte, un anexo con la tabla de fichas que la
sostienen. Va en `docs/spec/principios/`, como clase nueva de página de la wiki.

Tres rondas, como hizo kimun: borrador, crítica de un agente independiente que recibe las fichas
y no mis conclusiones, y revisión.

### 8. Probar los principios contra casos reales

Antes de darlos por buenos se usan para decidir casos que ya conocemos: las 17 páginas de objeto,
el reparto de anillos, y defectos concretos (`docs update` sin reglas, la dirección por posición,
los padres de tags en la caché). Un principio que no decide ningún caso se corta. Un caso que
ningún principio decide señala un principio que falta.

### 9. Aprobación

JP revisa la página. Hasta entonces todo es candidato. Lo aprobado pasa después a átomos del
desk, que es la pieza que el workspace ya tiene para conocimiento durable.

## Cómo se reparte el trabajo

- **Pasos 1 a 3**: subagentes baratos en paralelo, uno por grupo de fuentes (kimun; contratos y
  ADR; `propuesta/` y specs viejos; resto de `docs/` y átomos; capacidades desde el código). No se
  pisan porque cada uno lee un grupo distinto y solo devuelve fichas.
- **Pasos 4 a 7**: los hago yo, con las fichas a la vista. La crítica la hace un agente aparte.
- **Paso 8**: yo, y es donde se ve si el método sirvió.
- **Pasos 6 y 9**: JP.

## Reglas del método

- Las palabras de JP se citan textuales y con fecha. No se parafrasean hacia algo más fuerte.
- Una idea que a JP le gustó no es una decisión.
- Todo lo que sea inferencia de un agente se marca como tal.
- Ningún subagente recibe mis conclusiones; recibe las fuentes y el formato de ficha.
- No se edita ni se borra documentación vieja en esta pasada: solo se clasifica.

## Qué queda en pausa mientras tanto

- El refactor por anillos: el subagente dejó la primera etapa escrita en su worktree, sin
  commitear, y se detuvo con el modo plan.
- El contrato de la puerta de persistencia y de grafo.

## Verificación

El método funcionó si al final hay: (a) una página de principios donde cada uno pasa las cuatro
pruebas y tiene origen; (b) las dos listas del paso 3; (c) la lista de contradicciones; y (d) el
paso 8 muestra que los principios deciden los casos conocidos sin ayuda.

## Criterio 5W1H+ (JP, 2026-11-27)

Con las preguntas de los átomos del desk: los principios rectores son en su mayoría el **por
qué** y el **qué**. El resto del spec (objetos, operaciones, mecanismos) es el **cómo** y el
**dónde**. Se pueden cruzar, pero una afirmación que solo contesta cómo o dónde no va en la
página de principios: va en el spec, colgada del principio que la justifica.
