---
id: feature-rust-library-stack
title: Rust Core Library Stack Proposal
five_wh_one_plus: how
tags:
- architecture:decision
- concept:rust-core
- concept:store
---

# Rust Core Library Stack Proposal

Este informe detalla las librerías (crates) recomendadas en el ecosistema Rust para implementar los componentes especificados en la arquitectura objetivo (`target-components.yml` y `target-store-graph.yml`).

## 1. FFI & Boundary (Python <-> Rust)
* **`pyo3`**: La opción estándar para exponer código Rust nativo hacia Python de forma eficiente. Permitirá que el `python_cli_layer` invoque las operaciones de Rust (parser, store queries, materialización) pasando directamente por memoria sin necesidad de levantar demonios o hacer IPC costoso.
* **`tracing` y `tracing-subscriber`**: Para instrumentación, observabilidad y logging estructurado. A través de un custom subscriber en `pyo3`, los eventos de progreso en Rust (ej. "parseando 500 archivos") pueden emitirse directamente a Python para que renderice interfaces (como `rich` progress bars).

## 2. Graph Store y Persistencia (Append-Only)
* **`rusqlite`**: Para manejar la persistencia local en `.sldb/` usando SQLite. Dado que la base de datos es de tipo *append-only* e inmutable, el modelo síncrono y ligero de `rusqlite` es ideal para un CLI, ofreciendo control absoluto sobre las transacciones y bloqueos (file-locks).
* **`petgraph`**: Para la representación en memoria y algoritmos de grafos (navegación de `RelationEdges`, dependencias topológicas). Fundamental para construir y analizar el `knowledge_graph`.

## 3. AST Canónico y Reversibilidad (Reversible Docs)
* **`rowan`**: Librería creada por el equipo de `rust-analyzer` para árboles sintácticos sin pérdida (*lossless syntax trees*). Es **estrictamente necesaria** para cumplir el contrato de *Reversible Families* (`AST -> render -> AST -> render`), ya que mantiene cada byte original (espacios en blanco, trivia) en el árbol sintáctico.
* **`pulldown-cmark`**: Para procesamiento y validación general de Markdown donde no se exija recreación estricta de formato, o como base para inicializar un árbol `rowan`.
* **`tree-sitter` (y `tree-sitter-rs`)**: Específicamente mencionado en la arquitectura para implementar el `TreeSitterAdapter` y soportar *Non-Reversible Families* (ej. código fuente o HTML).

## 4. Hashing e Identidad (Canonical Identity)
* **`blake3`**: Algoritmo criptográfico ultra-rápido. Perfecto para firmar contenido (`SourceHash`), calcular hashes de nodos y construir árboles de Merkle para los índices semánticos. Su paralelismo intrínseco acelerará enormemente los rebuilds del repositorio.

## 5. Índices Derivados (Derived Indexes) y Serialización
* **`serde` y `serde_json`**: Indispensables para (de)serializar los AST, las proyecciones y exportaciones del `SemanticExporter`.
* **`rmp-serde` (MessagePack)** o **`bincode`**: Para almacenar las cargas dinámicas de los `RelationASTs` directamente en blobs binarios compactos dentro del Graph Store (SQLite), minimizando el peso del caché y la base de datos local.
* **`tantivy`** o **SQLite FTS5**: Específicamente para resolver el `SearchIndex` requerido en la arquitectura. `tantivy` ofrece búsqueda full-text de nivel industrial puramente en Rust, mientras que FTS5 puede manejarse directamente desde `rusqlite`.

## 6. Concurrencia y Performance
* **`rayon`**: Para el *data-parallelism* (procesamiento paralelo) durante la fase de *Importers*. La lectura, parseo de los AST, hashing y extracción de anclajes de cientos de documentos se puede distribuir eficientemente en todos los cores disponibles con una línea de código (`par_iter`).
* **`dashmap`**: Mapas concurrentes de altísimo rendimiento, muy útiles para recolectar referencias de anclajes (`AnchorNodes`) desde múltiples hilos antes de hacer la inserción *append-only* masiva a SQLite.

## 7. Manejo de Errores y Robustez
* **`thiserror`**: Para definir tipos de error estrictos en el `RustCore`, vital para mantener la integridad de la base de datos y la confianza en la compilación del AST.
* **`anyhow`**: Para la propagación ágil de errores en los bordes de la aplicación (ej. en la capa FFI hacia Python), dando contextos amigables al usuario.
