## REFORMULACION
ROOT es un nodo agregado de planificación, no ejecutable, del repo `sldb`. Su propósito es que sldb evalúe por sí mismo reglas declaradas sobre documentos, aristas y hashes, con explicación e incrementalidad, sin persistir resultados; deskops autora las reglas. El resultado sustantivo es integrar cuatro paquetes: fundamentos (decisión, semántica, costura de backend), sustrato (payload proyectado y lenguaje de predicados), reglas y anclas (`RuleDoc`, anclas `doc:` con hash de contrato) y operación (evaluación en escritura/transición/check, transiciones como datos y retiro de lenguajes viejos). Límites: no autentica actores, no produce hechos externos, mundo cerrado solo por store, no persiste derivados, no modifica deskops y no adopta otro motor en esta fase. ROOT cierra cuando cierran sus hijos y se satisfacen sus gates; no se promueve ni ejecuta como tarea.

## AMBIGUEDADES
Ninguna. Los gates `pending` son intencionales y `G_CONSUMER` queda explícitamente fuera del cierre.

## DRY-RUN
Hipotético, sin ejecutar. Se leerían `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md`, los scopes/aceptaciones de PK01–PK04 y la evidencia de gates. ROOT no cambia archivos; sus hijos escribirían en `src/sldb`, tests, `docs/architecture/` y `CHANGELOG`.

Entradas/salidas entre hijos:
- **PK01**: registra la decisión, fija semántica/gramática/firma de evaluación y define `GraphBackend` con networkx; entrega `G_BOUNDARY`, `G_SEMANTICS`, `G_SEAM`.
- **PK02**: recibe esa base; proyecta payload al grafo, corrige staleness e implementa el lenguaje nuevo con shims deprecados y goldens de equivalencia.
- **PK03**: recibe lenguaje y proyección; entrega `RuleDoc`/`rules check` y anclas `doc:`/`anchors check`.
- **PK04**: recibe `GO05`; GO09 puede correr en paralelo con PK03 según el scope de ROOT. Entrega `effects` en `edges_holding`, evaluación en escritura/transición/check, retiro de shims y el ejemplo end-to-end.

Validación conjunta: todos los hijos cerrados; `G_BOUNDARY`, `G_SEMANTICS` y `G_SEAM` satisfechos; test de integración de GO08; incrementalidad probada; aviso de deprecación y retiro verificados; `CHANGELOG` y `docs/architecture` al día.

## FUTURO
GO01 commitea y reemplaza el texto de `G_BOUNDARY`; GO02 y GO03 pasan revisión en frío; GO08 define y prueba el ejemplo end-to-end; GO05 prueba el aviso; GO10 retira los lenguajes viejos; deskops produce `G_CONSUMER` después. El humano/ dueño indica el host de pytest y acepta revisiones.
