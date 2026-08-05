---
layer: shell
id: atom-reference-edge
title: Atom reference edge
five_wh_one_plus: what
tags:
- system:sldb
- domain:documentation-traceability
provenance: docs/architecture/contracts/specyaml-schema-contract.md
---

# Atom reference edge

## Answer

An atom reference edge is a cross-document link that carries only the atom's id: the referencing document points at the atom, never copies its prose.

## Supporting points

- The atom remains the sole governor of the concept; references cannot contradict it because they contain no content.
- Renaming an atom id is a breaking change for every referencing document.
- The `atoms:` field in spec2viz node entries is the canonical instance of this edge.

## Related atoms

### Depends on

- [depends_on:: [[concept-binding]]]

### Supports

- [supports:: [[specyaml-nexus]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
