REFORMULACION
Propósito: planificar que sldb evalúe reglas declaradas sobre documentos, aristas y hashes, con explicación, incremental y sin persistir resultados; deskops autora las reglas. Resultado: cerrar PK01–PK04, satisfacer G_BOUNDARY, G_SEMANTICS y G_SEAM, probar el end-to-end e incrementalidad vía GO08, retirar lenguajes viejos vía GO10 y dejar CHANGELOG/docs al día. Repo dueño: sldb. Límites: no autentica actores, no produce hechos externos, mundo cerrado por store/commit, no juzga calidad; consumo por deskops queda fuera (G_CONSUMER). ROOT es agregado: no se promueve ni ejecuta; cierra cuando cierran sus hijos.

AMBIGUEDADES
1. “CHANGELOG y docs/architecture al día.” No define qué entradas ni qué documentación mínima; obligaría a inventar un criterio de cierre distinto del aceptado por cada hijo.

DRY-RUN
Hipotético, sin ejecutar: no se promueve ROOT; se promoverían y ejecutarían sus hijos. PK01 en serie: GO01 registra/commitea decisión y nota (G_BOUNDARY); GO02 fija gramática, semántica y firma de evaluación (G_SEMANTICS); GO03 define `GraphBackend` (`load`, `eval`) y lo implementa con networkx sin cambiar salidas (G_SEAM). Entrega a PK02: decisión, spec y costura. PK02: GO04 proyecta payload y corrige staleness; GO05 implementa el lenguaje sobre esa proyección y deja shims con aviso. Entrega: consultas sin re-extraer, `any()`/`all()` con explicación y goldens de equivalencia. PK03: GO06 define `RuleDoc`/`rules check`; GO07 define anclas `doc:` y estados; entrega findings y `anchor_state`. PK04: GO09 lleva `effects` a aristas/`edges_holding`; GO08 agrega `findings` y evalúa en escritura/transición/check; GO10 retira shims. Validación conjunta: gates satisfechos, pytest sin rojos ni saltos, envelopes CLI, test end-to-end e incremental de GO08, docs/CHANGELOG, y `effects`/`findings` en claves separadas.

FUTURO
G_CONSUMER lo produce el plan de deskops; la disposición de revisión la escribe quien opera el desk de sldb en `reviews/rN.md`; los TaskDoc fijan nombres exactos e hipótesis ante contratos ausentes.
