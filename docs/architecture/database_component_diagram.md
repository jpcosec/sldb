# SLDB Holistic Database Architecture

This diagram illustrates the complete architecture of the Structured Language Database (SLDB). It maps the journey of data from high-level Python contracts down to the persistent physical file system, highlighting the extraction, integrity (Merkle hashing), and graph connection layers.

```mermaid
flowchart TD
    %% Boundary: User & Contracts
    subgraph ClientSpace ["Application & Contracts"]
        CLI["CLI / API Interface"]
        Models["Pydantic Models (StructuredNLDoc)"]
        CLI <--> Models
    end

    %% Layer: Core Translation Engine (Bidirectional Markdown <-> Objects)
    subgraph CoreEngine ["Core Translation Engine (src/sldb/core)"]
        Renderer["Renderer\n(Jinja2 + Markers)"]
        Extractor["Data Extractor\n(Pattern Matching)"]
        Router["SharedNodeHandler\n(1 Node per Router)"]
        AST["MarkdownASTHandler\n(SLDBNode Abstraction)"]
        
        Renderer --> Router
        Extractor --> Router
        Router <--> AST
    end

    %% Layer: Knowledge Graph & Queries
    subgraph GraphEngine ["Graph & Query Engine"]
        Query["Query Resolution\n(ls, get, glob)"]
        Links["Link Manager\n(Transclusions & Pointers)"]
        Semantic["Semantic Engine\n(Global & Local Concepts)"]
        
        Query --> Semantic
        Links --> Semantic
    end

    %% Layer: Integrity & Store Management
    subgraph StoreEngine ["Store Engine (src/sldb/store)"]
        Ops["Store Operations\n(Tracking, Lifecycle)"]
        Hashing["Integrity Manager\n(4-Layer Merkle Hash)"]
        IO["I/O Manager\n(YAML Serialization)"]
        Diagnostics["Diagnostics\n(Idempotency & Tamper Checks)"]
        
        Ops --> Hashing
        Ops --> IO
        Diagnostics --> Hashing
    end

    %% Layer: Physical Persistence
    subgraph FileSystem ["Physical Data Layer (File System)"]
        MDFiles["Markdown Documents\n(*.md)"]
        
        subgraph SLDBFolder [".sldb/ (Hidden Metadata)"]
            StoreIndex["store_index.yaml\n(Hash A)"]
            ModelIndex["models/*.yaml\n(Hash B)"]
            DocIndex["documents/*.yaml\n(Hashes C & D)"]
            DAG["semantic_dag.yaml\n(Graph Edges)"]
            
            StoreIndex --> ModelIndex
            ModelIndex --> DocIndex
        end
    end

    %% Inter-layer Connections
    Models <-->|Validates/Generates| CoreEngine
    CLI --> Ops
    CLI --> Query
    CLI --> Links
    CLI --> Diagnostics
    
    CoreEngine -->|Reads/Writes Strings| MDFiles
    
    GraphEngine --> IO
    GraphEngine --> AST
    
    IO --> SLDBFolder
    
    %% Emphasize the separation between raw data and metadata
    MDFiles -.->|Tracked By| DocIndex
```

### Component Highlights

1. **Application & Contracts**: The user interacts with the database purely through typed Pydantic models (`StructuredNLDoc`). The system enforces these shapes.
2. **Core Translation Engine**: Responsible for the bidirectional translation. It guarantees that `Markdown -> Object -> Markdown` is perfectly idempotent. The `SharedNodeHandler` routes every AST node (`SLDBNode`) to specialized extractors (lists, tables, YAML), supporting infinitely nested structures.
3. **Graph & Query Engine**: Elevates flat files into a knowledge graph. It resolves semantic links, manages transclusions (composing larger documents from smaller ones), and maintains local vs. global semantic boundaries.
4. **Store Engine**: The database manager. It tracks documents and calculates a 4-layer Merkle-style hash cascade (Hash A, B, C, D) to detect tampering, content drift, or model schema changes.
5. **Physical Data Layer**: The actual storage mechanism. Content is stored as plain, portable `.md` files. Metadata (hashes, schema references, graph edges) is strictly isolated in the `.sldb/` folder, allowing the Markdown to remain fully independent of the database tooling if needed.
