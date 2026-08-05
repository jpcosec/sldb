Te dejo una versión inicial de `README.md`, centrada en la arquitectura y sus decisiones.

# Knowledge Kernel

Kernel extensible para almacenar, consultar, transformar y versionar documentos estructurados mediante un grafo inmutable.

El sistema está diseñado para servir como núcleo común para:

* documentos estructurados;
* código fuente;
* reportes;
* agentes;
* interfaces gráficas;
* interfaces de línea de comandos;
* motores semánticos;
* reglas lógicas;
* automatizaciones y herramientas externas.

El kernel se implementa en Rust. Lisp funciona como lenguaje de consulta, transformación y extensión.

---

## Objetivo

El proyecto busca proporcionar una representación canónica para cualquier objeto que pueda expresarse como una estructura sintáctica o semántica.

Un documento puede tener múltiples representaciones:

```text
Archivo Markdown
      ↓
AST sintáctica
      ↓
Grafo canónico
      ↓
├── AST estructural
├── AST semántica
├── vista para agentes
├── interfaz gráfica
├── representación CLI
├── embeddings
└── hechos lógicos
```

Todas estas vistas derivan de una misma revisión inmutable.

---

## Principios de diseño

### 1. El grafo canónico es la fuente de verdad

El kernel no utiliza Markdown, Lisp, Tree-sitter o Pydantic como modelo persistente principal.

La representación canónica está formada por:

```text
Document
Revision
Node
Edge
Transaction
Artifact
```

Los formatos externos se parsean hacia este modelo y se renderizan desde él.

---

### 2. Toda modificación crea una revisión

El estado existente nunca se modifica directamente.

```text
Revision R1
    +
Transaction T1
    ↓
Revision R2
```

Cada revisión conserva:

* su hash raíz;
* la transacción que la produjo;
* sus revisiones padre;
* el actor responsable;
* la versión de los motores utilizados;
* información de provenance.

Esto permite auditoría, comparación, rollback y reproducción.

---

### 3. Lisp es un metalenguaje

Lisp no controla directamente la base de datos.

Las expresiones Lisp se compilan a planes declarativos:

```text
TransactionPlan
QueryPlan
ProjectionPlan
EffectPlan
```

El kernel valida estos planes antes de ejecutarlos.

Ejemplo conceptual:

```lisp
(transaction
  (replace-node section-id
    (section
      :title "Nueva sección"
      :children new-content)))
```

La expresión anterior no muta directamente el grafo. Produce operaciones primitivas que Rust valida y aplica.

---

### 4. Rust protege las invariantes

Rust es responsable de:

* identidad estable;
* tipos;
* validación;
* transacciones;
* control de concurrencia;
* hashing;
* persistencia;
* capacidades y permisos;
* canonicalización;
* aislamiento de efectos.

La separación fundamental es:

```text
Lisp expresa intención.
Rust garantiza consistencia.
```

---

## Modelo de grafo

Un documento no se representa necesariamente como un árbol único.

Las aristas tienen semánticas diferentes:

| Tipo        | Uso                                    |
| ----------- | -------------------------------------- |
| `Ownership` | Estructura jerárquica del documento    |
| `Reference` | Enlaces hacia otros nodos o documentos |
| `Semantic`  | Relaciones conceptuales                |
| `Derived`   | Inferencias, embeddings y análisis     |

Las aristas `Ownership` forman el árbol o DAG estructural.

Las aristas `Reference`, `Semantic` y `Derived` pueden formar grafos más generales.

---

## Modelo de dominio

### Document

Representa una entidad documental estable.

```rust
struct Document {
    id: DocumentId,
    document_type: DocumentType,
    source: Option<SourceRef>,
    current_revision: RevisionId,
}
```

### Revision

Representa un estado inmutable del documento.

```rust
struct Revision {
    id: RevisionId,
    parents: Vec<RevisionId>,
    transaction: TransactionId,
    root_hash: ContentHash,
    created_at: Timestamp,
}
```

### Node

Unidad básica de información.

```rust
struct Node {
    id: NodeId,
    node_type: TypeId,
    payload: PayloadRef,
    metadata: Metadata,
}
```

