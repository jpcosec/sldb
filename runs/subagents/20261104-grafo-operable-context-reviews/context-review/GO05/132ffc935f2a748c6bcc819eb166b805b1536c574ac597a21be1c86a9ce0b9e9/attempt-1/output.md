REFORMULACION

Propósito: implementar en sldb el parser y evaluador único del lenguaje fijado por GO02, sobre la facet payload de GO04 y el backend de GO03: booleanos completos, caminos con cuantificadores, clausura transitiva, sustitución desde el sujeto, `incomplete` en el borde de links y explicación estructurada. Resultado: una API única detrás de `where_matches`, `edges_holding`, `StructuredQuery` y `--where`, con goldens de compatibilidad, `where_parse` y `FieldCondition` como shims deprecados, tests de GO02 verdes, CLI con envelope y `--explain`, documentación y CHANGELOG. Repo dueño: sldb. Límites: no retira los shims (GO10), no altera resultados existentes, no autentica actores ni produce hechos externos. Es un nodo de entrega, no un agregado.

AMBIGUEDADES

Ninguna.

DRY-RUN

Un ejecutor futuro leería `docs/architecture/rules-language.md` (GO02), el protocolo `GraphBackend` (GO03), la proyección y `contract_signature` (GO04), `docs/cli-envelope.md` y el código actual de `where_parse`, `FieldCondition`, `where_matches`, `edges_holding` y `StructuredQuery`. Como primer paso capturaría goldens de cada expresión de la tabla de GO02 con los parsers actuales. Luego construiría parser/AST y evaluador en `store/graph/language/`, los shims con `DeprecationWarning`, el enrutado de `api/where.py`, `edges_holding` y CLI, y los tests de equivalencia, spec, cero `Validator.extract`, aviso y envelope. Dependencias: GO02 y GO04; G_SEAM llega transitivamente vía GO03←GO04. Validaciones futuras: pytest, `sldb docs find --where` con `any()/all()` y `--explain`, conteo de extracciones, captura de warning y entrada en `warnings`, revisión de docs/CHANGELOG.

FUTURO

GO06 consumirá parser y findings; GO07 leerá `anchor_state` como campo; GO10 retirará los shims; el desk de sldb acepta la revisión y resuelve G_SEMANTICS/G_SEAM; PK02 valida el conjunto. Nada de esto se ejecuta aquí.
