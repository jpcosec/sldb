REFORMULACION
ROOT es un agregado (PK01–PK04), no ejecutable: termina cuando cierran sus hijos. Encargo: que sldb evalúe reglas declaradas sobre documentos, aristas y hashes, con explicación e incremental, sin persistir resultados; deskops autora las reglas. Resultado: cuatro paquetes en orden (fundamentos, sustrato, reglas y anclas, operación). Repo dueño: sldb. Límites: sin auth, sin hechos externos, sin tocar deskops, sin motor externo; G_CONSUMER queda fuera.

AMBIGUEDADES
1. "una regla de ejemplo con cuantificador sobre relación y un ancla doc: con hash de contrato evaluadas por sldb desde la CLI con envelope y explicación": ningún hijo declara producir ese ejemplo conjunto; GO05/GO06/GO07 cubren piezas separadas. Obligaría a inventar qué nodo lo entrega y su fixture.
2. "--where antiguo deprecado con aviso" frente a PK02 "where_parse y FieldCondition marcados deprecados con tests de equivalencia": no se fija si el aviso es requisito verificable. Obligaría a inventar su criterio de aceptación.

DRY-RUN (hipotético, sin ejecutar)
PK01: GO01 registra la frontera → GO02 fija semántica y gramática (entrega rules-language.md y tests; G_SEMANTICS exige D6) → GO03 fija GraphBackend y networkx (entrega protocolo e implementación sin cambiar salidas; G_SEAM exige D5). Transfiere a PK02 semántica aceptada y costura.
PK02: GO04 proyecta payload y corrige staleness (entrada: índice actual; salida: nodos con campos) → GO05 implementa el lenguaje de GO02 sobre GO04 (salida: --where nuevo sin re-extraer; any/all con explicación; deprecación con tests de equivalencia). Transfiere lenguaje y proyección a PK03.
PK03: GO06 define RuleDoc y rules check (salida: findings con severidad y cláusula fallida) → GO07 define ancla doc: con hash de contrato (salida: anchors check intact/changed/lost). Transfiere reglas y anclas a PK04.
PK04: GO08 evalúa en escritura y transición, incremental (salida: error rechazado con explicación; alerta no falla) → GO09 lleva el efecto a la arista (salida: edges_holding lee attributes; edges check valida condiciones).
Validación conjunta: hijos cerrados; G_SEMANTICS y G_SEAM satisfechos; ejemplo end-to-end por CLI con envelope y explicación; --where deprecado con aviso; CHANGELOG y docs/architecture al día. G_CONSUMER no bloquea.

FUTURO
El dueño confirma D5 y D6 (habilitan G_SEAM y G_SEMANTICS); deskops produce G_CONSUMER en su plan; la promoción de hijos usa deskops add task; el TaskDoc fija nombres de archivos/funciones/tests; la validación corre en robocop2.
