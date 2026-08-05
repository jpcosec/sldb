Había interfaces externas dispersas en los diagramas anteriores, pero falta un **diagrama explícito de puertos y adaptadores**.

## 1. Interfaces externas del kernel

```plantuml
@startuml
title Interfaces externas — Ports and Adapters

skinparam componentStyle rectangle

rectangle "Clientes" {
    component CLI
    component UI
    component "Agentes / MCP" as Agents
    component "Aplicación Rust embebida" as Embedded
}

rectangle "Interfaces de entrada" {
    interface "Kernel API" as KernelAPI
    interface "Query API" as QueryAPI
    interface "Transaction API" as TransactionAPI
    interface "Projection API" as ProjectionAPI
    interface "Event API" as EventAPI
    interface "Lisp DSL" as LispAPI
}

rectangle "Knowledge Kernel" {
    component "Command Dispatcher" as Commands
    component "Transaction Engine" as Tx
    component "Query Engine" as Query
    component "Projection Engine" as Projection
    component "Event Bus" as Events
}

rectangle "Interfaces de salida" {
    interface "Document Adapter" as DocumentAdapter
    interface "Storage Backend" as StorageAdapter
    interface "Effect Adapter" as EffectAdapter
    interface "Semantic Provider" as SemanticAdapter
    interface "Agent Provider" as AgentAdapter
}

rectangle "Sistemas externos" {
    component "Filesystem" as FS
    component Git
    component "Bases de datos" as Databases
    component "LLM / Embeddings" as Models
    component "Herramientas / APIs" as Tools
    component "Subagentes" as Subagents
}

CLI --> KernelAPI
UI --> KernelAPI
Agents --> KernelAPI
Embedded --> KernelAPI

KernelAPI --> Commands
QueryAPI --> Query
TransactionAPI --> Tx
ProjectionAPI --> Projection
EventAPI --> Events
LispAPI --> Commands

Commands --> Tx
Commands --> Query
Commands --> Projection

Tx --> StorageAdapter
Query --> StorageAdapter
Projection --> DocumentAdapter
Projection --> SemanticAdapter
Events --> EffectAdapter

DocumentAdapter --> FS
DocumentAdapter --> Git
StorageAdapter --> Databases
SemanticAdapter --> Models
EffectAdapter --> Tools
AgentAdapter --> Subagents

note bottom of KernelAPI
Puede exponerse como:
- API Rust embebida
- IPC local
- HTTP
- gRPC
end note

@enduml
```

---

## 2. Contratos públicos del kernel

```plantuml
@startuml
title Contratos de interfaces públicas

interface KernelApi {
    +open_document(id): DocumentHandle
    +begin_transaction(base): TransactionBuilder
    +query(query): QueryResult
    +project(spec): ProjectionResult
    +subscribe(filter): EventStream
}

interface TransactionApi {
    +put_node(node): OperationId
    +remove_node(id): OperationId
    +put_edge(edge): OperationId
    +remove_edge(id): OperationId
    +attach_artifact(artifact): OperationId
    +commit(): RevisionId
    +abort()
}

interface QueryApi {
    +execute(plan): QueryResult
    +get_node(id, revision): Node
    +get_subgraph(root, revision): GraphView
    +history(document): List<Revision>
    +diff(left, right): ChangeSet
}

interface ProjectionApi {
    +structural_ast(document, revision): Ast
    +semantic_graph(document, revision): GraphView
    +render(document, format): Bytes
    +embedding_view(document): EmbeddingSet
}

interface EventApi {
    +subscribe(filter): EventStream
    +acknowledge(event)
}

interface LispApi {
    +evaluate(expression): LispResult
    +compile_transaction(expression): TransactionPlan
    +compile_query(expression): QueryPlan
    +compile_effect(expression): EffectPlan
}

KernelApi --> TransactionApi
KernelApi --> QueryApi
KernelApi --> ProjectionApi
KernelApi --> EventApi

LispApi --> TransactionApi
LispApi --> QueryApi
LispApi --> ProjectionApi

@enduml
```