### Edge

Relación tipada entre nodos.

```rust
struct Edge {
    id: EdgeId,
    source: NodeId,
    target: NodeId,
    edge_type: EdgeType,
    semantics: EdgeSemantics,
    metadata: Metadata,
}
```

---

## Operaciones primitivas

Todas las transformaciones deben compilar a un conjunto pequeño de operaciones.

```text
PutNode
RemoveNode
PutEdge
RemoveEdge
SetDocumentRoot
AttachArtifact
EmitDomainEvent
```

Operaciones de alto nivel como:

```text
Renombrar sección
Mover bloque
Extraer función
Reorganizar capítulo
Aplicar plantilla
```

son macros construidas sobre estas primitivas.

---

## Arquitectura

```text
                        ┌──────────────────────┐
                        │ CLI / UI / Agentes   │
                        └──────────┬───────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ API Rust / IPC / HTTP / Lisp│
                    └──────────────┬──────────────┘
                                   │
        ┌──────────────────────────▼──────────────────────────┐
        │                     Kernel Core                     │
        │                                                     │
        │ Transaction Engine   Query Engine   Projection Engine│
        │ Type Registry        Merkle Engine  Event Bus        │
        └─────────────┬──────────────────────────┬─────────────┘
                      │                          │
          ┌───────────▼──────────┐   ┌──────────▼───────────┐
          │ Storage y revisiones │   │ Hooks y efectos      │
          └──────────────────────┘   └──────────────────────┘
```

---

## Componentes principales

### Transaction Engine

Responsable de:

* validar operaciones;
* comprobar permisos;
* aplicar cambios sobre una revisión base;
* detectar conflictos;
* crear nuevas revisiones;
* actualizar el `head` del documento;
* publicar eventos.

Es el único componente autorizado para crear nuevas revisiones.

---

### Graph Repository

Proporciona acceso al grafo canónico.

Puede utilizar Petgraph como vista materializada en memoria, pero los identificadores internos de Petgraph no deben utilizarse como identidad persistente.

```text
NodeId persistente ≠ petgraph::NodeIndex
```

---

### Projection Engine

Genera vistas derivadas del grafo.

Ejemplos:

* AST estructural;
* AST semántica;
* Markdown;
* JSON;
* HTML;
* interfaz de usuario;
* vista para agentes;
* conjunto de embeddings;
* base de hechos lógicos.

Cada resultado queda asociado a:

```text
Revision
ProjectionSpec
EngineVersion
SourceHash
ResultHash
```

---

### Query Engine

Permite consultar:

* nodos;
* subárboles;
* relaciones;
* revisiones;
* diferencias;
* provenance;
* hechos lógicos;
* similitud semántica.

El motor puede combinar:

* consultas estructurales;
* Datalog;
* operaciones booleanas;
* búsqueda vectorial.

---

### Merkle Engine

Calcula hashes deterministas sobre la representación canónica.

El hashing es perezoso.

Cuando cambia un nodo:

1. Se marca el nodo como sucio.
2. Se invalidan los hashes de sus ancestros estructurales.
3. Los hashes se recalculan cuando son necesarios.

El Merkle estructural utiliza principalmente aristas `Ownership`.

Esto evita ciclos provocados por referencias semánticas o enlaces cruzados.

---

### Event Bus

Publica eventos internos:

```text
TransactionCommitted
RevisionCreated
DocumentImported
ProjectionInvalidated
ExternalSourceChanged
EffectCompleted
ConflictDetected
```

Los hooks reaccionan a estos eventos.

---

## Persistencia

La fuente de verdad está formada por:

```text
Transaction Log
Revision Store
Content-Addressed Store
Document Heads
```

Los siguientes componentes son reconstruibles:

```text
Petgraph
Índices
Caches
Embeddings
Proyecciones
Hechos derivados
```

### Transaction Log

Registro append-only de todas las transacciones.

Una transacción ya confirmada nunca se modifica.

### Content-Addressed Store

Guarda contenido mediante su hash:

```text
hash → contenido
```

Esto permite:

