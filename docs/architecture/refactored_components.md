# SLDB Refactored Component Diagram

This document contains a visual representation of the SLDB architecture following the modularity refactoring, demonstrating the separation of concerns and clear dependencies between the CLI, the Store engine, and the Core extraction/rendering layers.

```mermaid
flowchart TD
    %% CLI Layer
    subgraph CLI ["CLI Layer (src/sldb/cli)"]
        Dispatcher["main.py (CLI Dispatcher)"]
        Parser["parser.py (Argparse)"]
        Utils["utils.py (Helpers)"]
        
        subgraph Commands ["Command Handlers"]
            BasicCLI["basic.py"]
            DocCLI["doc.py"]
            InitCLI["init.py"]
            LinkCLI["links.py"]
            ModelCLI["model.py"]
            QueryCLI["query.py"]
            StoreCLI["store.py"]
        end
    end

    %% Core Engine
    subgraph Core ["Core Engine (src/sldb/core)"]
        Node["node.py (SLDBNode)"]
        AST["ast.py (AST Handler)"]
        Exceptions["exceptions.py"]
        
        subgraph Processing ["Extraction & Rendering"]
            DataExt["data_extractor.py"]
            Renderer["renderer.py"]
            SharedHandler["node_handler.py (1 Node per Router)"]
            
            DataExt --> SharedHandler
            Renderer --> SharedHandler
        end
    end

    %% Store Engine
    subgraph Store ["Store Engine (src/sldb/store)"]
        Ops["ops.py (High-level Ops)"]
        IO["io.py (Disk Access)"]
        Hashing["hashing.py (Merkle Cascade)"]
        Query["query.py (Semantic/Structural)"]
        Semantic["semantic.py (DAG Mgmt)"]
        Models["models.py (Store Schemas)"]
        Diag["diagnostics.py"]
    end

    %% Links Engine
    subgraph Links ["Links Engine (src/sldb/links.py)"]
        Recovery["Link Recovery"]
        Composition["Document Composition"]
    end

    %% Dependencies
    Dispatcher -->|Builds| Parser
    Dispatcher -->|Routes to| Commands
    
    Commands --> Utils
    Commands -.-> Processing
    Commands -.-> Ops
    Commands -.-> Query
    LinkCLI -.-> Links

    Ops --> IO
    Ops --> Hashing
    Ops --> Semantic
    
    Processing --> Node
    Processing --> AST
    
    Query --> IO
    Semantic --> IO
    
    Links --> IO
```
