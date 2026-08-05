---
layer: shared
id: ports-and-adapters
title: Ports and adapters
five_wh_one_plus: how
tags:
- system:sldb
- domain:architecture-boundaries
- domain:architecture-integration
provenance: source docs/core/interfaces.md
---

# Ports and adapters

## Answer

Ports and adapters is the architecture rule that the kernel only depends on its own traits and contracts while concrete libraries, protocols, and services stay behind replaceable adapters.

## Supporting points

- Document sources, parsers, renderers, storage backends, semantic providers, effect executors, and agent providers are all adapter roles.
- Tree-sitter, Rowan, redb, Cozo, Wasmtime, PyO3, HTTP, MCP, and embedding services are implementation details behind those ports.
- This protects the canonical model from accidental coupling to one stack choice.

## Related atoms

### Depends on

- [depends_on:: [[kernel-api]]]
- [depends_on:: [[graph-store]]]

### Supports

- [supports:: [[python-cli-orchestration-layer]]]
- [supports:: [[canonicalizer]]]
- [supports:: [[semantic-exporter]]]

### Constrains

- [constrains:: [[decision-pyo3-ffi]]]
- [constrains:: [[decision-rusqlite-store]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