* deduplicación;
* verificación de integridad;
* comparación eficiente;
* reutilización entre revisiones.

### Document Heads

Cada documento mantiene un puntero hacia su revisión actual.

La actualización debe utilizar compare-and-swap para detectar commits concurrentes.

---

## Archivos externos

El kernel puede indexar archivos existentes sin requerir un daemon permanente.

Cuando se accede a un documento:

1. Se inspecciona la metadata externa.
2. Se verifica si el contenido pudo cambiar.
3. Se lee únicamente cuando es necesario.
4. Se parsea hacia una AST sintáctica.
5. Se canonicaliza.
6. Se compara con la revisión actual.
7. Se genera una transacción.

```text
Archivo externo
    ↓
Parser
    ↓
AST sintáctica
    ↓
Canonicalizer
    ↓
Operaciones
    ↓
Nueva revisión
```

---

## Round-trip determinista

La garantía principal es:

```text
canonicalize(parse(render(C))) == C
```

donde `C` es una AST canónica.

No es obligatorio que:

```text
render(parse(source)) == source
```

El sistema puede ofrecer dos modos:

### Modo canónico

Produce una representación textual normalizada y determinista.

### Modo lossless

Conserva comentarios, espacios, tokens y detalles de formato necesarios para reconstruir el archivo original.

Rowan puede utilizarse para representar árboles sintácticos lossless.

---

## Proyecciones semánticas

La semántica no modifica directamente el documento.

Se almacena como información derivada.

```text
Revision
   ├── StructuralProjection
   ├── SemanticProjection
   ├── EmbeddingProjection
   └── LogicProjection
```

### Embeddings

Los embeddings deben guardar:

* hash del contenido fuente;
* modelo;
* versión del modelo;
* estrategia de segmentación;
* vector resultante.

### Lógica

La base lógica puede materializar hechos desde el grafo:

```lisp
(section document-1 section-4)
(references section-4 concept-9)
(depends-on task-3 task-1)
```

Estos hechos pueden procesarse mediante Datalog o el motor booleano propio.

---

## Hooks y efectos

Los hooks no deben ejecutar directamente operaciones externas dentro de una transacción.

Flujo correcto:

```text
Evento
  ↓
Hook
  ↓
EffectPlan
  ↓
Outbox persistente
  ↓
Effect Runner
  ↓
Git / API / herramienta / agente
  ↓
EffectResult
  ↓
Nueva transacción
```

Esto evita estados parciales cuando una herramienta externa falla.

---

## Capabilities

Cada efecto debe declarar permisos explícitos.

Ejemplos:

```text
filesystem.read
filesystem.write
git.commit
git.push
network.http
agent.invoke
process.execute
```

Los macros Lisp, plugins y agentes reciben únicamente las capabilities necesarias.

---

## Interfaces externas

El kernel expone varias interfaces intercambiables.

### Interfaces de entrada

* API Rust embebida;
* Lisp REPL;
* CLI;
* IPC local;
* HTTP;
* gRPC;
* MCP;
* eventos.

### Interfaces de salida

```rust
trait DocumentSource;
trait Parser;
trait Renderer;
trait StorageBackend;
trait SemanticProvider;
trait EffectExecutor;
trait AgentProvider;
```

Las bibliotecas y servicios concretos quedan detrás de estos traits.

---

## Librerías propuestas

| Función               | Biblioteca             |
| --------------------- | ---------------------- |
| Lisp embebido         | Steel                  |
| S-expressions         | `lexpr`, `serde-lexpr` |
| Parsing incremental   | Tree-sitter            |
| AST lossless          | Rowan                  |
| Persistencia embebida | redb                   |
| Grafo en memoria      | Petgraph               |
| Hashing               | BLAKE3                 |
| Datalog estático      | Ascent                 |
| Datalog dinámico      | CozoDB                 |
| Cálculo incremental   | Salsa                  |
| Plugins aislados      | Wasmtime               |
| Serialización         | Serde                  |

Estas bibliotecas deben quedar encapsuladas detrás de interfaces propias.

El modelo canónico no debe depender directamente de ellas.

---

## Estrategias de implementación

### Ruta rápida

