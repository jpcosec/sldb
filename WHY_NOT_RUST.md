# Por qué abortamos el Rust Kernel a favor de Full Clojure

Este branch (`refactor-target-rustflavor`) contiene la Prueba de Concepto (PoC) de un Evaluador de Lisp escrito en Rust (con `petgraph` y parseo de EDN) y todas las exploraciones iniciales sobre cómo construir el motor SLDB desde cero en Rust.

## Razones del Aborto

1. **Reinventar la Rueda**: Reconstruir todo el ecosistema de Clojure (estructuras de datos inmutables HAMT, EDN parser, transaccionalidad STM, motor Datalog relacional y sistema de Macros) en Rust nos tomaría 6 meses de trabajo duro de infraestructura antes de poder aportar valor al negocio.
2. **Clojure ya hace esto nativamente**: SLDB requiere que los Documentos sean Mapas y Vectores (EDN) y que las reglas de negocio sean Lisp, con mutaciones que produzcan copias inmutables estructuralmente compartidas (Revisiones Canónicas). Ese es el diseño fundacional y exacto de Clojure (y Datomic/DataScript). 
3. **El obstáculo de la JVM solucionado**: El único problema de Clojure era el arranque lento en la JVM para aplicaciones CLI. Esto se resuelve al 100% migrando al ecosistema de **Babashka** (Clojure compilado nativamente vía GraalVM), que proporciona arranques de CLI instantáneos, distribución de binarios estáticos sin requerir Java, e integración nativa con EDN, JSON y el SO.

Por lo tanto, la arquitectura de SLDB se purgará de la obligación de "Rust Kernel" y pivotará oficialmente a un núcleo **Clojure/Babashka + DataScript (Graph Datalog)**. 
Este branch queda como registro histórico del "Rust Flavor".
