No de forma explícita. Los UML anteriores muestran **interfaces abstractas**. Hay que agregar un diagrama de implementación que distinga `<<crate>>`, `<<adaptado>>` y `<<propio>>`.

## Stack reutilizable

| Componente                | Usaría                     | Estrategia                                                                                                                                                                                           |
| ------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lisp y macros             | **Steel**                  | Integrarlo completo. Ya ofrece Scheme embebible, macros y binding sencillo con funciones Rust. Está pre-1.0, así que conviene aislarlo detrás de un trait propio. ([GitHub][1])                      |
| S-expressions             | `lexpr` + `serde-lexpr`    | Serialización Lisp ↔ tipos Rust. No usar `lexpr::Value` como modelo interno definitivo. ([Docs.rs][2])                                                                                               |
| Parsing externo           | **Tree-sitter**            | Reutilizar runtime y gramáticas existentes para código y documentos. Soporta parsing incremental y árboles incluso con errores. ([GitHub][3])                                                        |
| Árbol sintáctico lossless | **Rowan**                  | Para comentarios, espacios, tokens y edición estructural determinista. Su green tree es inmutable y barato de reconstruir parcialmente. ([GitHub][4])                                                |
| Persistencia propia       | **redb**                   | Tablas para transacciones, revisiones, blobs, heads e índices. Tiene ACID, MVCC, copy-on-write y formato estable. ([GitHub][5])                                                                      |
| Grafo en memoria          | **petgraph `StableGraph`** | Vista materializada y algoritmos. Los `NodeId` canónicos deben seguir siendo tuyos, no `NodeIndex`. ([GitHub][6])                                                                                    |
| Hashing                   | **BLAKE3**                 | Usar directamente la implementación. Tú defines qué campos y aristas entran al Merkle del documento. ([GitHub][7])                                                                                   |
| Lógica estática           | **Ascent**                 | Para análisis derivados definidos al compilar: transitividad, dependencias, validaciones. Permite estructuras de datos propias. ([GitHub][8])                                                        |
| Lógica dinámica           | **CozoDB**                 | Alternativa para reglas Datalog almacenadas como datos, consultas de grafo y time travel. Puede reemplazar gran parte de `redb + query engine`, pero está pre-1.0 y usa MPL-2.0. ([GitHub][9])       |
| Cálculo perezoso          | **Salsa**, opcional        | Inspiración para invalidación y proyecciones bajo demanda. La propia biblioteca todavía se declara en desarrollo, por lo que no la pondría inicialmente en el centro de persistencia. ([GitHub][10]) |
| Hooks aislados            | **Wasmtime/WASI**          | Plugins y herramientas no confiables con permisos explícitos sobre archivos, red, CPU y memoria. ([GitHub][11])                                                                                      |
| Serialización Rust        | **Serde**                  | DTO, eventos, operaciones y adapters de almacenamiento. ([GitHub][12])                                                                                                                               |

## Qué conviene copiar o adaptar

### Adoptar prácticamente completo

* Steel: reader, macro expander, VM, REPL y módulos.
* Tree-sitter: runtime y gramáticas.
* BLAKE3: hashing.
* redb o CozoDB: motor persistente.
* Wasmtime: sandbox.
* Petgraph: algoritmos y representación temporal.

### Copiar como arquitectura, no necesariamente código

* **Git:** blobs, árboles, commits, refs, content-addressed storage y garbage collection.
* **Datomic:** hechos inmutables, transacciones ordenadas, tiempo de transacción y consultas sobre revisiones.
* **rust-analyzer/Rowan:** green tree inmutable, red tree navegable y nodos reconstruibles.
* **Salsa:** consultas memoizadas, dependencias e invalidación perezosa.
* **Tree-sitter:** actualización basada en rangos modificados.
* **CozoDB/Ascent:** evaluación seminaive, relaciones derivadas e índices por relación.

## Qué sigue siendo necesariamente propio

Esto representa el valor central del proyecto:

```text
CanonicalNode / CanonicalEdge
DocumentRevision
Transaction y operaciones primitivas
Reglas de identidad estable
Canonicalización
Round-trip parse/render
Merkle semántico por subárbol
Tipos de aristas
Proyecciones estructurales y semánticas
Compilación Lisp → TransactionPlan / QueryPlan / EffectPlan
Anclaje entre documentos
Provenance
Modelo de capabilities
```

## Dos rutas posibles

### Prototipo más rápido

```text
Steel
  ↓
TransactionPlan / QueryPlan
  ↓
CozoDB
  ├── almacenamiento
  ├── Datalog
  ├── grafo
  └── historial

Tree-sitter / Rowan → documentos
BLAKE3              → integridad
Wasmtime            → efectos
```

CozoDB permite evitar inicialmente la construcción de:

* motor de consultas;
* gran parte del almacenamiento;
* índices de relaciones;
* evaluación Datalog;
* algoritmos básicos de grafo.

### Kernel completamente controlado

```text
Steel
  ↓
Kernel propio
  ├── redb
  ├── petgraph
  ├── BLAKE3
  ├── Ascent
  ├── Tree-sitter / Rowan
  └── Wasmtime
```

Mi recomendación sería **comenzar con CozoDB detrás de un `StorageBackend` reemplazable**, pero mantener tuyos el modelo canónico, las transacciones y los hashes. Así puedes validar el sistema sin programar una base de datos completa y reemplazar Cozo posteriormente si limita el modelo.

En términos aproximados, podrías reutilizar **60–70 % de la infraestructura**. El 30–40 % propio sería precisamente el kernel diferencial: canonicalización, identidad, proyecciones, provenance y semántica de las operaciones.

[1]: https://github.com/mattwparas/steel?utm_source=chatgpt.com "mattwparas/steel: An embedded scheme interpreter in Rust"
[2]: https://docs.rs/serde-lexpr/latest/serde_lexpr/?utm_source=chatgpt.com "serde_lexpr - Rust"
[3]: https://github.com/tree-sitter/tree-sitter?utm_source=chatgpt.com "GitHub - tree-sitter/tree-sitter: An incremental parsing system for programming tools · GitHub"
[4]: https://github.com/rust-analyzer/rowan?utm_source=chatgpt.com "rust-analyzer/rowan"
[5]: https://github.com/cberner/redb?utm_source=chatgpt.com "cberner/redb: An embedded key-value database in pure Rust"
[6]: https://github.com/petgraph/petgraph?utm_source=chatgpt.com "petgraph/petgraph: Graph data structure library for Rust."
[7]: https://github.com/BLAKE3-team/BLAKE3?utm_source=chatgpt.com "the official Rust and C implementations of the BLAKE3 ..."
[8]: https://github.com/s-arash/ascent?utm_source=chatgpt.com "s-arash/ascent: Logic programming in Rust"
[9]: https://github.com/cozodb/cozo?utm_source=chatgpt.com "cozodb/cozo: A transactional, relational-graph- ..."
[10]: https://github.com/salsa-rs/salsa?utm_source=chatgpt.com "Salsa"
[11]: https://github.com/bytecodealliance/wasmtime?utm_source=chatgpt.com "GitHub - bytecodealliance/wasmtime: A lightweight WebAssembly runtime that is fast, secure, and standards-compliant · GitHub"
[12]: https://github.com/serde-rs/serde?utm_source=chatgpt.com "GitHub - serde-rs/serde: Serialization framework for Rust · GitHub"