```text
Steel
  ↓
Kernel mínimo
  ↓
CozoDB
```

CozoDB puede proporcionar inicialmente:

* persistencia;
* consultas Datalog;
* índices;
* operaciones de grafo;
* historial.

El kernel conserva el control de:

* identidad;
* canonicalización;
* transacciones;
* hashes;
* proyecciones;
* permisos.

### Ruta controlada

```text
Steel
  ↓
Kernel propio
  ├── redb
  ├── Petgraph
  ├── BLAKE3
  ├── Ascent
  ├── Tree-sitter
  ├── Rowan
  └── Wasmtime
```

Esta ruta requiere más desarrollo, pero proporciona mayor control sobre el modelo.

---

## Invariantes

El kernel debe garantizar:

1. Ninguna revisión existente puede modificarse.
2. Toda mutación produce una nueva revisión.
3. Toda revisión apunta a una transacción válida.
4. Los identificadores permanecen estables mientras se conserve la identidad.
5. El contenido canónico produce hashes deterministas.
6. Los datos derivados pueden reconstruirse.
7. Los efectos externos no mutan directamente el grafo.
8. Toda operación externa requiere capabilities explícitas.
9. Las transacciones son atómicas.
10. La canonicalización es determinista.
11. Las referencias externas no afectan circularmente el Merkle estructural.
12. Los motores y proyecciones registran su versión.
13. Un resultado derivado siempre conserva provenance.
14. Los conflictos concurrentes nunca se resuelven silenciosamente.

---

## Estructura de crates

```text
kernel-core
kernel-storage
kernel-graph
kernel-merkle
kernel-query
kernel-document
kernel-projection
kernel-semantics
kernel-lisp
kernel-hooks
kernel-api
kernel-cli
```

### `kernel-core`

Contiene únicamente:

* tipos fundamentales;
* identificadores;
* operaciones;
* transacciones;
* errores;
* invariantes.

No debería depender de:

* Steel;
* Petgraph;
* Tree-sitter;
* CozoDB;
* embeddings;
* APIs externas.

---

## Roadmap inicial

### Fase 1: núcleo

* `Node`, `Edge`, `Document`, `Revision`;
* operaciones primitivas;
* almacenamiento en memoria;
* motor de transacciones;
* hashes BLAKE3;
* historial de revisiones.

### Fase 2: documentos

* parser Markdown;
* AST canónica;
* renderer determinista;
* round-trip;
* importación de archivos.

### Fase 3: Lisp

* integración con Steel;
* compilación a `TransactionPlan`;
* compilación a `QueryPlan`;
* macros de transformación.

### Fase 4: consultas y semántica

* Petgraph;
* consultas estructurales;
* motor lógico;
* embeddings;
* proyecciones semánticas.

### Fase 5: automatización

* event bus;
* hooks;
* outbox;
* Wasmtime;
* Git;
* subagentes.

---

## No objetivos iniciales

La primera versión no debería intentar construir:

* una base de datos distribuida;
* un editor de texto completo;
* sincronización en tiempo real;
* un Lisp desde cero;
* un motor vectorial propio;
* un sistema de plugins nativos sin sandbox;
* resolución automática universal de conflictos.

El primer objetivo es validar el modelo canónico y el ciclo:

```text
parse
→ canonicalize
→ transact
→ persist
→ query
→ project
→ render
```

---

## Resumen

La arquitectura combina:

```text
Rust
    → invariantes, persistencia y seguridad

Lisp
    → extensibilidad, macros y composición

Grafo canónico
    → representación común

Log inmutable
    → historial y reproducibilidad

Merkle perezoso
    → integridad y comparación eficiente

Proyecciones
    → documentos, interfaces y semántica

Ports and Adapters
    → bibliotecas y servicios reemplazables
```

El resultado es un kernel pequeño y estable sobre el cual pueden construirse documentos, agentes, herramientas y sistemas semánticos sin acoplar el núcleo a una interfaz o tecnología específica.

Esto podría convertirse después en un `ARCHITECTURE.md`, dejando el `README.md` reducido a instalación, ejemplo mínimo y estado del proyecto.

