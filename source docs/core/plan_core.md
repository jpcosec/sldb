Sí. Lo más importante que falta no es otro UML, sino una **especificación normativa del kernel**: qué significa cada operación, qué invariantes existen y qué comportamiento debe ser idéntico entre implementaciones.

# Plan de implementación

## Fase 0 — Especificación

Antes de programar:

* modelo canónico;
* identidad de nodos;
* semántica de aristas;
* operaciones primitivas;
* canonicalización;
* cálculo de hashes;
* reglas de revisión;
* conflictos;
* provenance;
* capabilities.

**Criterio de salida:** poder describir manualmente una transacción completa y su resultado exacto.

---

## Fase 1 — Kernel mínimo en memoria

Implementar:

```text
Document
Node
Edge
Revision
Transaction
Operation
MemoryStorage
TransactionEngine
```

Sin Lisp, archivos externos, embeddings ni plugins.

Debe soportar:

* crear documento;
* agregar y reemplazar nodos;
* conectar nodos;
* generar revisiones;
* consultar revisiones pasadas;
* producir un diff.

**Criterio de salida:** todas las invariantes funcionan en memoria.

---

## Fase 2 — Persistencia y Merkle

Agregar:

* `StorageBackend`;
* redb o CozoDB;
* transaction log;
* content-addressed storage;
* document heads;
* BLAKE3;
* invalidación perezosa;
* recuperación después de crash.

**Criterio de salida:** cerrar y abrir el proceso produce exactamente el mismo estado e historial.

---

## Fase 3 — Primer tipo documental

Elegir solo Markdown.

```text
Markdown
→ parser
→ AST canónica
→ revisión
→ renderer
→ Markdown
```

Implementar:

* parser;
* canonicalizer;
* renderer determinista;
* nodos estructurales;
* source spans;
* comentarios y metadata;
* round-trip.

**Criterio de salida:**

```text
canonicalize(parse(render(C))) == C
```

---

## Fase 4 — CLI y UX de desarrollo

Antes de hacer una UI gráfica, crear una UX de inspección sólida:

```bash
kernel init
kernel import report.md
kernel tree report.md
kernel query '(descendants section-id)'
kernel diff rev1 rev2
kernel history report.md
kernel explain node-id
kernel transact changes.lisp --dry-run
kernel render report.md
kernel verify report.md
```

Funciones críticas:

* `--dry-run`;
* diff antes de commit;
* historial;
* provenance;
* explicación de hashes;
* visualización de errores;
* inspección de operaciones Lisp expandidas.

---

## Fase 5 — Lisp

Integrar Steel detrás de una interfaz propia.

Primero soportar:

```text
QueryPlan
TransactionPlan
```

Después:

```text
ProjectionPlan
EffectPlan
Macros
```

La UX debe permitir ver la expansión:

```bash
kernel lisp expand transformation.scm
kernel lisp compile transformation.scm
kernel lisp run transformation.scm --dry-run
```

**Criterio de salida:** ninguna expresión Lisp puede saltarse el motor de transacciones.

---

## Fase 6 — Proyecciones

Agregar:

* AST estructural;
* grafo semántico;
* JSON canónico;
* Markdown;
* vista para agentes;
* UI tree view.

Cada proyección debe registrar:

```text
revision
projection spec
engine version
source hash
result hash
```

---

## Fase 7 — Semántica

Separar dos subsistemas:

### Semántica continua

* embeddings;
* similitud;
* segmentación;
* índices vectoriales.

### Semántica lógica

* hechos;
* reglas;
* inferencias;
* operaciones booleanas.

Ambos deben considerarse **datos derivados**, nunca fuente primaria.

---

## Fase 8 — Hooks y agentes

Agregar:

* event bus;
* hook registry;
* capability manager;
* effect outbox;
* Wasmtime;
* adaptador Git;
* subagentes;
* MCP.

Primero efectos locales y simples. Red y ejecución de procesos después.

---

# Plan de UX

## Principios

### 1. Todo cambio debe ser explicable

Antes de aplicar una transacción:

```text
Qué nodos cambia
Qué relaciones agrega
Qué revisión usa como base
Qué capacidades requiere
Qué efectos externos generará
```

### 2. La revisión debe ser visible

La UX siempre debería mostrar:

```text
document
revision
source status
dirty branches
pending effects
conflicts
```

### 3. El usuario opera sobre conceptos

La UX no debería obligar a conocer IDs internos.

```text
"sección Introducción"
"función calculate_total"
"párrafo bajo Resultados"
```

El kernel resuelve eso a `NodeId`, pero debe mostrar cualquier ambigüedad.

### 4. Toda operación peligrosa tiene dry-run

Especialmente:

* escrituras de archivos;
* Git;
* llamadas externas;
* ejecución de procesos;
* invocación de agentes;
* transformaciones masivas.

### 5. La UI es una proyección

La interfaz gráfica no debe mantener un modelo paralelo. Debe consumir:

```text
ProjectionResult
QueryResult
TransactionPreview
EventStream
```

---

# Estrategia de testing

## Tests unitarios

Para:

* operaciones primitivas;
* validación de tipos;
* canonicalización;
* hashing;
* resolución de IDs;
* permisos;
* serializers.

## Property-based testing

Usaría `proptest`.

Propiedades importantes:

```text
canonicalize(canonicalize(x)) == canonicalize(x)

parse(render(canonicalize(x))) == canonicalize(x)

hash(x) == hash(x)

replay(log) == current_state

applying_invalid_transaction leaves state unchanged
```

## Golden tests

Guardar documentos y outputs esperados:

```text
fixtures/
├── markdown/
│   ├── input.md
│   ├── canonical.sexp
│   ├── rendered.md
│   └── graph.json
```

Sirven para detectar cambios accidentales de formato.

## Fuzzing

Usaría `cargo-fuzz` para:

* parsers;
* Lisp reader;
* canonicalizer;
* deserialización;
* operaciones malformadas;
* documentos parcialmente corruptos.

## Model-based testing

Crear un modelo simple en memoria y comparar su comportamiento con redb o CozoDB.

```text
ReferenceModel
       vs
ProductionKernel
```

Especialmente útil para transacciones e historial.

## Tests de concurrencia

Casos:

* dos commits sobre la misma revisión;
* cambios independientes;
* reemplazo y eliminación simultáneos;
* conflictos semánticos;
* compare-and-swap fallido;
* retries.

Usaría `loom` para partes concurrentes delicadas.

## Tests de crash recovery

Simular caídas:

```text
después de escribir el log
antes de escribir la revisión
antes de actualizar head
después de ejecutar un efecto
```

El resultado debe ser un estado consistente y recuperable.

## Tests de seguridad

* hook sin capabilities;
* plugin intentando acceder a otro directorio;
* efecto duplicado;
* replay de evento;
* Lisp intentando invocar primitivas internas;
* resource exhaustion;
* ciclos maliciosos en el grafo.

## Tests de rendimiento

Benchmarks con `criterion`:

* importar documento;
* modificar una hoja;
* recalcular rama Merkle;
* consultar subgrafo;
* renderizar;
* hacer diff;
* reconstruir índices;
* replay del log.

---

# Documentos que faltan

## Imprescindibles

```text
README.md
ARCHITECTURE.md
KERNEL_SPEC.md
DATA_MODEL.md
TRANSACTIONS.md
CANONICALIZATION.md
PROJECTIONS.md
EXTERNAL_INTERFACES.md
SECURITY.md
TESTING.md
ROADMAP.md
```

## Muy recomendables

```text
LISP_LANGUAGE.md
QUERY_LANGUAGE.md
HOOKS_AND_EFFECTS.md
PROVENANCE.md
CONFLICTS_AND_MERGING.md
STORAGE_FORMAT.md
SCHEMA_EVOLUTION.md
PLUGIN_SYSTEM.md
UX_GUIDELINES.md
OPERATIONS.md
CONTRIBUTING.md
```

## Registros de decisiones

Agregar una carpeta:

```text
docs/adr/
├── 0001-canonical-graph.md
├── 0002-lisp-as-metalanguage.md
├── 0003-append-only-transactions.md
├── 0004-lazy-merkle.md
├── 0005-ports-and-adapters.md
└── 0006-effects-outside-transactions.md
```

Los ADR explican por qué se tomó cada decisión y qué alternativas se descartaron.

---

# El documento principal que falta

## `KERNEL_SPEC.md`

Debe ser normativo, no explicativo.

Debería definir:

1. Tipos fundamentales.
2. Identidad de nodos.
3. Semántica de cada arista.
4. Operaciones válidas.
5. Orden de validación de una transacción.
6. Construcción de revisiones.
7. Algoritmo de canonicalización.
8. Algoritmo exacto de hashing.
9. Manejo de referencias y ciclos.
10. Conflictos y merges.
11. Provenance.
12. Versionado de schemas.
13. Semántica de efectos.
14. Códigos de error.
15. Compatibilidad entre versiones.

Este documento permitiría reimplementar el kernel en otro lenguaje y obtener el mismo comportamiento.

# Estructura documental recomendada

```text
docs/
├── architecture/
│   ├── ARCHITECTURE.md
│   ├── diagrams/
│   └── adr/
├── specification/
│   ├── KERNEL_SPEC.md
│   ├── DATA_MODEL.md
│   ├── TRANSACTIONS.md
│   ├── CANONICALIZATION.md
│   └── STORAGE_FORMAT.md
├── extension/
│   ├── LISP_LANGUAGE.md
│   ├── PLUGIN_SYSTEM.md
│   └── HOOKS_AND_EFFECTS.md
├── interfaces/
│   ├── EXTERNAL_INTERFACES.md
│   ├── CLI.md
│   └── API.md
└── development/
    ├── ROADMAP.md
    ├── TESTING.md
    ├── BENCHMARKS.md
    └── CONTRIBUTING.md
```

El orden correcto sería: **especificación → kernel en memoria → persistencia → Markdown → CLI → Lisp → proyecciones → semántica → efectos y agentes**. Esto reduce el riesgo de construir mucha infraestructura sobre un modelo canónico todavía inestable.