---

## 3. Adaptadores externos

```plantuml
@startuml
title Interfaces de integración externa

interface DocumentSource {
    +identify(): SourceIdentity
    +metadata(): SourceMetadata
    +read(range): Bytes
    +write(content, expected_version): SourceVersion
}

interface Parser {
    +supports(media_type): bool
    +parse(bytes): SyntaxTree
}

interface Renderer {
    +supports(document_type, format): bool
    +render(ast): Bytes
}

interface StorageBackend {
    +append_transaction(tx): TransactionId
    +put_revision(revision)
    +get_revision(id): Revision
    +put_content(hash, bytes)
    +get_content(hash): Bytes
    +compare_and_swap_head(document, expected, next): bool
}

interface SemanticProvider {
    +embed(request): EmbeddingResult
    +classify(request): SemanticResult
}

interface EffectExecutor {
    +validate(plan): CapabilityRequest
    +execute(effect): EffectResult
}

interface AgentProvider {
    +invoke(agent, context): AgentResult
}

class FilesystemSource
class GitSource
class HttpSource
class TreeSitterParser
class MarkdownRenderer
class RedbBackend
class CozoBackend
class EmbeddingService
class WasmEffectExecutor
class LocalAgentAdapter
class McpAgentAdapter

DocumentSource <|.. FilesystemSource
DocumentSource <|.. GitSource
DocumentSource <|.. HttpSource

Parser <|.. TreeSitterParser
Renderer <|.. MarkdownRenderer

StorageBackend <|.. RedbBackend
StorageBackend <|.. CozoBackend

SemanticProvider <|.. EmbeddingService
EffectExecutor <|.. WasmEffectExecutor

AgentProvider <|.. LocalAgentAdapter
AgentProvider <|.. McpAgentAdapter

@enduml
```

---

## 4. Flujo desde una interfaz externa

```plantuml
@startuml
title Operación desde CLI, UI o agente

actor Client
participant "External API" as API
participant "Authentication /\nCapabilities" as Auth
participant "Command Dispatcher" as Dispatcher
participant "Transaction Engine" as Tx
participant "Event Bus" as Events
participant "External Adapter" as Adapter

Client -> API : request(command, base_revision)
API -> Auth : validate identity + capabilities
Auth --> API : authorized

API -> Dispatcher : dispatch(command)

alt consulta
    Dispatcher --> API : QueryResult
else transformación
    Dispatcher -> Tx : execute(TransactionPlan)
    Tx --> Dispatcher : RevisionId
    Tx -> Events : TransactionCommitted
    Dispatcher --> API : RevisionId
else efecto externo
    Dispatcher -> Events : enqueue EffectPlan
    Events -> Adapter : execute effect
    Adapter --> Events : EffectResult
    Events -> Tx : persist result
end

API --> Client : typed response

@enduml
```

## Interfaces externas principales

| Dirección | Interfaz           | Ejemplos                      |
| --------- | ------------------ | ----------------------------- |
| Entrada   | API Rust           | Kernel embebido               |
| Entrada   | Lisp DSL           | REPL, macros, agentes         |
| Entrada   | HTTP/gRPC/IPC      | CLI, UI, procesos externos    |
| Entrada   | eventos            | filesystem, Git, herramientas |
| Salida    | `DocumentSource`   | archivos, Git, HTTP           |
| Salida    | `StorageBackend`   | redb, CozoDB                  |
| Salida    | `SemanticProvider` | embeddings, LLM               |
| Salida    | `EffectExecutor`   | Git, shell, APIs              |
| Salida    | `AgentProvider`    | subagentes, MCP               |

La idea central es que el kernel solo conozca **traits propios**. Tree-sitter, Steel, CozoDB, Wasmtime, Git o proveedores de modelos quedan detrás de adaptadores reemplazables.

