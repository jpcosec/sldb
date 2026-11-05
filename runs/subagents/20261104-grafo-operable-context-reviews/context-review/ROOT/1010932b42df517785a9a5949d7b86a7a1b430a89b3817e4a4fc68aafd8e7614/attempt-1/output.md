REFORMULACION

ROOT es un agregado de planificación, no ejecutable. Encargo: que sldb evalúe reglas declaradas sobre documentos, aristas y hashes, con explicación, incremental, sin persistir derivados; deskops autora las reglas. Repo dueño: sldb. Resultado: cuatro paquetes en orden —fundamentos (decisión, semántica, costura), sustrato (payload proyectado y lenguaje único), reglas y anclas (`RuleDoc`, `rules check`, anclas `doc:`), operación (evaluación en escritura/transición/check y transiciones como datos)—. Límites: no autentica actores, no produce hechos externos, mundo cerrado por store, no juzga; no migra a kimun; no cambia deskops salvo nota por canal entre desks; journal y split `.sldb/.sldb_cache` son prerrequisito operativo. Cierra con hijos cerrados, G_BOUNDARY/G_SEMANTICS/G_SEAM satisfechos, ejemplo de GO08 documentado en `rules.md`, aviso de deprecación de GO05 y CHANGELOG/docs al día; G_CONSUMER no bloquea.

AMBIGUEDADES

1. «con explicación, incremental, sin persistir resultados» (scope) frente a una aceptación que no menciona incrementalidad: obligaría a inventar si el cierre exige prueba de incremental/punto fijo o basta el ejemplo end-to-end.
2. «Cuatro paquetes en orden» sin aristas visibles entre PK01–PK04: obligaría a inventar si es secuencia estricta o mera enumeración, y si PK04 puede solaparse con PK03.

DRY-RUN

Sin ejecutar: ROOT no corre; cierra por hijos.
- PK01: GO01 registra D1 y commitea pill/atom/nota → G_BOUNDARY; GO02 fija gramática, semántica y firma de `eval` → G_SEMANTICS (D6); GO03 fija `GraphBackend` (`load`, `eval`) e implementa networkx sin cambiar salidas → G_SEAM (D5). Transfiere decisión, spec y protocolo.
- PK02: GO04 proyecta payload y arregla staleness; GO05 implementa el lenguaje sobre esa proyección y depreca `where_parse`/`FieldCondition` con aviso. Entradas: GO02+GO04. Salida: `--where` sin re-extraer y `any()/all()` con explicación.
- PK03: GO06 define `RuleDoc` y `rules check`; GO07 define ancla `doc:` y estados `intact/changed/lost`. Usan lenguaje y proyección; salen findings y `anchors check`.
- PK04: GO08 evalúa `on_write/on_transition/on_check`, incremental y punto fijo, usando reglas y anclas; GO09 lleva efectos a `attributes`, hace que `edges_holding` los devuelva y `edges check` valide condiciones. Convergen en `edges_holding`. Salida: ejemplo end-to-end.
Validación conjunta: hijos cerrados, gates, ejemplo de GO08 como test documentado, aviso de GO05, CHANGELOG/docs.

FUTURO

El dueño confirma D5 y D6; GO01 commitea la pill/atom/nota; revisores aceptan G_SEMANTICS y G_SEAM; deskops produce G_CONSUMER en su propio plan; cada hijo se promueve con `deskops add task --from-drawer`.
